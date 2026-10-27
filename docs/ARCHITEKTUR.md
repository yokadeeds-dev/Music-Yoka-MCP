# Music-Yoka-MCP – Architektur

Status: **Entwurf zur Freigabe** (Schritt 1). Stand 2026-10-27.
Feature-Prioritäten: `docs/FEATURE_MATRIX.md`. Entscheidungen: `docs/ENTSCHEIDUNGEN.md`.

---

## 1. Ziel

- Zentrale Datenbank über **~100.000 lokale Musikdateien** auf vielen Rechnern und Datenträgern
  (später auch CD/DVD).
- Zugriff für Claude über einen **MCP-Server** (Python).
- **Hauptnutzen: Sichtbarkeit in Traktor** – Comment 2, Color, Cat. No. in `collection.nml`.
- Verknüpfung mit **Spotify-Yoka-MCP** (Abgleich lokal ↔ Spotify).
- Kein Ziel: Anzeige auf dem S8-Display.

## 2. Harte Regeln (Sicherheitsmodell)

| Regel | Technische Umsetzung |
|---|---|
| Ordnerstruktur bleibt unverändert | Kein Code-Pfad ruft `mkdir`, `rmdir`, `rename` auf Ordner auf. Datei-Umbenennung nur im **selben Ordner** (Prüfung `parent(alt) == parent(neu)` vor Ausführung). Leere Ordner werden nie entfernt. |
| Einzige Ausnahme: Duplikat-Quarantäne | Konfigurierter Quarantäne-Pfad **außerhalb** der Musikstruktur, bevorzugt auf demselben Datenträger (atomares Verschieben, kein Kopieren über Datenträger). |
| Nie automatisch löschen | Jede Schreibaktion ist ein **Plan**: Vorschau → Freigabe → Ausführung → Undo. Löschen gibt es nur als „in Quarantäne verschieben". Endgültiges Leeren der Quarantäne ist ein eigener, separat freigegebener Plan. |
| Freigabe durch Yoka, nicht durch Claude | Claude kann Pläne **erstellen**, aber nicht **freigeben**. Freigabe nur über lokale CLI (`music-yoka plan approve <id>`) oder MCP-Elicitation, die Yoka im Client bestätigt. Vertrauensgrenze = der Server, nicht das Modell. |
| `collection.nml` nur bei geschlossenem Traktor | Vor jedem NML-Schreibvorgang Prozessprüfung (Traktor läuft → Abbruch), Backup mit Zeitstempel, atomares Schreiben (temp-Datei + Ersetzen), danach Parse-Test. |
| Alten Wert sichern | Jede Änderung (Tag, NML-Feld, Dateiname, Ort) schreibt vorher einen Eintrag in `wert_historie`. Undo liest daraus. |
| Sequenziell, Freigabe nach jedem Schritt | Arbeitspakete laut `docs/PLAN.md`; jedes endet mit Freigabe. |

## 3. Standardlösungen – Bewertung

