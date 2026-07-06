"""Task 2: Unit 3 -- ID-check cluster, DOB math, and underage-sale penalties."""
import sc_edit as e

d = e.load()
s3 = e.section(d, 3)

# 1. Three valid ID forms
s1 = e.make_text([
    "In South Carolina you must verify a customer's age with a valid, government-issued photo ID before selling alcohol. The three forms you will see most often are a valid driver's license, a state-issued identification card, and a valid passport (a military ID is also acceptable). The document must be unexpired, must have a photo, and must clearly show the date of birth. If you are not confident the ID is valid and belongs to the customer, do not complete the sale."
])

# 2. Locate DOB on ID (image)
s2 = e.make_text([
    "Every valid ID shows a date of birth. On a South Carolina driver's license it appears near the name and photo, labeled 'DOB.' Always read the date of birth directly from the card rather than trusting the customer's word or a quick glance at the photo. Confirm the birth date, the expiration date, and that the photo matches the person in front of you."
])
e.add_image_to_slide(s2, "sc-img-id-anatomy",
                     "Diagram of a South Carolina driver's license with the date-of-birth field highlighted.")

# 3. Vertical vs horizontal license (image)
s3_slide = e.make_text([
    "South Carolina issues vertical (portrait) driver's licenses and ID cards to people under 21, and horizontal (landscape) licenses to people 21 and older. A vertical orientation is an immediate visual signal that the holder was under 21 when the card was issued, so you must check the date of birth carefully. Never rely on orientation alone -- always confirm the actual date of birth, because a person with a vertical license may have since turned 21, and cards can be altered."
])
e.add_image_to_slide(s3_slide, "sc-img-vertical-vs-horizontal",
                     "Side-by-side comparison of a vertical under-21 South Carolina license and a horizontal 21-and-older license.")

# 4. Calc required DOB (image)
s4 = e.make_text([
    "To sell alcohol legally, the customer must be at least 21 years old today. The fastest check is to take today's date and subtract 21 years -- this gives the 'required date of birth.' Anyone born on or before that date is 21 or older; anyone born after it is under 21 and cannot be sold alcohol. For example, if today is July 6, 2026, the required date of birth is July 6, 2005: a customer must have been born on or before July 6, 2005."
])
e.add_image_to_slide(s4, "sc-img-dob-math",
                     "Visual showing today's date minus 21 years to find the required date of birth.")

# 5. Apply DOB comparison
s5 = e.make_text([
    "Once you know the required date of birth, compare it to the date of birth printed on the ID. If the ID's date of birth is on or before the required date, the customer is old enough. If it is after the required date, the customer is under 21 and you must refuse the sale. Do the math every time -- do not estimate age from appearance, and do not round up because a customer 'looks old enough.'"
])

# 6. ID anyone appearing underage
s6 = e.make_text([
    "South Carolina expects consistent ID checks. A common, defensible house rule is to check the ID of anyone who appears to be under 30 (some establishments use 35 or 40), but the safest practice is to check every customer, every time, regardless of perceived age. Consistent checks protect you personally: failure to require identification to verify age is prima facie evidence of an illegal sale under South Carolina law."
])

# 7. Spotting fake/altered IDs
s7 = e.make_text([
    "A fake or altered ID is the most common way an underage buyer tries to get served. Check the physical card: feel for uneven thickness, bumps, or peeling around the photo and date of birth. Look for blurry text, mismatched fonts, missing or dull holograms, and edges that have been split or re-glued. Compare the photo, height, and description to the person. Ask a verifying question the real holder would answer instantly, such as their middle name, ZIP code, or zodiac sign for the birth date shown."
])

# 8. Handling a fake ID
s8 = e.make_text([
    "If you determine an ID is fake, altered, borrowed, or belongs to someone else, do not sell alcohol. Follow your establishment's policy: politely decline the sale, and depending on house rules, hold the ID and notify a manager. Never argue or accuse loudly. Document what happened if your establishment requires an incident report. Refusing the sale protects you from criminal liability."
])

# 9. Five-step ID check (Completion, image)
s9 = e.make_completion(
    "A thorough ID check follows the same steps every time: {{item_1}} {{item_2}} {{item_3}} {{item_4}} {{item_5}} Consistency is what keeps the check legal and reliable.",
    [
        {"id": "item_1", "title": "Feel the card",
         "revealed_text": "Feel the card for uneven thickness, bumps, or peeling around the photo and date of birth."},
        {"id": "item_2", "title": "Look at security features",
         "revealed_text": "Look for holograms, microprint, clear fonts, and edges that have not been split or re-glued."},
        {"id": "item_3", "title": "Check the date of birth",
         "revealed_text": "Read the date of birth and compare it to today's required date of birth (today minus 21 years)."},
        {"id": "item_4", "title": "Compare photo and description",
         "revealed_text": "Match the photo, height, and description to the person in front of you."},
        {"id": "item_5", "title": "Decide",
         "revealed_text": "If anything fails or you are unsure, refuse the sale and follow house policy."},
    ],
)
e.add_image_to_slide(s9, "sc-img-idcheck-steps",
                     "Five-step ID check sequence: feel the card, look at security features, check the date of birth, compare photo and description, decide.")

