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

function stripLetter(s) {
  return norm(String(s).replace(/^[A-D]\.\s*/i, ''));
}

const mismatches = [];
for (const q of exam.questions) {
  const hit = bank.find((b) => norm(b.question) === norm(q.text));
  if (!hit) continue;
  const examCorrect = q.options.filter((o) => o.correct).map((o) => stripLetter(o.text));
  const bankCorrect = hit.correct.map(stripLetter);
  const ok = examCorrect.some((ec) =>
    bankCorrect.some((bc) => bc.includes(ec) || ec.includes(bc) || ec.slice(0, 40) === bc.slice(0, 40))
  );
  if (!ok) {
    mismatches.push({ order: q.order, exam: examCorrect, bank: bankCorrect, q: q.text.slice(0, 100) });
  }
}
console.log('Correct-answer mismatches vs content:', mismatches.length);
mismatches.forEach((m) => console.log(JSON.stringify(m, null, 2)));

const groups = {};
for (const q of exam.questions) {
  const k = norm(q.text).slice(0, 55);
  (groups[k] = groups[k] || []).push(q.order);
}
console.log('\nNear-dup clusters:');
Object.entries(groups)
  .filter(([, v]) => v.length > 1)
  .forEach(([k, v]) => console.log(v.join(','), '-', k));

console.log('\nQ23 full:');
const q23 = exam.questions.find((q) => q.order === 23);
console.log(JSON.stringify(q23, null, 2));