| Lösung | Stärke | Grenze bei uns | Empfehlung |
|---|---|---|---|
| **beets** | Plugins `chroma`, `lastgenre`, `duplicates`, `keyfinder`, `autobpm`, MusicBrainz-Matching | Bibliothek arbeitet mit **absoluten Pfaden**, kennt keine Offline-Datenträger und keine Rechner; Import ist interaktiv und bei 100k langsam; Default-Konfiguration verschiebt/benennt Dateien | **Nicht als Kern-DB.** Die gleichen Bibliotheken direkt nutzen (`pyacoustid`, `musicbrainzngs`, `pylast`). beets optional als Vergleich für einzelne Ordner (mit `move: no`, `copy: no`, `write: no`). |
| **dupeGuru** | Bewährter Musik-Modus (Tags, Inhalt) | GUI, nicht datenträgerbewusst, keine Versionen-Logik (Remix ≠ Duplikat) | Nur als **Zweitmeinung** bei Verdachtsfällen. |
| **Chromaprint / AcoustID** | Standard für Audio-Fingerabdruck | AcoustID-API ca. 3 Anfragen/s | **Nutzen** (Modul 1, Modul 4 Stufe 2). |
| **MusicBrainz** | Release-Daten, ISRC, first-release-date, Disc-ID | 1 Anfrage/s | **Nutzen** mit lokalem Cache. |
| **Essentia** | BPM, Key, Energie, Lautheit in einem | **Keine Windows-Wheels** auf PyPI (nur Linux/macOS) – zu prüfen | Auf Mac oder WSL2 ausführen; unter Windows `librosa` + `pyloudnorm` als Ersatz. |
| **Traktor-Analyse** | BPM, Key, Beatgrid, Lautheit liegen in `collection.nml` schon vor | Nur für Tracks in der Collection | **Zuerst übernehmen**, nur Fehlendes selbst berechnen. |
| **NI-Stem-Dateien** (`.stem.mp4`) | Enthalten Drums und Bass bereits getrennt | Nur wo vorhanden | **Bevorzugte Quelle** für Bassart-Erkennung. |

## 4. Systemübersicht

```
 Rechner A (Windows)        Rechner B (Mac, Traktor)        NAS / USB / HDD
 ┌──────────────────┐      ┌──────────────────────┐
 │ music-yoka scan  │      │ music-yoka scan      │
 │ (leichter Agent) │      │ + NML-Lesen/Schreiben│
 └────────┬─────────┘      └──────────┬───────────┘
          │ Scan-Export (SQLite-Datei je Lauf)    │
          └──────────────┬─────────────────────────┘
                         ▼
               ┌───────────────────┐
               │ Zentrale DB        │  SQLite auf lokaler Platte des Hauptrechners
               │ + Import-Dienst    │  (nie über Netzwerkfreigabe geöffnet)
               └─────────┬─────────┘
                         │
     ┌───────────────────┼─────────────────────┐
     ▼                   ▼                     ▼
 MCP-Server         Module (Worker)        CLI (Freigaben,
 (stdio, Claude)    Analyse, Abfragen      Undo, Status)
                         │
                         ▼
             Spotify-Yoka-MCP-Cache (nur lesend) / externe APIs
```

### 4.1 Mehrere Rechner

- **Phase 1: Export/Import.** Jeder Scanner schreibt eine eigenständige Scan-Datei
  (SQLite, Schema-Version, Datenträger-ID, Zeitstempel). Die zentrale DB importiert sie.
  Vorteil: funktioniert offline, kein Dienst nötig, keine Netzwerk-Sperren.
- **Später optional: zentraler Dienst** (HTTP, nur LAN) für Live-Abfragen von anderen Rechnern.
- **Nie:** SQLite-Datei über SMB/AFP öffnen (Sperren unzuverlässig → Korruption).

### 4.2 Wo läuft was

| Komponente | Ort | Grund |
|---|---|---|
| Zentrale DB + MCP-Server | **Mac** (F1) | Eine Wahrheit; Claude Desktop und Traktor auf demselben Rechner |
| Scanner | jeder Rechner mit Musik | liest nur, schreibt Scan-Datei; Windows-Scans werden auf den Mac importiert |
| NML-Schreiber | **Mac** (F2, Traktor läuft nur dort) | NML liegt dort, Traktor-Prozessprüfung lokal |
| Audio-Analyse (Essentia) | Mac | Essentia ist dort per pip verfügbar |
| Datei-Schreibaktionen (Tags, Umbenennen, Quarantäne) | Rechner, an dem der Datenträger hängt | nur online-Datenträger |

## 5. Datenträger und Dateiidentität

### 5.1 Datenträger-ID

