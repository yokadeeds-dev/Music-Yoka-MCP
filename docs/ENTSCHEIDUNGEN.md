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
| M16 | Datei-Datum nach Tag-Schreiben nicht zurücksetzen | Backups erkennen Änderungen sonst nicht; Traktor soll Änderung sehen (F6, nach Empfehlung) | entschieden, in P2/4 bestätigt |
| M17 | Quarantäne: `_MusicYoka_Quarantaene` je Datenträger in der Wurzel, flach, mit `manifest.json`; nicht auf Backup-/Read-only-Medien | atomares Verschieben, Wiederherstellung ohne DB (F8, nach Empfehlung) | entschieden |
| M18 | Inhalt Comment erst nach Feldinventar festlegen | vorhandene Felder (z. B. Genre) zuerst nutzen, keine Doppelbelegung (F5, Yoka) | erledigt → M21 |
| M19 | Windows bekommt eine Lese-Kopie der DB (Export vom Mac, MCP dort nur lesend); später DB-Dienst im LAN für Live-Abfragen. Mac bleibt führend (M12). Transport der Kopie per Dateiablage (LAN oder Drive-Ordner), nicht über Git | Abfragen auch am Windows-Rechner, ohne zweite Wahrheit und ohne SQLite über Netzwerk (M5). Git: Binärdatei wird bei jedem Export komplett neu versioniert, Repo wächst ständig, Größengrenze 100 MB je Datei | entschieden (Yoka, 2026-10-27) |
| M20 | DJ-Pool-Grundregel: Pfad enthält einen Ordner `+ Kachina +` → **KACHINA**, sonst → **YOKA**. Gilt auf allen Datenträgern; weitere Pools später ergänzbar | Vorgabe Yoka für Cat. No. (Modul 11, P5a). Stand 4.5.1: 5.247 KACHINA (5.221 auf `AUDIO_XOS`, 26 auf `Macintosh HD`), 14.310 YOKA | entschieden (Yoka, 2026-10-27) |
| M21 | Comment = durchsuchbare Stichworte ohne eigenes Feld, z. B. `E7 · Vocal · Tribal` (Energie 1–10 + Merkmale). Genre bleibt im Genre-Feld. Vorhandene Comments (Werbung, alte Bassart-Versuche `IXXxI` u. a.) werden überschrieben, alter Wert in `wert_historie` | Feldinventar P2: Comment heute fast nur Werbung/alte Versuche; Traktor durchsucht Comment (F5) | entschieden (Yoka, 2026-10-27) |
| M22 | Farben: Rot, Orange, Blau im Bestand gültig, bleiben. Gelb, Grün, Magenta-Indizes 6/7 sind alte Versuche → über Modul 9 neu vorschlagen. 424 in 4.5.1 verlorene Rot/Blau-Tracks aus 4.5.0 später als Wiederherstellung vorschlagen | Vorgabe Yoka; Feldinventar P2 | entschieden (Yoka, 2026-10-27) |
| M23 | Farbschema nach Phasen einer Techno-Party: Grün = Chill/Ambient/Psybient, Blau = Morgen, Gelb = Mittag/Sonne, Orange = Nachmittag/Sonnenuntergang, Rot = Nacht/Energie inkl. Tiefe Nacht/Afterhour. Peak Time und eigene Tiefe-Nacht-Farbe entfallen vorerst; Magenta und Cyan sind Reserve | Peak Time ist eher ein Genre; Tiefe Nacht = Nacht. Traktor hat kein Violett (Yoka) | entschieden (Yoka, 2026-10-27) |
| M24 | Bassmuster in Comment 2 nur **16 Zeichen (1 Takt)** statt 64; Format `OLDSCHOOL · I0X0I0X0I0X0I0X0` | 64 Zeichen sind zu lang, 1 Takt reicht zur Unterscheidung (Yoka, nach Schreibtest P2) | entschieden (Yoka, 2026-10-27) |
| M25 | Traktor-Feldzuordnung verifiziert: Comment 2 = `INFO@RATING`, Cat. No. = `INFO@CATALOG_NO`, Comment = `INFO@COMMENT`, Color = `INFO@COLOR` mit 1 Rot, 2 Orange, 3 Gelb, 4 Grün, 5 Blau, 6 Cyan, 7 Magenta | Schreibtest P2/3 mit Traktor 4.5.1: Anzeige, Suche und Rückschreiben geprüft (Yoka) | belegt (2026-10-27) |
| M26 | Schreibregeln Tags ↔ NML: Datei-Tags und NML immer im selben Plan konsistent schreiben; beim Comment alle COMM-Frames setzen; PRIV `TRAKTOR4` nicht anfassen; Datei-Datum nicht zurücksetzen (M16) | ID3-Test P2/4: Traktor liest neuere Dateien beim Laden neu und überschreibt NML; COMM gewinnt gegen veralteten PRIV | Vorschlag, Freigabe Yoka |
