"""Report: align Unit 2 ES to EN (EN source of truth)."""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

es = json.loads(Path(r"d:\GetLicensed\content\dist\sc-content\sc-content.es.json").read_text(encoding="utf-8"))
en = json.loads(Path(r"d:\GetLicensed\content\dist\sc-content\sc-content.en.json").read_text(encoding="utf-8"))


def unit_slides(data, n):
    return next(s for c in data["courses"] for s in c["sections"] if s.get("order_index") == n)["slides"]


def full(slide):
    c0 = slide["contents"][0]
    text = c0.get("text") or {}
    inter = c0.get("interactive") or {}
    bits = []
    bits += text.get("paragraphs") or []
    bits += text.get("bullet_points") or []
    if text.get("body"):
        bits.append(text["body"])
    if inter.get("question"):
        bits.append(inter["question"])
    if inter.get("content_structure"):
        bits += inter["content_structure"]
    if inter.get("reveal_items"):
        for it in inter["reveal_items"]:
            bits.append(f"{it.get('title', '')}: {it.get('revealed_text', '')}")
    return " ".join(bits)


def brief(slide, n=120):
    return f"{slide['content_type']}| {full(slide).replace(chr(10), ' ')[:n]}"


TOPICS = [
    ("intro", [r"2a\.", r"in this unit"], [r"2a\.", r"en esta unidad"]),
    ("cns_completion", [r"central nervous system", r"alcohol is a \{\{item_1\}\}"], [r"sistema nervioso", r"el alcohol es un \{\{item_1\}\}"]),
    ("enters_blood", [r"enters the bloodstream", r"does not need to be digested"], [r"corriente sangu", r"entra en la sangre", r"no necesita digerirse"]),
    ("path_completion", [r"predictable path", r"first, it is \{\{item_1\}\}"], [r"camino predecible", r"ruta predecible"]),
    ("liver_one_drink", [r"liver processes", r"one standard drink per hour"], [r"h[ií]gado procesa", r"una bebida est[aá]ndar por hora"]),
    ("bac_rises_impairment", [r"blood alcohol concentration \(bac\) measures the amount", r"as bac rises, impairment"], [r"concentraci[oó]n de alcohol en sangre \(bac\) mide", r"a medida que aumenta el bac"]),
    ("bac_factors_completion", [r"several factors change how quickly alcohol raises", r"body weight"], [r"varios factores cambian", r"peso corporal"]),
    ("drugs_dangerous", [r"interacts dangerously", r"sedatives, opioids"], [r"interact[uú]a de forma peligrosa", r"sedantes, opioides"]),
    ("tolerance_mask", [r"tolerance means a regular heavy drinker", r"does not make a person safe to drive"], [r"la tolerancia significa", r"no vuelve segura", r"no hace que.*seguro"]),
    ("legal_008", [r"0\.08%", r"inferred to be under the influence"], [r"0\.08%", r"bajo la influencia"]),
    ("quiz_three_drinks_different", [r"two guests each had three drinks", r"far more impaired"], [r"dos clientes tomaron tres", r"mucho m[aá]s incapacitado", r"dos invitados"]),
    ("brain_stages_completion", [r"affects the brain in stages", r"early signs include"], [r"afecta el cerebro en etapas", r"primeros signos"]),
    ("individual_factors", [r"not everyone reacts to alcohol the same way", r"body size, gender"], [r"no todo el mundo reacciona", r"tama[nñ]o corporal"]),
    ("intox_speed_completion", [r"factors affect intoxication speed", r"drinking on an \{\{item_1\}\}"], [r"factores afectan la velocidad", r"beber con un \{\{item_1\}\}"]),
    ("coordination_decisions", [r"impacts coordination and decision-making", r"reaction time slows"], [r"afecta la coordinaci[oó]n", r"toma de decisiones"]),
    ("behavior_changes", [r"behavior may change", r"louder or more emotional"], [r"comportamiento puede cambiar", r"m[aá]s ruidosos"]),
    ("physical_signs_completion", [r"common physical signs include"], [r"signos f[ií]sicos comunes"]),
    ("quiz_several_drinks_quickly", [r"orders several drinks quickly", r"slower speech and unsteady"], [r"varias bebidas r[aá]pidamente", r"movimiento inestable"]),
    ("bac_definition", [r"measures how much alcohol is in a person", r"shown as a percentage"], [r"mide.*alcohol.*sangre", r"porcentaje"]),
    ("bac_rises_faster", [r"bac rises when alcohol enters", r"liver removes alcohol"], [r"el bac aumenta cuando", r"h[ií]gado elimina"]),
    ("bac_key_factors_completion", [r"bac is affected by several key factors"], [r"el bac se ve afectado por varios"]),
    ("standard_drink_def", [r"a standard drink is a way to measure"], [r"bebida est[aá]ndar es una forma"]),
    ("drinks_not_equal", [r"not all drinks are equal", r"large pour or strong mix"], [r"no todas las bebidas", r"vertido grande|mezcla fuerte"]),
    ("standard_examples_completion", [r"common standard drink examples"], [r"ejemplos.*bebida est[aá]ndar"]),
    ("time_only_lowers_bac", [r"time is the only factor that lowers bac"], [r"tiempo.*reduce el bac|s[oó]lo el tiempo"]),
    ("judgment_declines", [r"judgment and coordination decline"], [r"juicio y la coordinaci[oó]n"]),
    ("higher_bac_completion", [r"higher bac levels lead"], [r"niveles m[aá]s altos de bac"]),
    ("tracking_drinks", [r"tracking drinks helps you estimate"], [r"seguimiento de las bebidas"]),
    ("servers_prevent_overservice", [r"preventing over-service"], [r"exceso de servicio"]),
    ("quiz_two_strong_mixed", [r"two strong mixed drinks", r"faster speech and reduced coordination"], [r"dos c[oó]cteles fuertes", r"habla m[aá]s r[aá]pida"]),
    ("bac_more_than_amount", [r"bac is affected by more than just how much"], [r"bac se ve afectado por m[aá]s"]),
    ("body_weight_role", [r"body weight plays a major role"], [r"peso corporal juega|peso corporal desempe"]),
    ("personal_factors_completion", [r"several personal factors affect bac"], [r"factores personales afectan"]),
    ("food_slows_absorption", [r"food in the stomach slows", r"empty stomach allows"], [r"comida en el est[oó]mago", r"est[oó]mago vac[ií]o"]),
    ("rate_of_drinking", [r"rate of drinking is one of the biggest"], [r"tasa de consumo de alcohol"]),
    ("drinking_patterns_completion", [r"drinking patterns strongly affect bac"], [r"patrones de consumo de alcohol afectan"]),
    ("tolerance_response", [r"tolerance refers to how a person responds"], [r"la tolerancia se refiere"]),
    ("tolerance_misleading_completion", [r"tolerance can be misleading"], [r"la tolerancia puede ser enga"]),
    ("environmental_factors", [r"environmental factors can also influence", r"heat, fatigue, and stress"], [r"factores ambientales", r"calor, la fatiga"]),
    ("understanding_bac_decisions", [r"understanding bac factors helps you make better"], [r"comprender los factores bac"]),
    ("quiz_not_eaten", [r"have not eaten all day", r"after two drinks"], [r"no ha comido en todo el d", r"despu[eé]s de dos"]),
    ("elimination_process", [r"alcohol elimination is the process"], [r"eliminaci[oó]n del alcohol es el proceso|eliminaci[oó]n.*proceso"]),
    ("one_drink_per_hour", [r"eliminates about one standard drink per hour"], [r"elimina.*bebida est[aá]ndar por hora"]),
    ("elimination_paths_completion", [r"alcohol leaves the body through a slow process"], [r"el alcohol sale del cuerpo"]),
    ("sobering_myths_intro", [r"certain actions can reduce intoxication quickly", r"common myths"], [r"ciertas acciones pueden reducir", r"mitos comunes"]),
    ("coffee_myth", [r"coffee is a common example", r"does not remove alcohol"], [r"caf[eé] es un ejemplo", r"no elimina el alcohol"]),
    ("myths_completion", [r"common myths about sobering up include"], [r"mitos comunes sobre"]),
    ("food_once_in_blood", [r"food can slow alcohol absorption if eaten", r"once alcohol is in the bloodstream"], [r"alimentos pueden retardar", r"una vez que el alcohol"]),
    ("fresh_air_myth", [r"fresh air may help", r"does not reduce bac"], [r"aire fresco", r"no reduce el bac"]),
    ("false_beliefs_completion", [r"false beliefs can lead to unsafe"], [r"falsas creencias"]),
    ("act_on_facts_not_myths", [r"act based on facts, not myths"], [r"actuar.*hechos", r"no en mitos"]),
    ("understanding_elimination_decisions", [r"understanding elimination helps you make safer"], [r"comprender la eliminaci"]),
    ("quiz_coffee_sobers", [r"orders coffee", r"sobers them up|fine to (continue|keep) drinking"], [r"pide caf[eé]", r"sobriedad|seguir bebiendo"]),
    ("drugs_many_types", [r"alcohol can interact with many types of drugs"], [r"interactuar con muchos tipos de drogas"]),
    ("drugs_increase_quickly", [r"drug interactions can increase intoxication quickly"], [r"interacciones medicamentosas pueden aumentar"]),
    ("drug_types_completion", [r"interact with different drug types", r"increase drowsiness"], [r"diferentes tipos de drogas", r"aumentar la somnolencia"]),
    ("rx_warn_against", [r"prescription medications warn against alcohol"], [r"medicamentos recetados advierten"]),
    ("otc_cold_antihistamine", [r"over-the-counter medications can also", r"cold medicines and antihistamines"], [r"venta libre tambi", r"resfriado y los antihistam"]),
    ("otc_risks_completion", [r"common otc risks include"], [r"riesgos otc comunes"]),
    ("illegal_drugs_combo", [r"illegal drugs can create dangerous combinations"], [r"drogas ilegales pueden crear"]),
    ("stimulants_risky", [r"mixing alcohol with stimulants"], [r"mezclar alcohol con estimulantes"]),
    ("drug_types_effects_completion", [r"different substances create different risks"], [r"diferentes sustancias crean"]),
    ("injury_illness_risk", [r"increase the chance of injury or illness"], [r"posibilidades de sufrir lesiones"]),
    ("suspect_drug_action", [r"if you suspect drug interaction", r"slow or stop alcohol service"], [r"si sospechas una interacci", r"reduce.*o suspende"]),
    ("quiz_meds_drowsy", [r"taking medication earlier", r"strong drowsiness"], [r"tomar medicaci", r"somnolencia"]),
    ("quiz_strong_mixed_judgment", [r"strong mixed drinks in a row|several strong mixed", r"judgment"], [r"bebidas fuertes mezcladas", r"juicio"]),
    ("quiz_feel_fine_slurred", [r"feel fine", r"slurred speech and unsteady walking"], [r"se siente bien", r"caminar inestable|dificultad para hablar"]),
]


