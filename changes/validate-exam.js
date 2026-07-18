const exam = require('../final-exam.sc.json');
const bank = require('./content-quiz-bank.json');

function norm(s) {
  return String(s || '')
    .toLowerCase()
    .replace(/[\u200b\u00a0]/g, '')
    .replace(/[^a-z0-9 ]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}
function strip(s) {
  return norm(String(s).replace(/^[A-D]\.\s*/i, ''));
}

const issues = [];

if (exam.questions.length !== 80) issues.push('Expected 80 questions, got ' + exam.questions.length);

const seen = new Set();
for (const q of exam.questions) {
  const key = norm(q.text);
  if (seen.has(key)) issues.push('Duplicate: Q' + q.order);
  seen.add(key);

  if (!q.options || q.options.length !== 4) issues.push('Q' + q.order + ' needs 4 options');
  const corrects = (q.options || []).filter((o) => o.correct);
  if (corrects.length !== 1) issues.push('Q' + q.order + ' correct count=' + corrects.length);

  for (const o of q.options || []) {
    if (/[\u200b]/.test(o.text) || /[\u200b]/.test(q.text)) issues.push('Q' + q.order + ' has zero-width chars');
    if (!o.correct && /ask another customer|join in|change the story|encourage speed|serve a double|wait until they fall|^[A-D]\. Ignore /i.test(o.text)) {
      issues.push('Q' + q.order + ' cartoon distractor: ' + o.text);
    }
  }

  // Match bank (allow DOB year addition)
  let hit = bank.find((b) => norm(b.question) === key);
  if (!hit && /june 1, 2026/.test(key)) {
    hit = bank.find((b) => /june 5, 2005/.test(norm(b.question)));
  }
  if (!hit && key.endsWith('step')) {
    hit = bank.find((b) => norm(b.question).startsWith(key));
  }
  if (!hit) {
    issues.push('Q' + q.order + ' not found in content bank: ' + q.text.slice(0, 80));
    continue;
  }
  const examCorrect = strip(corrects[0].text);
  const bankCorrect = strip(hit.correct[0]);
  // Compare core meaning (first 50 chars often enough for long answers)
  if (!(examCorrect.includes(bankCorrect.slice(0, 40)) || bankCorrect.includes(examCorrect.slice(0, 40)))) {
    issues.push('Q' + q.order + ' correct answer mismatch vs content');
    issues.push('  exam: ' + examCorrect.slice(0, 80));
    issues.push('  bank: ' + bankCorrect.slice(0, 80));
  }
}

// Specific factual checks
const dob = exam.questions.find((q) => /September 2, 2005/.test(q.text));
if (!dob || !/July 6, 2026/.test(dob.text)) issues.push('Missing dated DOB question');
const dob2 = exam.questions.find((q) => /June 5, 2005/.test(q.text));
if (!dob2 || !/2026/.test(dob2.text)) issues.push('June DOB question missing year 2026');
if (exam.questions.some((q) => /June 5, 2004/.test(q.text))) issues.push('Bad DOB year 2004 still present');

const stats = exam.questions.find((q) => /NHTSA|0\.08/.test(q.text));
const statsCorrect = stats?.options.find((o) => o.correct)?.text;
if (!/39%/.test(statsCorrect || '')) issues.push('Stats correct answer should be ~39%');

console.log(issues.length ? 'ISSUES:\n' + issues.join('\n') : 'VALIDATION PASSED');
console.log('Questions:', exam.questions.length);

// Print short catalog
for (const q of exam.questions) {
  const c = q.options.find((o) => o.correct);
  console.log('Q' + String(q.order).padStart(2, '0') + ' | ' + c.text.replace(/^[A-D]\.\s*/, '').slice(0, 70));
  console.log('     ' + q.text.slice(0, 100));
}
