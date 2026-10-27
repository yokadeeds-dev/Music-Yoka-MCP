"""ID3-Test Traktor (P2, Schritt 4): ID3-Comment, Datei-Datum, PRIV-Frame.

Frage: Wann liest Traktor den ID3-Comment aus der Datei, und gewinnt dann die Datei,
die NML oder Traktors eigener PRIV-Frame? Vier synthetische MP3s:

    A  nur ID3-Comment, NML ohne Comment
    B  NML neuer als Datei, Comment unterschiedlich
    C  Datei neuer als NML, Comment unterschiedlich
    D  wie B; Yoka ändert den Comment in Traktor (→ PRIV), danach ändert
       mutagen den ID3-Comment (Runde 2)

Runde 3 (eigene Test-Collection, Befehle mit Endung 3):

    E  Comment 2, Cat. No., Color nur in NML, Datei neuer → bleiben sie beim Einlesen?
    F  Yoka ändert Comment 2, Cat. No., Color in Traktor → wohin schreibt Traktor sie?

Benötigt .venv (mutagen, lameenc). Ablauf:

    .venv/bin/python tools/traktor_id3test.py vorbereiten
    .venv/bin/python tools/traktor_id3test.py einsetzen
    … Traktor Runde 1 …
    .venv/bin/python tools/traktor_id3test.py auswerten
    .venv/bin/python tools/traktor_id3test.py runde2     # ID3-Comment von D per mutagen ändern
    … Traktor Runde 2 …
    .venv/bin/python tools/traktor_id3test.py auswerten
    .venv/bin/python tools/traktor_id3test.py zurueck
    (Runde 3: vorbereiten3, einsetzen3, auswerten3, runde3b, auswerten3, runde3c, auswerten3, zurueck3)
"""

from __future__ import annotations

import os
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import quoteattr

import lameenc
from mutagen.id3 import COMM, ID3, TIT2, TPE1

sys.path.insert(0, str(Path(__file__).resolve().parent))
import traktor_schreibtest as basis  # noqa: E402

ORDNER = basis.REPO / "testdaten" / "traktor_id3test"
ORDNER3 = basis.REPO / "testdaten" / "traktor_id3test_r3"
ALT = datetime(2026, 1, 1, 12, 0).timestamp()  # Datei-Datum „alt“

# (Kennung, ID3-Comment, NML-Comment oder None, NML-Datum, Datei-Datum alt?, weitere INFO-Attribute)
TRACKS = [
    ("A", "ID3 A", None, "2026/1/1", False, {}),
    ("B", "ID3 B", "NML B", "2026/10/27", True, {}),
    ("C", "ID3 C", "NML C", "2026/1/1", False, {}),
    ("D", "ID3 D", "NML D", "2026/10/27", True, {}),
]
TRACKS3 = [
    ("E", "ID3 E", "NML E", "2026/1/1", False,
     {"COLOR": "4", "RATING": "Comment2 E", "CATALOG_NO": "KACHINA"}),
    ("F", "ID3 F", "NML F", "2026/10/27", True, {}),
]


def datei(kennung: str, ordner: Path = ORDNER) -> Path:
    return ordner / f"MusicYoka_ID3_{kennung}.mp3"


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


