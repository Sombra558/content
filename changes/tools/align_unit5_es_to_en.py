"""Rebuild ES Unit 5 slides to match EN Unit 5 order (EN = source of truth)."""
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

# (en_index, en_substring, es_substring)
MARKERS: list[tuple[int, str, str]] = [
    (0, "5A. When to Refuse", "5A. Cuándo Rechazar"),
    (1, "calm, firm, and respectful", "calma, firmeza y respeto"),
    (2, "same escalation steps every time", "mismos pasos de escalamiento"),
    (3, "House policies turn responsible service", "políticas internas convierten"),
    (4, "refusing an illegal or unsafe sale always outranks", "rechazar una venta ilegal o insegura siempre"),
    (5, "I know the owner", "Conozco al dueño"),
    (6, "walking toward the parking lot", "caminar hacia el estacionamiento"),
    (7, "legal and professional responsibility in South Carolina", "obligación legal y profesional"),
    (8, "refuse service if a customer is under 21", "menor de 21 años"),
    (9, "signs of intoxication such as", "signos de intoxicación como"),
    (10, "prohibits selling alcohol to an intoxicated person", "prohíbe vender alcohol a una persona ebria"),
    (11, "Legal justification for refusal", "justificación legal de la denegación"),
    (12, "disruptive or unsafe", "problemático o inseguro"),
    (13, "involve management when refusing service in situations", "involucrar a la gerencia al rechazar el servicio en situaciones"),
    (14, "firm, calm, and respectful. Do not argue", "firme, tranquila y respetuosa"),
    (15, "Do not offer alternatives that involve alcohol", "No ofrezcas alternativas que involucren alcohol"),
    (16, "follow your establishment’s policies when refusing service", "políticas de tu establecimiento al rechazar"),
    (17, "Refusal protects you from", "negativa te protege"),
    (18, "slurring words, stumbling, and becoming loud", "arrastra las palabras, tropieza y hace ruido"),
    (19, "clear, consistent process", "proceso claro y consistente"),
    (20, "Step 1: Observe the customer carefully", "Paso 1:"),
    (21, "When observing, watch for", "Al observar"),
    (22, "Step 2: Decide clearly and confidently", "Paso 2:"),
    (23, "Step 3: Choose the right moment", "Paso 3:"),
    (24, "Step 4: Stay calm and professional", "Paso 4:"),
    (25, "Use clear language like", "lenguaje claro"),
    (26, "Step 5: Be direct and respectful", "Paso 5:"),
    (27, "Step 6: Do not negotiate", "Paso 6:"),
    (28, "Step 7: Stay aware of your surroundings", "Paso 7:"),
    (29, "If needed, move to", "Si es necesario"),
    (30, "correct first step", "primer paso correcto"),
    (31, "continues the refusal process after you have told", "continúa explicando el proceso de rechazo"),
    (32, "Step 8: Do not continue alcohol service", "Paso 8:"),
    (33, "After refusal, avoid", "Después de rechazar"),
    (34, "Step 9: Offer non-alcoholic alternatives", "Paso 9:"),
    (35, "Step 10: Monitor the customer", "Paso 10:"),
    (36, "Step 11: Involve management when needed", "Paso 11:"),
    (37, "Escalate when you see", "Solicita apoyo de la gerencia cuando"),
    (38, "Step 12: Keep a safe distance", "Paso 12:"),
    (39, "Step 13: Follow house procedures for documentation", "Paso 13:"),
    (40, "Step 14: Support safe outcomes", "Paso 14:"),
    (41, "Encourage safe choices like", "llamar a un paseo"),
    (42, "continues asking for another drink", "continúa pidiendo otra bebida"),
    (43, "Communication is critical when refusing", "comunicación es fundamental"),
    (44, "keep your tone calm and steady", "tono tranquilo y firme"),
    (45, "Use a calm tone by", "Utiliza un tono tranquilo"),
    (46, "clear and direct language", "lenguaje claro y directo"),
    (47, "Avoid blaming the customer", "Evita culpar al cliente"),
    (48, "Use “I” statements", "declaraciones en primera persona"),
    (49, "Examples include", "Algunos ejemplos de lo que puedes decir"),
    (50, "Listen without arguing", "Escucha sin discutir"),
    (51, "Do not match the customer’s emotions", "No te pongas a la altura de las emociones"),
    (52, "body language that supports de-escalation", "lenguaje corporal"),
    (53, "Use body language like", "lenguaje corporal como"),
    (54, "becomes upset after being refused service and raises their voice", "se enoja después de que se le rechaza el servicio y alza la voz"),
    (55, "Difficult or confrontational customers", "clientes difíciles o conflictivos"),
    (56, "do not take behavior personally", "no te tomes el comportamiento como algo personal"),
    (57, "Watch for warning signs like", "Debes estar atento a señales de advertencia"),
    (58, "Do not argue or try to prove a point", "No discutas ni intentes demostrar"),
    (59, "Set clear boundaries", "establece límites claros"),
    (60, "Avoid physical contact", "Evita el contacto físico"),
    (61, "Protect your safety by", "Proteja tu seguridad"),
    (62, "Involve management early when a customer becomes confrontational", "Involucra a la gerencia desde el principio"),
    (63, "refuses to leave or becomes disruptive, follow your establishment’s procedures", "se niega a irse o se vuelve problemático, sigue los procedimientos"),
    (64, "Keep other customers in mind", "Ten en cuenta a otros clientes"),
    (65, "Focus on control by", "Para tener el control debes"),
    (66, "becomes confrontational after being refused service and begins arguing loudly", "se vuelve conflictivo después de que se le rechaza el servicio"),
    (67, "Escalation procedures are used when", "procedimientos de escalada se utilizan"),
    (68, "involve management anytime you feel unsure", "involucrar a la gerencia cada vez que te sientas inseguro"),
    (69, "Escalate when you see", "Debes estar alerta cuando veas"),
    (70, "clear and simple communication when requesting help", "comunicación clara y sencilla al solicitar ayuda"),
    (71, "Stay aware of the customer while waiting for help", "mantenerte al tanto del cliente mientras esperas ayuda"),
    (72, "Follow your establishment’s specific escalation procedures at all times", "procedimientos de escalamiento específicos de tu establecimiento"),
    (73, "Your role during escalation includes", "Tu función durante la escalada"),
    (74, "Once management arrives, allow them to take the lead", "Una vez que llegue la gerencia"),
    (75, "Maintain a safe distance from the customer at all times", "distancia de seguridad con el cliente"),
    (76, "Avoid physical involvement unless you are trained", "Evita la participación física"),
    (77, "Focus on safety by", "Apoya la seguridad con"),
    (78, "loud, refuses to leave, and starts making threats", "se vuelve ruidoso, se niega a irse y comienza a amenazar"),
    (79, "Offering alternatives is an important part", "Ofrecer alternativas es una parte importante"),
    (80, "Alternatives do not replace refusal", "Las alternativas no son para reemplazar"),
    (81, "Offer safe options like", "Ofrece opciones seguras como"),
    (82, "Offering water is a simple and effective step", "Ofrecer agua es un paso sencillo"),
    (83, "Food can be offered if appropriate", "Se puede ofrecer comida"),
    (84, "Non-alcoholic beverages are another good option", "bebidas sin alcohol son otra buena opción"),
    (85, "When offering alternatives, use phrases like", "Cuando ofrezcas alternativas, utiliza frases como"),
    (86, "Transportation is one of the most important alternatives", "El transporte es una de las alternativas"),
    (87, "calling a ride service", "servicio de transporte"),
    (88, "Do not force alternatives on the customer", "No fuerces al cliente a aceptar alternativas"),
    (89, "Support safe outcomes by", "Para lograr resultados seguros"),
    (90, "refused alcohol due to intoxication. What is the best next step", "negado el consumo de alcohol por estar intoxicado"),
    (91, "Protecting yourself legally is a key part", "protegerte legalmente"),
    (92, "held responsible for illegal alcohol service", "responsable por el servicio ilegal de alcohol"),
    (93, "Protect yourself by", "Para protegerte, sigue estos consejos"),
    (94, "Always follow your establishment’s policies. These policies are designed to meet legal", "Sigue siempre las políticas de tu establecimiento. Estas políticas están diseñadas"),
    (95, "Documentation is important after certain incidents", "La documentación es importante"),
    (96, "When documenting, be accurate and objective", "Al documentar, debes ser preciso y objetivo"),
    (97, "Include details like", "En la documentación del hecho incluya detalles como"),
    (98, "Complete documentation as soon as possible", "Completa la documentación lo antes posible"),
    (99, "If law enforcement or management reviews", "Si las autoridades o la administración revisan"),
    (100, "Never falsify or change documentation", "Nunca falsifiques ni cambies la documentación"),
    (101, "Strong documentation habits include", "hábitos de documentación sólidos incluyen"),
    (102, "After refusing service to an intoxicated customer, what should you do to protect yourself legally", "Después de rechazar a dar el servicio a un cliente en estado de ebriedad"),
    (103, "slurred speech and poor balance", "habla con dificultad y tiene poco equilibrio"),
    (104, "becomes upset after being refused and raises their voice", "se molesta por rechazar a servirle y alza la voz"),
    (105, "just water", "solo agua"),
    (106, "refuses to leave after being denied service and begins bothering", "se niega a irse después de que se le rechazo"),
    (107, "quiet but unsteady", "callado pero inestable"),
    (108, "difficult refusal, what step helps protect you legally", "negativa difícil"),
]


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


