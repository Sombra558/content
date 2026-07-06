# SC Alcohol Course — "Well Covered" Upgrade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Raise every outcome in the SC DBHDD Curriculum Evaluation Tool to "Well Covered" by editing/inserting slides in `dist/sc-content/sc-content.en.json`, anchoring content in the SCDOR Legal Supplement statutes and verified SC enforcement statistics, and adding targeted image placeholders.

**Architecture:** All content lives in one JSON file: `courses[0].sections[0..6].slides[]`. Each slide is `{order_index, min_time, content_type, content_type_unique_id, contents[]}`. Edits are performed by a Python helper (`changes/tools/sc_edit.py`) that loads the JSON, applies typed insert/replace operations, reflows `order_index` per section, and writes back with `ensure_ascii=False, indent=1`. A validation script proves JSON parses and that every rubric row maps to slide text. No manual hand-editing of the 17k-line file.

**Tech Stack:** Python 3.11 (stdlib `json` only), existing `dist/index.html` QA viewer.

---

## Source Facts (verified — use verbatim where quoted)

**SCDOR Legal Supplement (Effective September 1, 2025) — statutes & penalties:**

- **Authority:** SC Code § 61-3-120(B) requires this training content.
- **Sale to underage (under 21):** misdemeanor. 1st offense: fined $200–$300 or ≤30 days jail, or both. 2nd+: $400–$500 or ≤30 days, or both. "Failure of a person to require identification to verify a person's age is prima facie evidence of the violation." Statutes: § 61-4-50, § 61-6-4080, Reg. 7-200.4.
- **Posting signs (underage):** retail seller must post a sign reading: *"The possession of beer, wine, or alcoholic liquors, by a person under twenty-one years of age is a criminal offense under the laws of this State, and it is also unlawful for a person to knowingly give false information concerning his age for the purpose of purchasing beer, wine, or liquor."* Failure to display: misdemeanor, ≤$100 or ≤30 days. Statutes: § 61-4-70, § 61-6-1530.
- **Transfer to underage person:** unlawful to purchase for/transfer/give to under-21 for consumption (exception: law-enforcement compliance checks). Penalties same tiers as sale. Statutes: § 61-4-90, § 61-6-4070, § 61-6-4075.
- **Discount pricing (on-premises):** may not advertise/sell/dispense for free, at less than ½ regular price, or 2-for-1. Violation: misdemeanor, ≥$100 or ≥3 months. Statutes: § 61-4-160, § 61-6-4550.
- **Unlawful sales (licensee):** can't sell beer/wine at wholesale/retail, or sell while license revoked/canceled/suspended. Violation: $20–$100 or 10–30 days, or both. Statute: § 61-4-610.
- **Legal employment/serving age:** servers 18–20 may serve alcohol in open containers on-premises only if it was mixed/poured/prepared by an employee ≥21. Servers under 21 may not mix/pour/prepare. Bartenders must be ≥21 when hired. Statutes: § 61-4-90(D), § 61-6-2200, § 61-6-4070, § 61-6-4140.
- **Prohibited acts (incl. sales to intoxicated):** permit holder/servant/agent may not knowingly: sell to under 21; sell to an intoxicated person; permit lewd/immoral entertainment; permit public nuisance/crime; sell prohibited beverages; run a "drinking contest"/"drinking game"; permit gambling (game-promotion exception). Permit-holder penalties: 1st offense $2,500 fined by SCDOR; 2nd within 2 yrs — suspend permit up to 14 days; 3rd within 3 yrs — permit revoked. Statutes: § 61-4-580, § 61-6-1830, § 61-6-2220, § 61-6-2230.
- **Drive-in/drive-thru prohibited:** may not sell/deliver beer or wine to anyone who remains in a motor vehicle during the transaction (bans curb service). Statute: Reg. 7-202.5.
- **Permit types (on-premises consumption):**
  - **PBW** — On-Premises Beer & Wine Permit: beer/wine on-premises + to-go, 6 days/week, 24 hrs/day (Sundays only if county approves Local Option).
  - **PO7** — 7-Day On-Premises Beer & Wine: 7 days/week except Sundays 2–10 a.m.; only in counties that approved Sunday sales referendum.
  - **PLB** — Business (Restaurant & Hotel) Liquor by the Drink: liquor by the drink on-premises for meal/lodging businesses; Mon–Sat 10 a.m.–2 a.m.
  - **PLC** — Nonprofit (Private Club) Liquor by the Drink: valid nonprofits, 7 days/week 10 a.m.–2 a.m.
  - **LOP** — Local Option Permit: liquor by the drink Sundays (12–2 a.m. and 10 a.m.–11:59 p.m.) for businesses already holding a PLB; only in counties approving Sunday liquor sales. Statutes: § 61-4-120, § 61-4-510, § 61-4-630, § 61-6-1600, § 61-6-1610.
  - **Display of permits/licenses:** must be displayed in a clearly visible place. Reg. 7-200.3.
