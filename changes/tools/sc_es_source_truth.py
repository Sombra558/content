"""Make sc-content.es.json follow sc-content.en.json as source of truth.

What this script does:
1. Treat current English JSON as canonical ordering/structure.
2. Match existing Spanish slides to English slides using language-invariant
   anchors: statutes, money, percentages, acronyms, asset ids, and shape.
3. Drop clear ES-only slide types that no longer exist in EN.
4. Rebuild each ES unit in EN order from matched Spanish slides.
5. Fill any true EN-only gaps from small curated Spanish overrides.
6. Emit a Spanish audit-keyword map for grading.
"""

from __future__ import annotations

import copy
import json
import os
import re
from collections import defaultdict
from typing import Dict, List, Optional, Sequence, Tuple


ROOT = os.path.join("dist", "sc-content")
EN_PATH = os.path.join(ROOT, "sc-content.en.json")
ES_PATH = os.path.join(ROOT, "sc-content.es.json")
ES_KEYWORDS_PATH = os.path.join("changes", "tools", "sc_audit_es_keywords.json")

STATUTE = re.compile(r"\b\d{1,2}-\d{1,4}-\d{1,5}(?:\.\d+)?\b")
REGCITE = re.compile(r"\b7-\d{3}(?:\.\d+)?\b")
MONEY = re.compile(r"\$[\d,]+(?:\.\d+)?")
PERCENT = re.compile(r"\b\d+(?:\.\d+)?%")
ACRONYM = re.compile(
    r"\b(?:PBW|PO7|PLB|PLC|LOP|BAC|DUI|SLED|SCDOR|SCDPS|NHTSA|FARS|MYDORWAY|DOB)\b"
)
PLAIN_NUMBER = re.compile(r"\b\d{1,2},\d{3}\b|\b\d{2,4}\b")

EN_AUDIT_KEYWORDS = {
    "key laws: permitting/licensing": ["permit", "license"],
    "key laws: DUI": ["driving under the influence", "dui"],
    "key laws: concealed weapons": ["concealed weapon", "concealable weapon"],
    "physiological effects / BAC": ["blood alcohol concentration", "bac"],
    "factors affecting BAC": ["factors that affect", "affect bac", "factors affecting bac"],
    "drug interactions": ["prescription", "medication", "drug interaction"],
    "individual tolerance": ["tolerance"],
    "role refusing sale to minors": ["refuse", "under 21", "under twenty-one"],
    "life consequences to minors": ["scholarship", "criminal record", "life consequence"],
    "seek help / problem drinking": ["problem drinking", "seek help", "intervention"],
    "check ID procedure": ["check identification", "check id", "id-checking"],
    "fake/illegal ID": ["fake id", "fake identification", "false identification"],
    "ID anyone appearing underage": ["appears under", "appear underage", "regardless of perceived age"],
    "penalized for underage sale": ["prima facie", "$200", "misdemeanor"],
    "signs of intoxication": ["signs of intoxication", "visibly intoxicated"],
    "manager as resource": ["manager", "management"],
    "business/marketing/liability/standard drink": ["standard drink", "liquor liability", "responsible marketing"],
    "recent SC enforcement stats": ["413", "fatalities", "scdps", "fars"],
    "state laws + consequences (sale to minors/intox)": ["upon conviction", "fined between"],
    "server penalties for sale to minors": ["prima facie", "fined between $200"],
    "calc required DOB": ["minus 21", "subtract 21", "21 years"],
    "three valid ID forms": ["driver's license", "identification card", "passport"],
    "locate DOB on ID": ["date of birth", "dob"],
    "apply DOB comparison": ["compare", "required date of birth"],
    "vertical vs horizontal license": ["vertical", "horizontal"],
    "refusal techniques": ["refuse service", "refusal"],
    "escalation procedures": ["escalate", "escalation", "involve a manager"],
    "house policies / incident reporting": ["house policy", "house policies", "incident report"],
    "ongoing training / refreshers": ["refresher", "ongoing training", "recertif", "self-assessment"],
    "implied consent": ["implied consent"],
    "open container": ["open container"],
    "MYDORWAY certificate": ["mydorway"],
    "scholarship consequences": ["palmetto fellows", "sc hope", "sc life"],
    "liquor liability insurance": ["liquor liability", "$1 million", "insurance"],
    "drive-thru/curbside promo": ["drive-thru", "curb service", "7-202.5"],
}

