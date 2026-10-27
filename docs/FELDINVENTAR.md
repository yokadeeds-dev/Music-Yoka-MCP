# Feldinventar Traktor (P2, Schritt 1)

Stand 2026-10-27. Quelle: **Kopie** von `Traktor 4.5.1/collection.nml` (19.557 Einträge),
nur lesend ausgewertet mit `tools/nml_feldinventar.py`. Die Kopie liegt in `testdaten/`
(per `.gitignore` ausgeschlossen). Diese Datei enthält nur Zählungen, keine Tracknamen.

## 1. Traktor-Spalte ↔ NML-Attribut ↔ ID3-Frame

Spalte „ID3" = **Annahme**, wird im Schreibtest (P2, Schritt 4) an synthetischen MP3s geprüft.
„—" = in dieser Collection nie belegt (Traktor schreibt leere Attribute nicht).

| Traktor-Spalte | NML-Attribut | ID3 (Annahme) | belegt | Bemerkung |
|---|---|---|---:|---|
| Title | `ENTRY@TITLE` | TIT2 | 100,0 % | |
| Artist | `ENTRY@ARTIST` | TPE1 | 58,4 % | |
| Release (Album) | `ALBUM@TITLE` | TALB | 57,3 % | |
| Track No. | `ALBUM@TRACK` / `@OF_TRACKS` | TRCK | 45,2 % | |
| Mix | `INFO@MIX` | TIT3 | — | **frei** |
| Remixer | `INFO@REMIXER` | TPE4 | 0,2 % | fast frei |
| Producer | `INFO@PRODUCER` | TCOM? | 0,1 % | fast frei, nur Werbung |
| Label | `INFO@LABEL` | TPUB | 8,6 % | |
| Cat. No. | `INFO@CATALOG_NO` | TXXX? | — | **frei** → DJ-Pool (M-Vorgabe) |
| Genre | `INFO@GENRE` | TCON | 21,9 % | 134 Werte, mit Werbung/Tippfehlern |
| Comment | `INFO@COMMENT` | COMM | 17,5 % | Inhalt siehe § 3 (F5) |
| Comment 2 | `INFO@RATING` | ? | — | **frei** → OLDSCHOOL + Bassmuster (16 Zeichen, M24) |
| Lyrics | `INFO@KEY_LYRICS` | USLT | 0,3 % | nur Werbung/Release-Infos |
| Key Text | `INFO@KEY` | TKEY | 55,7 % | Open-Key-Notation (`11m`, `12d`) |
| Key (Analyse) | `MUSICAL_KEY@VALUE` | – | 99,2 % | 0–23, Traktor-intern |
| BPM | `TEMPO@BPM` | TBPM | 99,2 % | |
| Rating (Sterne) | `INFO@RANKING` | POPM | 7,2 % | 0/51/102/153/204/255; Yokas eigene Wertung, nicht anfassen |
| Color | `INFO@COLOR` | – (nur PRIV?) | 1,0 % | Werte 1–7, siehe § 2 |
| Release Date | `INFO@RELEASE_DATE` | TDRC/TYER | 43,3 % | fast immer `JJJJ/1/1` = nur Jahr |
| Import Date | `INFO@IMPORT_DATE` | – | 100,0 % | |
| Last Played / Playcount | `INFO@LAST_PLAYED` / `@PLAYCOUNT` | – | 17,6 % | |
| Cover | `INFO@COVERARTID` | APIC | 44,1 % | |
| Bitrate, Länge, Größe | `INFO@BITRATE`, `@PLAYTIME(_FLOAT)`, `@FILESIZE` | – | 90–99 % | technisch |
| Analyse-Status | `INFO@FLAGS` | – | 99,2 % | Bitmaske, 16 Werte |
| Lautheit | `LOUDNESS@*` | – | 99,3 % | |
| Cues / Grid | `CUE_V2` (TYPE 0/4/5) | – | 99,2 % | Grid-Start für Bassart (P5i) |
| Stems | `STEMS@STEMS` | – | 16,4 % | Stem-Dateien vorhanden |
| Pfad | `LOCATION@VOLUME/DIR/FILE/VOLUMEID` | – | 100,0 % | 7 Volumes |
| Fingerabdruck | `ENTRY@AUDIO_ID` | – | 99,3 % | Traktor-eigen, hilft beim Wiederfinden verschobener Dateien |