- Schema: `HDD-001`, `SSD-001`, `PC-01`, `NAS-01`, `USB-001`, `CD-0001`, `DVD-0001`.
- Erkennung doppelt abgesichert:
  1. **Kennungsdatei** `.music-yoka-volume.json` im Wurzelverzeichnis (ID, UUID, Anlagedatum).
     Wird nur nach Freigabe angelegt; ist eine Datei, kein Ordner.
  2. **Volume-Seriennummer / Volume-UUID** (Windows `GetVolumeInformation`, macOS `diskutil info`).
- Read-only-Medien (CD/DVD): keine Kennungsdatei, stattdessen Seriennummer bzw. MusicBrainz-Disc-ID.
- Felder: Lagerort, Kapazität, Rolle (Archiv / Arbeitskopie / Backup), Rechner,
  Mountpunkt/Laufwerksbuchstabe (zuletzt gesehen), zuletzt gescannt, online/offline.
- **Offline-Datenträger bleiben vollständig durchsuchbar** (nur Schreibaktionen gesperrt).

### 5.2 Datei = Datenträger-ID + relativer Pfad

- Pfad relativ zur Datenträger-Wurzel, Trenner `/`.
- **Unicode-Normalisierung NFC** beim Speichern (macOS liefert NFD → sonst Scheinduplikate
  und kaputte Abgleiche zwischen Mac und Windows). Originalschreibweise zusätzlich gespeichert.
- Groß-/Kleinschreibung: Flag je Datenträger (NTFS/APFS meist case-insensitive).

### 5.3 Hashes

| Hash | Zweck | Verfahren |
|---|---|---|
| `file_hash` | Änderung erkennen, Stufe-1-Duplikate (identische Datei) | BLAKE3 über die ganze Datei |
| `audio_hash` | Identische Audiodaten trotz anderer Tags | BLAKE3 nur über den Audio-Datenbereich (ohne ID3/Vorbis/MP4-Metadaten) |
| `fingerprint` | Gleiche Aufnahme, anderes Format/Bitrate | Chromaprint (`fpcalc`) |

`audio_hash` ist wichtig, weil wir selbst Tags schreiben: Danach ändert sich `file_hash`,
die Datei ist aber dieselbe.

## 6. Scanner

- **Inkrementell:** Größe + mtime unverändert → überspringen. Sonst Hash neu.
- **Fortsetzbar:** Fortschritt je Ordner in der Scan-Datei; Abbruch und Wiederaufnahme jederzeit.
- **Parallel:** Hashing/Tag-Lesen in Prozess-Pool; Anzahl je Datenträgertyp (HDD: 1–2 Threads,
  SSD/NVMe: mehr). HDDs nicht mit vielen parallelen Lesern zerlesen.
- **Priorisierbar:** Datenträger/Ordner-Reihenfolge per Konfiguration.
- **Nur lesend.** Der Scanner schreibt nie in den Datenträger (außer der freigegebenen Kennungsdatei).
- Tag-Reader: `mutagen` (MP3/ID3, FLAC, AIFF, WAV, M4A/MP4, OGG, Opus).
- Formate ohne Tags (WAV) → Metadaten aus Dateiname/Ordner nur als *Vorschlag*.

### Mengengerüst (Schätzung, zu messen)

| Schritt | Kosten je Track | 100k Tracks |
|---|---|---|
| Hash (Ø 12 MB, HDD 150 MB/s) | ~0,1 s | ~3 h je Datenträger-TB |
| Tags lesen | < 10 ms | Minuten |
| Chromaprint | 0,2–0,5 s | 6–14 h (parallel deutlich weniger) |
| AcoustID-Abfrage (3/s) | – | ~9 h |
| MusicBrainz (1/s, gecacht) | – | bis ~28 h, einmalig |
| BPM/Key/Energie | 1–3 s | 1–3 Tage CPU, parallel Stunden |
| Bassart (Separation eines 4-Takt-Ausschnitts) | 10–60 s | nur auf Auswahl sinnvoll |

## 7. Datenmodell (Überblick, Detail in Schritt 3)