ES_AUDIT_KEYWORDS = {
    "key laws: permitting/licensing": ["permiso", "permisos", "licencia", "licencias"],
    "key laws: DUI": ["bajo la influencia", "dui"],
    "key laws: concealed weapons": ["arma oculta", "armas ocultas", "concealable weapons"],
    "physiological effects / BAC": ["concentración de alcohol en sangre", "bac"],
    "factors affecting BAC": ["factores que afectan", "afectan el bac", "afectan la concentración"],
    "drug interactions": ["recetados", "medicamentos", "interacción con drogas", "venta libre"],
    "individual tolerance": ["tolerancia"],
    "role refusing sale to minors": ["rechace", "rechazar", "menor de 21", "menores de edad"],
    "life consequences to minors": ["beca", "becas", "antecedentes penales", "consecuencias"],
    "seek help / problem drinking": ["consumo problemático", "pedir ayuda", "intervención"],
    "check ID procedure": ["verificación de identidad", "verificar la identificación", "revisar la id"],
    "fake/illegal ID": ["identificación falsa", "identificación alterada", "identificación ilegal"],
    "ID anyone appearing underage": ["parezca menor", "edad aparente", "sin importar la edad aparente"],
    "penalized for underage sale": ["prima facie", "$200", "delito menor"],
    "signs of intoxication": ["señales de intoxicación", "visiblemente intoxicado"],
    "manager as resource": ["gerente", "gerencia", "administrador"],
    "business/marketing/liability/standard drink": ["bebida estándar", "responsabilidad por licor", "marketing responsable"],
    "recent SC enforcement stats": ["413", "muertes", "scdps", "fars"],
    "state laws + consequences (sale to minors/intox)": ["al ser condenado", "multa de entre"],
    "server penalties for sale to minors": ["prima facie", "multa de entre $200"],
    "calc required DOB": ["menos 21 años", "reste 21 años", "restarle 21 años"],
    "three valid ID forms": ["licencia de conducir", "tarjeta de identificación", "pasaporte"],
    "locate DOB on ID": ["fecha de nacimiento", "dob"],
    "apply DOB comparison": ["compare", "fecha de nacimiento requerida", "compárela"],
    "vertical vs horizontal license": ["vertical", "horizontal"],
    "refusal techniques": ["rechazar el servicio", "negativa", "negar otra bebida"],
    "escalation procedures": ["escalamiento", "escalar", "involucrar a un gerente"],
    "house policies / incident reporting": ["política del establecimiento", "políticas internas", "informe de incidente"],
    "ongoing training / refreshers": ["capacitación de repaso", "repasos", "autoevaluaciones", "módulos digitales"],
    "implied consent": ["consentimiento implícito"],
    "open container": ["contenedor abierto"],
    "MYDORWAY certificate": ["mydorway"],
    "scholarship consequences": ["palmetto fellows", "sc hope", "sc life"],
    "liquor liability insurance": ["responsabilidad por licor", "$1 millón", "seguro"],
    "drive-thru/curbside promo": ["drive-thru", "curb service", "7-202.5"],
}

