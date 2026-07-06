"""Task 4: Unit 6 -- ongoing training, liquor-liability insurance, dram-shop,
marketing restrictions, curbside ban, and MYDORWAY certificate slides."""
import sc_edit as e

d = e.load()
s6 = e.section(d, 6)

new = [
    e.make_text([
        "Responsible service is not a one-time lesson. South Carolina's framework and best practice expect servers to keep their knowledge current through refresher training, periodic self-assessments, and digital modules. Laws, permit rules, and penalties change -- the Legal Supplement itself carries an effective date -- so what you learned last year may not be current today."
    ]),
    e.make_text([
        "Make ongoing training a habit: complete refreshers when your employer offers them, recheck your own ID-checking and refusal skills regularly, and stay alert to updates in South Carolina alcohol law. Employers who keep every server certified also reduce their liquor-liability insurance requirement, so your continued training directly benefits the business."
    ]),
    e.make_multiple(
        "You hear that South Carolina may have changed a rule about serving hours, but you are not sure. What is the best professional response?",
        [
            "A. Keep serving the way you always have until someone complains",
            "B. Check current South Carolina resources or ask your manager, and complete refresher training to stay current",
            "C. Guess based on what other bars do",
            "D. Ignore it; training only matters when you are first hired",
        ],
        1,
        "Laws and rules change over time. Staying current through refresher training and checking authoritative South Carolina resources or your manager is part of responsible, ongoing professional conduct.",
    ),
    e.make_text([
        "Businesses open after 5 p.m. that sell alcohol for on-premises consumption must carry at least $1 million in liquor-liability coverage. South Carolina lets a business lower that requirement through risk mitigation -- for example, a $100,000 reduction when every server completes the SC Alcohol Server Certificate within 60 days of hire, or when the business stops serving at midnight (a $250,000 reduction). This is a direct financial reason your training and responsible service matter to your employer. Relevant statute: SC Code Section 61-2-145."
    ]),
    e.make_text([
        "If an intoxicated guest later causes harm, the establishment can share civil liability. Under South Carolina law a business is no longer liable for more than 50% of the damages from a DUI incident, and responsibility can be apportioned among multiple parties if a jury agrees. Responsible service -- cutting off intoxicated guests and refusing illegal sales -- is how you and your employer limit this exposure. Relevant statutes: SC Code Sections 15-38-15 through 15-38-40 and 61-2-147."
    ]),
    e.make_text([
        "South Carolina restricts alcohol promotions that encourage over-consumption. For on-premises consumption, a business may not advertise, sell, or dispense beer, wine, or liquor for free, at less than half the regular price, or on a two-for-one basis. It is also illegal to run a 'drinking contest' or 'drinking game.' Relevant statutes: SC Code Sections 61-4-160 and 61-6-4550."
    ]),
    e.make_text([
        "Curbside and drive-thru alcohol sales are prohibited. A permit holder or employee may not sell or deliver beer or wine to anyone who remains in a motor vehicle during the transaction -- this rule specifically bans drive-in, drive-thru, and curb service alcohol sales. Relevant statute: SC Code of Regulations 7-202.5."
    ]),
    e.make_text([
        "When you complete this course and pass the test, your Alcohol Server Certificate is issued through the South Carolina Department of Revenue (SCDOR). You can access your approved certificate and its certificate number through the MYDORWAY portal. Keep your certificate number -- employers and regulators may ask you to confirm your certification."
    ]),
]

anchor = e.find_first(s6, "management")
if anchor == -1:
    anchor = 3
print(f"anchor={anchor}, slides before={len(s6)}")

e.insert_after(s6, anchor, new)
e.reflow(s6)
e.save(d)
print(f"slides after={len(s6)}")
