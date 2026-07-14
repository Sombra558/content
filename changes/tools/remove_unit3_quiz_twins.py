"""Remove Unit 3 end-of-unit quiz twins from EN and ES (EN = source of truth).

Keeps mid-unit quizzes 29/65/89 and end quiz 137.
Removes: 138 (twin of 29), 139 (twin of 65), 141 (twin of 89), 143 (twin of 137).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"d:\GetLicensed\content")
EN_PATH = ROOT / "dist" / "sc-content" / "sc-content.en.json"
ES_PATH = ROOT / "dist" / "sc-content" / "sc-content.es.json"

# Indexes to remove (pre-removal Unit 3 indexes)
REMOVE = {138, 139, 141, 143}


def unit_section(data, n):
    return next(s for c in data["courses"] for s in c["sections"] if s.get("order_index") == n)


def reflow(slides):
    for i, slide in enumerate(slides):
        slide["order_index"] = i
        contents = slide.get("contents") or []
        for j, content in enumerate(contents):
            content["order_index"] = j if len(contents) > 1 else i


def question(slide):
    return (slide["contents"][0].get("interactive") or {}).get("question", "")[:90]


def process(path: Path, indent: int):
    data = json.loads(path.read_text(encoding="utf-8"))
    sec = unit_section(data, 3)
    before = len(sec["slides"])
    assert before == 144, before

    removed = []
    keep = []
    for i, slide in enumerate(sec["slides"]):
        if i in REMOVE:
            removed.append((i, slide["content_type"], question(slide)))
        else:
            keep.append(slide)

    assert len(keep) == 140, len(keep)
    assert len(removed) == 4, removed

    reflow(keep)
    sec["slides"] = keep
    path.write_text(json.dumps(data, ensure_ascii=False, indent=indent) + "\n", encoding="utf-8")

    print(f"\n{path.name}: {before} -> {len(keep)}")
    for i, ctype, q in removed:
        print(f"  removed [{i}] {ctype}: {q}")

    # verify remaining end quizzes
    quizzes = [
        (i, question(s))
        for i, s in enumerate(keep)
        if s["content_type"] == "Multiple"
    ]
    print(f"  quizzes left ({len(quizzes)}):")
    for i, q in quizzes:
        print(f"    [{i}] {q}")


def main():
    process(EN_PATH, indent=1)
    process(ES_PATH, indent=2)
    print("\nDone.")


if __name__ == "__main__":
    main()
