# Arbeitsplan

**Status: P2 läuft – Schritt 1 (Feldinventar) erledigt, F5 entschieden (M21), Farben M22. Nächster Schritt 3 (Schreibtest) wartet auf Freigabe.**

Regel: sequenziell, ein Paket je Session, Freigabe nach jedem Paket.
Jeder Commit pflegt diesen Plan mit.

## Pakete

| Paket | Inhalt | Ergebnis / Abnahme |
|---|---|---|
| **P1** | Repo, Architektur, Feature-Matrix, Entscheidungen | Freigabe Dokumente + offene Fragen F1–F8 |
| **P2** | Traktor-Tests + Feldinventar | **Feldinventar:** alle Traktor-Felder ↔ NML-Attribute ↔ ID3-Frames; Belegungsquote je Feld in einer *Kopie* der echten Collection (nur lesend); Vorschlag für freie Felder inkl. Comment (F5). 7 Farbnamen + NML-Indizes verifiziert; Comment 2 / Cat. No. / Color in NML-Kopie geschrieben, Traktor zeigt sie; ID3-Comment, Datei-Datum und PRIV-Frame-Verhalten dokumentiert (F6) |
| **P3** | DB-Schema | Tabellen Datenträger, Dateien, Tracks, Pools, Duplikatgruppen, Spotify-Match, Pläne, Wert-Historie; Migrationen; Tests |
| **P4** | Kern-Scanner + Datenträger-Erkennung | Scan eines Testdatenträgers, Wiederaufnahme, inkrementeller Zweitlauf; Export/Import; MCP lesend; CLI; Lese-Kopie für Windows (M19) |
| **P5a** | NML lesen + DJ-Pool → Cat. No. | Pool-Regeln mit Yoka; erster NML-Schreibplan |
| **P5b** | Release-Jahr + OLDSCHOOL | Prüfliste Widersprüche; Comment-2-Plan |
| **P5c** | Duplikate Stufe 1 | Gruppenliste, Quarantäne-Plan (kein Löschen) |
| **P5d** | Identifikation | AcoustID/MusicBrainz mit Cache und Ratenlimit |
| **P5e** | Farbvorschlag | Bestätigungsliste, Color-Plan |
| **P5f** | Genre | Last.fm pro Artist |
| **P5g** | Audio-Analyse | Traktor-Werte + Ergänzung |
| **P5h** | Duplikate Stufe 2/3 + beste Version | inkl. Fake-Lossless |
| **P5i** | Bassart | PoC auf 50 Tracks, dann Ausrollen je Ordner/Genre |
| **P5j** | Dateinamenpflege | Umbenennungsplan inkl. NML-Pfade |
| **P5k** | Playlists | M3U/M3U8, Rekordbox XML, Traktor |
| **P5l** | Spotify-Abgleich | nach Erweiterung Spotify-Repo |
| **P5m** | CD/DVD | Disc-ID, Daten-Discs |
| **P6** | DB-Dienst im LAN (M19) | Live-Abfragen vom Windows-Rechner; Mac führend; nur bei Bedarf |

Reihenfolge P5: zuerst, was in Traktor sofort sichtbar wird (Cat. No., Comment 2 OLDSCHOOL, Color),
dann Analyse und Pflege.

## Fortschritt

- 2026-10-27 P1: Dokumente erstellt (ARCHITEKTUR, FEATURE_MATRIX, ENTSCHEIDUNGEN, PLAN).
- 2026-10-27 P1: F1–F4, F7 von Yoka entschieden; F6, F8 nach Empfehlung; F5 nach P2 verschoben (M12–M18).
- 2026-10-27 P1: Repo yokadeeds-dev/Music-Yoka-MCP angelegt; P1 von Yoka freigegeben, M1–M10 entschieden.
- 2026-10-27 M19: Lese-Kopie für Windows (P4), DB-Dienst im LAN später (P6).
- 2026-10-27 P2/1: Feldinventar (`docs/FELDINVENTAR.md`, `tools/nml_feldinventar.py`); Comment 2/Cat. No. nirgends belegt; 424 Farb-Tracks aus 4.5.0 fehlen in 4.5.1.
- 2026-10-27 P2/1: Farbmenü von Yoka geliefert (kein Violett, dafür Cyan).
- 2026-10-27 M21/M22: Comment-Inhalt entschieden; Farbbestand Rot/Orange/Blau gültig.
- 2026-10-27 M20: Pool-Grundregel `+ Kachina +` → KACHINA, sonst YOKA.

## Offene Punkte

- Farbindex 6 (Cyan oder Violett/Magenta?) im Schreibtest klären.
- Modul 9: Ersatz für Violett (Tiefe Nacht/Afterhour) festlegen, sobald Index 6 geklärt.
- Verlorene Farben aus 4.5.0 (424 Tracks, Rot/Blau): Wiederherstellung als Plan (M22, frühestens P5a).
- Auftrag im Spotify-Repo: `isrc`, `duration_ms`, `playlist_tracks` (vor P5l).
