"""Task 7: Unit 5 -- refusal, escalation, house-policy, and accountability."""
import sc_edit as e

d = e.load()
s5 = e.section(d, 5)

new = [
    e.make_text([
        "Refusing service works best when it is calm, firm, and respectful. Use clear language such as, 'I cannot serve you another alcoholic drink tonight,' and avoid debating or blaming the guest. Offer water, food, a nonalcoholic beverage, or help arranging transportation. Your goal is to end alcohol service safely while preserving dignity and reducing conflict."
    ]),
    e.make_completion(
        "Use the same escalation steps every time: {{item_1}} {{item_2}} {{item_3}} {{item_4}} {{item_5}} A consistent process protects guests, staff, and the business.",
        [
            {"id": "item_1", "title": "Pause service",
             "revealed_text": "Stop serving alcohol while you assess the situation."},
            {"id": "item_2", "title": "Offer alternatives",
             "revealed_text": "Offer water, food, nonalcoholic drinks, or time to rest."},
            {"id": "item_3", "title": "Involve a manager",
             "revealed_text": "Bring in a manager or supervisor when the guest resists, becomes upset, or needs a formal refusal."},
            {"id": "item_4", "title": "Arrange safe transport",
             "revealed_text": "Help the guest get a ride, call a rideshare or taxi, or contact a sober friend."},
            {"id": "item_5", "title": "Document the incident",
             "revealed_text": "Complete an incident report according to house policy."},
        ],
    ),
    e.make_text([
        "House policies turn responsible service into a repeatable process. A strong policy explains when to check ID, when to refuse service, when to involve a manager, how to prevent a guest from driving, and when to complete an incident report. Following the policy protects you because it shows your decisions were consistent, documented, and based on safety rather than personal judgment alone."
    ]),
    e.make_text([
        "In South Carolina, refusing an illegal or unsafe sale always outranks making the sale or pleasing a customer. A single sale is never worth a criminal charge, a lost certificate, or a life-changing crash. Confident, consistent refusals are a mark of professionalism, not rudeness -- and your establishment's culture of accountability depends on every server holding this line."
    ]),
    e.make_multiple(
        "A guest becomes irritated after you refuse another drink and says, 'I know the owner. Serve me anyway.' What should you do?",
        [
            "A. Serve the drink to avoid conflict",
            "B. Stay calm, repeat the refusal, offer water or a nonalcoholic option, and involve a manager if the guest continues to push",
            "C. Argue until they admit they are intoxicated",
            "D. Ignore them and walk away without telling anyone",
        ],
        1,
        "A refusal should be calm, firm, and respectful. Repeat the boundary, offer alternatives, and involve a manager when the guest resists or escalates.",
    ),
    e.make_multiple(
        "A server cuts off a visibly intoxicated guest. The guest leaves angry and starts walking toward the parking lot with car keys in hand. What is the best next step?",
        [
            "A. Do nothing because service already stopped",
            "B. Follow escalation procedures: alert a manager or security, try to arrange safe transportation, and document the incident",
            "C. Serve coffee and assume they will sober up immediately",
            "D. Let them drive if they promise to go slowly",
        ],
        1,
        "Stopping service is only part of responsible service. Escalate, involve management/security, arrange safe transportation when possible, and document the incident according to house policy.",
    ),
]

anchor = e.find_first(s5, "refus")
if anchor == -1:
    anchor = 3
print(f"anchor={anchor}, before={len(s5)}")

e.insert_after(s5, anchor, new)
e.reflow(s5)
e.save(d)
print(f"after={len(s5)}")