| Tabelle | Inhalt |
|---|---|
| `datentraeger` | ID, UUID/Seriennummer, Typ, Rolle, Lagerort, Kapazität, Rechner, Status, zuletzt gescannt |
| `dateien` | Datenträger-ID, relativer Pfad, Größe, mtime, Hashes, Format, Bitrate, Samplerate, Bittiefe, Dauer, Scan-Stand |
| `tracks` | logische Aufnahme (Artist, Titel, Mix/Remix, ISRC, MBID, Release-Jahr + Konfidenz) – mehrere Dateien je Track |
| `tags_roh` | gelesene Tags je Datei (unverändert) |
| `analyse` | BPM, Key, Camelot, Energie, Lautheit, Spektral-Cutoff, Clipping, Bassmuster – mit Quelle (Traktor, Essentia, librosa, manuell) |
| `pools` / `pool_regeln` | DJ-Pools (YOKA, KACHINA, …) und Regeln Datenträger + Unterordner → Pool |
| `duplikat_gruppen` / `duplikat_mitglieder` | Gruppe, Stufe (Hash/Fingerabdruck/Verdacht), beste Version, Begründung, gewollte Backup-Kopie |
| `farben` | Farbvorschlag, Begründung, Status (vorgeschlagen/bestätigt/übernommen) |
| `traktor_eintraege` | Spiegel der NML-Einträge (LOCATION, INFO-Felder, BPM, Key, Color) je Collection |
| `spotify_match` | Spotify-Track-ID, Methode (ISRC / Artist+Titel+Dauer), Konfidenz, Status |
| `plaene` / `plan_schritte` | Vorschau, Freigabe (wer, wann), Ausführung, Undo-Status |
| `wert_historie` | Objekt, Feld, alter Wert, neuer Wert, Plan-ID, Zeitpunkt |
| `api_cache` | Antworten MusicBrainz/AcoustID/Last.fm/Discogs mit Ablaufdatum |
| `pruefliste` | offene Fälle (Widersprüche, unsichere Matches, Verdachtsduplikate) |

## 8. Plan-/Freigabe-/Undo-Mechanik

```
erstellen ──► Vorschau (Diff-Liste) ──► Freigabe Yoka ──► Ausführung ──► ausgeführt
                                          │                    │
                                          ▼                    ▼
                                      verworfen        Undo (aus wert_historie)
```

- Ein Plan enthält konkrete Schritte mit Vorher/Nachher (Datei, Feld, Wert, Pfad).
- **Vor Ausführung erneute Prüfung:** Datei unverändert (Hash/mtime wie in der Vorschau)?
  Sonst Schritt überspringen und in Prüfliste.
- Teilausführung erlaubt; jeder Schritt einzeln protokolliert und einzeln rückgängig machbar.
- Pläne sind Datenbankobjekte → auch über mehrere Sitzungen und Rechner nachvollziehbar.

## 9. Traktor-Anbindung (`collection.nml`)

### 9.1 Feldbelegung (Vorgabe)

| Traktor-Spalte | Inhalt | NML-Attribut (Annahme, Schritt 2 verifiziert) |
|---|---|---|
| Comment 2 | `OLDSCHOOL · <64-Zeichen-Bassmuster>`, ohne Oldschool nur Muster | `INFO@RATING` |
| Color | Farbschema Modul 9 | `INFO@COLOR` (1–7) |
| Cat. No. | DJ-Pool | `INFO@CATALOG_NO` |
| Comment | darf überschrieben werden; **Inhalt offen** – erst nach Feldinventar P2 (F5) | `INFO@COMMENT` + ID3 `COMM` |

### 9.2 Abläufe

- **Lesen:** NML parsen → `traktor_eintraege`; Zuordnung zur Datei über `LOCATION`
  (`VOLUME`, `DIR` mit `/:`-Trennern, `FILE`, `VOLUMEID`).
  Übernahme von Traktor-BPM, Key, Beatgrid, Farben (Trainingsdaten Modul 9).
