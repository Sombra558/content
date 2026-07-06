"""Safe editor for sc-content.en.json."""
import json, os

PATH = os.path.join("dist", "sc-content", "sc-content.en.json")


def load():
    with open(PATH, encoding="utf-8") as f:
        return json.load(f)


def save(data):
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)


def section(data, unit_number):
    return data["courses"][0]["sections"][unit_number - 1]["slides"]


def make_text(paragraphs, instruction="Read the following, then click Next."):
    return {
        "order_index": 0, "min_time": 3,
        "content_type": "Text", "content_type_unique_id": "text",
        "contents": [{"order_index": 0, "text": {"paragraphs": paragraphs, "instruction": instruction}}],
    }


def make_multiple(question, options, correct_index, correct_fb,
                  incorrect_fb="Incorrect.",
                  instruction="Read the scenario, then select the best answer."):
    ids = ["opt_a", "opt_b", "opt_c", "opt_d", "opt_e"]
    opts = [{"id": ids[i], "label": lbl, "is_correct": i == correct_index}
            for i, lbl in enumerate(options)]
    return {
        "order_index": 0, "min_time": 3,
        "content_type": "Multiple", "content_type_unique_id": "multiple",
        "contents": [{"order_index": 0, "interactive": {
            "question": question, "instruction": instruction, "options": opts,
            "feedback": {"correct": correct_fb, "incorrect": incorrect_fb}}}],
    }


def make_completion(structure, items, instruction="Click each item to learn more."):
    return {
        "order_index": 0, "min_time": 3,
        "content_type": "Completion", "content_type_unique_id": "completion",
        "contents": [{"order_index": 0,
                      "text": {"instruction": instruction},
                      "interactive": {"content_structure": [structure], "reveal_items": items}}],
    }


def make_image(asset_id, alt):
    return {"order_index": 1, "image": {"placeholder": True, "asset_id": asset_id,
                                        "alt": alt, "status": "pending"}}


def add_image_to_slide(slide, asset_id, alt):
    img = make_image(asset_id, alt)
    img["order_index"] = len(slide["contents"])
    slide["contents"].append(img)


def insert_after(slides, target_index, new_slides):
    for offset, s in enumerate(new_slides, start=1):
        slides.insert(target_index + offset, s)


def replace_paragraphs(slide, paragraphs):
    for block in slide["contents"]:
        if "text" in block and "paragraphs" in block["text"]:
            block["text"]["paragraphs"] = paragraphs
            return True
    return False


def reflow(slides):
    for i, s in enumerate(slides):
        s["order_index"] = i
        if s.get("contents"):
            s["contents"][0]["order_index"] = i


def find_first(slides, substring):
    sub = substring.lower()
    for i, s in enumerate(slides):
        if sub in json.dumps(s, ensure_ascii=False).lower():
            return i
    return -1
