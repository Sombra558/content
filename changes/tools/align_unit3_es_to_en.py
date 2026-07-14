"""Rebuild ES Unit 3 to match EN Unit 3 order/topic (EN = source of truth)."""
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"d:\GetLicensed\content")
ES_PATH = ROOT / "dist" / "sc-content" / "sc-content.es.json"
EN_PATH = ROOT / "dist" / "sc-content" / "sc-content.en.json"

# EN index -> current ES index (pre-alignment). Bijective except EN[93] uses
# orphan ES[136] slot whose content is replaced with a new translation.
EN_TO_ES = {
    0: 0,
    1: 6,
    2: 12,
    3: 3,
    4: 31,
    5: 13,
    6: 1,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    11: 11,
    12: 2,
    13: 5,
    14: 14,
    15: 15,
    16: 16,
    17: 17,
    18: 18,
    19: 19,
    20: 20,
    21: 21,
    22: 22,
    23: 23,
    24: 24,
    25: 25,
    26: 26,
    27: 27,
    28: 28,
    29: 29,
    30: 30,
    31: 43,
    32: 32,
    33: 33,
    34: 34,
    35: 35,
    36: 36,
    37: 37,
    38: 38,
    39: 39,
    40: 40,
    41: 41,
    42: 42,
    43: 45,
    44: 44,
    45: 55,
    46: 46,
    47: 47,
    48: 48,
    49: 92,  # completion items: DOB / 21+ / valid ID / time
    50: 50,
    51: 51,
    52: 52,
    53: 53,
    54: 54,
    55: 60,
    56: 56,
    57: 57,
    58: 58,
    59: 59,
    60: 63,
    61: 61,
    62: 62,
    63: 72,
    64: 64,
    65: 65,
    66: 66,
    67: 67,
    68: 68,
    69: 69,
    70: 70,
    71: 71,
    72: 74,
    73: 49,  # find DOB / compare / 21+ / time
    74: 84,
    75: 75,
    76: 76,
    77: 77,
    78: 78,
    79: 79,
    80: 80,
    81: 81,
    82: 82,
    83: 83,
    84: 90,
    85: 85,
    86: 86,
    87: 87,
    88: 88,
    89: 89,
    90: 93,
    91: 4,  # locate DOB reminder
    92: 73,  # find DOB / check year / today / 21+
    93: 136,  # REPLACE content — EN-only subtract-21 teaching slide
    94: 94,
    95: 91,
    96: 95,
    97: 97,
    98: 96,
    99: 98,
    100: 100,
    101: 101,
    102: 99,
    103: 102,
    104: 104,
    105: 103,
    106: 105,
    107: 106,
    108: 107,
    109: 109,
    110: 108,
    111: 110,
    112: 111,
    113: 113,
    114: 112,
    115: 114,
    116: 116,
    117: 115,
    118: 117,
    119: 118,
    120: 119,
    121: 121,
    122: 120,
    123: 122,
    124: 123,
    125: 125,
    126: 126,
    127: 124,
    128: 128,
    129: 127,
    130: 129,
    131: 130,
    132: 131,
    133: 133,
    134: 132,
    135: 134,
    136: 135,
    137: 137,
    138: 138,
    139: 139,
    140: 140,
    141: 141,
    142: 142,
    143: 143,
}

# Content overrides after remap (EN topic was missing or wrong shape in ES).
OVERRIDES = {
    42: {
        "paragraphs": [
            "Regla práctica: verifica la ID de forma consistente para cualquier persona que pueda ser menor de edad; "
            "si no hay una identificación válida, niega la venta."
        ],
        "instruction": "Lea lo siguiente y luego haga clic en Siguiente.",
    },
    46: {
        "paragraphs": [
            "Consistencia: utiliza el mismo proceso de verificación de identificación siempre; evita las excepciones."
        ],
        "instruction": "Lea lo siguiente y luego haga clic en Siguiente.",
    },
    93: {
        "paragraphs": [
            "Una forma sencilla de verificar la edad es restar 21 años a la fecha de hoy. Esto te da la fecha de nacimiento "
            "más reciente aceptable para ventas legales. Si el cliente nació en esa fecha o antes, es elegible. Si su fecha "
            "de nacimiento es posterior a esa fecha, es menor de edad y debes negar la venta."
        ],
        "instruction": "Lea lo siguiente y luego haga clic en Siguiente.",
    },
    23: {
        "paragraphs": [
            "El consumo de alcohol entre menores de edad puede perjudicar la educación y las oportunidades futuras; "
            "algunas infracciones pueden afectar la elegibilidad para becas. Negarte a una venta protege su futuro. "
            "Referencias: SC Code § 59-104-20; § 61-4-100; § 61-6-4085; Reg. 62-900.95."
        ],
        "instruction": "Lea lo siguiente y luego haga clic en Siguiente.",
    },
    91: {
        "paragraphs": [
            "La verificación de la edad comienza por localizar la fecha de nacimiento en la identificación. "
            "Normalmente está claramente etiquetada. No asumas la ubicación. Tómate un momento para encontrarla "
            "y léela con cuidado. Leer mal los números puede provocar errores. Siempre confirma que estás mirando "
            "la fecha correcta antes de tomar una decisión."
        ],
        "instruction": "Lea lo siguiente y luego haga clic en Siguiente.",
    },
}