Nicht in den NML-Attributen: Playlists (`PLAYLISTS`, Verweis über `PRIMARYKEY`), Sets (`SETS`),
`INDEXING`. Achtung beim Parsen: Playlist-Verweise sind ebenfalls `ENTRY`-Elemente, aber ohne `LOCATION`.

**Nachweis Comment 2 / Cat. No.:** `RATING`, `CATALOG_NO` und `MIX` kommen in **keiner** der
7 vorhandenen Collections (4.1.1–4.5.1) vor. Die Zuordnung ist im Schreibtest bestätigt (§ 4).

## 2. Farben

Belegt in 186 Einträgen: Index 1 (5), 2 (115), 3 (24), 4 (11), 5 (26), 6 (3), 7 (2).
Die Namen lassen sich nicht aus der NML ablesen.

- **Farbmenü Traktor 4.5.1** (Yoka): Red, Yellow, Blue, Magenta, Cyan, Green, Orange, None.
- **Anzeige der Beispieltracks** (Yoka): 1 Rot, 2 Orange, 3 Gelb, 4 Grün, 5 Blau, 6 Magenta, 7 Magenta.

**Im Schreibtest bestätigt (§ 4):** 1 Rot, 2 Orange, 3 Gelb, 4 Grün, 5 Blau, 6 Cyan, 7 Magenta.
Yokas Smartlists bestätigen das ebenfalls („o BLAU“ = `$COLOR == 5`, „o Orange“ = `$COLOR == 2`).
Farbschema Modul 9 siehe M23 (5 Farben, Magenta und Cyan Reserve).

**Bestand (Yoka):** Rot, Orange, Blau sind gültig vergeben (1: 5, 2: 115, 5: 26 Tracks).
Gelb, Grün, Index 6 und 7 (40 Tracks) sind alte Versuche und werden über Modul 9 neu gesetzt (M22).

**Befund: Farben in 4.5.1 verloren.** In der 4.5.0-Collection waren 609 Tracks farbig, in 4.5.1
nur 186. Die 424 fehlenden Farb-Tracks sind in 4.5.1 **gar nicht mehr in der Collection**
(Pfad nicht mehr vorhanden). 82 davon finden sich über `AUDIO_ID` unter neuem Pfad wieder
(meist aus Download-/Wetransfer-Ordnern in die Kachina-Ordner auf `AUDIO_XOS`), 80 davon
**ohne Farbe**. Die übrigen 342 sind nicht zuzuordnen. **Alle 424 sind gültige Farben**
(Rot 124, Blau 300) – also echte Arbeit, keine alten Versuche. Folge für Modul 9: die alten Collections
(4.1.1–4.5.0) als zusätzliche Trainingsdaten und Quelle für eine Farb-Wiederherstellung nutzen
(nur als Vorschlag mit Freigabe).

## 3. Comment heute (Grundlage für F5)

3.423 Einträge (17,5 %) haben einen Comment, 315 verschiedene Werte:

| Art | Einträge |
|---|---:|
| URLs/Werbung von Download-Seiten | ~1.550 |
| Zeichenfolge `IXXxI` (gleicher Wert in 899 Tracks) | 899 |
| lange `-`/`X`/`I`-Ketten (ca. 15 Tracks, Herkunft unklar) | ~18 |
| Sonstiges (Release-Gruppen, Jahreszahlen u. ä.) | ~960 |

Kein Comment enthält brauchbare, von Yoka gepflegte Information. `IXXxI` und die
`-`/`X`/`I`-Ketten sind alte Bassart-Versuche (Yoka) und werden überschrieben. Genre ist nur zu 22 % belegt und teils verschmutzt (Werbung im Genre-Feld,
`Psychadelic`/`Psychedelic`).

### F5 – entschieden (Yoka, 2026-10-27, M21)

