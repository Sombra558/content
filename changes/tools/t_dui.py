import sc_edit as e


data = e.load()
s7 = e.section(data, 7)

anchor = e.find_first(s7, "DUI")
if anchor == -1:
    anchor = e.find_first(s7, "driving")
if anchor == -1:
    anchor = 6

new = [
    e.make_completion(
        "South Carolina DUI penalties increase with each offense: {{item_1}} {{item_2}} {{item_3}} {{item_4}} Even a first offense can mean jail, fines, and license suspension.",
        [
            {
                "id": "item_1",
                "title": "First offense",
                "revealed_text": "Up to a $400 fine ($992 with assessments and surcharges), 48 hours to 30 days in jail, and driver's license suspension for 6 months.",
            },
            {
                "id": "item_2",
                "title": "Second offense",
                "revealed_text": "A $2,100 to $5,100 fine ($10,744.50 with assessments and surcharges), 5 days to 1 year in jail, and driver's license suspension for 1 year.",
            },
            {
                "id": "item_3",
                "title": "Third offense",
                "revealed_text": "A $3,800 to $6,300 fine ($13,234.50 with assessments and surcharges), 60 days to 3 years in jail, and driver's license suspension for 2 years; if within 5 years of the first offense, suspension is 4 years.",
            },
            {
                "id": "item_4",
                "title": "Fourth offense",
                "revealed_text": "Imprisonment from 1 to 5 years and permanent revocation of the driver's license.",
            },
        ],
    ),
    e.make_text(
        [
            "South Carolina's DUI law covers driving while under the influence of alcohol to the extent that the person's faculties to drive are materially and appreciably impaired. A BAC of 0.08% or higher creates an inference that the person was under the influence, and a BAC between 0.05% and 0.08% may be considered with other evidence. Relevant statutes: SC Code Sections 56-5-2930, 56-5-2933, and 56-5-2940."
        ]
    ),
    e.make_text(
        [
            "Felony DUI applies when impaired driving causes great bodily injury or death. If great bodily injury occurs, the mandatory penalty is a fine of $5,100 to $10,100 ($21,119.50 with assessments and surcharges) and imprisonment from 30 days to 15 years. If death occurs, the mandatory penalty is a fine of $10,100 to $25,100 ($52,244.50 with assessments and surcharges) and imprisonment from 1 to 25 years. Relevant statute: SC Code Section 56-5-2945."
        ]
    ),
    e.make_text(
        [
            "Implied consent means that anyone who drives in South Carolina is considered to have given consent to breath, blood, or urine testing when law enforcement alleges an alcohol- or drug-related violation. Refusing the test triggers an automatic 90-day driver's license suspension for drivers age 21 or older, or 180 days if the person had a prior alcohol-related conviction or suspension within the previous 10 years. Relevant statutes: SC Code Sections 56-5-2950 and 56-5-2951."
        ]
    ),
    e.make_text(
        [
            "South Carolina's open-container law prohibits having an open container of beer, wine, or liquor in a moving vehicle of any kind, except in the luggage compartment. A conviction can result in a fine of up to $100 or imprisonment for up to 30 days. Open-container rules matter to servers because letting guests leave with unfinished drinks increases legal risk for the guest and the establishment. Relevant statutes: SC Code Sections 61-4-110 and 61-6-4020."
        ]
    ),
    e.make_multiple(
        "A guest says they can refuse a breath test because they never agreed to testing. What should a server understand about South Carolina law?",
        [
            "A. Refusal has no consequence if the person is polite",
            "B. Driving in South Carolina is treated as implied consent to testing, and refusal can trigger an automatic license suspension",
            "C. Implied consent applies only to commercial drivers",
            "D. Refusal is allowed after midnight",
        ],
        1,
        "Under South Carolina implied-consent law, driving in the state is treated as consent to testing when an alcohol- or drug-related violation is alleged. Refusal can trigger an automatic license suspension.",
    ),
    e.make_multiple(
        "A guest wants to take an unfinished open beer in the car for the ride home. What is the correct response?",
        [
            "A. Allow it if the passenger holds it",
            "B. Do not allow it; South Carolina prohibits open containers of beer, wine, or liquor in a moving vehicle except in the luggage compartment",
            "C. Allow it if the driver is not intoxicated",
            "D. Pour it into a coffee cup",
        ],
        1,
        "South Carolina prohibits open containers of beer, wine, or liquor in a moving vehicle, except in the luggage compartment. Do not let guests leave with open alcohol for the car.",
    ),
]

e.insert_after(s7, anchor, new)
e.reflow(s7)
e.save(data)