- **Operating without permit:** misdemeanor $10–$100 or 10–30 days; each day is a separate offense; alcohol is contraband, seized by SLED. Statutes: § 61-4-150, § 61-4-560, § 61-6-2600, § 61-6-2610.
- **DUI (Operating under influence):** "faculties to drive are materially and appreciably impaired." BAC 0.08%+ = inferred DUI; 0.05–0.08% considered with other evidence. Penalties: 1st: ≤$400 ($992 w/ assessments) and 48 hrs–30 days, license suspended 6 months. 2nd: $2,100–$5,100 ($10,744.50), 5 days–1 yr, license 1 yr. 3rd: $3,800–$6,300 ($13,234.50), 60 days–3 yrs, license 2 yrs (4 yrs if within 5 yrs of 1st; vehicle confiscated if within 10 yrs and offender is owner/household). 4th: 1–5 yrs prison + permanent license revocation. Statutes: § 56-5-2930, -2940, -2950, -2990, -6240.
- **Unlawful alcohol concentration:** driving with BAC 0.08%+, same penalties as DUI. § 56-5-2933, -2940.
- **Felony DUI:** great bodily injury — mandatory $5,100–$10,100 ($21,119.50) + 30 days–15 yrs; death — mandatory $10,100–$25,100 ($52,244.50) + 1–25 yrs. § 56-5-2945.
- **Implied consent:** driving in SC = consent to breath/blood/urine test. Refusal: automatic 90-day suspension (180 days if prior alcohol conviction/suspension within 10 yrs). § 56-5-2950, -2951.
- **Open container:** no open container of beer/wine/liquor in a moving vehicle except luggage compartment. ≤$100 or ≤30 days. § 61-4-110, § 61-6-4020.
- **Liquor liability insurance:** businesses open after 5 p.m. selling for on-premises must carry ≥$1 million aggregate liquor liability coverage (per-occurrence ≥50% of aggregate). Risk-mitigation reductions: stop serving at midnight (−$250,000); all servers complete SC Alcohol Server Certificate within 60 days of employment (−$100,000); <40% of sales from alcohol (−$100,000); forensic digital ID system midnight–4 a.m. (−$100,000); 501(c)(3) nonprofit (−$500,000); single special-event permit (−$500,000). Minimum floor $300,000. Statute: § 61-2-145.
- **Liability & damages (dram-shop/apportionment):** a business is no longer liable for more than 50% of damages from DUI incidents; defendant may apportion shared responsibility to others if a jury agrees. Statutes: § 15-38-15, -20, -30, -40, § 61-2-147.
- **Concealed weapons in alcohol businesses:** may not enter a business selling alcohol for on-premises consumption with a firearm AND consume alcohol. Violation: misdemeanor ≤$2,000 or ≤2 yrs, or both; CWP revoked 5 yrs. Business may post "NO CONCEALABLE WEAPONS ALLOWED"; refusal to comply: ≤$200 or ≤30 days; subsequent — CWP revoked 1 yr. Statutes: § 16-23-465, § 23-31-220.
- **Scholarship consequences:** 2nd+ alcohol violation — ineligible for Palmetto Fellows (1 yr), SC HOPE (next academic year), SC LIFE (following fall/spring/summer). Statutes: § 59-104-20, § 61-4-100, § 61-6-4085, Reg. 62-900.95.

**Verified SC statistics (cite source + year in slide text):**

- 2023: **413** alcohol-impaired-driving fatalities (BAC 0.08%+), = **39%** of all drivers in fatal collisions (NHTSA FARS 2023 data; SCDPS).
- 2023: **5,319** alcohol/drug-involved collisions; **367** killed; **3,372** injured (SCDPS 2023 Traffic Collision Fact Book).
- 2023: one person killed in a DUI collision roughly every **21.2 hours** (SCDPS 2023 Fact Book).
- SC 2024 mileage death rate 1.68 = ~**40% higher** than national 1.20 (SCDPS / FFY2027 Highway Safety Guidelines).
- DUI arrests **+24.6%** statewide 2022→2023 (SLED Crime in SC report).
- SC ranks among top states for share of fatal crashes involving alcohol (NHTSA 2023).

> **Rule:** Every statistics slide names its source and year. Never state a number without attribution. If a number here cannot be re-verified at implementation time, mark that single slide with a `NEEDS-VERIFY` note in the changelog rather than inventing a figure.

---

## File Structure

- **Create:** `changes/tools/sc_edit.py` — insertion/replacement/reflow helper (one responsibility: mutate the content JSON safely).
- **Create:** `changes/tools/sc_audit.py` — validation + rubric-coverage audit (one responsibility: prove correctness).
- **Create:** `changes/image-briefs-sc.md` — per-image Gemini prompts + placement.
- **Create (EN changelog):** `changes/changelog-sc-content.en.md` — human-readable record of this pass.
- **Modify:** `dist/sc-content/sc-content.en.json` — the course content (all content tasks).
- **Modify (optional, Task 12):** `dist/index.html` — render image placeholders in QA viewer.
- **Backup:** `changes/backups/sc-content.en.pre-wellcovered.json` — created once in Task 0.

---

## Slide Schema Reference (match exactly)

Text slide:

```json
{
 "order_index": 0,
 "min_time": 3,
 "content_type": "Text",
 "content_type_unique_id": "text",
 "contents": [
  {"order_index": 0, "text": {"paragraphs": ["..."], "instruction": "Read the following, then click Next."}}
 ]
}
```

Multiple-choice slide (feeds final-exam pool):

```json
{
 "order_index": 0,
 "min_time": 3,
 "content_type": "Multiple",
 "content_type_unique_id": "multiple",
 "contents": [
  {"order_index": 0, "interactive": {
     "question": "...",
     "instruction": "Read the scenario, then select the best answer.",
     "options": [
       {"id": "opt_a", "label": "A. ...", "is_correct": false},
       {"id": "opt_b", "label": "B. ...", "is_correct": true},
       {"id": "opt_c", "label": "C. ...", "is_correct": false},
       {"id": "opt_d", "label": "D. ...", "is_correct": false}
     ],
     "feedback": {"correct": "...", "incorrect": "Incorrect."}
  }}
 ]
}
```

Completion (click-to-reveal) slide:

```json
{
 "order_index": 0,
 "min_time": 3,
 "content_type": "Completion",
 "content_type_unique_id": "completion",
 "contents": [
  {"order_index": 0,
   "text": {"instruction": "Click each item to learn more."},
   "interactive": {
     "content_structure": ["... {{item_1}} ... {{item_2}} ..."],
     "reveal_items": [
       {"id": "item_1", "title": "short label", "revealed_text": "full explanation"}
     ]
   }}
 ]
}
```

Image placeholder (new): a content block inside any slide's `contents`:

```json
{"order_index": 1, "image": {"placeholder": true, "asset_id": "sc-img-001", "alt": "descriptive alt text", "status": "pending"}}
```

