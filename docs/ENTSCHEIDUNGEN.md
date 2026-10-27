# Entscheidungen

Format: Nummer, Entscheidung, Grund, Status. P1 freigegeben am 2026-10-27.

| # | Entscheidung | Grund | Status |
|---|---|---|---|
| M1 | Eigene Kern-DB, kein beets als Bibliothek | beets kennt keine Datenträger/Offline-Medien, arbeitet mit absoluten Pfaden, Import bei 100k langsam | entschieden (Freigabe P1) |
| M2 | Bibliotheken der beets-Plugins direkt nutzen (`pyacoustid`, `musicbrainzngs`, `pylast`) | gleiche Qualität, volle Kontrolle | entschieden (Freigabe P1) |
| M3 | Datei = Datenträger-ID + relativer Pfad (NFC, `/`) | rechner- und mountpunktunabhängig; Mac/Windows-Unicode | entschieden (Freigabe P1) |
| M4 | Zwei Hashes: `file_hash` + `audio_hash` (BLAKE3) | eigene Tag-Schreibvorgänge dürfen Identität nicht ändern | entschieden (Freigabe P1) |
| M5 | Mehrere Rechner per Scan-Export/Import, kein SQLite über Netzwerk | Robustheit, offline-fähig | entschieden (Freigabe P1) |
| M6 | Jede Schreibaktion ist ein Plan; Freigabe nur durch Yoka (CLI/Elicitation), nicht durch Claude | harte Regel „nie automatisch", Vertrauensgrenze im Server | entschieden (Freigabe P1) |
| M7 | Löschen nur als Quarantäne-Verschiebung; Leeren der Quarantäne eigener Plan | harte Regel | entschieden (Freigabe P1) |
| M8 | Traktor-Analysewerte (BPM, Key, Grid) zuerst übernehmen | spart Rechenzeit, konsistent mit dem, was Yoka in Traktor sieht | entschieden (Freigabe P1) |
| M9 | Bassart nur auf 4-Takt-Ausschnitt, Stems bevorzugt (NI-Stem, vorhandene Stems) | Separation des ganzen Tracks ist bei 100k nicht machbar | entschieden (Freigabe P1) |
| M10 | Python ≥ 3.12, uv, offizielles `mcp`-SDK, stdio | wie Yoka-DAW-MCP | entschieden (Freigabe P1) |
| M11 | Spotify-Yoka-MCP-Cache nur lesen; fehlende Felder (ISRC, Dauer, Playlist-Zuordnung) dort ergänzen | klare Zuständigkeit je Repo | **entschieden (F7, Yoka)** |
| M12 | Zentrale DB und MCP-Server auf dem Mac | F1, Yoka | entschieden |
| M13 | Traktor nur auf dem Mac; NML-Schreiber nur dort | F2, Yoka | entschieden |
| M14 | Bassmuster: Kick und Bass auf derselben 16tel → `I` | F3, Yoka | entschieden |
| M15 | Audio-Code aus ki-studio-mackie als Kopie mit Herkunftsvermerk | F4, Yoka | entschieden |
| M16 | Datei-Datum nach Tag-Schreiben nicht zurücksetzen | Backups erkennen Änderungen sonst nicht; Traktor soll Änderung sehen (F6, nach Empfehlung) | entschieden, Test in P2 |
| M17 | Quarantäne: `_MusicYoka_Quarantaene` je Datenträger in der Wurzel, flach, mit `manifest.json`; nicht auf Backup-/Read-only-Medien | atomares Verschieben, Wiederherstellung ohne DB (F8, nach Empfehlung) | entschieden |
| M18 | Inhalt Comment erst nach Feldinventar festlegen | vorhandene Felder (z. B. Genre) zuerst nutzen, keine Doppelbelegung (F5, Yoka) | offen bis P2 |
| M19 | Windows bekommt eine Lese-Kopie der DB (Export vom Mac, MCP dort nur lesend); später DB-Dienst im LAN für Live-Abfragen. Mac bleibt führend (M12). Transport der Kopie per Dateiablage (LAN oder Drive-Ordner), nicht über Git | Abfragen auch am Windows-Rechner, ohne zweite Wahrheit und ohne SQLite über Netzwerk (M5). Git: Binärdatei wird bei jedem Export komplett neu versioniert, Repo wächst ständig, Größengrenze 100 MB je Datei | entschieden (Yoka, 2026-10-27) |
