"""Task 5: Unit 2 -- BAC factors, drug interactions, tolerance, legal BAC."""
import sc_edit as e

d = e.load()
s2 = e.section(d, 2)

# OP-A: attach standard-drink image to an existing slide
sd = e.find_first(s2, "standard drink")
if sd >= 0:
    e.add_image_to_slide(
        s2[sd],
        "sc-img-standard-drink",
        "Chart of standard drink equivalents: 12 oz beer, 5 oz wine, 1.5 oz distilled spirits.",
    )
    print(f"OP-A: attached sc-img-standard-drink to slide {sd}")
else:
    print("OP-A: skipped -- no slide containing 'standard drink' found")

# OP-B: build and insert new slides
completion = e.make_completion(
    "Several factors change how quickly alcohol raises a person's blood alcohol concentration (BAC): {{item_1}} {{item_2}} {{item_3}} {{item_4}} {{item_5}} Because these vary from person to person, the same number of drinks affects guests differently.",
    [
        {"id": "item_1", "title": "Body weight", "revealed_text": "A person with lower body weight generally reaches a higher BAC from the same amount of alcohol."},
        {"id": "item_2", "title": "Biological sex", "revealed_text": "Differences in body composition and enzymes mean alcohol often affects women faster than men."},
        {"id": "item_3", "title": "Rate of drinking", "revealed_text": "Drinking quickly raises BAC faster than the body can process the alcohol."},
        {"id": "item_4", "title": "Food in the stomach", "revealed_text": "Food slows alcohol absorption; drinking on an empty stomach raises BAC faster."},
        {"id": "item_5", "title": "Drink strength and carbonation", "revealed_text": "Stronger drinks and carbonated mixers can raise BAC more quickly."},
    ],
)

drugs_text = e.make_text([
    "Alcohol interacts dangerously with many prescription, over-the-counter, and illegal drugs. Sedatives, opioids, antihistamines, and other depressants can multiply alcohol's effects, so a guest may appear far more impaired than their number of drinks suggests. You cannot know what a guest has taken, so judge impairment by observed behavior, not just drink count."
])

tolerance_text = e.make_text([
    "Tolerance means a regular heavy drinker may not look as impaired as their BAC actually is. Tolerance does not make a person safe to drive -- it only masks the signs. Never use a guest's apparent 'ability to handle it' as a reason to keep serving; rely on drink count, time, and behavior."
])

legal_bac_text = e.make_text([
    "In South Carolina, a blood alcohol concentration of 0.08% or higher means a driver is inferred to be under the influence, and a BAC between 0.05% and 0.08% can be weighed with other evidence. Standard drinks raise BAC in predictable ways, which is why pacing and cutting off service matter. Relevant statutes: SC Code Sections 56-5-2930 and 56-5-2933."
])
e.add_image_to_slide(
    legal_bac_text,
    "sc-img-bac-chart",
    "Chart relating number of standard drinks and body weight to estimated blood alcohol concentration.",
)

quiz = e.make_multiple(
    "Two guests each had three drinks in an hour. One appears far more impaired than the other. What is the best explanation for a server to keep in mind?",
    [
        "A. The calmer guest is safe to keep serving",
        "B. Factors like body weight, food, drinking rate, tolerance, and medications change how alcohol affects each person, so judge impairment by behavior",
        "C. They must have miscounted their drinks",
        "D. BAC is the same for everyone after three drinks",
    ],
    1,
    "BAC and visible impairment vary with body weight, biological sex, food, drinking rate, tolerance, and any drugs taken. Always judge impairment by observed behavior, not just the number of drinks.",
)

new = [completion, drugs_text, tolerance_text, legal_bac_text, quiz]

anchor = e.find_first(s2, "blood alcohol")
if anchor == -1:
    anchor = 3
print(f"OP-B: inserting {len(new)} slides after index {anchor}")

e.insert_after(s2, anchor, new)
e.reflow(s2)
e.save(d)
print(f"Done. Unit 2 now has {len(s2)} slides.")
