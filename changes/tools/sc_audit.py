"""Validate sc-content.en.json and audit rubric coverage."""
import json, sys, os

PATH = os.path.join("dist", "sc-content", "sc-content.en.json")

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
        data = json.load(f)
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
