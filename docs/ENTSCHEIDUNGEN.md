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
| M11 | Spotify-Yoka-MCP-Cache nur lesen; fehlende Felder (ISRC, Dauer, Playlist-Zuordnung) dort ergänzen | klare Zuständigkeit je Repo | vorgeschlagen |
