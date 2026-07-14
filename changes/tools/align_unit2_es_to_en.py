"""Rebuild ES Unit 2 slides to match EN Unit 2 order (EN = source of truth)."""
import copy
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"d:\GetLicensed\content")
ES_PATH = ROOT / "dist" / "sc-content" / "sc-content.es.json"
EN_PATH = ROOT / "dist" / "sc-content" / "sc-content.en.json"

# EN index -> ES index (pre-alignment). EN[4] has no ES source.
EN_TO_ES = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    # 4: new translation
    5: 5,
    6: 6,
    7: 4,
    8: 8,
    9: 9,
    10: 10,
    11: 11,
    12: 7,
    13: 13,
    14: 12,
    15: 14,
    16: 16,
    17: 17,
    18: 18,
    19: 19,
    20: 20,
    21: 15,
    22: 21,
    23: 23,
    24: 24,
    25: 25,
    26: 26,
    27: 22,
    28: 28,
    29: 29,
    30: 30,
    31: 31,
    32: 32,
    33: 27,
    34: 33,
    35: 34,
    36: 36,
    37: 37,
    38: 35,
    39: 39,
    40: 40,
    41: 38,
    42: 41,
    43: 43,
    44: 44,
    45: 42,
    46: 46,
    47: 45,
    48: 48,
    49: 49,
    50: 47,
    51: 50,
    52: 52,
    53: 51,
    54: 53,
    55: 55,
    56: 54,
    57: 56,
    58: 58,
    59: 57,
    60: 59,
    61: 61,
    62: 60,
    63: 62,
    64: 63,
    65: 64,
    66: 65,
}

LIVER_SLIDE = {
    "order_index": 4,
    "min_time": 3,
    "content_type": "Text",
    "content_type_unique_id": "text",
    "contents": [
        {
            "order_index": 4,
            "text": {
                "paragraphs": [
                    "El hígado procesa el alcohol con el tiempo. Lo descompone a un ritmo constante. "
                    "La mayoría de las personas procesan aproximadamente una bebida estándar por hora. "
                    "Beber más rápido que esto hace que el alcohol se acumule en el torrente sanguíneo. "
                    "Esto conduce a niveles más altos de intoxicación. No puedes acelerar este proceso."
                ],
                "instruction": "Lea lo siguiente y luego haga clic en Siguiente.",
            },
        }
    ],
}


def unit_section(data, n):
    return next(s for c in data["courses"] for s in c["sections"] if s.get("order_index") == n)


def reflow_order(slides):
    for i, slide in enumerate(slides):
        slide["order_index"] = i
        for j, content in enumerate(slide.get("contents") or []):
            content["order_index"] = j if len(slide["contents"]) > 1 else i
            # Prefer matching prior convention: single-content slides use slide index
            if len(slide["contents"]) == 1:
                content["order_index"] = i


def main():
    es = json.loads(ES_PATH.read_text(encoding="utf-8"))
    en = json.loads(EN_PATH.read_text(encoding="utf-8"))
    es_sec = unit_section(es, 2)
    en_sec = unit_section(en, 2)
    old_es = es_sec["slides"]
    en_slides = en_sec["slides"]

    assert len(en_slides) == 67, len(en_slides)
    assert len(old_es) == 66, len(old_es)
    assert set(EN_TO_ES.values()) == set(range(66))
    assert set(EN_TO_ES) == set(range(67)) - {4}

    new_slides = []
    for en_i in range(67):
        if en_i == 4:
            slide = copy.deepcopy(LIVER_SLIDE)
        else:
            slide = copy.deepcopy(old_es[EN_TO_ES[en_i]])
        # Keep content type aligned with EN
        en_type = en_slides[en_i]["content_type"]
        if slide["content_type"] != en_type:
            raise SystemExit(
                f"Type mismatch at EN[{en_i}]: EN={en_type} ES_src={slide['content_type']}"
            )
        new_slides.append(slide)

    reflow_order(new_slides)
    es_sec["slides"] = new_slides

    ES_PATH.write_text(
        json.dumps(es, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    # Verify
    es2 = json.loads(ES_PATH.read_text(encoding="utf-8"))
    slides = unit_section(es2, 2)["slides"]
    print(f"ES Unit 2 slides: {len(slides)} (was 66)")
    print(f"EN Unit 2 slides: {len(en_slides)}")
    print("EN[4] ES[4]:", slides[4]["contents"][0]["text"]["paragraphs"][0][:120])
    # spot-check a moved slide
    print("EN[7]/ES[7] drugs:", slides[7]["contents"][0]["text"]["paragraphs"][0][:80])
    print("EN[65]/ES[65] quiz:", slides[65]["contents"][0]["interactive"]["question"][:80])
    types_ok = all(
        slides[i]["content_type"] == en_slides[i]["content_type"] for i in range(67)
    )
    print("All content_type aligned:", types_ok)
    orders_ok = all(s["order_index"] == i for i, s in enumerate(slides))
    print("order_index sequential:", orders_ok)


if __name__ == "__main__":
    main()