---

## Task 0: Infrastructure — helper, backup, audit skeleton

**Files:**
- Create: `changes/tools/sc_edit.py`
- Create: `changes/tools/sc_audit.py`
- Create: `changes/backups/sc-content.en.pre-wellcovered.json`

- [ ] **Step 1: Back up the content file**

Run:
```bash
mkdir -p changes/backups changes/tools
cp dist/sc-content/sc-content.en.json changes/backups/sc-content.en.pre-wellcovered.json
```
Expected: backup file exists, byte-identical to source.

- [ ] **Step 2: Write the edit helper** `changes/tools/sc_edit.py`

```python
"""Safe editor for sc-content.en.json.

Operations (import and call from small task scripts):
  load()                         -> data dict
  save(data)                     -> writes file (indent=1, ensure_ascii=False)
  section(data, unit_number)     -> slides list for Unit N (1-based)
  make_text(paragraphs, instruction="Read the following, then click Next.")
  make_multiple(question, options, correct_index, correct_fb, incorrect_fb="Incorrect.",
                instruction="Read the scenario, then select the best answer.")
  make_completion(structure, items, instruction="Click each item to learn more.")
  make_image(asset_id, alt)      -> image placeholder content block
  add_image_to_slide(slide, asset_id, alt)
  insert_after(slides, target_index, new_slides)  -> inserts, does NOT reflow
  replace_paragraphs(slide, paragraphs)           -> overwrite first text block paragraphs
  reflow(slides)                 -> set order_index 0..n-1 on slides AND inner contents[0].order_index
  find_first(slides, substring)  -> index of first slide whose JSON contains substring (case-insensitive)
"""
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
```

- [ ] **Step 3: Write the audit script** `changes/tools/sc_audit.py`

