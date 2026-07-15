"""Deep content audit for Unit 6 EN vs ES (read-only)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
from align_unit6_es_to_en import EN_PATH, ES_PATH, full, unit_section


def squash(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def inter(slide):
    return slide["contents"][0].get("interactive") or {}


TOPIC = {
    0: (["6A"], ["6A"]),
    1: (["duty to serve responsibly"], ["deber de servir"]),
    2: (["legally allowed to drink"], ["permitido beber"]),
    3: (["core legal responsibilities"], ["responsabilidades legales principales"]),
    4: (["constant awareness"], ["conciencia constante"]),
    5: (["Recognizing intoxication"], ["Reconocer la intoxicación"]),
    6: (["Common warning signs"], ["señales de advertencia comunes"]),
    7: (["refusing service when necessary"], ["rechazar el servicio cuando sea necesario"]),
    8: (["Following company policies"], ["Seguir las políticas de la empresa"]),
    9: (["beyond the establishment"], ["más allá del establecimiento"]),
    10: (["To stay compliant"], ["Para cumplir"]),
    11: (["Good communication"], ["buena comunicación"]),
    12: (["several drinks over a short period"], ["varias copas en un breve"]),
    13: (["Managers are a key resource"], ["gerentes son un recurso clave"]),
    14: (["Team accountability means everyone"], ["responsabilidad del equipo significa"]),
    15: (["Managers help support safe service"], ["gerentes ayudan a respaldar"]),
    16: (["involve a manager when you are unsure"], ["involucrar a un gerente cuando no estés"]),
    17: (["confrontational"], ["confrontación"]),
    18: (["Work as a team"], ["Trabaja en equipo"]),
    19: (["Supporting coworkers"], ["Apoyar a los compañeros"]),
    20: (["Consistency is critical"], ["consistencia es crítica"]),
    21: (["enforcing policies"], ["hacer cumplir"]),
    22: (["one-time lesson"], ["lección de una sola vez"]),
    23: (["ongoing training"], ["capacitación continua"]),
    24: (["serving hours"], ["horarios de servicio"]),
    25: (["after 5 p.m."], ["después de las 5"]),
    26: (["civil liability"], ["responsabilidad"]),
    27: (["restricts alcohol promotions"], ["restringe las promociones"]),
    28: (["drive-thru"], ["drive-thru"]),
    29: (["Alcohol Server Certificate"], ["Alcohol Server Certificate"]),
    30: (["escalate a situation"], ["siguientes situaciones"]),
    31: (["team culture supports"], ["cultura de equipo"]),
    32: (["refuse service due to signs"], ["niegas el servicio"]),
    33: (["Responsible marketing"], ["marketing"]),
    34: (["support moderate"], ["consumo moderado"]),
    35: (["Responsible promotions focus"], ["promociones responsables fomentan"]),
    36: (["Marketing decisions"], ["decisiones de marketing"]),
    37: (["Promotions can change"], ["promociones pueden cambiar"]),
    38: (["risks during promotions"], ["durante las promociones"]),
    39: (["presented to customers"], ["presenta el alcohol"]),
    40: (["even during promotions"], ["incluso durante las promociones"]),
    41: (["promotion guidelines"], ["pautas de promoción"]),
    42: (["Support responsible promotion"], ["promoción responsable"]),
    43: (["long-term"], ["largo plazo"]),
    44: (["drink special"], ["bebida especial"]),
    45: (["Standard drink awareness"], ["conocimiento estándar"]),
    46: (["general way to measure"], ["forma general"]),
    47: (["not size"], ["no en el tamaño"]),
    48: (["size and strength"], ["tamaño y la concentración"]),
    49: (["standard drink sizes"], ["tamaños de bebidas estándar"]),
    50: (["exceed one standard"], ["exceder una porción"]),
    51: (["pace service"], ["ritmo del servicio"]),
    52: (["affected differently"], ["manera diferente"]),
    53: (["communication with coworkers"], ["comunicación con compañeros"]),
    54: (["Use standard drink awareness"], ["bebidas estándar para"]),
    55: (["Understanding standard drinks"], ["Comprender las bebidas estándar"]),
    56: (["multiple shots"], ["varios tragos"]),
    57: (["Workplace culture sets the tone"], ["cultura del lugar de trabajo marca"]),
    58: (["Ethics in alcohol service"], ["ética en el servicio"]),
    59: (["workplace culture values"], ["cultura laboral sólida valora"]),
    60: (["Professional conduct means"], ["conducta profesional significa"]),
    61: (["key part of workplace culture"], ["parte clave de la cultura laboral"]),
    62: (["ethical service"], ["servicio ético"]),
    63: (["safety over sales"], ["seguridad sobre las ventas"]),
    64: (["shaping workplace culture"], ["configuración de la cultura"]),
    65: (["communicate with coworkers"], ["compañeros de trabajo"]),
    66: (["Maintain professionalism"], ["ser profesional"]),
    67: (["difficult decisions"], ["decisiones difíciles"]),
    68: (["coworker continues serving"], ["continúa atendiendo"]),
    69: (["damaged and hard to read"], ["dañada y difícil"]),
    70: (["unsure whether a customer is intoxicated"], ["No estás seguro de si un cliente está ebrio"]),
    71: (["busy shift"], ["turno ocupado"]),
    72: (["multiple drinks at once"], ["varias bebidas a la vez"]),
    73: (["asks you for a drink instead"], ["te pide una bebida"]),
}


def main():
    en = json.loads(EN_PATH.read_text(encoding="utf-8"))
    es = json.loads(ES_PATH.read_text(encoding="utf-8"))
    en_s = unit_section(en, 6)["slides"]
    es_s = unit_section(es, 6)["slides"]
    assert len(en_s) == len(es_s) == 74

    fails = []
    soft = []
    for i in range(74):
        if en_s[i]["content_type"] != es_s[i]["content_type"]:
            fails.append((i, "TYPE", en_s[i]["content_type"], es_s[i]["content_type"]))
            continue
        en_keys, es_keys = TOPIC[i]
        et, st = full(en_s[i]), full(es_s[i])
        if not any(k.lower() in et.lower() for k in en_keys):
            fails.append((i, "EN_ANCHOR", en_keys, et[:100]))
        if not any(k.lower() in st.lower() for k in es_keys):
            fails.append((i, "ES_ANCHOR", es_keys, st[:120]))
        if i == 30 and "escal" not in st.lower():
            soft.append((30, "stem says refuse-situations, EN says escalate", st[:120]))

    print(f"Hard fails: {len(fails)}")
    for f in fails:
        print(f)
    print(f"Soft: {soft}")

    print("\n=== COMPLETION REVEAL BANKS ===")
    item_drifts = []
    for i in range(74):
        if en_s[i]["content_type"] != "Completion":
            continue
        ei, si = inter(en_s[i]), inter(es_s[i])
        er, sr = ei.get("reveal_items") or [], si.get("reveal_items") or []
        print(f"\n[{i}] {len(er)}/{len(sr)}")
        print(" EN:", squash((ei.get("content_structure") or [""])[0])[:110])
        print(" ES:", squash((si.get("content_structure") or [""])[0])[:110])
        if len(er) != len(sr):
            item_drifts.append((i, "count", len(er), len(sr)))
        for k, (a, b) in enumerate(zip(er, sr)):
            at, bt = a.get("title", ""), b.get("title", "")
            print(f"  {k+1}. {at} | {bt}")
            # flag obvious meaning mismatches (heuristic: EN word not reflected)
            # manual notable ones checked below

    # Known soft item meaning checks
    notable = []
    for i in range(74):
        if en_s[i]["content_type"] != "Completion":
            continue
        er = inter(en_s[i]).get("reveal_items") or []
        sr = inter(es_s[i]).get("reveal_items") or []
        for k, (a, b) in enumerate(zip(er, sr)):
            at = (a.get("title") or "").lower()
            bt = (b.get("title") or "").lower()
            # specific known-risk pairs
            if at == "following policy" and "siguiendo" not in bt and "seguir" not in bt:
                # "siguiente política" is wrong for following policy
                if "siguiente" in bt:
                    notable.append((i, k + 1, a["title"], b["title"], "siguiente≠following"))
            if at == "stay longer" and "sin beber" in bt:
                notable.append((i, k + 1, a["title"], b["title"]))

    print("\n=== QUIZZES ===")
    quiz_issues = []
    for i in range(74):
        if en_s[i]["content_type"] != "Multiple":
            continue
        ei, si = inter(en_s[i]), inter(es_s[i])
        eo, so = ei.get("options") or [], si.get("options") or []

        def corr(opts):
            for j, o in enumerate(opts):
                if isinstance(o, dict) and o.get("is_correct"):
                    return j
            return None

        ce, cs = corr(eo), corr(so)
        print(f"\n[{i}] correct EN={ce} ES={cs} opts {len(eo)}/{len(so)}")
        print(" QEN:", squash(ei.get("question", ""))[:110])
        print(" QES:", squash(si.get("question", ""))[:110])
        for k in range(max(len(eo), len(so))):
            a = eo[k]["label"] if k < len(eo) else "—"
            b = so[k]["label"] if k < len(so) else "—"
            mark_e = "*" if ce == k else " "
            mark_s = "*" if cs == k else " "
            print(f"  {mark_e}{mark_s} {a[:75]}")
            print(f"     {b[:75]}")
        if ce != cs:
            quiz_issues.append((i, "correct", ce, cs))
        if len(eo) != len(so):
            quiz_issues.append((i, "optlen", len(eo), len(so)))

    print("\n=== THIN / LENGTH RATIO ===")
    thin = []
    for i in range(74):
        et, st = full(en_s[i]), full(es_s[i])
        if len(et) < 40:
            continue
        ratio = len(st) / len(et)
        if ratio < 0.55 or ratio > 2.0:
            thin.append(i)
            print(f"[{i}] ratio={ratio:.2f} EN={len(et)} ES={len(st)}")
            print(" EN:", squash(et)[:130])
            print(" ES:", squash(st)[:130])

    print("\n=== FULL SIDE-BY-SIDE ===")
    for i in range(74):
        print(f"{i:3d} {en_s[i]['content_type'][:10]:10s}")
        print(f"     EN: {squash(full(en_s[i]))[:95]}")
        print(f"     ES: {squash(full(es_s[i]))[:95]}")

    print("\n=== NOTABLE ITEM DRIFTS ===")
    # scan all reveal title pairs for a few heuristics
    for i in range(74):
        if en_s[i]["content_type"] != "Completion":
            continue
        er = inter(en_s[i]).get("reveal_items") or []
        sr = inter(es_s[i]).get("reveal_items") or []
        for k, (a, b) in enumerate(zip(er, sr)):
            at, bt = a.get("title", ""), b.get("title", "")
            if "following policy" in at.lower() and "siguiente" in bt.lower():
                notable.append((i, k + 1, at, bt, "siguiente política = next policy?"))
            if at.lower() == "decisions" and "decisiones" not in bt.lower():
                notable.append((i, k + 1, at, bt))
    for n in notable:
        print(n)

    print(
        "\nSUMMARY",
        "fails",
        len(fails),
        "quiz_issues",
        quiz_issues,
        "item_count_drifts",
        item_drifts,
        "thin",
        thin,
        "soft",
        soft,
        "notable",
        len(notable),
    )


if __name__ == "__main__":
    main()
