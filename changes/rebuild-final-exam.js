/**
 * Rebuild final-exam.sc.json from content quiz bank:
 * - Prefer diverse, high-value items (laws, DOB, ID, BAC, refusal, DUI)
 * - Drop near-duplicates
 * - Replace cartoonish distractors with plausible misconceptions
 * - Keep correct answers aligned with course content
 */
const fs = require('fs');
const path = require('path');

const bank = require('./content-quiz-bank.json');
const existing = require('../final-exam.sc.json');

function clean(s) {
  return String(s || '')
    .replace(/[\u200b\u00a0]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}

function stripLetter(s) {
  return clean(s).replace(/^[A-D]\.\s*/i, '');
}

function withLetter(i, text) {
  return `${'ABCD'[i]}. ${stripLetter(text)}`;
}

/** Plausible distractor rewrites keyed by normalized option text */
const DISTRACTOR_FIXES = {
  'ask another customer': 'Accept verbal confirmation from a friend at the table',
  'ask another customer for confirmation': 'Accept verbal confirmation from a friend at the table',
  'ask another customer to confirm': 'Accept verbal confirmation from a friend at the table',
  'ignore the quality issues': 'Accept it if the birthdate looks correct',
  'ignore the inconsistencies': 'Complete the sale if they answer most questions correctly',
  'ignore the exact date': 'Sell if they will turn 21 within the next few days',
  'ignore the expiration date': 'Accept it because the birthdate shows they are over 21',
  'ignore the altered area': 'Accept it if the photo still looks close enough',
  'ignore the photo mismatch': 'Accept it if they can answer questions about the address',
  'ignore the damage and continue': 'Accept it if they insist it was damaged accidentally',
  'ignore them completely': 'End the conversation and hope they leave on their own',
  'ignore the situation completely': 'Continue other work and reassess only if they become violent',
  'ignore the situation and move on': 'Rely on memory later instead of writing anything down',
  'ignore the situation': 'Assume they will handle themselves once they leave',
  'ignore the behavior': 'Wait to see if other guests complain before acting',
  'ignore the behavior unless it worsens': 'Continue service unless they become physically aggressive',
  'ignore the behavior unless it escalates further': 'Continue service unless they become physically aggressive',
  'ignore it unless they appear intoxicated': 'Keep the same pace until clear intoxication appears',
  'ignore it unless they ask for a drink': 'Wait until they order again before deciding',
  'ignore it': 'Stay focused on your own tables and let it go',
  'ignore them': 'Treat subtle signs as less important than loud behavior',
  'ignore the signs': 'Trust their claim that they feel fine',
  'ignore the signs and focus on other customers': 'Prioritize other guests until this one becomes disruptive',
  'ignore the concern': 'Keep serving while you watch from a distance',
  'ignore consumption levels': 'Prioritize speed and assume guests will self-limit',
  'ignore medication and continue service': 'Count only the alcohol and continue normal service',
  'ignore food factor and continue service': 'Continue normal service because two drinks is a low count',
  'ignore behavior and continue service': 'Continue service because they say they feel fine',
  'ignore signs and continue service': 'Continue service because they say they feel fine',
  'ignore the environment and focus only on drink count': 'Base decisions only on drink count, not pace or food',
  'ignore the strength and continue normal service': 'Treat it as one drink and keep the same pace',
  'join in': 'Assume your coworker has a reason and keep serving other guests',
  'serve faster': 'Speed up service so the guest leaves sooner',
  'serve faster to keep up with demand': 'Match their ordering pace to keep the table happy',
  'encourage speed': 'Help them leave quickly so the problem is out of the building',
  'change the story to avoid trouble': 'Rely on memory later instead of writing anything down',
  'raise your voice back': 'Match their volume so they understand you are serious',
  'raise your voice to be heard': 'Speak louder so they understand you are serious',
  'walk away immediately': 'Leave the area without stating the refusal again',
  'let them go': 'Allow them to leave without further involvement',
  'do nothing': 'Skip documentation if the guest eventually leaves',
  'do nothing because service already stopped': 'Stop at cutting them off and take no further action',
  'wait until they fall before acting': 'Wait for clearer physical collapse before intervening',
  'serve a double instead': 'Serve beer or wine instead, assuming Sunday rules do not apply',
  'only after 9 p.m.': 'Sell after dinner hours because age rules are looser then',
  'yes, 2005 means they are 21': 'Yes, any 2005 birth year means they are already 21',
  'pour it into a coffee cup': 'Transfer it to an unmarked cup so it is less obvious',
  'allow it if the passenger holds it': 'Allow it if a passenger, not the driver, holds the open container',
  'allow it if the driver is not intoxicated': 'Allow it if the driver appears sober',
  'refusal has no consequence if the person is polite': 'Refusal has no penalty if the driver cooperates otherwise',
  'implied consent applies only to commercial drivers': 'Implied consent applies only to commercial drivers',
  'refusal is allowed after midnight': 'Testing rules do not apply after midnight',
  'keep serving the way you always have until someone complains': 'Keep current habits until a manager announces a change',
  'guess based on what other bars do': 'Follow what nearby businesses appear to be doing',
  'ignore it; training only matters when you are first hired': 'Skip refresher training unless your employer requires it',
};

function fixDistractor(text) {
  const key = stripLetter(text).toLowerCase();
  if (DISTRACTOR_FIXES[key]) return DISTRACTOR_FIXES[key];
  // Soft patterns
  if (/^ask another customer/i.test(key)) {
    return 'Accept verbal confirmation from a friend at the table';
  }
  if (/^ignore /i.test(key) && key.length < 45) {
    return 'Continue service unless the situation becomes disruptive';
  }
  return stripLetter(text);
}

function toExamQuestion(bankItem, order) {
  const labels = ['A', 'B', 'C', 'D'];
  // Preserve option letter order from content (A-D)
  const byLetter = { A: null, B: null, C: null, D: null };
  for (const opt of [...bankItem.correct, ...bankItem.wrong]) {
    const m = clean(opt).match(/^([A-D])\.\s*(.*)$/i);
    if (!m) continue;
    byLetter[m[1].toUpperCase()] = {
      text: m[2],
      correct: bankItem.correct.some((c) => clean(c) === clean(opt)),
    };
  }

  // If parsing failed, rebuild from arrays
  if (Object.values(byLetter).some((v) => !v)) {
    const correctText = stripLetter(bankItem.correct[0]);
    const wrongs = bankItem.wrong.map(stripLetter);
    // Place correct in original letter if possible
    const correctLetter = (bankItem.correct[0].match(/^([A-D])\./i) || [, 'C'])[1].toUpperCase();
    const letters = ['A', 'B', 'C', 'D'];
    let wi = 0;
    for (const L of letters) {
      if (L === correctLetter) byLetter[L] = { text: correctText, correct: true };
      else byLetter[L] = { text: wrongs[wi++] || 'Continue service without further checks', correct: false };
    }
  }

  const options = labels.map((L, i) => {
    const item = byLetter[L];
    const text = item.correct ? stripLetter(item.text) : fixDistractor(item.text);
    return {
      order: i,
      text: `${L}. ${text}`,
      correct: !!item.correct,
    };
  });

  // Ensure exactly one correct
  const corrects = options.filter((o) => o.correct);
  if (corrects.length !== 1) {
    throw new Error(`Bad correct count for: ${bankItem.question}`);
  }

  return {
    order,
    text: clean(bankItem.question),
    options,
  };
}

/** Curated selection: unique concepts, balanced across units */
const SELECTED_QUESTIONS = [
  // Unit 1 — laws / liability / weapons
  'Your restaurant holds a PLB (Business Liquor by the Drink) license but not a Local Option Permit. A guest asks for a cocktail at 1 p.m. on Sunday. What is correct?',
  'You are working at a restaurant. A customer asks if they can purchase a type of alcohol your location does not normally sell. You are unsure if your business is licensed for it. What should you do?',
  'A young-looking customer orders a drink. They say they forgot their ID but insist they are 21. Their friend offers to confirm their age. What should you do?',
  'You notice a customer becoming loud, unsteady, and slow to respond. They order another drink and mention they will drive home soon. What should you do?',
  'You notice a customer with a visible firearm in an establishment that has posted restrictions against weapons. The customer is calm and not causing a disturbance. What should you do?',
  'You serve a customer who shows clear signs of intoxication. Later, they are involved in an accident after leaving the business. What type of consequences could result?',
  'A customer who looks under 21 attempts to order alcohol but does not have an ID. They insist they are old enough. What should you do?',
  'A customer presents an ID that looks damaged and does not clearly match their appearance. They insist it is valid. What is the best action?',
  'You notice a customer slurring their speech and struggling to stay balanced. They order another drink. What should you do?',

  // Unit 2 — BAC / physiology
  'Two guests each had three drinks in an hour. One appears far more impaired than the other. What is the best explanation for a server to keep in mind?',
  'A guest orders several drinks quickly. Within a short time, you notice slower speech and unsteady movement. The guest insists they feel fine and asks for another drink. Based on alcohol absorption and effects, what is the safest action?',
  'A guest orders two strong mixed drinks in a short time. You notice faster speech and reduced coordination. The guest asks for another drink right away. Based on BAC and standard drink understanding, what is the safest action?',
  'A guest has been drinking slowly but mentions they have not eaten all day. After two drinks, you notice quicker mood changes and reduced coordination. The guest asks for another drink. What is the safest action?',
  'A guest drinks several beverages and then orders coffee. They say they are fine to continue drinking because the coffee “sobers them up.” What is the safest response?',
  'A guest has one drink but shows strong drowsiness and poor coordination. They mention taking medication earlier. They ask for another drink. What is the safest action?',
  'A guest orders strong mixed drinks back to back. They appear alert but show poor judgment and risk-taking behavior. What is the best response?',
  'A guest says they “feel fine” after several drinks. You observe slurred speech and unsteady walking. What should guide your decision?',

  // Unit 3 — ID / underage / DOB
  "Today is July 6, 2026. A customer's ID shows a date of birth of September 2, 2005. Can you sell them alcohol?",
  'A customer hands you a license. The photo hair and face look different, the card feels bumpy around the birth date, and the person cannot recall their own ZIP code. What should you do?',
  'An adult guest orders a beer, then immediately slides it to a visibly underage companion at the table. What is the correct response?',
  'A customer appears young but insists they are 21. You are unsure and the line is growing. What should you do?',
  'A customer cannot provide valid identification but insists they are over 21 and becomes frustrated. What should you do?',
  'A customer presents an ID that appears valid, but it is expired. They insist it should still be accepted. What should you do?',
  'A customer presents an ID that looks real, but the print appears blurry and the edges seem uneven. What should you do?',
  'A customer correctly answers questions about their ID, but you still feel unsure about its authenticity. What should you do?',
  'A customer becomes frustrated when you take extra time to check their ID carefully. What is the best response?',
  'Today’s date is June 1. A customer’s date of birth is June 5, 2005. What should you do?',
  'A customer presents an ID with a clear photo, but the birthdate looks scratched and altered. What should you do?',
  'A customer presents an ID that seems valid, but their answers do not match the information. They become impatient and ask you to hurry. What should you do?',
  'A customer without ID becomes loud and insists you serve them because others are waiting. What should you do?',
  'A customer gives an ID, but the photo does not clearly match their face. What should you do?',
  'A customer cannot answer basic questions about their ID and avoids eye contact. What should you do?',

  // Unit 4 — recognizing intoxication
  'A guest is slurring words, swaying on the stool, and just knocked over a glass while reaching for their drink. What should you do?',
  'A guest begins speaking loudly, stumbling slightly, and struggling to focus on conversation. What stage of impairment are they most likely in?',
  'A guest is stumbling, has slurred speech, and is spilling their drink repeatedly. What should you do?',
  'A guest becomes loud, interrupts others, and starts arguing with staff after several drinks. What is the best action?',
  'A guest has not eaten, is drinking quickly, and is in a loud group celebrating. What is the best approach?',
  'A guest is ordering drinks quickly and has not eaten. What is the best way to prevent over-service?',
  'A guest is repeatedly ordering drinks, showing mood swings, and ignoring your attempts to slow service. What should you do?',
  'A guest orders two drinks quickly and begins speaking loudly. They are laughing and encouraging others to drink faster. What is your best first step?',
  'A guest has glassy eyes, is repeating themselves, and drops their credit card twice. What do these signs indicate?',
  'A guest has not eaten, is drinking quickly, and is part of a loud celebration group. What risk is present?',
  'A guest insists they are fine but is stumbling and knocking into furniture. What should you rely on?',
  'A guest becomes argumentative and ignores your attempts to slow service. What is the best next step?.',
  'A quiet guest appears calm but has slow reactions and unfocused eyes. What should you do?',

  // Unit 5 — refusal / escalation
  "A guest becomes irritated after you refuse another drink and says, 'I know the owner. Serve me anyway.' What should you do?",
  'A server cuts off a visibly intoxicated guest. The guest leaves angry and starts walking toward the parking lot with car keys in hand. What is the best next step?',
  'A customer is slurring words, stumbling, and becoming loud. They ask for another drink. What should you do?',
  'You observe a customer showing clear signs of intoxication. What is the correct first step?',
  'After refusing service, a customer continues asking for another drink. What should you do?',
  'A customer becomes upset after being refused service and raises their voice. What is the best response?',
  'A customer becomes confrontational after being refused service and begins arguing loudly. What should you do?',
  'A customer becomes loud, refuses to leave, and starts making threats after being refused service. What should you do?',
  'A customer has been refused alcohol due to intoxication. What is the best next step?',
  'After refusing service to an intoxicated customer, what should you do to protect yourself legally?',
  'A customer shows slurred speech and poor balance but asks for another drink. What should you do?',
  'After refusing service, a customer asks for “just water” but continues requesting alcohol. What should you do?',
  'A customer refuses to leave after being denied service and begins bothering other guests. What is the correct action?',
  'You refused service and the customer becomes quiet but unsteady. What should you do next?',

  // Unit 6 — management / culture / promotions
  'A customer has had several drinks over a short period and is beginning to show signs of intoxication. What should you do next?',
  'You hear that South Carolina may have changed a rule about serving hours, but you are not sure. What is the best professional response?',
  'A customer becomes upset after you refuse service due to signs of intoxication. They raise their voice and demand another drink. What should you do next?',
  'A group is participating in a drink special and begins ordering drinks quickly. One customer is showing early signs of intoxication. What should you do?',
  'A customer orders a strong cocktail with multiple shots and finishes it quickly. They ask for another right away. What should you do?',
  'A coworker continues serving a customer who appears intoxicated. What should you do?',
  'A customer shows an ID that looks damaged and hard to read. You are unsure if it is valid. What should you do?',
  'You are unsure whether a customer is intoxicated. What is the best next step?',
  'A busy shift makes it hard to track how much customers are drinking. What should you do?',
  'A customer asks for multiple drinks at once for themselves. What is your best response?',
  'A coworker refuses service and the customer asks you for a drink instead. What should you do?',

  // Unit 7 — DUI / enforcement / real world
  'A guest says they can refuse a breath test because they never agreed to testing. What should a server understand about South Carolina law?',
  "A guest wants to take an unfinished open beer in the car for the ride home. What is the correct response?",
  "According to NHTSA FARS data, roughly what share of drivers in South Carolina's fatal crashes in 2023 had a blood alcohol concentration of 0.08% or higher?",
  'A guest has been drinking for several hours. It is late, and they plan to drive home. They show slower reactions and reduced awareness. What is the best action?',
  'A guest is stumbling, bumps into others, and drops a glass. They laugh and ask for another drink. What is the best action?',
  'A group becomes loud and disruptive near closing time. One guest is clearly intoxicated and tries to leave to drive home. Nearby customers are uncomfortable. What should you do?',
  'An officer enters your establishment during a busy shift and observes service. A guest who appears underage approaches the bar. What should you do?',
  'A guest shows clear signs of intoxication but insists they are fine and asks for another drink. What should you do?',
  'A guest has had several drinks and begins speaking slowly. They ask for another drink and mention driving home. What should you do?',
  'A guest tries to leave quickly after heavy drinking and says they are driving. What should you do?',
];

function norm(s) {
  return clean(s)
    .toLowerCase()
    .replace(/[^a-z0-9 ]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}

const byNorm = new Map();
for (const b of bank) {
  byNorm.set(norm(b.question), b);
}

const missing = [];
const selected = [];
for (const q of SELECTED_QUESTIONS) {
  const hit = byNorm.get(norm(q));
  if (!hit) missing.push(q);
  else selected.push(hit);
}

if (missing.length) {
  console.error('Missing from bank:', missing.length);
  missing.forEach((m) => console.error(' -', m));
  process.exit(1);
}

if (selected.length !== 80) {
  console.error('Expected 80 questions, got', selected.length);
  process.exit(1);
}

// Extra DOB year fix safety: never use 2004 with June 1 without year context that makes refuse correct
for (const item of selected) {
  if (/june 5,\s*2004/i.test(item.question)) {
    item.question = item.question.replace(/2004/g, '2005');
  }
}

const questions = selected.map((item, i) => toExamQuestion(item, i + 1));

// Final QA
const cartoon = [];
const askCustomer = [];
for (const q of questions) {
  for (const o of q.options) {
    if (o.correct) continue;
    const t = o.text.toLowerCase();
    if (/ask another customer|join in|change the story|encourage speed|serve a double|wait until they fall/.test(t)) {
      cartoon.push(`Q${q.order}: ${o.text}`);
    }
    if (/ignore\b/.test(t)) askCustomer.push(`Q${q.order}: ${o.text}`);
  }
  const c = q.options.filter((o) => o.correct);
  if (c.length !== 1) throw new Error('correct count ' + q.order);
}

const out = {
  exam: existing.exam,
  questions,
};

const outPath = path.join(__dirname, '..', 'final-exam.sc.json');
fs.writeFileSync(outPath, JSON.stringify(out, null, 2) + '\n');

console.log('Wrote', questions.length, 'questions to final-exam.sc.json');
console.log('Remaining cartoon patterns:', cartoon.length);
cartoon.forEach((c) => console.log(' ', c));
console.log('Remaining ignore-* distractors:', askCustomer.length);
askCustomer.slice(0, 20).forEach((c) => console.log(' ', c));

// Coverage summary
const units = {};
for (const item of selected) {
  const u = item.section.split(/[–—]/)[0].trim();
  units[u] = (units[u] || 0) + 1;
}
console.log('Unit coverage:', units);
