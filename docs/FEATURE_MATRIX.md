# Feature-Matrix

Status: **Entwurf zur Freigabe**. Prioritäten: **Muss** (Kern, Traktor-Sichtbarkeit),
**Soll** (hoher Nutzen, nach Kern), **Später**.
Spalte „Paket" verweist auf `docs/PLAN.md`.

## Kern

| Feature | Prio | Paket | Hinweis |
|---|---|---|---|
| Datenträger-Register (ID-Schema, Kennungsdatei, Seriennummer, Rolle, Lagerort) | Muss | P4 | Offline durchsuchbar |
| Scanner inkrementell, fortsetzbar, parallel | Muss | P4 | nur lesend |
| Tag-Reader (mutagen) | Muss | P4 | |
| Hashes `file_hash` + `audio_hash` | Muss | P4 | `audio_hash` stabil gegen Tag-Änderungen |
| Zentrale SQLite-DB + Migrationen | Muss | P3 | |
| Scan-Export/Import zwischen Rechnern | Muss | P4 | kein SQLite über Netzwerk |
| Plan → Freigabe → Ausführung → Undo, `wert_historie` | Muss | P3/P4 | Freigabe nur durch Yoka |
| MCP-Server (lesen, Pläne erstellen) | Muss | P4 | |
| CLI (Freigabe, Undo, Status) | Muss | P4 | |
| Zentraler LAN-Dienst | Später | – | erst wenn Export/Import nicht reicht |

## Traktor

| Feature | Prio | Paket | Hinweis |
|---|---|---|---|
| NML lesen (LOCATION, INFO, BPM, Key, Grid, Color) | Muss | P5a | Traktor-Analyse übernehmen |
| NML schreiben: Comment 2, Color, Cat. No. | Muss | P2 (Test), P5a | nur bei geschlossenem Traktor, Backup |
| 7 Farbnamen/Indizes verifizieren | Muss | P2 | |
| ID3-Comment schreiben + Konsistenzprüfung (PRIV-Frame) | Soll | P2 (Test), P5c | |
| Playlist-Verweise bei Umbenennung mitführen | Muss (für Modul 6) | P5j | |

## Module

| # | Modul | Prio | Paket | Kernpunkt |
|---|---|---|---|---|
| 11 | DJ-Pool → Cat. No. | Muss | P5a | Regeln mit Yoka erfassen |
| 10 | Release-Jahr + OLDSCHOOL → Comment 2 | Muss | P5b | Grenzjahr 2015, konfigurierbar |
| 4 | Duplikate Stufe 1 (Hash) | Muss | P5c | nur Prüfliste/Quarantäne-Plan |
| 1 | Identifikation (AcoustID + MusicBrainz) | Muss | P5d | Basis für Jahr, ISRC, Duplikate Stufe 2 |
| 9 | Farbvorschlag → Color | Muss | P5e | Bestätigung je Track; Trainingsdaten aus NML |
| 2 | Genre (Last.fm pro Artist) | Soll | P5f | Whitelist/Mapping |
| 3 | Audio-Analyse (BPM, Key, Energie, LUFS) | Soll | P5g | Traktor-Werte zuerst |
| 4 | Duplikate Stufe 2/3 + beste Version + Fake-Lossless | Soll | P5h | |
| 8 | Bassart → Comment 2 | Muss (Ziel), technisch Soll | P5i | Proof of Concept auf Stichprobe zuerst |
| 6 | Dateinamenpflege | Soll | P5j | nur selber Ordner, NML im selben Plan |
| 5 | Playlists M3U/M3U8, Rekordbox XML, Traktor | Soll | P5k | |
| – | Spotify-Abgleich (ISRC, Fehlliste) | Soll | P5l | braucht Erweiterung Spotify-Repo |
| 7 | CD/DVD | Später | P5m | |

## Bewusst nicht im Umfang

- Anzeige auf dem S8-Display.
- Ordner anlegen, umbenennen, verschieben, löschen (außer Quarantäne-Ziel).
- Automatisches Löschen jeglicher Art.
- Automatisches Taggen ohne Vorschau (kein beets-Autotagger auf der Sammlung).