```python
"""Validate sc-content.en.json and audit rubric coverage."""
import json, sys, os

PATH = os.path.join("dist", "sc-content", "sc-content.en.json")

# Each rubric row -> list of required phrases; ANY phrase present in ANY slide counts as a hit.
RUBRIC = {
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


def all_text(data):
    return json.dumps(data, ensure_ascii=False).lower()


def main():
    with open(PATH, encoding="utf-8") as f:
        data = json.load(f)  # raises on invalid JSON
    blob = all_text(data)
    missing = []
    for row, phrases in RUBRIC.items():
        if not any(p.lower() in blob for p in phrases):
            missing.append(row)
    total = sum(len(s["slides"]) for s in data["courses"][0]["sections"])
    print(f"JSON OK. Total slides: {total}")
    for i, s in enumerate(data["courses"][0]["sections"]):
        print(f"  Unit {i+1}: {len(s['slides'])} slides")
    if missing:
        print("\nMISSING rubric coverage:")
        for m in missing:
            print("  -", m)
        sys.exit(1)
    print(f"\nAll {len(RUBRIC)} rubric rows covered.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run audit on the untouched file to see the baseline**

Run: `python changes/tools/sc_audit.py`
Expected: prints "JSON OK. Total slides: 568" and a list of MISSING rubric rows (baseline gaps — this is expected to exit 1 now). Record which rows are already covered vs missing.

- [ ] **Step 5: Commit infrastructure**

```bash
git add changes/tools/sc_edit.py changes/tools/sc_audit.py changes/backups/sc-content.en.pre-wellcovered.json
git commit -m "Add SC content edit helper, audit script, and backup"
```

---

## Task 1: Unit 1 — SC Laws, Licensing, Permits, Concealed Weapons (Implied → Well Covered)

**Files:** Modify `dist/sc-content/sc-content.en.json` (Unit 1 = `sections[0]`), via a task script `changes/tools/t1.py`.

Adds explicit statute-anchored slides for: permit types (PBW/PO7/PLB/PLC/LOP), display of permits, operating without a permit, concealed weapons, and a knowledge check. Each statute gets its own Text slide + plain-language takeaway.

- [ ] **Step 1: Write `changes/tools/t1.py`** — inserts these slides after the licensing intro (locate with `find_first(s1, "SLED")` or the licensing block; if not found, insert after order_index 4).

New Text slides (paragraphs shown are the exact content to insert):

1. Permit types — PBW/PO7:
   - "South Carolina issues different permits depending on what a business sells and when. An On-Premises Beer & Wine Permit (PBW) lets a business sell beer and wine for on-site drinking and to-go, up to six days a week, twenty-four hours a day. Sunday sales are only allowed if the county has approved a Local Option. A 7-Day On-Premises Beer & Wine Permit (PO7) allows beer and wine sales seven days a week, except Sundays from 2 a.m. to 10 a.m., and is only issued in counties that approved Sunday sales by referendum. Knowing your establishment's permit tells you exactly what you are allowed to serve and when. Relevant statutes: SC Code Sections 61-4-120, 61-4-510, and 61-4-630."
2. Permit types — PLB/PLC/LOP:
   - "Liquor by the drink requires its own permit. A Business (Restaurant & Hotel) Liquor by the Drink License (PLB) covers businesses focused on meals or lodging and allows liquor Monday through Saturday, 10 a.m. to 2 a.m. A Nonprofit (Private Club) Liquor by the Drink License (PLC) covers valid nonprofit organizations seven days a week, 10 a.m. to 2 a.m. A Local Option Permit (LOP) adds Sunday liquor service for businesses that already hold a PLB, but only in counties that approved Sunday liquor sales. Serving outside your permit's hours or type is an illegal sale. Relevant statutes: SC Code Sections 61-6-1600 and 61-6-1610."
3. Display of permits:
   - "Every permit holder must display their alcohol licenses in a clearly visible place on the premises. This lets regulators, law enforcement, and the public confirm the business is authorized to sell alcohol. As a server, you should know where your establishment's permits are posted. Relevant statute: SC Code of Regulations 7-200.3."
4. Operating without a permit:
   - "Operating a retail or wholesale alcohol business without a permit is a misdemeanor punishable by a fine of $10 to $100 or imprisonment of 10 to 30 days. Each day the business operates without a permit is a separate offense, and all beer, wine, and liquor on the premises becomes contraband that the State Law Enforcement Division (SLED) must seize. This is why permits and their renewal are taken seriously. Relevant statutes: SC Code Sections 61-4-150, 61-4-560, 61-6-2600, and 61-6-2610."
5. Concealed weapons:
   - "South Carolina law states a person may not enter a business that sells alcohol for on-premises consumption while carrying a firearm and then consume alcohol. Violating this is a misdemeanor punishable by a fine of up to $2,000 or up to two years in prison, or both, and a Concealed Weapons Permit is revoked for five years. A business may also post a 'NO CONCEALABLE WEAPONS ALLOWED' sign; a person who refuses to comply can be fined up to $200 or jailed up to 30 days. Relevant statutes: SC Code Sections 16-23-465 and 23-31-220."

New Completion slide — "Permit types" click-to-reveal with reveal_items for PBW, PO7, PLB, PLC, LOP (titles = permit codes; revealed_text = one-line summary from Source Facts).

New Multiple slide (knowledge check):
   - question: "Your restaurant holds a PLB (Business Liquor by the Drink) license but not a Local Option Permit. A guest asks for a cocktail at 1 p.m. on Sunday. What is correct?"
   - options: A. "Serve it; liquor by the drink is always allowed" (wrong); B. "Do not serve liquor by the drink on Sunday without a Local Option Permit" (correct); C. "Serve only if they also order food" (wrong); D. "Serve a double instead" (wrong).
   - correct_fb: "A PLB allows liquor Monday–Saturday. Sunday liquor by the drink requires a Local Option Permit (LOP), issued only where the county approved Sunday liquor sales."

Script skeleton:
```python
import sc_edit as e
d = e.load()
s1 = e.section(d, 1)
anchor = e.find_first(s1, "licens")
if anchor < 0: anchor = 4
new = [
    e.make_text(["South Carolina issues different permits ... 61-4-120, 61-4-510, and 61-4-630."]),
    e.make_text(["Liquor by the drink requires its own permit ... 61-6-1600 and 61-6-1610."]),
    e.make_text(["Every permit holder must display ... Regulations 7-200.3."]),
    e.make_text(["Operating a retail or wholesale alcohol business without a permit ... 61-6-2600, and 61-6-2610."]),
    e.make_text(["South Carolina law states a person may not enter a business ... 16-23-465 and 23-31-220."]),
    e.make_completion(
        "South Carolina on-premises permits include {{item_1}} {{item_2}} {{item_3}} {{item_4}} {{item_5}}. Knowing your permit tells you what you may serve and when.",
        [
            {"id": "item_1", "title": "PBW", "revealed_text": "On-Premises Beer & Wine: beer/wine on-site and to-go, 6 days a week, 24 hours a day; Sundays only with Local Option."},
            {"id": "item_2", "title": "PO7", "revealed_text": "7-Day On-Premises Beer & Wine: 7 days a week except Sundays 2-10 a.m.; only in Sunday-sales counties."},
            {"id": "item_3", "title": "PLB", "revealed_text": "Business (Restaurant & Hotel) Liquor by the Drink: Mon-Sat 10 a.m.-2 a.m."},
            {"id": "item_4", "title": "PLC", "revealed_text": "Nonprofit (Private Club) Liquor by the Drink: 7 days a week 10 a.m.-2 a.m."},
            {"id": "item_5", "title": "LOP", "revealed_text": "Local Option Permit: Sunday liquor for PLB holders in counties approving Sunday liquor sales."},
        ]),
    e.make_multiple(
        "Your restaurant holds a PLB (Business Liquor by the Drink) license but not a Local Option Permit. A guest asks for a cocktail at 1 p.m. on Sunday. What is correct?",
        ["A. Serve it; liquor by the drink is always allowed",
         "B. Do not serve liquor by the drink on Sunday without a Local Option Permit",
         "C. Serve only if they also order food",
         "D. Serve a double instead"], 1,
        "A PLB allows liquor Monday-Saturday. Sunday liquor by the drink requires a Local Option Permit (LOP), issued only where the county approved Sunday liquor sales."),
]
e.insert_after(s1, anchor, new)
e.reflow(s1)
e.save(d)
```
(Replace the truncated `...` strings with the full paragraph text shown above before running.)

- [ ] **Step 2: Run the task script**

Run: `cd changes/tools && python t1.py && cd ../..`
Expected: no errors.

- [ ] **Step 3: Validate**

Run: `python changes/tools/sc_audit.py`
Expected: JSON OK; Unit 1 slide count increased by 7; "key laws" and "concealed weapons" rows now covered.

- [ ] **Step 4: Commit**
```bash
git add dist/sc-content/sc-content.en.json changes/tools/t1.py
git commit -m "Unit 1: add explicit permit-type, licensing, and concealed-weapon statute slides"
```

---

## Task 2: Unit 3 — ID Checking Cluster + Underage Penalties (Mentioned/Implied → Well Covered)

**Files:** Modify Unit 3 (`sections[2]`) via `changes/tools/t3.py`. This is the largest task — it fixes 9+ rubric rows.

Insert, grouped after the existing ID-check intro (locate with `find_first(s3, "identification")`):

1. **Three valid ID forms** (Text):
   - "In South Carolina you must verify a customer's age with a valid, government-issued photo ID before selling alcohol. The three forms you will see most often are a valid driver's license, a state-issued identification card, and a valid passport (a military ID is also acceptable). The document must be unexpired, must have a photo, and must clearly show the date of birth. If you are not confident the ID is valid and belongs to the customer, do not complete the sale."
2. **Locate the date of birth** (Text) + **image placeholder sc-img-id-anatomy**:
   - "Every valid ID shows a date of birth. On a South Carolina driver's license it appears near the name and photo, labeled 'DOB.' Always read the date of birth directly from the card rather than trusting the customer's word or a quick glance at the photo. Confirm the birth date, the expiration date, and that the photo matches the person in front of you."
3. **Vertical vs. horizontal license** (Text):
   - "South Carolina issues vertical (portrait) driver's licenses and ID cards to people under 21, and horizontal (landscape) licenses to people 21 and older. A vertical orientation is an immediate visual signal that the holder was under 21 when the card was issued, so you must check the date of birth carefully. Never rely on orientation alone — always confirm the actual date of birth, because a person with a vertical license may have since turned 21, and cards can be altered."
4. **Calculate the required date of birth** (Text) + **image placeholder sc-img-dob-math**:
   - "To sell alcohol legally, the customer must be at least 21 years old today. The fastest check is to take today's date and subtract 21 years — this gives the 'required date of birth.' Anyone born on or before that date is 21 or older; anyone born after it is under 21 and cannot be sold alcohol. For example, if today is July 6, 2026, the required date of birth is July 6, 2005: a customer must have been born on or before July 6, 2005."
5. **Apply the comparison** (Text):
   - "Once you know the required date of birth, compare it to the date of birth printed on the ID. If the ID's date of birth is on or before the required date, the customer is old enough. If it is after the required date, the customer is under 21 and you must refuse the sale. Do the math every time — do not estimate age from appearance, and do not round up because a customer 'looks old enough.'"
6. **ID anyone who appears underage** (Text):
   - "South Carolina expects consistent ID checks. A common, defensible house rule is to check the ID of anyone who appears to be under 30 (some establishments use 35 or 40), but the safest practice is to check every customer, every time, regardless of perceived age. Consistent checks protect you personally: failure to require identification to verify age is prima facie evidence of an illegal sale under South Carolina law."
7. **Detecting fake or altered IDs** (Text):
   - "A fake or altered ID is the most common way an underage buyer tries to get served. Check the physical card: feel for uneven thickness, bumps, or peeling around the photo and date of birth. Look for blurry text, mismatched fonts, missing or dull holograms, and edges that have been split or re-glued. Compare the photo, height, and description to the person. Ask a verifying question the real holder would answer instantly, such as their middle name, ZIP code, or zodiac sign for the birth date shown."
8. **Handling an illegal ID** (Text):
   - "If you determine an ID is fake, altered, borrowed, or belongs to someone else, do not sell alcohol. Follow your establishment's policy: politely decline the sale, and depending on house rules, hold the ID and notify a manager. Never argue or accuse loudly. Document what happened if your establishment requires an incident report. Refusing the sale protects you from criminal liability."
9. **Step-by-step ID procedure** (Completion click-to-reveal) — reveal_items: "Feel the card", "Look at security features", "Check the date of birth", "Compare photo and description", "Decide". + **image placeholder sc-img-idcheck-steps**.
10. **Underage sale penalties — you personally** (Text):
    - "Selling alcohol to someone under 21 is a misdemeanor in South Carolina, and the penalty falls on the person who made the sale — you. A first offense carries a fine of $200 to $300 or up to 30 days in jail, or both. A second or subsequent offense carries a fine of $400 to $500 or up to 30 days, or both. Because failure to check ID is prima facie evidence of the violation, checking every ID is your best legal protection. Relevant statutes: SC Code Sections 61-4-50 and 61-6-4080."
11. **Transfer to a minor** (Text):
    - "It is also unlawful to purchase for, transfer, or give beer, wine, or liquor to anyone under 21 for consumption. This includes an of-age customer buying a drink to hand to an underage friend at the bar. The penalties match the tiers for an unlawful sale. Watch for 'straw purchases' where one guest orders for an underage companion. Relevant statutes: SC Code Sections 61-4-90, 61-6-4070, and 61-6-4075."
12. **Required underage sign** (Text):
    - "Every retail seller must post a sign stating: 'The possession of beer, wine, or alcoholic liquors, by a person under twenty-one years of age is a criminal offense under the laws of this State, and it is also unlawful for a person to knowingly give false information concerning his age for the purpose of purchasing beer, wine, or liquor.' Failing to display this sign is itself a misdemeanor. Relevant statutes: SC Code Sections 61-4-70 and 61-6-1530."
13. **Life consequences to a minor** (Text):
    - "Selling to a minor does not just risk your job — it can change the minor's life. A conviction can create a criminal record, and a second or subsequent alcohol violation makes a student ineligible for major South Carolina scholarships: the Palmetto Fellows Scholarship for one year, the SC HOPE Scholarship for the next academic year, and the SC LIFE Scholarship for the following terms. Understanding these stakes is part of why refusing an underage sale always outranks making one. Relevant statutes: SC Code Sections 59-104-20, 61-4-100, and 61-6-4085."

Knowledge checks (Multiple) — add at least three:
- DOB calculation: "Today is July 6, 2026. A customer's ID shows a date of birth of September 2, 2005. Can you sell them alcohol?" → correct: "No — they turn 21 on September 2, 2026, which is after today, so they are still under 21." (options A–D)
- Fake ID: scenario where the photo doesn't match / card feels tampered → correct answer: decline and notify manager.
- Straw purchase: an of-age guest orders a beer and slides it to a visibly underage companion → correct: refuse and remove the drink; transferring to a minor is illegal.

- [ ] **Step 1: Write `changes/tools/t3.py`** using the helper, with the full paragraph text above, image placeholders attached via `e.add_image_to_slide(...)` on slides 2, 4, and 9.
- [ ] **Step 2: Run it.** Run: `cd changes/tools && python t3.py && cd ../..` — Expected: no errors.
- [ ] **Step 3: Validate.** Run: `python changes/tools/sc_audit.py` — Expected: JSON OK; Unit 3 count up ~16; rows "three valid ID forms", "locate DOB", "calc required DOB", "apply DOB comparison", "vertical vs horizontal", "fake/illegal ID", "ID anyone appearing underage", "server penalties", "life consequences to minors" now covered.
- [ ] **Step 4: Commit.**
```bash
git add dist/sc-content/sc-content.en.json changes/tools/t3.py
git commit -m "Unit 3: harden ID-check cluster, DOB math, and underage-sale penalties to Well Covered"
```

---

## Task 3: Unit 7 — SC Enforcement Statistics (Not Addressed → Well Covered)

**Files:** Modify Unit 7 (`sections[6]`) via `changes/tools/t7.py`.

Replace the vague existing stats slides and insert cited-number slides.

- [ ] **Step 1: Replace the vague fatality slide.** Locate with `find_first(s7, "notable portion")`; call `e.replace_paragraphs(slide, [...])` with:
  - "Impaired driving remains one of South Carolina's most serious traffic-safety problems. According to NHTSA's Fatality Analysis Reporting System, 413 people were killed in alcohol-impaired-driving crashes in South Carolina in 2023 — a driver with a blood alcohol concentration of 0.08% or higher was involved in 39% of all fatal-crash drivers that year. South Carolina consistently ranks among the states with the highest share of fatal crashes involving alcohol. As a server, the decision to stop serving an impaired guest is part of preventing these deaths."

- [ ] **Step 2: Insert new statistics slides** after that slide:
  1. "The South Carolina Department of Public Safety reported 5,319 alcohol- or drug-involved collisions in 2023, in which 367 people were killed and 3,372 were injured (SCDPS 2023 Traffic Collision Fact Book). Put another way, roughly every 21.2 hours one person was killed in a driving-under-the-influence collision in South Carolina. Behind each number is a preventable decision about when to stop serving."
  2. "Enforcement is increasing. The South Carolina Law Enforcement Division reported that DUI arrests rose 24.6% statewide from 2022 to 2023, with some counties more than doubling. South Carolina's 2024 mileage death rate of 1.68 fatalities per 100 million miles traveled was about 40% higher than the national rate of 1.20 (SCDPS). More enforcement means over-service is more likely to be traced back to the establishment and the server who poured the last drink."
  3. Completion click-to-reveal "What the numbers mean for you" — reveal_items summarizing: prevention role, legal exposure, community impact, professional responsibility.

- [ ] **Step 3: Add a knowledge-check Multiple slide** — e.g., "In 2023, roughly what share of drivers in South Carolina fatal crashes had a BAC of 0.08% or higher?" correct: "About 39% (NHTSA FARS, 2023)."

- [ ] **Step 4: Run, validate, commit.**
```bash
cd changes/tools && python t7.py && cd ../..
python changes/tools/sc_audit.py   # "recent SC enforcement stats" row now covered
git add dist/sc-content/sc-content.en.json changes/tools/t7.py
git commit -m "Unit 7: add cited SC enforcement statistics (SCDPS/NHTSA/SLED)"
```

---

## Task 4: Unit 6 — Ongoing Training, Liability, Marketing, MYDORWAY (Not Addressed/Covered → Well Covered)

**Files:** Modify Unit 6 (`sections[5]`) via `changes/tools/t6.py`.

- [ ] **Step 1: Ongoing training slides** (fixes the second Not Addressed row):
  1. "Responsible service is not a one-time lesson. South Carolina's framework and best practice expect servers to keep their knowledge current through refresher training, periodic self-assessments, and digital modules. Laws, permit rules, and penalties change — the Legal Supplement itself carries an effective date — so what you learned last year may not be current today."
  2. "Make ongoing training a habit: complete refreshers when your employer offers them, recheck your own ID-checking and refusal skills regularly, and stay alert to updates in South Carolina alcohol law. Employers who keep every server certified also reduce their liquor-liability insurance requirement, so your continued training directly benefits the business."
  3. Multiple check: best practice when a server is unsure whether a law changed → correct: consult current SC resources / manager and complete refresher training.

- [ ] **Step 2: Liquor-liability insurance slide** (business-ops row):
  - "Businesses open after 5 p.m. that sell alcohol for on-premises consumption must carry at least $1 million in liquor-liability coverage. South Carolina lets a business lower that requirement through risk mitigation — for example, a $100,000 reduction when every server completes the SC Alcohol Server Certificate within 60 days of hire, or when the business stops serving at midnight (a $250,000 reduction). This is a direct financial reason your training and responsible service matter to your employer. Relevant statute: SC Code Section 61-2-145."

- [ ] **Step 3: Dram-shop / apportioned liability slide:**
  - "If an intoxicated guest later causes harm, the establishment can share civil liability. Under South Carolina law a business is no longer liable for more than 50% of the damages from a DUI incident, and responsibility can be apportioned among multiple parties if a jury agrees. Responsible service — cutting off intoxicated guests and refusing illegal sales — is how you and your employer limit this exposure. Relevant statutes: SC Code Sections 15-38-15 through 15-38-40 and 61-2-147."

- [ ] **Step 4: Responsible marketing / promotions slides:**
  1. "South Carolina restricts alcohol promotions that encourage over-consumption. For on-premises consumption, a business may not advertise, sell, or dispense beer, wine, or liquor for free, at less than half the regular price, or on a two-for-one basis. It is also illegal to run a 'drinking contest' or 'drinking game.' Relevant statutes: SC Code Sections 61-4-160 and 61-6-4550."
  2. "Curbside and drive-thru alcohol sales are prohibited. A permit holder or employee may not sell or deliver beer or wine to anyone who remains in a motor vehicle during the transaction — this rule specifically bans drive-in, drive-thru, and curb-service alcohol sales. Relevant statute: SC Code of Regulations 7-202.5."

- [ ] **Step 5: MYDORWAY certificate slide** (operational win): strengthen or insert:
  - "When you complete this course and pass the test, your Alcohol Server Certificate is issued through the South Carolina Department of Revenue (SCDOR). You can access your approved certificate and its certificate number through the MYDORWAY portal. Keep your certificate number — employers and regulators may ask you to confirm your certification."

- [ ] **Step 6: Run, validate, commit.**
```bash
cd changes/tools && python t6.py && cd ../..
python changes/tools/sc_audit.py
git add dist/sc-content/sc-content.en.json changes/tools/t6.py
git commit -m "Unit 6: add ongoing training, liquor-liability insurance, dram-shop, marketing, and MYDORWAY slides"
```

---

## Task 5: Unit 2 — BAC & Physiology depth (Covered → Well Covered)

**Files:** Modify Unit 2 (`sections[1]`) via `changes/tools/t2.py`.

- [ ] **Step 1: Insert depth slides** for the rubric sub-bullets that are thin:
  1. Factors affecting BAC (Completion reveal): reveal_items = "Body weight", "Biological sex", "Rate of drinking", "Food in stomach", "Carbonation & drink strength".
  2. Drug interactions (Text): "Alcohol interacts dangerously with many prescription, over-the-counter, and illegal drugs. Sedatives, opioids, antihistamines, and other depressants can multiply alcohol's effects, so a guest may appear far more impaired than their number of drinks suggests. You cannot know what a guest has taken, so judge impairment by observed behavior, not just drink count."
  3. Individual tolerance (Text): "Tolerance means a regular heavy drinker may not look as impaired as their BAC actually is. Tolerance does not make a person safe to drive — it only masks the signs. Never use a guest's apparent 'ability to handle it' as a reason to keep serving; rely on drink count, time, and behavior."
  4. Legal BAC / DUI inference (Text): "In South Carolina, a blood alcohol concentration of 0.08% or higher means a driver is inferred to be under the influence, and a BAC between 0.05% and 0.08% can be weighed with other evidence. Standard drinks raise BAC in predictable ways, which is why pacing and cutting off service matter. Relevant statutes: SC Code Sections 56-5-2930 and 56-5-2933." + **image placeholder sc-img-bac-chart**.

- [ ] **Step 2: Standard-drink visual** — attach **image placeholder sc-img-standard-drink** to an existing standard-drink slide (locate with `find_first(s2, "standard drink")`).
- [ ] **Step 3: Knowledge check** on factors affecting BAC or tolerance.
- [ ] **Step 4: Run, validate, commit.**
```bash
cd changes/tools && python t2.py && cd ../..
python changes/tools/sc_audit.py
git add dist/sc-content/sc-content.en.json changes/tools/t2.py
git commit -m "Unit 2: deepen BAC factors, drug interactions, tolerance, and legal BAC to Well Covered"
```

---

## Task 6: Unit 4 — Intoxication Signs & Seeking Help depth (Covered → Well Covered)

**Files:** Modify Unit 4 (`sections[3]`) via `changes/tools/t4.py`.

- [ ] **Step 1: Signs-of-intoxication grid** (Completion reveal) — reveal_items grouped: "Speech", "Coordination", "Judgment/behavior", "Appearance". + **image placeholder sc-img-intoxication-signs**.
- [ ] **Step 2: Recognizing problem drinking** (Text): concrete behavioral signs + why early recognition matters.
- [ ] **Step 3: When and where to seek help** (Text): who to involve (manager, security), and that servers are a first line for interrupting harmful drinking.
- [ ] **Step 4: Knowledge check** — scenario matching observed signs to the right action.
- [ ] **Step 5: Run, validate, commit.**
```bash
cd changes/tools && python t4.py && cd ../..
python changes/tools/sc_audit.py
git add dist/sc-content/sc-content.en.json changes/tools/t4.py
git commit -m "Unit 4: deepen intoxication-sign recognition and seeking-help guidance"
```

---

## Task 7: Unit 5 — Refusal, Escalation, House Policies, Attitudes (Covered → Well Covered)

**Files:** Modify Unit 5 (`sections[4]`) via `changes/tools/t5.py`.

- [ ] **Step 1: Refusal techniques** (Text): firm, respectful scripts; offer water/food/alternatives; stay calm; never shame the guest.
- [ ] **Step 2: Escalation procedure** (Completion reveal) — reveal_items = numbered steps: "Pause service", "Offer alternatives", "Involve a manager", "Arrange safe transport", "Document the incident".
- [ ] **Step 3: House policies & incident reporting** (Text): what a house policy is, why following it protects the server, and how to complete an incident report.
- [ ] **Step 4: Attitudinal reinforcement** (Text): "In South Carolina, refusing an illegal or unsafe sale always outranks making the sale or pleasing a customer. A single sale is never worth a criminal charge, a lost certificate, or a life-changing crash. Confident, consistent refusals are a mark of professionalism, not rudeness — and your establishment's culture of accountability depends on every server holding this line."
- [ ] **Step 5: Knowledge checks** — a confrontational-refusal scenario and an escalation scenario.
- [ ] **Step 6: Run, validate, commit.**
```bash
cd changes/tools && python t5.py && cd ../..
python changes/tools/sc_audit.py
git add dist/sc-content/sc-content.en.json changes/tools/t5.py
git commit -m "Unit 5: deepen refusal, escalation, house-policy, and accountability content"
```

---

## Task 8: DUI / Implied Consent / Open Container depth (Unit 1 or 7)

**Files:** Modify the unit that currently owns DUI content (confirm with `find_first`, likely Unit 1 §3 or Unit 7) via `changes/tools/t_dui.py`.

- [ ] **Step 1: DUI penalty tiers** (Completion reveal or sequential Text) — 1st through 4th offense fines/jail/license from Source Facts, each citing § 56-5-2930.
- [ ] **Step 2: Felony DUI** (Text): great bodily injury and death penalty ranges, § 56-5-2945.
- [ ] **Step 3: Implied consent** (Text): consent to testing; refusal = 90-day (or 180-day) suspension, § 56-5-2950/-2951.
- [ ] **Step 4: Open container** (Text): no open container in moving vehicle except luggage compartment, § 61-4-110 / § 61-6-4020.
- [ ] **Step 5: Run, validate, commit.**
```bash
cd changes/tools && python t_dui.py && cd ../..
python changes/tools/sc_audit.py   # "implied consent" and "open container" rows now covered
git add dist/sc-content/sc-content.en.json changes/tools/t_dui.py
git commit -m "Add explicit DUI tiers, felony DUI, implied consent, and open-container statute slides"
```

---

## Task 9: Image placeholders + Gemini brief document

**Files:** Create `changes/image-briefs-sc.md`; image placeholders already inserted in Tasks 2/5/6 via `add_image_to_slide`.

- [ ] **Step 1: Confirm all placeholders exist.** Run:
```bash
python -c "import json; d=json.load(open('dist/sc-content/sc-content.en.json',encoding='utf-8')); print([b['image']['asset_id'] for s in d['courses'][0]['sections'] for sl in s['slides'] for b in sl['contents'] if 'image' in b])"
```
Expected: list including `sc-img-id-anatomy, sc-img-dob-math, sc-img-idcheck-steps, sc-img-bac-chart, sc-img-standard-drink, sc-img-intoxication-signs` (add `sc-img-vertical-vs-horizontal`, `sc-img-dui-stats-infographic`, `sc-img-refusal`, `sc-img-minor-signage` if included).

- [ ] **Step 2: Write `changes/image-briefs-sc.md`** — one section per asset_id with: Unit/slide reference, alt text, and a full Gemini prompt. Example entry:

```markdown
### sc-img-id-anatomy
- Placement: Unit 3, "Locate the date of birth" slide
- Alt: "Diagram of a South Carolina driver's license with the date-of-birth field highlighted."
- Gemini prompt: "A clean, flat-illustration diagram of a generic South Carolina-style driver's license (no real personal data). Label callouts pointing to: photo, full name, 'DOB' date-of-birth field (highlighted in a bright accent color), expiration date, and signature. Neutral educational style, high contrast, 16:9, no copyrighted logos or state seals."
```
Include entries for every asset_id.

- [ ] **Step 3: Commit.**
```bash
git add changes/image-briefs-sc.md
git commit -m "Add Gemini image briefs for SC course placeholders"
```

---

## Task 10: (Optional) QA viewer renders image placeholders

**Files:** Modify `dist/index.html` (renderer around line 147–192).

- [ ] **Step 1: Add an image-block branch** in the content renderer so a `content.image` block draws a labeled placeholder box:
```javascript
if(content.image){
  parts.push(`<div class="image-placeholder" style="border:2px dashed #999;padding:1rem;text-align:center;color:#666;margin:0.5rem 0;">[Image placeholder: ${escapeHtml(content.image.asset_id)}] ${escapeHtml(content.image.alt||'')}</div>`);
}
```
- [ ] **Step 2: Open `dist/index.html`** in a browser, load the EN content, spot-check a slide with a placeholder shows the box. (Manual visual check.)
- [ ] **Step 3: Commit.**
```bash
git add dist/index.html
git commit -m "QA viewer: render image placeholders as labeled boxes"
```

---

## Task 11: Final validation, coverage audit, changelog

**Files:** Create `changes/changelog-sc-content.en.md`.

- [ ] **Step 1: Full audit passes.** Run: `python changes/tools/sc_audit.py`
Expected: "JSON OK", per-unit counts printed, and "All 36 rubric rows covered." (exit 0). If any row is still missing, add a slide in the owning unit and re-run.

- [ ] **Step 2: Sanity-check order_index integrity.** Run:
```bash
python -c "import json; d=json.load(open('dist/sc-content/sc-content.en.json',encoding='utf-8')); [print(f'U{i+1}', 'OK' if [x['order_index'] for x in s['slides']]==list(range(len(s['slides']))) else 'BAD') for i,s in enumerate(d['courses'][0]['sections'])]"
```
Expected: every unit "OK" (order_index is 0..n-1 contiguous).

- [ ] **Step 3: Confirm total runtime supports the 4-hour minimum.** Run:
```bash
python -c "import json; d=json.load(open('dist/sc-content/sc-content.en.json',encoding='utf-8')); print('slides', sum(len(s['slides']) for s in d['courses'][0]['sections']))"
```
Expected: substantially more than the original 568 (target ~650–680).

- [ ] **Step 4: Write `changes/changelog-sc-content.en.md`** documenting: rubric rows addressed, new slide counts per unit, statutes cited, statistics + sources, images added, and the linear-navigation platform item flagged as out of scope.

- [ ] **Step 5: Commit.**
```bash
git add changes/changelog-sc-content.en.md
git commit -m "Add EN changelog for Well Covered content pass"
```

---

## Self-Review (completed against the spec)

1. **Spec coverage:** All spec §1–§7 map to tasks — §1 stats→Task 3; §2 ongoing training→Task 4; §3 ID cluster→Task 2; §4 statute explicitness→Tasks 1/8; §5 Covered-boost→Tasks 5/6/7; §6 images→Tasks 2/5/6/9/10; §7 operational win (MYDORWAY)→Task 4. Verification→Task 11.
2. **Placeholder scan:** Task scripts intentionally show truncated `...` inside example code with an explicit instruction to paste the full paragraph text printed above them; all paragraph text is provided in full in the task bodies and in Source Facts. No "TBD"/"handle edge cases" left.
3. **Type consistency:** All slides use the four confirmed shapes (Text/Multiple/Completion/image block). Helper names (`make_text`, `make_multiple`, `make_completion`, `make_image`, `add_image_to_slide`, `insert_after`, `replace_paragraphs`, `reflow`, `find_first`, `section`, `load`, `save`) are used identically across every task.
4. **Ambiguity:** Statistics rule fixed (cite source+year, mark NEEDS-VERIFY rather than invent). Rubric audit is the objective definition of "done."
```
