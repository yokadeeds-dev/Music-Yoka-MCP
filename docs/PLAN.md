# Arbeitsplan

**Status: P2 fachlich fertig (Schritte 1–4 inkl. Runde 3). Offen: Freigabe M27 und Abnahme P2 durch Yoka. Danach P3.**

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
- 2026-10-27 M23: Farbschema nach Party-Phasen, 5 Farben, Magenta/Cyan Reserve.
- 2026-10-27 P2/3: Schreibtest mit Traktor 4.5.1 bestanden (M25), Original byte-genau zurück; Bassmuster 16 Zeichen (M24).
- 2026-10-27 P2/4: ID3-Test (2 Runden), Original byte-genau zurück; Traktor liest neuere Dateien beim Laden neu, COMM schlägt PRIV; M16 bestätigt, M26 vorgeschlagen.
- 2026-10-27 P2/4 Runde 3: reine NML-Felder nur im PRIV; alter PRIV überschreibt Color/Comment 2 beim Neu-Einlesen; Abgleich MODIFIED_* verhindert das (Runde 3c, wiederholt mit Laden ins Deck; M27 vorgeschlagen). M26 freigegeben.
- 2026-10-27 M20: Pool-Grundregel `+ Kachina +` → KACHINA, sonst YOKA.

## Offene Punkte

- Verlorene Farben aus 4.5.0 (424 Tracks, Rot/Blau): Wiederherstellung als Plan (M22, frühestens P5a).
- Smartlists sollen nur nach Farbe filtern (Yoka); MORNING/NACHT/COSMIC ALTERNATIVE filtern heute nach Comment → später genauer ansehen.
- Auftrag im Spotify-Repo: `isrc`, `duration_ms`, `playlist_tracks` (vor P5l).
