# SC Alcohol Course Content — "Well Covered" Upgrade Design

Date: 2026-07-06
Target file: `dist/sc-content/sc-content.en.json` (English only; Spanish sync is a later pass)
Driver: SC DBHDD/OSUS Curriculum Evaluation Tool review (reviewed 6/22/26) + SCDOR Legal Supplement

## Goal

Raise **every** rubric outcome in the state's Curriculum Evaluation Tool to **Well Covered** ("comprehensively addressed, all relevant components fully explored and clearly presented"). This includes both the outcomes the reviewer rated below "Covered" and the ones already rated "Covered". Reviewer's overall comment: "Use the SCDOR Legal Supplement and the checklists provided" — so statutes are cited explicitly throughout.

## Non-Goals

- Final exam edits. The state accepted the exam; it pools questions from content, so improving in-content questions improves the exam automatically.
- Spanish JSON (`sc-content.es.json`) — translated later.
- Platform/LMS fixes. The "linear navigation — Not Met (final exam)" finding and the TBD operational criteria (SCDOR reporting, MYDORWAY certificate flow, proctoring, 5-year records, fee) are operational, not content. Flagged to the owner; one cheap content win included (see §7).
- Actual image generation. Placeholders only, with a briefs doc for Gemini.

## Reviewer Findings Summary

**Not Addressed (2):**
1. Recent SC law-enforcement information (drunk driving, accidents, injuries, fatalities statistics)
2. Ongoing training participation (refreshers, self-assessments, digital modules)

**Implied (6):** key SC laws (permitting/licensing, DUI, concealed weapons); legal responsibility not to sell to minors/intoxicated (attitudinal); avoiding sale > customer satisfaction (attitudinal); responses avoiding negative life consequences for minors (attitudinal); state laws + consequences for sale to minors/intoxicated (performance); state penalties for servers selling to minors (performance).

**Mentioned (10):** life consequences to minors; ID-check procedure incl. fake/illegal ID handling; ID anyone appearing underage; penalties for underage sale; business ops (responsible marketing, liability, standard drink size); calculate required DOB; three valid ID forms in SC; locate DOB on ID; apply DOB comparison; demonstrate thorough ID-check procedure.

**Covered (16, still need boost to Well Covered):** BAC/physiology; help for problem drinking; intoxication signs; manager as resource; list of sales-staff responsibilities; fake-ID detection (performance row); handling difficult situations; refusal techniques; escalation procedures; house policies; responsible marketing attitudes; training/professional conduct value; confidence/self-efficacy in refusal; accountability culture; compliance/ethics norms; job-responsibility choices.

## The "Well Covered" Recipe (applied per rubric outcome)

1. **Named explicitly** — slide text uses the rubric's own vocabulary so the reviewer can find it (e.g., "calculate the required date of birth", "three valid forms of identification").
2. **Statute anchor** — citation + short verbatim excerpt from the SCDOR Legal Supplement.
3. **Components enumerated** — every sub-bullet in the rubric row treated individually.
4. **Applied scenario** — worked example or mini-case.
5. **Reinforcement** — interactive/knowledge-check slide per cluster (these feed the final-exam question pool).
6. **Visual** — only where it genuinely helps (see §6).

## Work Sections

### 1. Stats injection — Unit 7 (Not Addressed → Well Covered)

- Web-research current SC data: SCDOT Traffic Collision Fact Book, SCDPS, NHTSA state data (alcohol-related fatalities, alcohol-involved crash share, DUI arrests, underage-drinking stats).
- Every figure carries source + year in slide text. No invented numbers; only verified figures are used.
- Rewrite the ~6 existing vague Unit 7 slides (currently say "a notable portion of fatalities" with no numbers) + insert ~3-5 new statistics slides + 1 stats infographic image placeholder.

### 2. Ongoing training — Unit 6 (Not Addressed → Well Covered)

- 2-3 new slides: refresher-training expectation, self-assessment habit, staying current when laws change, digital-module retraining. Framed as professional norms plus management practice.

