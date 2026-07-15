"""Check Unit 6 EN/ES index + content alignment (read-only)."""
from __future__ import annotations

import json
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


# (en_index, en_substring, es_substring)
MARKERS: list[tuple[int, str, str]] = [
    (0, "6A. Responsibilities", "6A. Responsabilidades"),
    (1, "duty to serve responsibly at all times", "deber de servir de manera responsable"),
    (2, "verify that customers are legally allowed", "verificar que los clientes tengan permitido"),
    (3, "core legal responsibilities include", "responsabilidades legales principales"),
    (4, "constant awareness", "conciencia constante"),
    (5, "Recognizing intoxication is part of your job", "Reconocer la intoxicación es parte"),
    (6, "Common warning signs include", "señales de advertencia comunes"),
    (7, "refusing service when necessary. This includes refusing alcohol to under", "Eres el responsable de rechazar"),
    (8, "Following company policies is part of your legal", "Seguir las políticas de la empresa"),
    (9, "preventing harm beyond the establishment", "prevención de daños más allá"),
    (10, "To stay compliant, always", "Para cumplir con las normas"),
    (11, "Good communication is part of responsible service", "buena comunicación es parte"),
    (12, "several drinks over a short period", "varias copas en un breve"),
    (13, "Managers are a key resource for alcohol servers", "gerentes son un recurso clave"),
    (14, "Team accountability means everyone shares", "responsabilidad del equipo significa"),
    (15, "Managers help support safe service by providing", "gerentes ayudan a respaldar"),
    (16, "involve a manager when you are unsure about a customer", "involucrar a un gerente cuando no estés"),
    (17, "Managers also help handle difficult or confrontational", "gerentes también ayudan a manejar"),
    (18, "Work as a team by", "Trabaja en equipo"),
    (19, "Supporting coworkers is part of team accountability", "Apoyar a los compañeros"),
    (20, "Consistency is critical in alcohol service", "consistencia es crítica"),
    (21, "Managers are responsible for enforcing policies", "gerentes son responsables de hacer cumplir"),
    (22, "not a one-time lesson", "no es una lección de una sola vez"),
    (23, "Make ongoing training a habit", "capacitación continua en un hábito"),
    (24, "changed a rule about serving hours", "cambiado una regla sobre horarios"),
    (25, "Businesses open after 5 p.m.", "negocios abiertos después de las 5"),
    (26, "civil liability", "compartir responsabilidad"),
    (27, "restricts alcohol promotions that encourage", "restringe las promociones de alcohol"),
    (28, "Curbside and drive-thru alcohol sales are prohibited", "curbside y drive-thru están prohibidas"),
    (29, "Alcohol Server Certificate is issued", "Alcohol Server Certificate se emite"),
    (30, "Know when to escalate a situation", "Know when to escalate"),  # placeholder; refined below
    (31, "strong team culture supports responsible", "sólida cultura de equipo"),
    (32, "becomes upset after you refuse service due to signs", "se molesta después de que niegas"),
    (33, "Responsible marketing and promotion are important", "marketing y la promoción responsables"),
    (34, "Alcohol promotions should support moderate", "promociones de alcohol deben apoyar"),
    (35, "Responsible promotions focus on", "promociones responsables fomentan"),
    (36, "Marketing decisions are usually made by management", "decisiones de marketing suelen"),
    (37, "Promotions can change how customers behave", "promociones pueden cambiar"),
    (38, "Watch for risks during promotions", "atento durante las promociones"),
    (39, "how alcohol is presented to customers", "cómo se presenta el alcohol"),
    (40, "even during promotions. A discount", "incluso durante las promociones"),
    (41, "setting promotion guidelines", "pautas de promoción"),
    (42, "Support responsible promotion by", "promoción responsable mediante"),
    (43, "Responsible promotion supports long-term", "promoción responsable respalda"),
    (44, "participating in a drink special", "participa en una bebida especial"),
    (45, "Standard drink awareness helps", "conocimiento estándar de las bebidas"),
    (46, "A standard drink is a general way to measure", "bebida estándar es una forma general"),
    (47, "standard drink is based on alcohol content, not size", "basa en el contenido de alcohol, no en el tamaño"),
    (48, "Drink size and strength can vary", "tamaño y la concentración"),
    (49, "may not understand standard drink sizes", "no comprendan los tamaños"),
    (50, "exceed one standard serving", "exceder una porción estándar"),
    (51, "helps you pace service", "controlar el ritmo del servicio"),
    (52, "Different customers are affected differently", "afectado de manera diferente"),
    (53, "supports communication with coworkers and managers", "favorece la comunicación con compañeros"),
    (54, "Use standard drink awareness to", "conocimiento de bebidas estándar para"),
    (55, "Understanding standard drinks is part of responsible", "Comprender las bebidas estándar"),
    (56, "strong cocktail with multiple shots", "cóctel fuerte con varios tragos"),
    (57, "Workplace culture sets the tone", "cultura del lugar de trabajo marca"),
    (58, "Ethics in alcohol service means doing the right thing", "ética en el servicio de alcohol"),
    (59, "strong workplace culture values", "cultura laboral sólida valora"),
    (60, "Professional conduct means staying calm", "conducta profesional significa"),
    (61, "Team accountability is a key part of workplace culture", "parte clave de la cultura laboral"),
    (62, "Support ethical service by", "servicio ético"),
    (63, "prioritize safety over sales", "priorizar la seguridad sobre las ventas"),
    (64, "Managers play a key role in shaping workplace culture", "papel clave en la configuración de la cultura"),
    (65, "how you communicate with coworkers", "comunica con tus compañeros"),
    (66, "Maintain professionalism by", "ser profesional"),
    (67, "encourages confidence in making difficult decisions", "fomenta la confianza"),
    (68, "coworker continues serving a customer who appears intoxicated", "continúa atendiendo a un cliente que parece ebrio"),
    (69, "ID that looks damaged and hard to read", "identificación que parece dañada"),
    (70, "unsure whether a customer is intoxicated. What is the best next step", "No estás seguro de si un cliente está ebrio"),
    (71, "busy shift makes it hard to track", "turno ocupado dificulta"),
    (72, "multiple drinks at once for themselves", "varias bebidas a la vez"),
    (73, "coworker refuses service and the customer asks you", "niega el servicio y el cliente te pide"),
]


