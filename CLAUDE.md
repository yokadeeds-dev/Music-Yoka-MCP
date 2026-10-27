# Music-Yoka-MCP – Einstieg für jede Session

Antworten auf Deutsch, knapp, Aktion zuerst.
Stand und nächstes Paket: `docs/PLAN.md` (Statuszeile). Architektur: `docs/ARCHITEKTUR.md`.

## HARTE REGELN (nie verhandelbar)

- **Ordnerstruktur unverändert:** keine Ordner anlegen/umbenennen/verschieben/löschen,
  keine Dateien in andere Ordner verschieben. Einzige Ausnahme: Duplikat-Quarantäne
  außerhalb der Musikstruktur. Leere Ordner bleiben.
- **Nie automatisch löschen:** Vorschau → Freigabe Yoka → Ausführung → Undo.
- **`collection.nml`** nur bei geschlossenem Traktor, immer mit Backup.
- **Vor jedem Überschreiben** alten Wert in der DB sichern (`wert_historie`).
- **Sequenziell arbeiten**, Freigabe nach jedem Paket.
- Claude darf Pläne erstellen, **nie freigeben**.

## Tests

Nie gegen echte Musikdatenträger oder die echte `collection.nml` testen –
nur synthetische Testdateien und NML-Kopien.

## Arbeitsweise

- Ein Paket pro Session; jeder Commit pflegt `docs/PLAN.md` mit.
- Neue Entscheidungen in `docs/ENTSCHEIDUNGEN.md` (M-Nummern).
- Kein Arbeitsstand außerhalb des Repos.
