"""Task 1: insert permit-type, licensing, and concealed-weapon slides into Unit 1."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
# sc_edit.PATH is relative to the repo root, so make sure we run from there.
os.chdir(os.path.join(_HERE, "..", ".."))

import sc_edit as e

d = e.load()
s1 = e.section(d, 1)

anchor = e.find_first(s1, "licens")
if anchor == -1:
    anchor = 4

new = [
    e.make_text([
        "South Carolina issues different permits depending on what a business sells and when. An On-Premises Beer & Wine Permit (PBW) lets a business sell beer and wine for on-site drinking and to-go, up to six days a week, twenty-four hours a day. Sunday sales are only allowed if the county has approved a Local Option. A 7-Day On-Premises Beer & Wine Permit (PO7) allows beer and wine sales seven days a week, except Sundays from 2 a.m. to 10 a.m., and is only issued in counties that approved Sunday sales by referendum. Knowing your establishment's permit tells you exactly what you are allowed to serve and when. Relevant statutes: SC Code Sections 61-4-120, 61-4-510, and 61-4-630."
    ]),
    e.make_text([
        "Liquor by the drink requires its own permit. A Business (Restaurant & Hotel) Liquor by the Drink License (PLB) covers businesses focused on meals or lodging and allows liquor Monday through Saturday, 10 a.m. to 2 a.m. A Nonprofit (Private Club) Liquor by the Drink License (PLC) covers valid nonprofit organizations seven days a week, 10 a.m. to 2 a.m. A Local Option Permit (LOP) adds Sunday liquor service for businesses that already hold a PLB, but only in counties that approved Sunday liquor sales. Serving outside your permit's hours or type is an illegal sale. Relevant statutes: SC Code Sections 61-6-1600 and 61-6-1610."
    ]),
    e.make_text([
        "Every permit holder must display their alcohol licenses in a clearly visible place on the premises. This lets regulators, law enforcement, and the public confirm the business is authorized to sell alcohol. As a server, you should know where your establishment's permits are posted. Relevant statute: SC Code of Regulations 7-200.3."
    ]),
    e.make_text([
        "Operating a retail or wholesale alcohol business without a permit is a misdemeanor punishable by a fine of $10 to $100 or imprisonment of 10 to 30 days. Each day the business operates without a permit is a separate offense, and all beer, wine, and liquor on the premises becomes contraband that the State Law Enforcement Division (SLED) must seize. This is why permits and their renewal are taken seriously. Relevant statutes: SC Code Sections 61-4-150, 61-4-560, 61-6-2600, and 61-6-2610."
    ]),
    e.make_text([
        "South Carolina law states a person may not enter a business that sells alcohol for on-premises consumption while carrying a firearm and then consume alcohol. Violating this is a misdemeanor punishable by a fine of up to $2,000 or up to two years in prison, or both, and a Concealed Weapons Permit is revoked for five years. A business may also post a 'NO CONCEALABLE WEAPONS ALLOWED' sign; a person who refuses to comply can be fined up to $200 or jailed up to 30 days. Relevant statutes: SC Code Sections 16-23-465 and 23-31-220."
    ]),
    e.make_completion(
        "South Carolina on-premises permits include {{item_1}} {{item_2}} {{item_3}} {{item_4}} {{item_5}}. Knowing your permit tells you what you may serve and when.",
        [
            {"id": "item_1", "title": "PBW", "revealed_text": "On-Premises Beer & Wine: beer/wine on-site and to-go, 6 days a week, 24 hours a day; Sundays only with Local Option."},
            {"id": "item_2", "title": "PO7", "revealed_text": "7-Day On-Premises Beer & Wine: 7 days a week except Sundays 2-10 a.m.; only in Sunday-sales counties."},
            {"id": "item_3", "title": "PLB", "revealed_text": "Business (Restaurant & Hotel) Liquor by the Drink: Mon-Sat 10 a.m.-2 a.m."},
            {"id": "item_4", "title": "PLC", "revealed_text": "Nonprofit (Private Club) Liquor by the Drink: 7 days a week 10 a.m.-2 a.m."},
            {"id": "item_5", "title": "LOP", "revealed_text": "Local Option Permit: Sunday liquor for PLB holders in counties approving Sunday liquor sales."},
        ],
    ),
    e.make_multiple(
        "Your restaurant holds a PLB (Business Liquor by the Drink) license but not a Local Option Permit. A guest asks for a cocktail at 1 p.m. on Sunday. What is correct?",
        [
            "A. Serve it; liquor by the drink is always allowed",
            "B. Do not serve liquor by the drink on Sunday without a Local Option Permit",
            "C. Serve only if they also order food",
            "D. Serve a double instead",
        ],
        1,
        "A PLB allows liquor Monday-Saturday. Sunday liquor by the drink requires a Local Option Permit (LOP), issued only where the county approved Sunday liquor sales.",
    ),
]

e.insert_after(s1, anchor, new)
e.reflow(s1)
e.save(d)
print(f"Inserted {len(new)} slides after anchor {anchor}; Unit 1 now has {len(s1)} slides.")
