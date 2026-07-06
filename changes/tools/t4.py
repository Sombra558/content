"""Task 6: Unit 4 -- intoxication-sign recognition and seeking-help guidance."""
import sc_edit as e

d = e.load()
s4 = e.section(d, 4)

# 1. Four areas of intoxication signs (Completion, image)
c1 = e.make_completion(
    "Signs of intoxication usually show up in four areas: {{item_1}} {{item_2}} {{item_3}} {{item_4}} Watch for changes over time, not just a single moment.",
    [
        {"id": "item_1", "title": "Speech",
         "revealed_text": "Slurred, loud, rambling, or repetitive speech."},
        {"id": "item_2", "title": "Coordination",
         "revealed_text": "Swaying, stumbling, dropping items, or trouble with simple tasks like handling money."},
        {"id": "item_3", "title": "Judgment and behavior",
         "revealed_text": "Aggression, over-familiarity, risk-taking, or sudden mood changes."},
        {"id": "item_4", "title": "Appearance",
         "revealed_text": "Glassy or bloodshot eyes, flushed face, or a disheveled look."},
    ],
)
e.add_image_to_slide(c1, "sc-img-intoxication-signs",
                     "Grid of common intoxication signs grouped by speech, coordination, judgment, and appearance.")

# 2. Recognizing problem drinking early
c2 = e.make_text([
    "Recognizing problem drinking early lets you act before a guest becomes a danger to themselves or others. Watch for guests who drink quickly, order rounds back to back, become louder or more withdrawn, or ask for drinks despite clear signs of impairment. Noticing these patterns early gives you time to slow service, offer food or water, and prepare to refuse further alcohol."
])

# 3. When and where to seek help
c3 = e.make_text([
    "Know when and where to seek help. If a guest's drinking becomes a safety concern, involve your manager or security right away, and arrange safe transportation when needed. Servers are often the first line of defense against alcohol-related harm, so raising a concern early is a sign of professionalism, not weakness. Never let a visibly intoxicated guest drive."
])

# 4. Multiple: intoxicated guest scenario
c4 = e.make_multiple(
    "A guest is slurring words, swaying on the stool, and just knocked over a glass while reaching for their drink. What should you do?",
    [
        "A. Serve one more since they are still sitting down",
        "B. Stop alcohol service, offer water or food, and involve a manager while arranging safe transportation",
        "C. Wait until they fall before acting",
        "D. Move them to a booth and keep serving",
    ],
    1,
    "Slurred speech, swaying, and loss of coordination are clear signs of intoxication. Stop serving alcohol, offer water or food, involve a manager, and help arrange safe transportation.",
)

new = [c1, c2, c3, c4]

anchor = e.find_first(s4, "intoxicat")
if anchor == -1:
    anchor = 3
print(f"anchor={anchor}, before={len(s4)}")

e.insert_after(s4, anchor, new)
e.reflow(s4)
e.save(d)
print(f"after={len(s4)}")