def detect(slide, lang):
    t = full(slide).lower()
    hits = []
    for tid, en_pats, es_pats in TOPICS:
        pats = en_pats if lang == "en" else es_pats
        if any(re.search(p, t) for p in pats):
            hits.append(tid)
    return hits


en2, es2 = unit_slides(en, 2), unit_slides(es, 2)

en_topics = []
for i, s in enumerate(en2):
    hits = detect(s, "en")
    en_topics.append(hits[0] if hits else f"UNKNOWN_{s['content_type']}_{i}")

es_topics = []
for i, s in enumerate(es2):
    hits = detect(s, "es")
    es_topics.append(hits[0] if hits else f"UNKNOWN_{s['content_type']}_{i}")

es_used = set()
plan = []
for i, topic in enumerate(en_topics):
    match = None
    if not topic.startswith("UNKNOWN"):
        for j, et in enumerate(es_topics):
            if j in es_used:
                continue
            if et == topic:
                match = j
                break
    if match is not None:
        es_used.add(match)
        status = "SAME_INDEX" if match == i else "REORDER"
        plan.append((i, match, topic, status))
    else:
        plan.append((i, None, topic, "MISSING_IN_ES"))

print(f"EN={len(en2)} ES={len(es2)}\n")
print("| New idx | EN idx | ES source idx | Topic | Action |")
print("|--------:|-------:|--------------:|-------|--------|")
for new_i, (en_i, es_j, topic, status) in enumerate(plan):
    es_cell = "-" if es_j is None else str(es_j)
    print(f"| {new_i} | {en_i} | {es_cell} | `{topic}` | {status} |")

