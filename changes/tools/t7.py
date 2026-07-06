"""Task 3: Unit 7 -- cited SC enforcement statistics (SCDPS/NHTSA/SLED)."""
import sc_edit as e

FATALITY_PARA = (
    "Impaired driving remains one of South Carolina's most serious traffic-safety "
    "problems. According to NHTSA's Fatality Analysis Reporting System, 413 people "
    "were killed in alcohol-impaired-driving crashes in South Carolina in 2023 -- a "
    "driver with a blood alcohol concentration of 0.08% or higher was involved in "
    "39% of all fatal-crash drivers that year. South Carolina consistently ranks "
    "among the states with the highest share of fatal crashes involving alcohol. As "
    "a server, the decision to stop serving an impaired guest is part of preventing "
    "these deaths."
)

d = e.load()
s7 = e.section(d, 7)
before = len(s7)

idx = e.find_first(s7, "notable portion")
if idx >= 0:
    ok = e.replace_paragraphs(s7[idx], [FATALITY_PARA])
    assert ok, "replace_paragraphs failed on vague fatality slide"
    path_taken = "REPLACED vague slide at index %d" % idx
else:
    idx = e.find_first(s7, "fatalities")
    if idx == -1:
        idx = 2
    e.insert_after(s7, idx, [e.make_text([FATALITY_PARA])])
    idx = idx + 1  # new fatality slide position; insert the rest after it
    path_taken = "INSERTED new fatality slide at index %d" % idx

new_slides = [
    e.make_text([
        "The South Carolina Department of Public Safety reported 5,319 alcohol- or "
        "drug-involved collisions in 2023, in which 367 people were killed and 3,372 "
        "were injured (SCDPS 2023 Traffic Collision Fact Book). Put another way, "
        "roughly every 21.2 hours one person was killed in a driving-under-the-"
        "influence collision in South Carolina. Behind each number is a preventable "
        "decision about when to stop serving."
    ]),
    e.make_text([
        "Enforcement is increasing. The South Carolina Law Enforcement Division "
        "reported that DUI arrests rose 24.6% statewide from 2022 to 2023, with some "
        "counties more than doubling. South Carolina's 2024 mileage death rate of "
        "1.68 fatalities per 100 million miles traveled was about 40% higher than "
        "the national rate of 1.20 (SCDPS). More enforcement means over-service is "
        "more likely to be traced back to the establishment and the server who "
        "poured the last drink."
    ]),
    e.make_completion(
        "The statistics point back to your role: {{item_1}} {{item_2}} {{item_3}} "
        "{{item_4}} Every responsible refusal changes the numbers.",
        [
            {"id": "item_1", "title": "Prevention",
             "revealed_text": "Stopping service to an impaired guest can prevent a crash before it happens."},
            {"id": "item_2", "title": "Legal exposure",
             "revealed_text": "Over-service can be traced back to the server and establishment through enforcement and investigation."},
            {"id": "item_3", "title": "Community impact",
             "revealed_text": "Each alcohol-related death and injury affects families, coworkers, and the wider community."},
            {"id": "item_4", "title": "Professional responsibility",
             "revealed_text": "Responsible service is a measurable part of reducing South Carolina's impaired-driving toll."},
        ],
    ),
    e.make_multiple(
        "According to NHTSA FARS data, roughly what share of drivers in South "
        "Carolina's fatal crashes in 2023 had a blood alcohol concentration of "
        "0.08% or higher?",
        [
            "A. About 10%",
            "B. About 25%",
            "C. About 39%",
            "D. About 75%",
        ],
        2,
        "In 2023, about 39% of drivers in South Carolina fatal crashes had a BAC of "
        "0.08% or higher, and 413 people were killed in alcohol-impaired-driving "
        "crashes (NHTSA FARS, 2023).",
    ),
]

e.insert_after(s7, idx, new_slides)
e.reflow(s7)
e.save(d)

print(path_taken)
print("Unit 7 slide count: %d -> %d" % (before, len(s7)))