def find_es(es_slides, es_sub, ctype, used):
    sub = es_sub.lower()
    hits = []
    for j, s in enumerate(es_slides):
        if j in used:
            continue
        if s["content_type"] != ctype:
            continue
        if sub in full(s).lower():
            hits.append(j)
    return hits


def reflow_order(slides):
    for i, slide in enumerate(slides):
        slide["order_index"] = i
        contents = slide.get("contents") or []
        for j, content in enumerate(contents):
            content["order_index"] = j if len(contents) > 1 else i


def build_map(en_slides, es_slides, markers):
    used = set()
    mapping = {}
    missing = []
    multi = []
    for en_i, en_sub, es_sub in markers:
        ctype = en_slides[en_i]["content_type"]
        if en_sub.lower() not in full(en_slides[en_i]).lower():
            missing.append((en_i, "EN_MISS", en_sub))
            continue
        hits = find_es(es_slides, es_sub, ctype, used)
        if not hits:
            missing.append((en_i, "NO_ES", es_sub))
            continue
        if len(hits) > 1:
            multi.append((en_i, hits, es_sub))
        mapping[en_i] = hits[0]
        used.add(hits[0])
    return mapping, used, missing, multi


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    es = json.loads(ES_PATH.read_text(encoding="utf-8"))
    en = json.loads(EN_PATH.read_text(encoding="utf-8"))
    es_sec = unit_section(es, 5)
    en_sec = unit_section(en, 5)
    en_slides = en_sec["slides"]
    es_slides = es_sec["slides"]
    assert len(en_slides) == len(es_slides) == 109
    by_i = {i: (i, a, b) for i, a, b in MARKERS}
    markers = [by_i[i] for i in range(109)]
    assert len(markers) == 109
    mapping, used, missing, multi = build_map(en_slides, es_slides, markers)
    orphans = sorted(set(range(109)) - used)
    unmapped = sorted(set(range(109)) - set(mapping))

    print(f"Mapped {len(mapping)}/109")
    print(f"Moved {sum(1 for i, j in mapping.items() if i != j)}")
    print(f"Missing {len(missing)} Multi {len(multi)}")
    print(f"Orphans {orphans}")
    print(f"Unmapped {unmapped}")

    if missing:
        print("\n=== MISSING ===")
        for row in missing:
            i = row[0]
            print(row)
            print(f"  EN[{i}]: {full(en_slides[i])[:140]}")

    if multi:
        print("\n=== MULTI-HIT (using first) ===")
        for row in multi:
            print(row)

    # Unique-type orphan pairing fallback
    if unmapped and orphans and len(unmapped) == len(orphans):
        print("\nAttempting unique leftover pairing...")
        for i in list(unmapped):
            ctype = en_slides[i]["content_type"]
            cands = [j for j in orphans if es_slides[j]["content_type"] == ctype]
            if len(cands) == 1:
                mapping[i] = cands[0]
                orphans.remove(cands[0])
                unmapped.remove(i)
                print(f"  paired EN[{i}] <- ES[{cands[0]}]")
                print(f"    EN: {full(en_slides[i])[:120]}")
                print(f"    ES: {full(es_slides[cands[0]])[:120]}")

    print(f"\nFinal mapped {len(mapping)}/109 orphans={orphans} unmapped={unmapped}")
    print("\n=== MOVES ===")
    for i in range(109):
        if i not in mapping:
            continue
        j = mapping[i]
        if i != j:
            print(f"EN[{i}] <- ES[{j}]")
            print(f"  EN: {full(en_slides[i])[:100]}")
            print(f"  ES: {full(es_slides[j])[:100]}")

    if len(mapping) != 109 or orphans or unmapped:
        print("\nREFUSING APPLY: map incomplete")
        if args.apply:
            raise SystemExit(2)
        return

    for i, j in mapping.items():
        if en_slides[i]["content_type"] != es_slides[j]["content_type"]:
            raise SystemExit(f"Type mismatch EN[{i}] vs ES[{j}]")

    if not args.apply:
        print("\nMap complete. Re-run with --apply to write.")
        return

    new_slides = [copy.deepcopy(es_slides[mapping[i]]) for i in range(109)]
    reflow_order(new_slides)
    es_sec["slides"] = new_slides
    ES_PATH.write_text(json.dumps(es, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # verify
    es2 = json.loads(ES_PATH.read_text(encoding="utf-8"))
    slides = unit_section(es2, 5)["slides"]
    assert len(slides) == 109
    assert all(s["order_index"] == i for i, s in enumerate(slides))
    assert all(slides[i]["content_type"] == en_slides[i]["content_type"] for i in range(109))
    print("\nWrote ES Unit 5 remapped to EN order.")
    for i in [1, 2, 5, 6, 9, 17, 18]:
        print(f"  [{i}] {full(slides[i])[:100]}")


if __name__ == "__main__":
    main()