missing = [p for p in plan if p[3] == "MISSING_IN_ES"]
orphans = [j for j in range(len(es2)) if j not in es_used]
moves = [p for p in plan if p[3] == "REORDER"]
sames = [p for p in plan if p[3] == "SAME_INDEX"]

print("\n## Counts")
print(f"- Same index already: {len(sames)}")
print(f"- Reorder (exists in ES, wrong place): {len(moves)}")
print(f"- Missing in ES: {len(missing)}")
print(f"- ES orphans (no EN topic): {len(orphans)} -> {orphans}")

print("\n## Why EN has 1 more slide")
print(f"EN count {len(en2)} vs ES count {len(es2)} (delta {len(en2)-len(es2)}).")
if missing:
    print("\nEN slides with no ES counterpart:")
    for en_i, es_j, topic, status in missing:
        print(f"\n### EN[{en_i}] topic=`{topic}` type={en2[en_i]['content_type']}")
        print(full(en2[en_i])[:700])
        print("\nNeighbors:")
        for k in range(max(0, en_i - 2), min(len(en2), en_i + 3)):
            mark = ">>>" if k == en_i else "   "
            print(f"{mark} EN[{k}] `{en_topics[k]}` | {brief(en2[k], 100)}")
        print("\nES around same index:")
        for k in range(max(0, en_i - 2), min(len(es2), en_i + 3)):
            print(f"    ES[{k}] `{es_topics[k]}` | {brief(es2[k], 100)}")

print("\n## ES orphans detail")
for j in orphans:
    print(f"\n### ES[{j}] topic=`{es_topics[j]}` type={es2[j]['content_type']}")
    print(full(es2[j])[:700])

print("\n## UNKNOWN detections")
for i, t in enumerate(en_topics):
    if t.startswith("UNKNOWN"):
        print(f"EN[{i}] {brief(en2[i], 140)}")
for i, t in enumerate(es_topics):
    if t.startswith("UNKNOWN"):
        print(f"ES[{i}] {brief(es2[i], 140)}")

print("\n## Proposed implementation steps")
print("1. Rebuild ES Unit 2 slide array to length 67, following EN order.")
print("2. For each EN slide: place matched ES translation at the same index (reuse existing Spanish text).")
print("3. For EN-only slide(s): add a new Spanish translation of that EN content.")
print("4. Drop ES orphan slides that have no EN counterpart (or merge unique sentences into a neighbor if needed).")
print("5. Reflow order_index; leave EN unchanged.")