def main():
    en = json.loads(EN_PATH.read_text(encoding="utf-8"))
    es = json.loads(ES_PATH.read_text(encoding="utf-8"))
    en_s = unit_section(en, 6)["slides"]
    es_s = unit_section(es, 6)["slides"]
    assert len(en_s) == len(es_s) == 74

    # refine marker 30 from actual ES leftovers later; first pass dump unused completions
    used: set[int] = set()
    mapping: dict[int, int] = {}
    missing = []
    multi = []

    # Override ES marker for 30 once we see candidates
    markers = list(MARKERS)

    for en_i, en_sub, es_sub in markers:
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

    orphans = sorted(set(range(74)) - used)
    unmapped = sorted(set(range(74)) - set(mapping))

    # leftover pairing by unique type
    if unmapped and orphans:
        print("\nLeftover pairing attempt...")
        for i in list(unmapped):
            ctype = en_s[i]["content_type"]
            cands = [j for j in orphans if es_s[j]["content_type"] == ctype]
            print(f"  EN[{i}] unused same-type ES: {cands}")
            for j in cands:
                print(f"    ES[{j}]: {full(es_s[j])[:120]}")
            if len(cands) == 1:
                mapping[i] = cands[0]
                orphans.remove(cands[0])
                unmapped.remove(i)
                print(f"  paired EN[{i}] <- ES[{cands[0]}]")

    moves = [(i, mapping[i]) for i in sorted(mapping) if mapping[i] != i]
    same = [i for i in sorted(mapping) if mapping[i] == i]

    print(f"Mapped {len(mapping)}/74  moves={len(moves)}  missing={len(missing)} multi={len(multi)}")
    print(f"Already aligned: {len(same)}")
    print(f"Misaligned: {[i for i,_ in moves]}")
    if missing:
        print("MISSING:", missing)
    if multi:
        print("MULTI:", multi)
    print("orphans", orphans, "unmapped", unmapped)

    print("\n=== MOVES (EN index <- current ES index) ===")
    for i, j in moves:
        print(f"EN[{i}] <- ES[{j}]  ({en_s[i]['content_type']})")
        print(f"  EN: {full(en_s[i])[:100]}")
        print(f"  ES: {full(es_s[j])[:100]}")

    # same-index topic fails among early block
    print("\n=== SAME-INDEX QUICK FAIL (0-32) ===")
    for i in range(33):
        if i not in mapping:
            print(f"[{i}] unmapped")
            continue
        if mapping[i] != i:
            print(f"[{i}] ES currently has wrong topic (belongs at EN from ES[{mapping[i]}])")
            print(f"     EN wants: {full(en_s[i])[:80]}")
            print(f"     ES has:   {full(es_s[i])[:80]}")


if __name__ == "__main__":
    main()
