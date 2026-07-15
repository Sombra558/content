"""Check Unit 7 EN/ES index + content alignment (read-only)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"d:\GetLicensed\content")
EN_PATH = ROOT / "dist" / "sc-content" / "sc-content.en.json"
ES_PATH = ROOT / "dist" / "sc-content" / "sc-content.es.json"


def unit_section(data, n):
    return next(s for c in data["courses"] for s in c["sections"] if s.get("order_index") == n)


def full(slide):
    c0 = slide["contents"][0]
    text = c0.get("text") or {}
    inter = c0.get("interactive") or {}
    bits = []
    bits += text.get("paragraphs") or []
    bp = text.get("bullet_points")
    if isinstance(bp, list):
        bits += bp
    if inter.get("question"):
        bits.append(inter["question"])
    if inter.get("content_structure"):
        bits += inter["content_structure"]
    for it in inter.get("reveal_items") or []:
        bits.append(it.get("title", ""))
    return " ".join(bits)


def squash(s):
    return re.sub(r"\s+", " ", s or "").strip()


def inter(slide):
    return slide["contents"][0].get("interactive") or {}


# Distinctive EN/ES pairs for bijective map
MARKERS = [
    (0, "7A. SC DUI Statistics", "7A. Estadísticas"),
    (1, "DUI penalties increase with each offense", "sanciones por DUI"),
    (2, "DUI law covers driving while under the influence", "ley de DUI de Carolina del Sur cubre"),
    (3, "Felony DUI applies when", "DUI grave aplica"),
    (4, "Implied consent means", "consentimiento implícito"),
    (5, "open-container law prohibits", "contenedor abierto"),
    (6, "refuse a breath test because they never agreed", "negarse a una prueba de aliento"),
    (7, "unfinished open beer in the car", "cerveza abierta sin terminar"),
    (8, "alcohol-related crashes and DUI arrests each year", "accidentes relacionados con el alcohol y arrestos"),
    (9, "most serious traffic-safety problems", "problemas más graves de seguridad vial"),
    (10, "5,319 alcohol- or drug-involved", "5,319 colisiones"),
    (11, "DUI arrest", "aplicación de la ley está aumentando"),
    (12, "statistics point back to your role", "estadísticas vuelven a tu función"),
    (13, "NHTSA FARS", "NHTSA FARS"),
    (14, "commonly linked to DUI", "comúnmente están vinculados a DUI"),
    (15, "DUI arrests in South Carolina are actively enforced", "arrestos por DUI en Carolina del Sur son aplicados"),
    (16, "Sobriety checkpoints", "puestos de control de sobriedad"),
    (17, "DUI trends show increased risk", "tendencias de DUI muestran"),
    (18, "common high-risk periods for DUI", "períodos comunes de alto"),
    (19, "showed visible signs of intoxication before leaving", "signos visibles de intoxicación ante"),
    (20, "Repeat DUI offenses", "delitos repetidos de DUI"),
    (21, "requires alcohol server training to reduce risks", "exige capacitación para los servidores"),
    (22, "drinking for several hours. It is late", "varias horas bebiendo"),
    (23, "Alcohol-related injuries and fatalities remain", "lesiones y muertes relacionadas con el alcohol"),
    (24, "slows brain function and physical coordination", "ralentiza la función cerebral"),
    (25, "Alcohol can lead to", "alcohol puede provocar"),
    (26, "Alcohol-related fatalities are often linked", "muertes relacionadas con el alcohol a menudo"),
    (27, "Many injuries happen inside or near establishments", "lesiones ocurren dentro o cerca"),
    (28, "Risk increases when alcohol is combined", "riesgo aumenta cuando el alcohol se combina"),
    (29, "Risk increases with", "El riesgo aumenta con"),
    (30, "increase aggression and reduce self-control", "aumentar la agresión"),
    (31, "multiple missed chances to intervene", "múltiples oportunidades de intervenir"),
    (32, "preventing alcohol-related harm through responsible service", "prevención de los daños relacionados"),
    (33, "To reduce risk,", "Para reducir el riesgo"),
    (34, "stumbling, bumps into others, and drops a glass", "tropieza, choca con otros"),
    (35, "direct impact on community safety", "impacto directo en la seguridad de la comunidad"),
    (36, "Public safety concerns increase when alcohol is misused", "seguridad pública aumentan cuando se abusa"),
    (37, "Community impact may include", "impacto en la comunidad puede incluir"),
    (38, "strain local resources", "sobrecargar los recursos locales"),
    (39, "Neighborhood quality of life", "calidad de vida del vecindario"),
    (40, "Public intoxication can create safety concerns", "intoxicación en público"),
    (41, "Public safety risks include", "riesgos para la seguridad pública incluyen"),
    (42, "supports a safer environment for everyone", "entorno más seguro para todos"),
    (43, "understanding community impact as part of alcohol", "comprender el impacto en la comunidad"),
    (44, "Working as a team improves community safety", "Trabajar en equipo mejora"),
    (45, "To support community safety", "respaldar la seguridad de la comunidad"),
    (46, "loud and disruptive near closing time", "ruidoso y perturbador cerca"),
    (47, "Law enforcement plays a key role in overseeing", "fuerzas del orden desempeñan"),
    (48, "Compliance checks are used to verify", "controles de cumplimiento se utilizan"),
    (49, "Compliance checks may involve", "comprobaciones de cumplimiento pueden"),
    (50, "routine visits to licensed establishments", "visitas de rutina"),
    (51, "Underage compliance operations", "operaciones de cumplimiento con menores"),
    (52, "monitoring service to intoxicated individuals", "vigilancia a personas en estado de ebriedad"),
    (53, "Enforcement focuses on", "controles por parte de las autoridades se centran"),
    (54, "Failure to follow alcohol laws", "incumplimiento de las leyes sobre el alcohol"),
    (55, "Managers play an important role during enforcement", "papel importante durante las interacciones"),
    (56, "awareness of enforcement and complia", "conciencia s"),
    (57, "To stay compliant,", "Para cumplir con las normas el servidor"),
    (58, "officer enters your establishment during a busy shift", "oficial ingresa a tu establecimiento"),
    (59, "Real-world cases show how alcohol service decisions", "casos del mundo real muestran"),
    (60, "visibly impaired guest continued to be served", "visiblemente discapacitado"),  # may be drift word
    (61, "Warning signs in this case included", "señales de advertencia en este caso"),
    (62, "underage individual who was served alcohol without proper ID", "menor de edad a quien le sirvieron"),
    (63, "intoxicated guests have been involved in fights", "involucrados en peleas"),
    (64, "delayed response", "retraso en la respuesta"),
    (65, "affect more than just the individual involved", "afectan a algo más que al individuo"),
    (66, "real incidents connect to service decisions", "incidentes reales se conectan"),
    (67, "To prevent similar cases", "evitar casos similares"),
    (68, "insists they are fine and asks for another drink", "insiste en que está bien"),
    (69, "speaking slowly. They ask for another drink and menti", "hablar lentamente"),
    (70, "coworker continues serving a guest who appears intoxicated", "continúa atendiendo a un huésped que parece ebrio"),
    (71, "tries to leave quickly after heavy drinking", "irse rápidamente después de haber bebido"),
]


def main():
    en = json.loads(EN_PATH.read_text(encoding="utf-8"))
    es = json.loads(ES_PATH.read_text(encoding="utf-8"))
    en_s = unit_section(en, 7)["slides"]
    es_s = unit_section(es, 7)["slides"]
    assert len(en_s) == len(es_s) == 72

    used = set()
    mapping = {}
    missing = []
    multi = []
    for en_i, en_sub, es_sub in MARKERS:
        ctype = en_s[en_i]["content_type"]
        if en_sub.lower() not in full(en_s[en_i]).lower():
            missing.append((en_i, "EN_MISS", en_sub))
            continue
        hits = []
        for j, s in enumerate(es_s):
            if j in used or s["content_type"] != ctype:
                continue
            if es_sub.lower() in full(s).lower():
                hits.append(j)
        if not hits:
            missing.append((en_i, "NO_ES", es_sub))
            continue
        if len(hits) > 1:
            multi.append((en_i, hits, es_sub))
        mapping[en_i] = hits[0]
        used.add(hits[0])

    orphans = sorted(set(range(72)) - used)
    unmapped = sorted(set(range(72)) - set(mapping))
    moves = [(i, mapping[i]) for i in sorted(mapping) if mapping[i] != i]

    print(f"Mapped {len(mapping)}/72 moves={len(moves)} missing={len(missing)} multi={len(multi)}")
    print("MISSING", missing)
    print("MULTI", multi)
    print("orphans", orphans, "unmapped", unmapped)
    print("Misaligned indices:", [i for i, _ in moves])
    for i, j in moves:
        print(f"  EN[{i}] <- ES[{j}]")
        print(f"    EN: {full(en_s[i])[:90]}")
        print(f"    ES: {full(es_s[j])[:90]}")

    # quiz correct indices
    print("\n=== QUIZZES ===")
    quiz_issues = []
    for i in range(72):
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
        print(f"[{i}] correct {ce}/{cs} opts {len(eo)}/{len(so)}")
        print("  EN:", squash(ei.get("question", ""))[:100])
        print("  ES:", squash(si.get("question", ""))[:100])
        if ce != cs or len(eo) != len(so):
            quiz_issues.append((i, ce, cs, len(eo), len(so)))

    # completion item counts + notable drifts
    print("\n=== COMPLETIONS ===")
    notable = []
    for i in range(72):
        if en_s[i]["content_type"] != "Completion":
            continue
        ei, si = inter(en_s[i]), inter(es_s[i])
        er, sr = ei.get("reveal_items") or [], si.get("reveal_items") or []
        print(f"\n[{i}] {len(er)}/{len(sr)}")
        print(" EN:", squash((ei.get("content_structure") or [""])[0])[:110])
        print(" ES:", squash((si.get("content_structure") or [""])[0])[:110])
        for a, b in zip(er, sr):
            at, bt = a.get("title", ""), b.get("title", "")
            print(f"  {at} | {bt}")
            if "siguiente" in bt.lower() and "follow" in at.lower():
                notable.append((i, at, bt, "siguiente≠following"))
            if "discapacitado" in bt.lower() or "discapacitado" in squash(si.get("content_structure", [""])[0]).lower():
                pass

    # thin / length
    print("\n=== THIN ===")
    thin = []
    for i in range(72):
        et, st = full(en_s[i]), full(es_s[i])
        if len(et) < 40:
            continue
        ratio = len(st) / len(et)
        if ratio < 0.55 or ratio > 2.0:
            thin.append(i)
            print(f"[{i}] {ratio:.2f}")
            print(" EN:", squash(et)[:120])
            print(" ES:", squash(st)[:120])

    # known wording issues
    print("\n=== WORDING SPOT CHECKS ===")
    for i in [52, 60]:
        print(f"[{i}] EN:", squash(full(en_s[i]))[:160])
        print(f"     ES:", squash(full(es_s[i]))[:160])

    print("\nSUMMARY quiz_issues", quiz_issues, "thin", thin, "notable", notable, "moves", len(moves))


if __name__ == "__main__":
    main()