- **Schreiben:** nur Plan-basiert; Traktor-Prozess muss beendet sein; Backup
  `collection_YYYYMMDD-HHMMSS.nml`; atomar ersetzen; danach Parse- und Stichprobentest.
- **Umbenennen (Modul 6):** Dateiname, `LOCATION@FILE` **und** alle Playlist-Verweise
  (`PRIMARYKEY KEY="…"`) im selben Plan. Sonst verliert Traktor die Datei in Playlists.
- **ID3-Comment schreiben** ändert das Datei-Datum → Traktor liest Tags evtl. neu und kann
  den Traktor-eigenen `PRIV`-Frame bevorzugen. Deshalb Reihenfolge:
  1. Datei-Tags schreiben, 2. NML schreiben, 3. Konsistenzprüfung nach Traktor-Start
  (Stichprobe NML gegen DB).
- Mehrere Traktor-Installationen/Versionen: Collection-Pfad je Rechner konfigurierbar,
  Mac-Standard `~/Documents/Native Instruments/Traktor 4.5.x/`.

## 10. Module

Jedes Modul: einzeln ausführbar, per Konfiguration an/aus, mit Umfang
(Datenträger / Ordner / Pool / Genre), Priorität und Fortschrittsstand.
Ergebnis eines Moduls ist **immer zuerst DB-Wissen**; Änderungen an Dateien/NML nur über Pläne.

| # | Modul | Kern | Quellen / Werkzeuge |
|---|---|---|---|
| 1 | Identifikation | Fingerabdruck → AcoustID → MusicBrainz-Recording/ISRC | `pyacoustid`, `fpcalc`, `musicbrainzngs` |
| 2 | Genre | Last.fm-Top-Tags **pro Artist** (nicht pro Track), Whitelist/Mapping | `pylast`, beets-`lastgenre`-Whitelist als Vorlage |
| 3 | Audio-Analyse | BPM, Key/Camelot, Energie, Lautheit (LUFS) | Traktor-Werte zuerst; Essentia (Mac/WSL2) oder librosa + pyloudnorm |
| 4 | Duplikate | Stufen Hash → Fingerabdruck → Verdacht; beste Version | eigene Logik, § 10.1 |
| 5 | Playlists | Export M3U/M3U8, Rekordbox XML, Traktor-Playlist in NML | Standardformate |
| 6 | Dateinamen | „Artist - Titel" / „Artist - Titel (Remix-Artist Remix)", nur im selben Ordner | geprüfte DB-Metadaten, NML-Pfade im selben Plan |
| 7 | CD/DVD | Audio-CD: Disc-ID; Daten-Discs scannen, danach offline | `discid`, Scanner |
| 8 | Bassart | 64-Zeichen-Muster aus Kick + Bass, § 10.2 | NI-Stems / vorhandene Stems; sonst Separation (ki-studio-mackie) |
| 9 | Farbe | Vorschlag je Track, Übernahme nach Bestätigung | BPM, Energie, Genre, Key; vorhandene Traktor-Farben als Trainingsdaten |
| 10 | Release-Jahr + Oldschool | frühestes plausibles Datum, Konfidenz, Widersprüche → Prüfliste; < Grenzjahr → OLDSCHOOL | ID3, MusicBrainz `first-release-date`, Discogs, Spotify |
| 11 | DJ-Pool | Regeln Datenträger + Unterordner → Pool | Einrichtung gemeinsam mit Yoka |

### 10.1 Duplikat-Logik

- **Stufe 1 – Hash:** gleicher `audio_hash` → sicheres Duplikat.
- **Stufe 2 – Fingerabdruck:** gleicher Chromaprint + Dauer ±2 s → gleiche Aufnahme.
- **Stufe 3 – Verdacht:** ähnliche Tags/Dauer → **nur Prüfliste**, nie Aktion.
- **Keine Duplikate:** Original / Extended / Radio Edit / Remix (Mix-Bezeichnung + Dauer
  unterscheiden sich). Gleicher Track in verschiedenen DJ-Pools bleibt erhalten.
