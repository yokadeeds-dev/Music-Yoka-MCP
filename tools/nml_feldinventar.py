"""Feldinventar einer Traktor-collection.nml (nur lesend).

Zählt je Element/Attribut innerhalb von COLLECTION/ENTRY, wie viele Einträge
einen nicht-leeren Wert haben, und die Anzahl unterschiedlicher Werte.

Nur gegen Kopien laufen lassen (CLAUDE.md). Ausgabe ist Markdown mit
aggregierten Zahlen; Beispielwerte (--beispiele) nur fürs Terminal,
da sie persönliche Inhalte enthalten.

Aufruf:
    python3 tools/nml_feldinventar.py testdaten/collection_kopie.nml [--beispiele 10]
"""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path


def inventar(pfad: Path):
    belegt: Counter[str] = Counter()          # "INFO@COMMENT" -> Einträge mit Wert
    werte: dict[str, Counter[str]] = defaultdict(Counter)
    elemente: Counter[str] = Counter()        # Einträge, die das Element haben
    eintraege = 0
    oberste: Counter[str] = Counter()

    tiefe = 0
    for ereignis, elem in ET.iterparse(pfad, events=("start", "end")):
        if ereignis == "start":
            tiefe += 1
            if tiefe == 2:
                oberste[elem.tag] += 1
            continue
        tiefe -= 1
        if elem.tag != "ENTRY" or tiefe != 2:
            if tiefe == 1:
                elem.clear()
            continue

        eintraege += 1
        gesehen: set[str] = set()       # Elemente und Felder je Eintrag nur einmal zählen
        for knoten, praefix in [(elem, "ENTRY")] + [(k, k.tag) for k in elem]:
            if praefix != "ENTRY" and praefix not in gesehen:
                elemente[praefix] += 1
                gesehen.add(praefix)
            for schluessel, wert in knoten.attrib.items():
                feld = f"{praefix}@{schluessel}"
                if wert.strip():
                    werte[feld][wert] += 1
                    if feld not in gesehen:
                        belegt[feld] += 1
                        gesehen.add(feld)
        elem.clear()

    return eintraege, oberste, elemente, belegt, werte


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("nml", type=Path)
    ap.add_argument("--beispiele", type=int, default=0,
                    help="häufigste Werte je Feld zeigen (nur Terminal, nicht committen)")
    ap.add_argument("--felder", nargs="*", default=None,
                    help="Beispiele nur für diese Felder, z. B. INFO@COLOR")
    args = ap.parse_args()

    eintraege, oberste, elemente, belegt, werte = inventar(args.nml)

    print(f"# Feldinventar `{args.nml.name}`\n")
    print(f"Einträge (COLLECTION/ENTRY): **{eintraege}**\n")
    print("Oberste Elemente: " + ", ".join(f"{k} ({v})" for k, v in oberste.items()) + "\n")
    print("| Element | Einträge mit Element | Anteil |")
    print("|---|---:|---:|")
    for tag, n in elemente.most_common():
        print(f"| {tag} | {n} | {n / eintraege:.1%} |")
    print()
    print("| Feld | belegt | Anteil | versch. Werte |")
    print("|---|---:|---:|---:|")
    for feld in sorted(belegt, key=lambda f: (f.split("@")[0], -belegt[f])):
        n = belegt[feld]
        print(f"| {feld} | {n} | {n / eintraege:.1%} | {len(werte[feld])} |")

    if args.beispiele:
        print("\n## Beispielwerte (nicht committen)\n", file=sys.stderr)
        for feld in sorted(werte):
            if args.felder and feld not in args.felder:
                continue
            haeufig = werte[feld].most_common(args.beispiele)
            text = "; ".join(f"{w[:60]!r}×{c}" for w, c in haeufig)
            print(f"{feld}: {text}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