1. **Genre bleibt im Genre-Feld** (Modul 2 füllt/bereinigt es) – keine Doppelung im Comment.
2. **Comment = durchsuchbare Stichworte, die sonst kein Feld haben**, z. B.
   `E7 · Vocal · Tribal` (Energie 1–10 aus Modul 3 + kurze Merkmale).
   Traktor durchsucht Comment, damit sind die Stichworte im Browser filterbar.
3. Vorhandene Werbe-Comments werden dabei überschrieben (laut Vorgabe erlaubt;
   alter Wert in `wert_historie`).
4. **Frei bleiben** vorerst: Mix, Producer, Lyrics (Reserve).

## 4. Schreibtest (P2, Schritt 3, 2026-10-27)

Werkzeug `tools/traktor_schreibtest.py`. Ablauf: Traktor beendet (Prozessprüfung) → Backup
`collection_20261027-083058.nml` + SHA-256 → Test-Collection mit 7 synthetischen WAV-Tracks
(`testdaten/traktor_test/`) atomar eingesetzt → Prüfung in Traktor durch Yoka → Traktor
beendet → Rückschrieb ausgewertet → Original zurück, **Prüfsumme identisch**.

| Prüfung | Ergebnis |
|---|---|
| `INFO@COLOR` 1–7 | 1 Rot, 2 Orange, 3 Gelb, 4 Grün, 5 Blau, 6 Cyan, 7 Magenta |
| `INFO@RATING` → Spalte Comment 2 | ✔ angezeigt, auch `OLDSCHOOL · ` + 64 Zeichen, `·` korrekt |
| `INFO@CATALOG_NO` → Spalte Cat. No. | ✔ |
| `INFO@COMMENT` → Spalte Comment | ✔ |
| Browser-Suche | findet Werte aus Cat. No. und Comment 2 (z. B. `YOKA OLDSCHOOL`) |
| Rückschreiben durch Traktor beim Beenden | alle Werte unverändert erhalten |

Folge: 64 Zeichen sind in der Spalte zu lang → Bassmuster auf 16 Zeichen (M24).
Hinweis: Die Smartlists „MORNING (2)“/„NACHT“/„COSMIC ALTERNATIVE“ filtern nach Comment.
Nur 3 Tracks haben tatsächlich `MORNING` als Comment (alle schon Blau); bei Umsetzung von M21
sollten diese Smartlists auf `$COLOR` umgestellt werden (Vorschlag, Yoka entscheidet).

## 5. ID3-Test (P2, Schritt 4, 2026-10-27)

Werkzeug `tools/traktor_id3test.py` (`.venv` mit mutagen, lameenc). 4 synthetische MP3s mit
ID3v2.3-Comment, Test-Collection wie in § 4, zwei Traktor-Runden, Original danach byte-genau zurück.

| Track | Ausgang | Beim Start | Nach Laden ins Deck |
|---|---|---|---|
| A | nur ID3 `ID3 A`, NML leer, Datei neuer | leer | `ID3 A` |
| B | ID3 `ID3 B` (Datei 2026-01-01), NML `NML B` (neuer) | `NML B` | `NML B` |
| C | ID3 `ID3 C` (Datei neuer), NML `NML C` (2026-01-01) | `NML C` | `ID3 C` |
| D, Runde 1 | wie B; Yoka ändert in Traktor auf `Traktor D` | `NML D` | → `Traktor D` |
| D, Runde 2 | beide COMM per mutagen `Mutagen D`, PRIV unverändert `Traktor D`, Datei neuer | – | `Mutagen D` |

Befunde:

1. **`ENTRY@MODIFIED_DATE`/`MODIFIED_TIME` = Datei-Datum (UTC, Sekunden seit Mitternacht)**
   zum Zeitpunkt des letzten Einlesens/Schreibens durch Traktor.
2. **Traktor liest Datei-Tags neu, wenn ein Track geladen wird und die Datei neuer ist als
   `MODIFIED_*`.** Beim Start allein wird nichts neu gelesen. Der Wert aus der Datei
   **überschreibt** dann den NML-Wert.
3. **Comment ändern in Traktor** schreibt in die Datei: `COMM` (desc leer), `COMM` (desc
   `ID3v1 Comment`) und einen **PRIV-Frame `TRAKTOR4`** (770 B, enthält u. a. den Comment als
   UTF-16 im Block `COMM`). Datei-Datum wird neu.
