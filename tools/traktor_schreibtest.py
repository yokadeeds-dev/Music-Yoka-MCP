"""Schreibtest Traktor-Collection (P2, Schritt 3).

Ersetzt die echte collection.nml vorübergehend durch eine Test-Collection mit
7 synthetischen Tracks (COLOR 1–7, Comment 2, Cat. No., Comment) und stellt das
Original danach byte-genau wieder her. Nur nach Freigabe durch Yoka benutzen.

    python3 tools/traktor_schreibtest.py vorbereiten   # Testtöne + Test-NML in testdaten/
    python3 tools/traktor_schreibtest.py einsetzen     # Prozessprüfung, Backup, Test-NML einsetzen
    python3 tools/traktor_schreibtest.py auswerten     # was hat Traktor zurückgeschrieben?
    python3 tools/traktor_schreibtest.py zurueck       # Original zurück, Prüfsumme vergleichen
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import struct
import subprocess
import sys
import time
import wave
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import quoteattr

REPO = Path(__file__).resolve().parent.parent
TESTORDNER = REPO / "testdaten" / "traktor_test"
ZUSTAND = TESTORDNER / "zustand.json"
TEST_NML = TESTORDNER / "collection_test.nml"
COLLECTION = Path.home() / "Documents/Native Instruments/Traktor 4.5.1/collection.nml"

TRACKS = [
    # (Index, Comment 2, Cat. No., Comment)
    (1, "OLDSCHOOL · I0X0I0X0I0X0I0X0I0X0I0X0I0X0I0X0I0X0I0X0I0X0I0X0I0X0I0X0I0X0I0X0", "YOKA", "E7 · Test 1"),
    (2, "IXXXIXXXIXXXIXXXIXXXIXXXIXXXIXXXIXXXIXXXIXXXIXXXIXXXIXXXIXXXIXXX", "KACHINA", "E5 · Test 2"),
    (3, "Comment2 Test 3", "YOKA", "E3 · Test 3"),
    (4, "Comment2 Test 4", "KACHINA", "E4 · Test 4"),
    (5, "Comment2 Test 5", "YOKA", "E6 · Test 5"),
    (6, "Comment2 Test 6", "KACHINA", "E8 · Test 6"),
    (7, "Comment2 Test 7", "YOKA", "E9 · Test 7"),
]


def sha256(pfad: Path) -> str:
    h = hashlib.sha256()
    with open(pfad, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def traktor_laeuft() -> bool:
    return subprocess.run(["pgrep", "-x", "Traktor Pro 4"], capture_output=True).returncode == 0


def testton(pfad: Path, nummer: int, sekunden: int = 30, bpm: float = 128.0) -> None:
    """Sinus plus Kick-Impulse, damit Traktor etwas zu analysieren hat."""
    rate = 44100
    beat = 60.0 / bpm
    frequenz = 110.0 * (1 + nummer / 7)
    rahmen = bytearray()
    for n in range(rate * sekunden):
        t = n / rate
        phase = t % beat
        kick = math.sin(2 * math.pi * 55 * phase) * math.exp(-phase * 30) if phase < 0.15 else 0.0
        wert = 0.25 * math.sin(2 * math.pi * frequenz * t) + 0.6 * kick
        rahmen += struct.pack("<h", int(max(-1.0, min(1.0, wert)) * 32000))
    with wave.open(str(pfad), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(bytes(rahmen))


def nml_dir(ordner: Path) -> str:
    return "".join(f"/:{teil}" for teil in ordner.parts[1:]) + "/:"


def vorbereiten() -> None:
    TESTORDNER.mkdir(parents=True, exist_ok=True)
    eintraege = []
    for index, comment2, catno, comment in TRACKS:
        datei = f"MusicYoka_Test_{index}.wav"
        testton(TESTORDNER / datei, index)
        eintraege.append(
            f'<ENTRY MODIFIED_DATE="2026/10/27" MODIFIED_TIME="36000" '
            f'TITLE="Farbe {index}" ARTIST="MusicYoka Test">'
            f'<LOCATION DIR={quoteattr(nml_dir(TESTORDNER))} FILE="{datei}" '
            f'VOLUME="Macintosh HD" VOLUMEID="Macintosh HD"></LOCATION>\n'
            f'<MODIFICATION_INFO AUTHOR_TYPE="user"></MODIFICATION_INFO>\n'
            f'<INFO COLOR="{index}" RATING={quoteattr(comment2)} CATALOG_NO="{catno}" '
            f'COMMENT={quoteattr(comment)} IMPORT_DATE="2026/10/27"></INFO>\n'
            f"</ENTRY>\n"
        )
    nml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n'
        '<NML VERSION="20"><HEAD COMPANY="www.native-instruments.com" PROGRAM="Traktor Pro 4"></HEAD>\n'
        f'<COLLECTION ENTRIES="{len(eintraege)}">' + "".join(eintraege) + "</COLLECTION>\n"
        '<SETS ENTRIES="0"></SETS>\n'
        '<PLAYLISTS><NODE TYPE="FOLDER" NAME="$ROOT"><SUBNODES COUNT="0"></SUBNODES></NODE></PLAYLISTS>\n'
        "<INDEXING></INDEXING>\n</NML>\n"
    )
    TEST_NML.write_text(nml, encoding="utf-8")
    ET.parse(TEST_NML)  # Parse-Test
    print(f"{len(TRACKS)} Testtöne und {TEST_NML.name} in {TESTORDNER}")


def einsetzen() -> None:
    if traktor_laeuft():
        sys.exit("Abbruch: Traktor läuft.")
    if ZUSTAND.exists():
        sys.exit(f"Abbruch: {ZUSTAND} existiert – Test läuft schon, erst 'zurueck'.")
    stempel = time.strftime("%Y%m%d-%H%M%S")
    backup = COLLECTION.with_name(f"collection_{stempel}.nml")
    shutil.copy2(COLLECTION, backup)
    pruefsumme = sha256(COLLECTION)
    if sha256(backup) != pruefsumme:
        sys.exit("Abbruch: Backup weicht ab.")
    shutil.copy2(backup, TESTORDNER / backup.name)  # zweite Sicherung im Repo (ignoriert)
    ZUSTAND.write_text(json.dumps({"backup": str(backup), "sha256": pruefsumme}, indent=2))
    tmp = COLLECTION.with_name("collection.nml.musicyoka-tmp")
    shutil.copyfile(TEST_NML, tmp)
    if traktor_laeuft():
        tmp.unlink()
        sys.exit("Abbruch: Traktor wurde gestartet.")
    os.replace(tmp, COLLECTION)
    print(f"Backup: {backup}\nSHA-256: {pruefsumme}\nTest-Collection eingesetzt.")


def auswerten() -> None:
    if traktor_laeuft():
        sys.exit("Traktor läuft noch – erst schließen, dann schreibt Traktor die NML.")
    for entry in ET.parse(COLLECTION).getroot().iter("ENTRY"):
        if entry.find("LOCATION") is None:
            continue
        info = entry.find("INFO")
        print(entry.get("TITLE"), "|", entry.get("ARTIST"))
        print("   INFO:", dict(info.attrib) if info is not None else None)
        print("   Elemente:", [k.tag for k in entry])


def zurueck() -> None:
    if traktor_laeuft():
        sys.exit("Abbruch: Traktor läuft.")
    zustand = json.loads(ZUSTAND.read_text())
    backup = Path(zustand["backup"])
    if sha256(backup) != zustand["sha256"]:
        sys.exit("Abbruch: Backup hat sich verändert!")
    shutil.copyfile(COLLECTION, TESTORDNER / "collection_test_nach_traktor.nml")
    tmp = COLLECTION.with_name("collection.nml.musicyoka-tmp")
    shutil.copy2(backup, tmp)
    os.replace(tmp, COLLECTION)
    ok = sha256(COLLECTION) == zustand["sha256"]
    print("Original wiederhergestellt, Prüfsumme", "IDENTISCH" if ok else "ABWEICHEND!")
    if ok:
        ZUSTAND.rename(ZUSTAND.with_suffix(".erledigt.json"))


if __name__ == "__main__":
    befehle = {"vorbereiten": vorbereiten, "einsetzen": einsetzen,
               "auswerten": auswerten, "zurueck": zurueck}
    if len(sys.argv) != 2 or sys.argv[1] not in befehle:
        sys.exit(__doc__)
    befehle[sys.argv[1]]()