- **Beste Version** (gewichtete, konfigurierbare Punkte):
  verlustfrei > verlustbehaftet → Bitrate/Samplerate/Bittiefe → **Fake-Lossless-Prüfung**
  (Spektral-Cutoff, z. B. FLAC mit Abriss bei 16 kHz = ehemals MP3) → Vollständigkeit
  (Dauer vs. Referenz) → Tag-Qualität → Clipping → Speicherort-Priorität.
- **Gewollte Backup-Kopien** (Datenträger-Rolle „Backup" oder manuell markiert) zählen nicht.
- Aktionen (Quarantäne) nur auf **online**-Datenträgern, nur per Plan.

### 10.2 Bassart-Erkennung

- Raster: 16tel, 16 Zeichen je Takt, **immer 4 Takte = 64 Zeichen**.
- Zeichen: `I` = Kick, `X` = Bass, `0` = Leerstelle.
  - Offbeat: `I0X0I0X0I0X0I0X0` (×4)
  - Reiter/16tel: `IXXXIXXXIXXXIXXX` (×4)
  - Kick und Bass auf derselben 16tel → **`I`** (Kick hat Vorrang, F3).
- Ablauf:
  1. **Beatgrid:** Traktor-Grid (BPM + erster Downbeat aus NML) bevorzugen, sonst eigene Beat-/Downbeat-Erkennung.
  2. **Ausschnitt:** 4 Takte aus einem repräsentativen Abschnitt (z. B. erster Abschnitt mit voller Energie) –
     nicht der ganze Track. Spart >90 % Rechenzeit.
  3. **Stems:** NI-Stem-Datei (Drums, Bass) → sonst vorhandene Stems → sonst Separation
     (`stem_pipeline.py` SCNet → `larsnet_drumsep.py` für Kick aus `drums.wav`, Repo ki-studio-mackie).
  4. **Onsets** je Stem (Spectral Flux, wie `drums_to_midi.py`) → auf 16tel quantisieren.
  5. Muster schreiben, Konfidenz speichern; unsichere Muster → Prüfliste.
- Optional je Ordner/Genre/Datenträger.
- Wiederverwendung aus ki-studio-mackie: **Kopie** der nötigen Funktionen mit Herkunftsvermerk
  (Quelldatei + Commit) im Dateikopf (F4). Feste Pfade wie `F:\Tools\larsnet` werden zu Konfiguration.

## 11. Spotify-Verknüpfung

- Spotify-Yoka-MCP (TypeScript, Cache `~/.spotify-mcp.db`) wird **nur gelesen**.
- **Lücken im heutigen Spotify-Cache:** kein ISRC, keine Dauer, `tracks.id` als
  Primärschlüssel mit einer `playlist_id` (Track in mehreren Playlists wird überschrieben).
  → **Spotify-Repo wird erweitert** (F7): `isrc`, `duration_ms`, Tabelle `playlist_tracks`.
  Eigener Auftrag im Spotify-Repo, Voraussetzung für P5l.
- Abgleich: **ISRC**, Fallback Artist + Titel + Dauer (±3 s), unsichere Treffer → Prüfliste.
- Auswertungen: lokal vs. nur Spotify, Playlist-Übernahme, gemeinsame Genre-Daten,
  **Fehlliste** (Spotify-Track ohne lokale verlustfreie Version).
- Spotify-API-Bedingungen (Entwicklermodus, verfügbare Endpunkte) bei Umsetzung prüfen.

## 12. MCP-Schnittstelle (Entwurf)

Prinzip wie Yoka-DAW: **lesen frei, schreiben nur über Pläne, freigeben nur Yoka.**

| Gruppe | Tools (Entwurf) |
|---|---|
| Status | `get_status`, `list_volumes`, `get_volume` |
| Suche | `search_tracks` (Artist, Titel, Genre, BPM, Key, Pool, Jahr, Datenträger, online/offline), `get_track`, `get_file` |
| Scans/Module | `start_job`, `get_job`, `list_jobs` |
| Prüfungen | `list_review_items`, `resolve_review_item` (setzt nur DB-Wissen) |
| Duplikate | `list_duplicate_groups`, `get_duplicate_group` |
| Pläne | `create_plan` (Typ: tags, nml, rename, quarantine, playlist), `get_plan`, `list_plans` |
| Undo | `undo_plan` (selbst wieder ein Plan mit Freigabe) |
| Spotify | `match_spotify`, `list_missing_lossless` |

`approve_plan` gibt es **nicht** als frei aufrufbares Tool (§ 2).

## 13. Technik

- Python ≥ 3.12, Paketverwaltung **uv** (wie Yoka-DAW `src/mcp/`).
- MCP: offizielles `mcp`-SDK (FastMCP), stdio.
- SQLite mit WAL, Schema-Migrationen versioniert.
- Tests: pytest mit kleinen synthetischen Audiodateien und Beispiel-NML.
- Konfiguration: eine TOML-Datei je Rechner (Datenträger-Wurzeln, Collection-Pfad,
  Module, Prioritäten, Grenzjahr, Quarantäne-Pfade, API-Schlüssel per Umgebungsvariable).

## 14. Fragen und Entscheidungen

| # | Frage | Entscheidung (2026-10-27) |
|---|---|---|
| F1 | Auf welchem Rechner liegt die zentrale DB? | **Mac** (Yoka). |
| F2 | Läuft Traktor nur auf dem Mac? | **Ja** (Yoka). NML-Schreiber nur dort. |
| F3 | Zeichen, wenn Kick und Bass auf derselben 16tel liegen? | **`I`, Kick hat Vorrang** (Yoka). |
| F4 | ki-studio-mackie-Audio: Abhängigkeit oder Kopie? | **Kopie** mit Herkunftsvermerk (Yoka). |
| F5 | Was steht im ID3-Comment? | **Offen.** Erst Feldinventar in P2: welche Traktor-Felder es gibt, welche schon belegt sind (z. B. Genre), welche frei bleiben. Danach Entscheidung. |
| F6 | Datei-Datum nach Tag-Schreiben zurücksetzen? | **Nein** (nach Empfehlung). Gründe: Backup-Werkzeuge erkennen Änderungen über das Datum – mit zurückgesetztem Datum würden Backups die neuen Tags nie bekommen; Traktor soll die Änderung bemerken. Absicherung: Konsistenzprüfung NML ↔ DB nach Traktor-Start. Verhalten in P2 testen. |
| F7 | Spotify-Repo erweitern (ISRC, Dauer, playlist_tracks)? | **Ja** (Yoka). |
| F8 | Quarantäne-Ort je Datenträger? | **Nach Empfehlung:** ein Ordner `_MusicYoka_Quarantaene` je Datenträger in dessen Wurzel, neben (nicht in) den Musikordnern. Siehe § 14.1. |

### 14.1 Quarantäne (F8)

- **Gleicher Datenträger:** Verschieben ist dann ein atomares Umbenennen – kein Kopieren,
  kein zusätzlicher Speicher, kein halber Zustand bei Abbruch.
- **Flach, ohne Unterordner:** Dateiname `<Plan-ID>_<Datei-ID>_<Originalname>`.
- **`manifest.json` im Quarantäne-Ordner:** Originalpfad, Hash, Plan-ID, Datum je Datei –
  Wiederherstellung auch ohne zentrale DB möglich.
- **Anlegen nur einmal je Datenträger, per eigenem Plan mit Freigabe** (einzige erlaubte Ordneranlage).
- **Keine Quarantäne** auf Datenträgern mit Rolle „Backup" und auf Read-only-Medien.
- Pfad je Datenträger in der Konfiguration überschreibbar.
- Leeren der Quarantäne: eigener Plan mit Freigabe, nie automatisch.
