# Entscheidungen

Format: Nummer, Entscheidung, Grund. Status **vorgeschlagen** bis Freigabe P1.

| # | Entscheidung | Grund | Status |
|---|---|---|---|
| M1 | Eigene Kern-DB, kein beets als Bibliothek | beets kennt keine Datenträger/Offline-Medien, arbeitet mit absoluten Pfaden, Import bei 100k langsam | vorgeschlagen |
| M2 | Bibliotheken der beets-Plugins direkt nutzen (`pyacoustid`, `musicbrainzngs`, `pylast`) | gleiche Qualität, volle Kontrolle | vorgeschlagen |
| M3 | Datei = Datenträger-ID + relativer Pfad (NFC, `/`) | rechner- und mountpunktunabhängig; Mac/Windows-Unicode | vorgeschlagen |
| M4 | Zwei Hashes: `file_hash` + `audio_hash` (BLAKE3) | eigene Tag-Schreibvorgänge dürfen Identität nicht ändern | vorgeschlagen |
| M5 | Mehrere Rechner per Scan-Export/Import, kein SQLite über Netzwerk | Robustheit, offline-fähig | vorgeschlagen |
| M6 | Jede Schreibaktion ist ein Plan; Freigabe nur durch Yoka (CLI/Elicitation), nicht durch Claude | harte Regel „nie automatisch", Vertrauensgrenze im Server | vorgeschlagen |
| M7 | Löschen nur als Quarantäne-Verschiebung; Leeren der Quarantäne eigener Plan | harte Regel | vorgeschlagen |
| M8 | Traktor-Analysewerte (BPM, Key, Grid) zuerst übernehmen | spart Rechenzeit, konsistent mit dem, was Yoka in Traktor sieht | vorgeschlagen |
| M9 | Bassart nur auf 4-Takt-Ausschnitt, Stems bevorzugt (NI-Stem, vorhandene Stems) | Separation des ganzen Tracks ist bei 100k nicht machbar | vorgeschlagen |
| M10 | Python ≥ 3.12, uv, offizielles `mcp`-SDK, stdio | wie Yoka-DAW-MCP | vorgeschlagen |
| M11 | Spotify-Yoka-MCP-Cache nur lesen; fehlende Felder (ISRC, Dauer, Playlist-Zuordnung) dort ergänzen | klare Zuständigkeit je Repo | **entschieden (F7, Yoka)** |
| M12 | Zentrale DB und MCP-Server auf dem Mac | F1, Yoka | entschieden |
| M13 | Traktor nur auf dem Mac; NML-Schreiber nur dort | F2, Yoka | entschieden |
| M14 | Bassmuster: Kick und Bass auf derselben 16tel → `I` | F3, Yoka | entschieden |
| M15 | Audio-Code aus ki-studio-mackie als Kopie mit Herkunftsvermerk | F4, Yoka | entschieden |
| M16 | Datei-Datum nach Tag-Schreiben nicht zurücksetzen | Backups erkennen Änderungen sonst nicht; Traktor soll Änderung sehen (F6, nach Empfehlung) | entschieden, Test in P2 |
| M17 | Quarantäne: `_MusicYoka_Quarantaene` je Datenträger in der Wurzel, flach, mit `manifest.json`; nicht auf Backup-/Read-only-Medien | atomares Verschieben, Wiederherstellung ohne DB (F8, nach Empfehlung) | entschieden |
| M18 | Inhalt Comment erst nach Feldinventar festlegen | vorhandene Felder (z. B. Genre) zuerst nutzen, keine Doppelbelegung (F5, Yoka) | offen bis P2 |