4. **ID3-`COMM` gewinnt gegen einen veralteten PRIV-Frame.** Traktor aktualisiert den PRIV-Frame
   beim Einlesen nicht.
5. Nur Laden ins Deck schreibt nichts in die Datei.

Folgen für das Schreiben (→ ARCHITEKTUR § 9.2, M26):

- M16 (Datei-Datum nicht zurücksetzen) ist **bestätigt**: Nur so übernimmt Traktor neue Tags.
- Beim Tag-Schreiben **alle** COMM-Frames gleich setzen (auch `ID3v1 Comment`); PRIV nicht anfassen.
- NML und Datei-Tags im **selben Plan** konsistent schreiben – sonst überschreibt Traktor beim
  nächsten Laden den NML-Wert mit dem älteren Datei-Wert.
- Reine NML-Felder: siehe § 6 – ohne Gegenmaßnahme gefährdet.

## 6. Runde 3: reine NML-Felder beim Neu-Einlesen (2026-10-27)

Eigene Test-Collection (`testdaten/traktor_id3test_r3/`), Original danach byte-genau zurück.

| Runde | Ausgang (Track E) | Ergebnis nach Laden ins Deck |
|---|---|---|
| 3 | Comment 2 / Cat. No. / Color nur in NML, Datei neuer, **ohne PRIV** | alle drei bleiben ✔, Comment ← ID3 |
| 3 (Edit) | Yoka ändert Comment 2, Cat. No., Color in Traktor | Datei: nur `COMM` ×2 + **PRIV `TRAKTOR4`** (Blöcke u. a. `CTLG`, `COLR`); kein TXXX o. ä. |
| 3b | NML neu (`NML C2E`, `NML CatE`, Cyan), ID3-Comment neu, Datei neuer, **PRIV alt** (`Traktor F2`, `Traktor CatF`, Gelb) | Cat. No. bleibt ✔ · **Color ← PRIV (Gelb)** ✘ · **Comment 2 ← ID3-Comment-Text** ✘ · Comment ← ID3 |
| 3c | wie 3b, aber NML `MODIFIED_DATE/TIME` = neues Datei-Datum (UTC) | **alle NML-Werte bleiben** ✔ (kein Neu-Einlesen) |

Befunde:

1. Comment 2, Cat. No. und Color stehen in der Datei **nur im PRIV-Frame `TRAKTOR4`**,
   und nur, wenn sie in Traktor bearbeitet wurden.
2. Liest Traktor eine neuere Datei mit **altem PRIV** ein, überschreibt es **Color** (aus PRIV)
   und **Comment 2** (mit dem ID3-Comment-Text; Mechanismus unklar, bei D ohne Comment 2 im PRIV
   nicht aufgetreten). Cat. No. blieb erhalten.
3. Setzt man nach dem Datei-Schreiben `ENTRY@MODIFIED_DATE/TIME` auf das neue Datei-Datum (UTC),
   liest Traktor nicht neu ein – die NML-Werte bleiben vollständig. → M27.

Restrisiko: Erzwingt jemand in Traktor ein Neu-Einlesen (z. B. Tags neu laden / Konsistenzprüfung),
greift Befund 2 wieder. Gegenmittel später: Konsistenzprüfung NML ↔ DB nach Traktor-Lauf (§ 9.2).

## Anhang: Rohzählung

Elemente und Felder je Eintrag (je Eintrag einmal gezählt). Erzeugt mit
`python3 tools/nml_feldinventar.py testdaten/collection_4.5.1_kopie.nml`.

Einträge (COLLECTION/ENTRY): **19557**

Oberste Elemente: HEAD (1), COLLECTION (1), SETS (1), PLAYLISTS (1), INDEXING (1)

| Element | Einträge mit Element | Anteil |
|---|---:|---:|
| LOCATION | 19557 | 100.0% |
| MODIFICATION_INFO | 19557 | 100.0% |
| INFO | 19557 | 100.0% |
| LOUDNESS | 19414 | 99.3% |
| TEMPO | 19409 | 99.2% |
| CUE_V2 | 19409 | 99.2% |
| MUSICAL_KEY | 19395 | 99.2% |
| ALBUM | 11247 | 57.5% |
| STEMS | 3200 | 16.4% |
| LOOPINFO | 1 | 0.0% |