def unit_section(data, n):
    return next(s for c in data["courses"] for s in c["sections"] if s.get("order_index") == n)


def full(slide):
    c0 = slide["contents"][0]
    text = c0.get("text") or {}
    inter = c0.get("interactive") or {}
    bits = []
    bits += text.get("paragraphs") or []
    if inter.get("question"):
        bits.append(inter["question"])
    if inter.get("content_structure"):
        bits += inter["content_structure"]
    for it in inter.get("reveal_items") or []:
        bits.append(f"{it.get('title', '')}: {it.get('revealed_text', '')}")
    return " ".join(bits)


def reflow_order(slides):
    for i, slide in enumerate(slides):
        slide["order_index"] = i
        contents = slide.get("contents") or []
        for j, content in enumerate(contents):
            content["order_index"] = j if len(contents) > 1 else i


def apply_text_override(slide, override):
    c0 = slide["contents"][0]
    if "text" not in c0:
        c0["text"] = {}
    c0["text"]["paragraphs"] = list(override["paragraphs"])
    if "instruction" in override:
        c0["text"]["instruction"] = override["instruction"]
    # Drop interactive if this was somehow not a pure text slide
    c0.pop("interactive", None)
    slide["content_type"] = "Text"
    slide["content_type_unique_id"] = "text"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    assert len(EN_TO_ES) == 144
    assert len(set(EN_TO_ES.values())) == 144
    assert set(EN_TO_ES) == set(range(144))
    assert set(EN_TO_ES.values()) == set(range(144))

    es = json.loads(ES_PATH.read_text(encoding="utf-8"))
    en = json.loads(EN_PATH.read_text(encoding="utf-8"))
    es_sec = unit_section(es, 3)
    en_sec = unit_section(en, 3)
    en_slides = en_sec["slides"]
    es_slides = es_sec["slides"]
    assert len(en_slides) == len(es_slides) == 144

    moved = [(i, j) for i, j in EN_TO_ES.items() if i != j]
    print(f"Moves: {len(moved)}")
    for i, j in moved:
        et, st = en_slides[i]["content_type"], es_slides[j]["content_type"]
        if et != st and i not in OVERRIDES:
            raise SystemExit(f"Type mismatch EN[{i}] {et} vs ES[{j}] {st}")
        print(f"  EN[{i}] {et} <- ES[{j}] {st}")
        print(f"    EN: {full(en_slides[i])[:90]}")
        print(f"    ES: {full(es_slides[j])[:90]}")

    print(f"\nOverrides: {sorted(OVERRIDES)}")

    if not args.apply:
        print("\nDry run OK. Re-run with --apply to write.")
        return

    new_slides = []
    for i in range(144):
        slide = copy.deepcopy(es_slides[EN_TO_ES[i]])
        if i in OVERRIDES:
            apply_text_override(slide, OVERRIDES[i])
        elif slide["content_type"] != en_slides[i]["content_type"]:
            raise SystemExit(f"Type mismatch after copy at {i}")
        new_slides.append(slide)

    reflow_order(new_slides)
    es_sec["slides"] = new_slides
    ES_PATH.write_text(json.dumps(es, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # verify
    es2 = json.loads(ES_PATH.read_text(encoding="utf-8"))
    slides = unit_section(es2, 3)["slides"]
    assert len(slides) == 144
    assert all(s["order_index"] == i for i, s in enumerate(slides))
    assert all(slides[i]["content_type"] == en_slides[i]["content_type"] for i in range(144))
    print("\nWrote ES Unit 3: 144 slides, types aligned, overrides applied.")
    for i in sorted(OVERRIDES):
        print(f"  ES[{i}]: {full(slides[i])[:120]}")


if __name__ == "__main__":
    main()