def vorbereiten(ordner: Path = ORDNER, tracks: list = TRACKS) -> None:
    ordner.mkdir(parents=True, exist_ok=True)
    eintraege = []
    for nummer, (kennung, id3_comment, nml_comment, nml_datum, datei_alt, weitere) in enumerate(tracks, 1):
        pfad = datei(kennung, ordner)
        mp3_schreiben(pfad, nummer)
        tags = ID3()
        tags.add(TIT2(encoding=3, text=f"ID3-Test {kennung}"))
        tags.add(TPE1(encoding=3, text="MusicYoka Test"))
        tags.add(COMM(encoding=3, lang="eng", desc="", text=id3_comment))
        tags.save(pfad, v2_version=3)
        if datei_alt:
            os.utime(pfad, (ALT, ALT))
        attribute = ({"COMMENT": nml_comment} if nml_comment else {}) | weitere
        info_attr = "".join(f" {k}={quoteattr(v)}" for k, v in attribute.items())
        eintraege.append(
            f'<ENTRY MODIFIED_DATE="{nml_datum}" MODIFIED_TIME="36000" '
            f'TITLE="ID3-Test {kennung}" ARTIST="MusicYoka Test">'
            f'<LOCATION DIR={quoteattr(basis.nml_dir(ordner))} FILE="{pfad.name}" '
            f'VOLUME="Macintosh HD" VOLUMEID="Macintosh HD"></LOCATION>\n'
            f'<MODIFICATION_INFO AUTHOR_TYPE="user"></MODIFICATION_INFO>\n'
            f'<INFO{info_attr} IMPORT_DATE="2026/10/27"></INFO>\n'
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
    test_nml = ordner / "collection_test.nml"
    test_nml.write_text(nml, encoding="utf-8")
    ET.parse(test_nml)
    zeigen(ordner, tracks)


def zeigen(ordner: Path = ORDNER, tracks: list = TRACKS) -> None:
    for kennung, *_ in tracks:
        print(kennung, tags_lesen(datei(kennung, ordner)))


def auswerten(ordner: Path = ORDNER, tracks: list = TRACKS) -> None:
    basis.auswerten()
    print()
    zeigen(ordner, tracks)


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


def runde3b() -> None:
    """E: NML-Werte neu, ID3-Comment neu (Datei neuer), PRIV mit alten Traktor-Werten."""
    if basis.traktor_laeuft():
        sys.exit("Abbruch: Traktor läuft.")
    wurzel = ET.parse(basis.COLLECTION)
    eintraege = [e for e in wurzel.getroot().iter("ENTRY") if e.find("LOCATION") is not None]
    if [e.get("TITLE") for e in eintraege] != ["ID3-Test E", "ID3-Test F"]:
        sys.exit("Abbruch: eingesetzte Collection ist nicht die Test-Collection von Runde 3.")
    info = eintraege[0].find("INFO")
    info.set("RATING", "NML C2E")
    info.set("CATALOG_NO", "NML CatE")
    info.set("COLOR", "6")
    wurzel.write(basis.COLLECTION, encoding="UTF-8", xml_declaration=True)
    pfad = datei("E", ORDNER3)
    tags = ID3(pfad)
    for frame in tags.getall("COMM"):
        frame.encoding = 3
        frame.text = ["Mutagen E"]
    tags.save(pfad, v2_version=3)
    print("NML E:", dict(info.attrib))
    print("E:", tags_lesen(pfad))


def runde3c() -> None:
    """E: Datei-Comment neu schreiben, NML konsistent inkl. MODIFIED_* = Datei-Datum (UTC)."""
    if basis.traktor_laeuft():
        sys.exit("Abbruch: Traktor läuft.")
    wurzel = ET.parse(basis.COLLECTION)
    eintraege = [e for e in wurzel.getroot().iter("ENTRY") if e.find("LOCATION") is not None]
    if [e.get("TITLE") for e in eintraege] != ["ID3-Test E", "ID3-Test F"]:
        sys.exit("Abbruch: eingesetzte Collection ist nicht die Test-Collection von Runde 3.")
    pfad = datei("E", ORDNER3)
    tags = ID3(pfad)
    for frame in tags.getall("COMM"):
        frame.encoding = 3
        frame.text = ["Mutagen E2"]
    tags.save(pfad, v2_version=3)
    utc = datetime.fromtimestamp(pfad.stat().st_mtime, tz=timezone.utc)
    eintrag = eintraege[0]
    eintrag.set("MODIFIED_DATE", f"{utc.year}/{utc.month}/{utc.day}")
    eintrag.set("MODIFIED_TIME", str(utc.hour * 3600 + utc.minute * 60 + utc.second))
    info = eintrag.find("INFO")
    info.set("COMMENT", "Mutagen E2")
    info.set("RATING", "NML C2E2")
    info.set("CATALOG_NO", "NML CatE2")
    info.set("COLOR", "6")
    wurzel.write(basis.COLLECTION, encoding="UTF-8", xml_declaration=True)
    print("NML E:", eintrag.get("MODIFIED_DATE"), eintrag.get("MODIFIED_TIME"), dict(info.attrib))
    print("E:", tags_lesen(pfad))


if __name__ == "__main__":
    befehle = {
        "vorbereiten": vorbereiten,
        "einsetzen": lambda: basis.einsetzen(ORDNER / "collection_test.nml"),
        "auswerten": auswerten,
        "runde2": runde2,
        "zurueck": lambda: basis.zurueck(ORDNER),
        "vorbereiten3": lambda: vorbereiten(ORDNER3, TRACKS3),
        "einsetzen3": lambda: basis.einsetzen(ORDNER3 / "collection_test.nml"),
        "auswerten3": lambda: auswerten(ORDNER3, TRACKS3),
        "runde3b": runde3b,
        "runde3c": runde3c,
        "zurueck3": lambda: basis.zurueck(ORDNER3),
    }
    if len(sys.argv) != 2 or sys.argv[1] not in befehle:
        sys.exit(__doc__)
    befehle[sys.argv[1]]()
