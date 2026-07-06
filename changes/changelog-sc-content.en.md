Changelog - sc-content.en.json Well Covered pass

Date: 2026-07-06

Scope:
- Updated `dist/sc-content/sc-content.en.json` only for course content.
- Updated `dist/index.html` so the QA viewer renders image placeholders as labeled dashed boxes.
- Added `changes/image-briefs-sc.md` with Gemini prompts for all image placeholders.
- Did not edit the final exam directly. The final exam pool benefits from the new in-content knowledge checks.

Reviewer goal:
- Raised the SC DBHDD/OSUS Curriculum Evaluation Tool outcomes toward the "Well Covered" standard by naming rubric outcomes directly, adding statute-specific slides from the SCDOR Legal Supplement, adding applied scenarios, and adding reinforcement questions.

Validation:
- `python changes/tools/sc_audit.py`
  - JSON OK.
  - Total slides: 626.
  - Unit counts: U1 72, U2 72, U3 144, U4 83, U5 109, U6 74, U7 72.
  - All 35 rubric rows covered.
- Order-index validation passed for all seven units.
- Image placeholder scan found 7 asset IDs:
  - `sc-img-bac-chart`
  - `sc-img-dob-math`
  - `sc-img-id-anatomy`
  - `sc-img-idcheck-steps`
  - `sc-img-intoxication-signs`
  - `sc-img-standard-drink`
  - `sc-img-vertical-vs-horizontal`

Major content additions:
- Unit 1: Added explicit permit and licensing slides for PBW, PO7, PLB, PLC, LOP; license display; operating without a permit; concealed-weapons restrictions; and a permit scenario question.
- Unit 2: Added BAC factor depth, prescription/OTC/illegal drug interaction guidance, tolerance guidance, legal BAC thresholds, a BAC scenario question, and standard-drink/BAC image placeholders.
- Unit 3: Added a full ID-checking cluster covering valid ID forms, DOB location, vertical vs. horizontal license cues, required DOB math, consistent ID checks, fake/altered ID detection, illegal ID handling, ID-check procedure, underage-sale penalties, straw-purchase transfer, required underage signage, scholarship/life consequences, and multiple scenario questions.
- Unit 4: Added intoxication-sign categories, problem-drinking recognition, when to involve management/security, safe transportation emphasis, and an intoxication response question.
- Unit 5: Added refusal scripts, escalation process, house-policy/incident-reporting guidance, accountability attitude language, and refusal/escalation scenario questions.
- Unit 6: Added ongoing training/refresher/self-assessment expectations, liquor-liability insurance requirements, dram-shop/apportioned liability, responsible marketing restrictions, drive-thru/curbside prohibition, MYDORWAY certificate language, and a refresher-training scenario question.
- Unit 7: Replaced vague statistics language with sourced SC statistics, added SCDPS/NHTSA/SLED figures, added DUI penalty tiers, felony DUI, implied consent, open-container rules, and related questions.

SC statistics added:
- 2023 NHTSA FARS / SCDPS: 413 alcohol-impaired-driving fatalities in South Carolina.
- 2023 NHTSA FARS / SCDPS: BAC 0.08%+ involved in 39% of fatal-crash drivers.
- 2023 SCDPS Traffic Collision Fact Book: 5,319 alcohol- or drug-involved collisions, 367 killed, 3,372 injured.
- 2023 SCDPS Traffic Collision Fact Book: roughly one DUI-collision death every 21.2 hours.
- SLED: DUI arrests rose 24.6% statewide from 2022 to 2023.
- SCDPS: 2024 mileage death rate 1.68 fatalities per 100 million miles traveled, about 40% higher than the national rate of 1.20.

Legal supplement topics reinforced:
- Sale to underage persons and prima facie ID-check evidence.
- Required underage-warning sign.
- Transfer of alcohol to underage persons.
- Permit types and operating limits.
- Display of licenses.
- Operating without a permit.
- Serving age and bartender age rules.
- Sales to intoxicated persons and permit-holder penalties.
- Discount pricing, drinking games, and responsible marketing.
- Drive-in, drive-thru, and curb-service prohibition.
- DUI, unlawful alcohol concentration, felony DUI, implied consent, and open container.
- Liquor-liability insurance and risk mitigation.
- Liability and damages.
- Concealed weapons in alcohol-serving businesses.
- Scholarship consequences for alcohol-related violations.

Out of scope / owner follow-up:
- The review form's "linear navigation / final exam" issue is a platform/LMS behavior item, not a JSON content item.
- Operational items marked TBD by the reviewer, such as SCDOR reporting, proctoring, fee limits, records retention, and certificate issuance workflow, should be confirmed outside this JSON content pass.