### 3. ID-checking cluster — Unit 3 primarily (9 rubric rows, Mentioned → Well Covered)

- **Three valid SC ID forms**: dedicated slide with explicit list + statute cite; knowledge check.
- **DOB calculation**: dedicated "today's date minus 21 years" method slide + worked examples + practice interaction.
- **Locate DOB on ID**: new slide with ID-anatomy image placeholder.
- **Vertical vs. horizontal license**: currently zero mentions; add (SC under-21 licenses are vertical).
- **Fake ID detection**: security-features checklist slide (holograms, microprint, edges, photo swap, feel), plus handling/confiscation rules for illegal IDs.
- **Step-by-step procedure**: a named, numbered ID-check sequence slide (feel the card, look at security features, compare photo/DOB, ask verifying questions, decision).
- **ID anyone appearing underage**: explicit consistency policy slide (e.g., "if they appear under 30/35, check") tied to house policy.

### 4. Statute explicitness — Units 1, 3 (Implied → Well Covered)

Pattern per user direction: **one statute per slide** — statute number + short verbatim excerpt from the Legal Supplement + one-line server takeaway. This lengthens the course and reduces repetition. Targets:

- Unit 1: permitting/licensing incl. permit types (PBW, PO7, PLB, PLC, LOP); concealed weapons in alcohol businesses (§ 23-31-215); DUI (§ 56-5-2930 et seq.); transfer/sale to minors (§ 63-19-2440/2450, § 61-4-90); hours/Sunday restrictions.
- Unit 3: server-specific penalties enumerated per offense (criminal fine/jail ranges, administrative fines, permit consequences) with explicit "if you are caught, you personally face…" framing.
- Attitudinal rows fixed with direct-statement edits in existing scenario slides: refusing a sale always outranks making a sale or pleasing a customer; consequences to the minor's life named concretely (criminal record, license loss, school/job impact).

### 5. Covered→Well Covered boost pass — all units

Light-touch depth pass on the 12 already-"Covered" rows. Per row: verify explicit naming, add 1-2 depth slides for rubric sub-bullets that are thin, add a scenario where missing. Targets include: drug-alcohol interactions and individual tolerance (U2), problem-drinking intervention resources (U4/U5), manager-as-resource concrete workflows (U6), escalation procedures with named steps (U5), house-policy enforcement incl. incident reporting (U6).

### 6. Images — targeted placeholders (~10-14)

- JSON placeholder inserted in slide contents; exact schema confirmed against the QA viewer (`dist/index.html`) before insertion so nothing breaks.
- New doc `changes/image-briefs-sc.md`: one entry per image — unit/slide reference, alt text, and the full Gemini generation prompt.
- Image list: ID anatomy with DOB highlighted; vertical vs. horizontal SC license comparison; three valid ID forms; DOB-math visual; BAC chart; standard drink equivalents; signs-of-intoxication grid; refusal body-language; required minor-sale signage; DUI stats infographic; escalation flowchart; ID-check step sequence.

### 7. Cheap operational win

Strengthen the single MYDORWAY mention into a clear closing slide: after passing, the certificate is issued through SCDOR and retrievable via MYDORWAY with certificate number. Addresses two TBD core criteria at the content level.

## Estimated Volume

~80-110 new slides, ~60 edited slides across all 7 units. Course lengthens, supporting the 4-hour minimum criterion.

## Verification

1. JSON validity check (parse) after every editing session.
2. Rubric audit script: grep-style scan proving each of the ~30 rubric rows maps to at least one slide using the rubric's vocabulary; output a coverage table.
3. Visual QA via existing `dist/index.html` viewer.
4. Update `changes/changelog-sc-content.es.md` (or an EN counterpart) documenting the pass.

## Risks

- Stats freshness: use the most recent published year available; cite year explicitly so future updates are easy.
- Slide-count inflation must stay pedagogically sound — statute slides always carry a plain-language takeaway, never bare legal text.
- `order_index` reflow required within units when inserting slides; script-driven, not manual.
