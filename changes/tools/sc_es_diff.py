"""Three-way diff: backup EN vs current EN vs current ES.

Goals:
1. Classify every current-EN slide as unchanged / edited / new relative to
   changes/backups/sc-content.en.pre-wellcovered.json.
2. Match every current-EN slide to a current-ES slide using language-invariant
   fingerprints (statute cites, dollar amounts, percentages, asset ids,
   content type, interactive shape) plus relative-order fallback.
3. Report: EN slides with no ES counterpart (untranslated), ES slides with a
   stale fingerprint (EN edited after sync), and index misalignment.

Output: console summary + changes/tools/es_diff_report.json
"""
import difflib
import json
import os
import re
from collections import defaultdict

EN_PATH = os.path.join("dist", "sc-content", "sc-content.en.json")
ES_PATH = os.path.join("dist", "sc-content", "sc-content.es.json")
BK_PATH = os.path.join("changes", "backups", "sc-content.en.pre-wellcovered.json")

STATUTE = re.compile(r"\b\d{1,2}-\d{1,4}-\d{1,5}(?:\.\d+)?\b")
REGCITE = re.compile(r"\b7-\d{3}(?:\.\d+)?\b")
MONEY = re.compile(r"\$[\d,]+(?:\.\d+)?")
PERCENT = re.compile(r"\b\d+(?:\.\d+)?%")
BIGNUM = re.compile(r"\b\d{1,2},\d{3}\b|\b\d{3,4}\b")
ACRONYM = re.compile(r"\b(?:PBW|PO7|PLB|PLC|LOP|BAC|DUI|SLED|SCDOR|SCDPS|NHTSA|FARS|MYDORWAY|DOB)\b")


def slide_text(slide):
    parts = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("content_type", "content_type_unique_id", "asset_id", "id", "status", "preview_url"):
                    continue
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif isinstance(o, str):
            parts.append(o)

    walk(slide)
    return " ".join(parts)


def shape(slide):
    """Language-independent structural signature."""
    ct = slide.get("content_type_unique_id", "")
    n_opts = n_items = n_imgs = 0
    assets = []
    for co in slide.get("contents", []):
        inter = co.get("interactive") or {}
        n_opts += len(inter.get("options", []))
        n_items += len(inter.get("reveal_items", []))
        if "image" in co:
            n_imgs += 1
            assets.append(co["image"].get("asset_id", ""))
    return ct, n_opts, n_items, n_imgs, tuple(sorted(assets))


def fingerprint(slide):
    t = slide_text(slide)
    toks = set()
    toks.update("S:" + m for m in STATUTE.findall(t))
    toks.update("R:" + m for m in REGCITE.findall(t))
    toks.update("$:" + m for m in MONEY.findall(t))
    toks.update("%:" + m for m in PERCENT.findall(t))
    toks.update("A:" + m for m in ACRONYM.findall(t))
    for co in slide.get("contents", []):
        if "image" in co:
            toks.add("IMG:" + co["image"].get("asset_id", ""))
    return toks


def jaccard(a, b):
    if not a and not b:
        return None  # no signal
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def units(data):
    return data["courses"][0]["sections"]


def classify_en(bk_slides, en_slides):
    """For each current EN slide: unchanged / edited / new vs backup."""
    bk_texts = [slide_text(s) for s in bk_slides]
    used = set()
    result = []
    for i, s in enumerate(en_slides):
        t = slide_text(s)
        # exact
        hit = next((j for j, bt in enumerate(bk_texts) if j not in used and bt == t), None)
        if hit is not None:
            used.add(hit)
            result.append(("unchanged", hit))
            continue
        # fuzzy
        best_j, best_r = None, 0.0
        for j, bt in enumerate(bk_texts):
            if j in used:
                continue
            r = difflib.SequenceMatcher(None, bt, t).quick_ratio()
            if r > best_r:
                best_j, best_r = j, r
        if best_j is not None and best_r >= 0.85:
            r = difflib.SequenceMatcher(None, bk_texts[best_j], t).ratio()
            if r >= 0.85:
                used.add(best_j)
                result.append(("unchanged", best_j))
                continue
            if r >= 0.55:
                used.add(best_j)
                result.append(("edited", best_j))
                continue
        result.append(("new", None))
    return result