# 10. Server penalties for sale to minors
s10 = e.make_text([
    "Selling alcohol to someone under 21 is a misdemeanor in South Carolina, and the penalty falls on the person who made the sale -- you. A first offense carries a fine of $200 to $300 or up to 30 days in jail, or both. A second or subsequent offense carries a fine of $400 to $500 or up to 30 days, or both. Because failure to check ID is prima facie evidence of the violation, checking every ID is your best legal protection. Relevant statutes: SC Code Sections 61-4-50 and 61-6-4080."
])

# 11. Purchase for / transfer to minors
s11 = e.make_text([
    "It is also unlawful to purchase for, transfer, or give beer, wine, or liquor to anyone under 21 for consumption. This includes an of-age customer buying a drink to hand to an underage friend at the bar. The penalties match the tiers for an unlawful sale. Watch for 'straw purchases' where one guest orders for an underage companion. Relevant statutes: SC Code Sections 61-4-90, 61-6-4070, and 61-6-4075."
])

# 12. Required sign
s12 = e.make_text([
    "Every retail seller must post a sign stating: 'The possession of beer, wine, or alcoholic liquors, by a person under twenty-one years of age is a criminal offense under the laws of this State, and it is also unlawful for a person to knowingly give false information concerning his age for the purpose of purchasing beer, wine, or liquor.' Failing to display this sign is itself a misdemeanor. Relevant statutes: SC Code Sections 61-4-70 and 61-6-1530."
])

# 13. Life/scholarship consequences to minors
s13 = e.make_text([
    "Selling to a minor does not just risk your job -- it can change the minor's life. A conviction can create a criminal record, and a second or subsequent alcohol violation makes a student ineligible for major South Carolina scholarships: the Palmetto Fellows Scholarship for one year, the SC HOPE Scholarship for the next academic year, and the SC LIFE Scholarship for the following terms. Understanding these stakes is part of why refusing an underage sale always outranks making one. Relevant statutes: SC Code Sections 59-104-20, 61-4-100, and 61-6-4085."
])

# 14. Multiple: DOB math
s14 = e.make_multiple(
    "Today is July 6, 2026. A customer's ID shows a date of birth of September 2, 2005. Can you sell them alcohol?",
    [
        "A. Yes, 2005 means they are 21",
        "B. No -- they turn 21 on September 2, 2026, which is after today, so they are still under 21",
        "C. Yes, if they also show a second ID",
        "D. Only after 9 p.m.",
    ],
    1,
    "The required date of birth today is July 6, 2005. A birth date of September 2, 2005 is after that, so the customer is still under 21 until September 2, 2026. Refuse the sale.",
)

# 15. Multiple: fake ID
s15 = e.make_multiple(
    "A customer hands you a license. The photo hair and face look different, the card feels bumpy around the birth date, and the person cannot recall their own ZIP code. What should you do?",
    [
        "A. Sell; the card is probably fine",
        "B. Refuse the sale, and hold the ID and notify a manager per house policy",
        "C. Sell but only beer",
        "D. Ask them to sign for it",
    ],
    1,
    "Multiple warning signs -- mismatched photo, tampered feel, and failure to answer a basic verifying question -- mean you do not sell. Decline, and follow house policy on holding the ID and notifying a manager.",
)

# 16. Multiple: straw purchase
s16 = e.make_multiple(
    "An adult guest orders a beer, then immediately slides it to a visibly underage companion at the table. What is the correct response?",
    [
        "A. Nothing; the adult bought it legally",
        "B. Remove or refuse the drink -- transferring alcohol to someone under 21 is illegal, and you may not keep serving the pair for that purpose",
        "C. Charge the underage guest for it",
        "D. Ask them to move tables",
    ],
    1,
    "Buying or transferring alcohol to a person under 21 for consumption is unlawful (a 'straw purchase'). Interrupt the transfer, refuse further service for that purpose, and involve a manager if needed.",
)

new = [s1, s2, s3_slide, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16]

anchor = e.find_first(s3, "identification")
if anchor == -1:
    anchor = 4
print(f"anchor={anchor}, before={len(s3)}")

e.insert_after(s3, anchor, new)
e.reflow(s3)
e.save(d)
print(f"after={len(s3)}")