TEXT_OVERRIDES = {
    "Quick rule: subtract 21 years from today's date; if the customer's birthdate is on or before that date, they are legal. If it's after, refuse the sale.": [
        "Regla rápida: reste 21 años a la fecha de hoy; si la fecha de nacimiento es igual o anterior, es legal. Si es posterior, niegue la venta."
    ],
    "If you suspect drug interaction, slow or stop alcohol service. Offer water or non-alcoholic options. Involve a manager if needed. Stay calm and professional. Your goal is to reduce risk and keep the situation safe.": [
        "Si sospecha una interacción con drogas, reduzca o suspenda el servicio de alcohol. Ofrezca agua u opciones sin alcohol. Involucre a un gerente si es necesario. Mantenga la calma y actúe con profesionalismo. Su objetivo es reducir el riesgo y mantener la situación segura."
    ],
    "Refusing underage sales supports a safer environment. It helps prevent harm and reduces risk in your community. Your actions make a difference in real situations. Taking your role seriously helps protect others and reinforces responsible alcohol service standards.": [
        "Rechazar las ventas a menores de edad contribuye a un entorno más seguro. Ayuda a prevenir daños y reduce el riesgo en tu comunidad. Tus acciones marcan la diferencia en situaciones reales. Tomar en serio tu papel ayuda a proteger a los demás y refuerza los estándares responsables del servicio de alcohol."
    ],
}

IMAGE_ALT_OVERRIDES = {
    "sc-img-standard-drink": "Gráfico de equivalentes de bebida estándar: cerveza de 12 oz, vino de 5 oz y destilado de 1.5 oz.",
    "sc-img-bac-chart": "Gráfico que relaciona la cantidad de bebidas estándar y el peso corporal con la concentración estimada de alcohol en sangre.",
    "sc-img-id-anatomy": "Diagrama de una licencia de conducir de Carolina del Sur con el campo de fecha de nacimiento resaltado.",
    "sc-img-vertical-vs-horizontal": "Comparación lado a lado entre una licencia vertical de menor de 21 años y una licencia horizontal para mayores de 21 años en Carolina del Sur.",
    "sc-img-dob-math": "Visual que muestra la fecha de hoy menos 21 años para encontrar la fecha de nacimiento requerida.",
    "sc-img-idcheck-steps": "Secuencia de cinco pasos para revisar una ID: tocar la tarjeta, revisar medidas de seguridad, revisar fecha de nacimiento, comparar foto y descripción, decidir.",
    "sc-img-intoxication-signs": "Cuadrícula de señales comunes de intoxicación agrupadas por habla, coordinación, juicio y apariencia.",
}