| Feld | belegt | Anteil | versch. Werte |
|---|---:|---:|---:|
| ALBUM@TITLE | 11197 | 57.3% | 5301 |
| ALBUM@TRACK | 8837 | 45.2% | 103 |
| ALBUM@OF_TRACKS | 468 | 2.4% | 27 |
| CUE_V2@NAME | 19409 | 99.2% | 4 |
| CUE_V2@DISPL_ORDER | 19409 | 99.2% | 1 |
| CUE_V2@TYPE | 19409 | 99.2% | 3 |
| CUE_V2@START | 19409 | 99.2% | 26228 |
| CUE_V2@LEN | 19409 | 99.2% | 236 |
| CUE_V2@REPEATS | 19409 | 99.2% | 1 |
| CUE_V2@HOTCUE | 19409 | 99.2% | 9 |
| CUE_V2@COLOR | 9144 | 46.8% | 1 |
| ENTRY@TITLE | 19554 | 100.0% | 16501 |
| ENTRY@MODIFIED_DATE | 19443 | 99.4% | 335 |
| ENTRY@MODIFIED_TIME | 19443 | 99.4% | 7580 |
| ENTRY@AUDIO_ID | 19413 | 99.3% | 17418 |
| ENTRY@ARTIST | 11417 | 58.4% | 5169 |
| ENTRY@LOCK | 37 | 0.2% | 2 |
| ENTRY@LOCK_MODIFICATION_TIME | 37 | 0.2% | 11 |
| INFO@IMPORT_DATE | 19556 | 100.0% | 393 |
| INFO@PLAYTIME | 19437 | 99.4% | 801 |
| INFO@BITRATE | 19434 | 99.4% | 3798 |
| INFO@FLAGS | 19410 | 99.2% | 16 |
| INFO@FILESIZE | 18027 | 92.2% | 9365 |
| INFO@PLAYTIME_FLOAT | 17777 | 90.9% | 11615 |
| INFO@KEY | 10898 | 55.7% | 114 |
| INFO@COVERARTID | 8627 | 44.1% | 4953 |
| INFO@RELEASE_DATE | 8477 | 43.3% | 325 |
| INFO@GENRE | 4275 | 21.9% | 134 |
| INFO@PLAYCOUNT | 3436 | 17.6% | 23 |
| INFO@LAST_PLAYED | 3436 | 17.6% | 202 |
| INFO@COMMENT | 3423 | 17.5% | 315 |
| INFO@LABEL | 1679 | 8.6% | 546 |
| INFO@RANKING | 1405 | 7.2% | 6 |
| INFO@COLOR | 186 | 1.0% | 7 |
| INFO@KEY_LYRICS | 61 | 0.3% | 20 |
| INFO@REMIXER | 39 | 0.2% | 34 |
| INFO@PRODUCER | 23 | 0.1% | 3 |
| LOCATION@DIR | 19557 | 100.0% | 671 |
| LOCATION@FILE | 19557 | 100.0% | 18054 |
| LOCATION@VOLUME | 19557 | 100.0% | 7 |
| LOCATION@VOLUMEID | 19557 | 100.0% | 7 |
| LOOPINFO@SAMPLE_TYPE_INFO | 1 | 0.0% | 1 |
| LOUDNESS@PEAK_DB | 19414 | 99.3% | 16106 |
| LOUDNESS@PERCEIVED_DB | 19414 | 99.3% | 17598 |
| LOUDNESS@ANALYZED_DB | 19400 | 99.2% | 17592 |
| MODIFICATION_INFO@AUTHOR_TYPE | 19557 | 100.0% | 2 |
| MUSICAL_KEY@VALUE | 19395 | 99.2% | 24 |
| STEMS@STEMS | 3200 | 16.4% | 667 |
| TEMPO@BPM | 19409 | 99.2% | 6482 |
| TEMPO@BPM_QUALITY | 19409 | 99.2% | 1 |
| TEMPO@BPM_TRANSIENTCOHERENCE | 14 | 0.1% | 14 |
