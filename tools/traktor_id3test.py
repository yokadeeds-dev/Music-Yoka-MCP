"""ID3-Test Traktor (P2, Schritt 4): ID3-Comment, Datei-Datum, PRIV-Frame.

Frage: Wann liest Traktor den ID3-Comment aus der Datei, und gewinnt dann die Datei,
die NML oder Traktors eigener PRIV-Frame? Vier synthetische MP3s:

    A  nur ID3-Comment, NML ohne Comment
    B  NML neuer als Datei, Comment unterschiedlich
    C  Datei neuer als NML, Comment unterschiedlich
    D  wie B; Yoka ändert den Comment in Traktor (→ PRIV), danach ändert
       mutagen den ID3-Comment (Runde 2)

Benötigt .venv (mutagen, lameenc). Ablauf:

    .venv/bin/python tools/traktor_id3test.py vorbereiten
    .venv/bin/python tools/traktor_id3test.py einsetzen
    … Traktor Runde 1 …
    .venv/bin/python tools/traktor_id3test.py auswerten
    .venv/bin/python tools/traktor_id3test.py runde2     # ID3-Comment von D per mutagen ändern
    … Traktor Runde 2 …
    .venv/bin/python tools/traktor_id3test.py auswerten
    .venv/bin/python tools/traktor_id3test.py zurueck
"""

from __future__ import annotations

import os
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import quoteattr

import lameenc
from mutagen.id3 import COMM, ID3, TIT2, TPE1

sys.path.insert(0, str(Path(__file__).resolve().parent))
import traktor_schreibtest as basis  # noqa: E402

ORDNER = basis.REPO / "testdaten" / "traktor_id3test"
TEST_NML = ORDNER / "collection_test.nml"
ALT = datetime(2026, 1, 1, 12, 0).timestamp()  # Datei-Datum „alt“

# (Kennung, ID3-Comment, NML-Comment oder None, NML-Datum, Datei-Datum alt?)
TRACKS = [
    ("A", "ID3 A", None, "2026/1/1", False),
    ("B", "ID3 B", "NML B", "2026/10/27", True),
    ("C", "ID3 C", "NML C", "2026/1/1", False),
    ("D", "ID3 D", "NML D", "2026/10/27", True),
]


def datei(kennung: str) -> Path:
    return ORDNER / f"MusicYoka_ID3_{kennung}.mp3"


def mp3_schreiben(pfad: Path, nummer: int) -> None:
    enc = lameenc.Encoder()
    enc.set_bit_rate(192)
    enc.set_in_sample_rate(44100)
    enc.set_channels(1)
    enc.set_quality(2)
    pfad.write_bytes(enc.encode(basis.testton_pcm(nummer, sekunden=20)) + enc.flush())


def tags_lesen(pfad: Path) -> dict:
    tags = ID3(pfad)
    return {
        "COMM": [f"{f.desc!r}={f.text[0]!r}" for f in tags.getall("COMM")],
        "PRIV": [f"{f.owner} ({len(f.data)} B)" for f in tags.getall("PRIV")],
        "Frames": sorted({k.split(":")[0] for k in tags.keys()}),
        "mtime": datetime.fromtimestamp(pfad.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
    }


def vorbereiten() -> None:
    ORDNER.mkdir(parents=True, exist_ok=True)
    eintraege = []
    for nummer, (kennung, id3_comment, nml_comment, nml_datum, datei_alt) in enumerate(TRACKS, 1):
        pfad = datei(kennung)
        mp3_schreiben(pfad, nummer)
        tags = ID3()
        tags.add(TIT2(encoding=3, text=f"ID3-Test {kennung}"))
        tags.add(TPE1(encoding=3, text="MusicYoka Test"))
        tags.add(COMM(encoding=3, lang="eng", desc="", text=id3_comment))
        tags.save(pfad, v2_version=3)
        if datei_alt:
            os.utime(pfad, (ALT, ALT))
        comment_attr = f" COMMENT={quoteattr(nml_comment)}" if nml_comment else ""
        eintraege.append(
            f'<ENTRY MODIFIED_DATE="{nml_datum}" MODIFIED_TIME="36000" '
            f'TITLE="ID3-Test {kennung}" ARTIST="MusicYoka Test">'
            f'<LOCATION DIR={quoteattr(basis.nml_dir(ORDNER))} FILE="{pfad.name}" '
            f'VOLUME="Macintosh HD" VOLUMEID="Macintosh HD"></LOCATION>\n'
            f'<MODIFICATION_INFO AUTHOR_TYPE="user"></MODIFICATION_INFO>\n'
            f'<INFO{comment_attr} IMPORT_DATE="2026/10/27"></INFO>\n'
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
    ET.parse(TEST_NML)
    zeigen()


def zeigen() -> None:
    for kennung, *_ in TRACKS:
        print(kennung, tags_lesen(datei(kennung)))


def auswerten() -> None:
    basis.auswerten()
    print()
    zeigen()


def runde2() -> None:
    if basis.traktor_laeuft():
        sys.exit("Abbruch: Traktor läuft.")
    pfad = datei("D")
    tags = ID3(pfad)
    for frame in tags.getall("COMM"):  # alle COMM-Frames, damit nur PRIV den alten Wert hat
        frame.encoding = 3
        frame.text = ["Mutagen D"]
    tags.save(pfad, v2_version=3)  # PRIV-Frames bleiben unangetastet
    time.sleep(1)
    print("D:", tags_lesen(pfad))


if __name__ == "__main__":
    befehle = {
        "vorbereiten": vorbereiten,
        "einsetzen": lambda: basis.einsetzen(TEST_NML),
        "auswerten": auswerten,
        "runde2": runde2,
        "zurueck": lambda: basis.zurueck(ORDNER),
    }
    if len(sys.argv) != 2 or sys.argv[1] not in befehle:
        sys.exit(__doc__)
    befehle[sys.argv[1]]()