def load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def slide_text(slide: dict) -> str:
    parts: List[str] = []

    def walk(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key in {"content_type", "content_type_unique_id", "asset_id", "id", "status", "preview_url"}:
                    continue
                walk(value)
        elif isinstance(obj, list):
            for value in obj:
                walk(value)
        elif isinstance(obj, str):
            parts.append(obj)

    walk(slide)
    return " ".join(parts)


def primary_paragraph(slide: dict) -> Optional[str]:
    for content in slide.get("contents", []):
        text = content.get("text") or {}
        paragraphs = text.get("paragraphs")
        if paragraphs:
            return paragraphs[0]
    return None


def slide_shape(slide: dict) -> Tuple[str, int, int, int, int]:
    content_type = slide.get("content_type_unique_id", "")
    option_count = reveal_count = image_count = 0
    has_preview = 1 if slide.get("preview_url") else 0
    for content in slide.get("contents", []):
        interactive = content.get("interactive") or {}
        option_count += len(interactive.get("options", []))
        reveal_count += len(interactive.get("reveal_items", []))
        if "image" in content:
            image_count += 1
    return content_type, option_count, reveal_count, image_count, has_preview


def fingerprint(slide: dict) -> set[str]:
    text = slide_text(slide)
    tokens: set[str] = set()
    tokens.update("S:" + match for match in STATUTE.findall(text))
    tokens.update("R:" + match for match in REGCITE.findall(text))
    tokens.update("$:" + match for match in MONEY.findall(text))
    tokens.update("%:" + match for match in PERCENT.findall(text))
    tokens.update("A:" + match for match in ACRONYM.findall(text))
    tokens.update("N:" + match for match in PLAIN_NUMBER.findall(text))
    for content in slide.get("contents", []):
        if "image" in content:
            tokens.add("IMG:" + content["image"].get("asset_id", ""))
    return tokens


def jaccard(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 0.0
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def compatible_shapes(en_slide: dict, es_slide: dict) -> bool:
    en_shape = slide_shape(en_slide)
    es_shape = slide_shape(es_slide)
    if en_shape[0] != es_shape[0]:
        return False
    if en_shape[1] != es_shape[1]:
        return False
    if en_shape[2] != es_shape[2]:
        return False
    if en_shape[3] != es_shape[3]:
        return False
    return True


def match_es_slides(en_slides: Sequence[dict], es_slides: Sequence[dict]) -> Dict[int, int]:
    """Reuse diff-time matching that proved existing ES content mostly aligned."""
    matches: Dict[int, int] = {}
    used_es: set[int] = set()

    # Pass 1: strongest language-invariant anchors first.
    candidates: List[Tuple[float, int, int]] = []
    for en_idx, en_slide in enumerate(en_slides):
        en_fp = fingerprint(en_slide)
        for es_idx, es_slide in enumerate(es_slides):
            if slide_shape(en_slide)[0] != slide_shape(es_slide)[0]:
                continue
            score = jaccard(en_fp, fingerprint(es_slide))
            if score >= 0.50:
                bonus = 0.05 if compatible_shapes(en_slide, es_slide) else 0.0
                candidates.append((score + bonus, en_idx, es_idx))
    for score, en_idx, es_idx in sorted(candidates, reverse=True):
        if en_idx in matches or es_idx in used_es:
            continue
        matches[en_idx] = es_idx
        used_es.add(es_idx)

    # Pass 2: leftover slides align by full shape and relative order.
    left_en = [idx for idx in range(len(en_slides)) if idx not in matches]
    left_es = [idx for idx in range(len(es_slides)) if idx not in used_es]
    by_shape_en: Dict[Tuple[str, int, int, int, int], List[int]] = defaultdict(list)
    by_shape_es: Dict[Tuple[str, int, int, int, int], List[int]] = defaultdict(list)
    for idx in left_en:
        by_shape_en[slide_shape(en_slides[idx])].append(idx)
    for idx in left_es:
        by_shape_es[slide_shape(es_slides[idx])].append(idx)
    for shape_key, en_indexes in by_shape_en.items():
        for en_idx, es_idx in zip(en_indexes, by_shape_es.get(shape_key, [])):
            matches[en_idx] = es_idx
            used_es.add(es_idx)

    # Pass 3: same-index fallback for no-signal text slides.
    for en_idx in range(len(en_slides)):
        if en_idx in matches or en_idx >= len(es_slides):
            continue
        es_idx = en_idx
        if es_idx in used_es:
            continue
        if slide_shape(en_slides[en_idx])[0] != slide_shape(es_slides[es_idx])[0]:
            continue
        matches[en_idx] = es_idx
        used_es.add(es_idx)

    return matches


def drop_es_only_slide_types(en_slides: Sequence[dict], es_slides: Sequence[dict]) -> Tuple[List[dict], List[int]]:
    allowed_types = {slide.get("content_type_unique_id") for slide in en_slides}
    kept: List[dict] = []
    dropped_indexes: List[int] = []
    for idx, slide in enumerate(es_slides):
        if slide.get("content_type_unique_id") not in allowed_types:
            dropped_indexes.append(idx)
        else:
            kept.append(copy.deepcopy(slide))
    return kept, dropped_indexes


def translate_slide_from_override(en_slide: dict, overrides: Dict[str, dict | List[str]]) -> Optional[dict]:
    paragraph = primary_paragraph(en_slide)
    if not paragraph:
        return None
    override = overrides.get(paragraph)
    if not override:
        return None
    translated = copy.deepcopy(en_slide)
    if isinstance(override, list):
        translated["contents"][0]["text"]["paragraphs"] = override
    else:
        text_block = translated["contents"][0]["text"]
        for key, value in override.items():
            text_block[key] = value
    return translated


def reflow_slides(slides: Sequence[dict]) -> List[dict]:
    flowed = copy.deepcopy(list(slides))
    for slide_idx, slide in enumerate(flowed):
        slide["order_index"] = slide_idx
        for content_idx, content in enumerate(slide.get("contents", [])):
            if "image" in content:
                content["order_index"] = content_idx
            else:
                content["order_index"] = slide_idx if content_idx == 0 else content_idx
    return flowed


def sync_image_blocks(en_slide: dict, es_slide: dict) -> dict:
    synced = copy.deepcopy(es_slide)
    existing_assets = {
        content["image"]["asset_id"]
        for content in synced.get("contents", [])
        if "image" in content
    }
    for content in en_slide.get("contents", []):
        if "image" not in content:
            continue
        asset_id = content["image"].get("asset_id")
        if asset_id in existing_assets:
            continue
        image_content = copy.deepcopy(content)
        if asset_id in IMAGE_ALT_OVERRIDES:
            image_content["image"]["alt"] = IMAGE_ALT_OVERRIDES[asset_id]
        synced.setdefault("contents", []).append(image_content)
        existing_assets.add(asset_id)
    return synced


def reconcile_unit(
    en_slides: Sequence[dict],
    es_slides: Sequence[dict],
    overrides: Dict[str, dict | List[str]],
) -> Tuple[List[dict], List[int], List[int]]:
    filtered_es, orphan_indexes = drop_es_only_slide_types(en_slides, es_slides)
    matches = match_es_slides(en_slides, filtered_es)

    rebuilt: List[dict] = []
    missing_en_indexes: List[int] = []
    used_es = set(matches.values())
    orphan_indexes.extend(
        idx for idx in range(len(filtered_es)) if idx not in used_es
    )

    for en_idx, en_slide in enumerate(en_slides):
        es_idx = matches.get(en_idx)
        if es_idx is not None:
            rebuilt.append(sync_image_blocks(en_slide, filtered_es[es_idx]))
            continue
        translated = translate_slide_from_override(en_slide, overrides)
        if translated is not None:
            rebuilt.append(translated)
            continue
        missing_en_indexes.append(en_idx)

    return reflow_slides(rebuilt), sorted(orphan_indexes), missing_en_indexes


def build_es_keyword_map(rubric: Dict[str, List[str]]) -> Dict[str, List[str]]:
    return {key: list(ES_AUDIT_KEYWORDS[key]) for key in rubric}


def sync_es_to_en_source_truth() -> dict:
    en = load_json(EN_PATH)
    es = load_json(ES_PATH)
    summary = {"units": [], "missing_translations": 0, "orphan_es_slides": 0}

    for unit_idx, (en_section, es_section) in enumerate(
        zip(en["courses"][0]["sections"], es["courses"][0]["sections"]),
        start=1,
    ):
        rebuilt, orphans, missing = reconcile_unit(
            en_section["slides"],
            es_section["slides"],
            TEXT_OVERRIDES,
        )
        es["courses"][0]["sections"][unit_idx - 1]["slides"] = rebuilt
        summary["units"].append(
            {
                "unit": unit_idx,
                "title": en_section["title"],
                "slides": len(rebuilt),
                "orphans_removed": len(orphans),
                "missing_translations": missing,
            }
        )
        summary["missing_translations"] += len(missing)
        summary["orphan_es_slides"] += len(orphans)

    save_json(ES_PATH, es)
    save_json(ES_KEYWORDS_PATH, build_es_keyword_map(EN_AUDIT_KEYWORDS))
    return summary


def main() -> None:
    summary = sync_es_to_en_source_truth()
    print("Synced ES JSON to EN source of truth.")
    for unit in summary["units"]:
        print(
            f"Unit {unit['unit']}: {unit['slides']} slides | "
            f"removed {unit['orphans_removed']} ES-only | "
            f"missing EN translations {len(unit['missing_translations'])}"
        )
    print(f"Total ES-only slides removed: {summary['orphan_es_slides']}")
    print(f"Total missing translations: {summary['missing_translations']}")
    print(f"Spanish audit keyword map: {ES_KEYWORDS_PATH}")


if __name__ == "__main__":
    main()