def match_es(en_slides, es_slides):
    """Match EN slides to ES slides inside one unit.

    Returns list per EN index: (es_index or None, method, score)
    """
    en_fp = [fingerprint(s) for s in en_slides]
    es_fp = [fingerprint(s) for s in es_slides]
    en_sh = [shape(s) for s in en_slides]
    es_sh = [shape(s) for s in es_slides]

    matches = [None] * len(en_slides)
    taken = set()

    # pass 1: fingerprint matching, best-first
    cands = []
    for i in range(len(en_slides)):
        for j in range(len(es_slides)):
            if en_sh[i][0] != es_sh[j][0]:
                continue  # content type must agree
            score = jaccard(en_fp[i], es_fp[j])
            if score is not None and score >= 0.5:
                bonus = 0.05 if en_sh[i] == es_sh[j] else 0.0
                cands.append((score + bonus, i, j))
    for score, i, j in sorted(cands, reverse=True):
        if matches[i] is None and j not in taken:
            matches[i] = (j, "fingerprint", round(score, 2))
            taken.add(j)

    # pass 2: leftovers -> align by relative order among same content type
    left_en = [i for i in range(len(en_slides)) if matches[i] is None]
    left_es = [j for j in range(len(es_slides)) if j not in taken]
    by_ct_en = defaultdict(list)
    by_ct_es = defaultdict(list)
    for i in left_en:
        by_ct_en[en_sh[i]].append(i)
    for j in left_es:
        by_ct_es[es_sh[j]].append(j)
    for sh_key, en_list in by_ct_en.items():
        es_list = by_ct_es.get(sh_key, [])
        for i, j in zip(en_list, es_list):
            matches[i] = (j, "order", None)
            taken.add(j)

    unmatched_es = [j for j in range(len(es_slides)) if j not in taken]
    return matches, unmatched_es


def main():
    en = load(EN_PATH)
    es = load(ES_PATH)
    bk = load(BK_PATH)

    report = []
    totals = defaultdict(int)

    for u, (en_sec, es_sec, bk_sec) in enumerate(zip(units(en), units(es), units(bk)), 1):
        en_slides, es_slides, bk_slides = en_sec["slides"], es_sec["slides"], bk_sec["slides"]
        status = classify_en(bk_slides, en_slides)
        matches, orphan_es = match_es(en_slides, es_slides)

        unit_rows = []
        for i, s in enumerate(en_slides):
            st, _ = status[i]
            m = matches[i]
            es_idx, method, score = m if m else (None, None, None)
            problems = []
            if es_idx is None:
                problems.append("NO_ES_MATCH")
            else:
                if method == "fingerprint" and score is not None and score < 0.99:
                    fp_en, fp_es = fingerprint(s), fingerprint(es_slides[es_idx])
                    missing = sorted(fp_en - fp_es)
                    extra = sorted(fp_es - fp_en)
                    if missing or extra:
                        problems.append("FP_DRIFT")
                if st == "edited" and method == "order":
                    problems.append("LIKELY_STALE_ES")
                if es_idx != i:
                    problems.append("MISORDERED")
            unit_rows.append({
                "en_index": i,
                "en_status": st,
                "content_type": s.get("content_type_unique_id"),
                "es_index": es_idx,
                "match_method": method,
                "match_score": score,
                "problems": problems,
                "en_snippet": slide_text(s)[:120],
                "es_snippet": slide_text(es_slides[es_idx])[:120] if es_idx is not None else None,
            })
            totals["en_" + st] += 1
            for p in problems:
                totals[p] += 1

        report.append({
            "unit": u,
            "title": en_sec["title"],
            "en_count": len(en_slides),
            "es_count": len(es_slides),
            "orphan_es_indexes": orphan_es,
            "slides": unit_rows,
        })
        totals["orphan_es"] += len(orphan_es)

    out = os.path.join("changes", "tools", "es_diff_report.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=1, ensure_ascii=False)

    print("=== SUMMARY ===")
    for k in sorted(totals):
        print(f"{k:>20}: {totals[k]}")
    print()
    for unit in report:
        bad = [r for r in unit["slides"] if r["problems"]]
        mis = sum(1 for r in unit["slides"] if "MISORDERED" in r["problems"])
        hard = [r for r in bad if set(r["problems"]) - {"MISORDERED"}]
        print(f"Unit {unit['unit']}: {unit['en_count']} EN / {unit['es_count']} ES | "
              f"misordered {mis} | serious {len(hard)} | orphan ES {len(unit['orphan_es_indexes'])}")
        for r in hard[:8]:
            print(f"   EN#{r['en_index']} [{r['en_status']}/{r['content_type']}] {r['problems']} -> ES#{r['es_index']}")
            print(f"      EN: {r['en_snippet'][:100]}")
            if r["es_snippet"]:
                print(f"      ES: {r['es_snippet'][:100]}")
    print(f"\nFull report: {out}")


if __name__ == "__main__":
    main()
