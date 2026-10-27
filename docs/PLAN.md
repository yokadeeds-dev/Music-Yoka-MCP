# Arbeitsplan

**Status: P1 fertig zur Freigabe – wartet auf Freigabe Yoka.**

Regel: sequenziell, ein Paket je Session, Freigabe nach jedem Paket.
Jeder Commit pflegt diesen Plan mit.

## Pakete

| Paket | Inhalt | Ergebnis / Abnahme |
|---|---|---|
| **P1** | Repo, Architektur, Feature-Matrix, Entscheidungen | Freigabe Dokumente + offene Fragen F1–F8 |
| **P2** | Traktor-Tests | 7 Farbnamen + NML-Indizes verifiziert; Comment 2 / Cat. No. / Color in Kopie der NML geschrieben, Traktor zeigt sie; ID3-Comment + PRIV-Frame-Verhalten dokumentiert |
| **P3** | DB-Schema | Tabellen Datenträger, Dateien, Tracks, Pools, Duplikatgruppen, Spotify-Match, Pläne, Wert-Historie; Migrationen; Tests |
| **P4** | Kern-Scanner + Datenträger-Erkennung | Scan eines Testdatenträgers, Wiederaufnahme, inkrementeller Zweitlauf; Export/Import; MCP lesend; CLI |
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

Reihenfolge P5: zuerst, was in Traktor sofort sichtbar wird (Cat. No., Comment 2 OLDSCHOOL, Color),
dann Analyse und Pflege.

## Fortschritt

- 2026-10-27 P1: Dokumente erstellt (ARCHITEKTUR, FEATURE_MATRIX, ENTSCHEIDUNGEN, PLAN).

## Offene Punkte

Siehe `docs/ARCHITEKTUR.md` § 14 (F1–F8).
