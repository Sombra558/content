const fs = require('fs');
const path = require('path');

const examPath = path.join(__dirname, '..', 'final-exam.sc.json');
const exam = require(examPath);

const q55 = exam.questions.find((q) => q.order === 55);
q55.options[0].text = 'A. Move on without creating an incident record';
q55.options[2].text = 'C. Alter details later if anyone asks about the refusal';

fs.writeFileSync(examPath, JSON.stringify(exam, null, 2) + '\n');

// Add year to content DOB questions (EN + ES) without reformatting whole files
for (const file of [
  path.join(__dirname, '..', 'dist', 'sc-content', 'sc-content.en.json'),
  path.join(__dirname, '..', 'dist', 'sc-content', 'sc-content.es.json'),
]) {
  if (!fs.existsSync(file)) continue;
  let raw = fs.readFileSync(file, 'utf8');
  const before = raw;
  // Match June 1. ... June 5, 2005 without an intervening 2026
  raw = raw.replace(/June 1(?!, 2026)(\. A customer)/g, 'June 1, 2026$1');
  raw = raw.replace(/June 1(?!, 2026)(\. Un cliente|\. La fecha)/gi, 'June 1, 2026$1');
  // Spanish may differ — also try common ES phrasing via JSON walk below if needed
  fs.writeFileSync(file, raw);
  console.log(path.basename(file), 'changed=', raw !== before);
}

// Spanish-specific DOB string search
const esPath = path.join(__dirname, '..', 'dist', 'sc-content', 'sc-content.es.json');
if (fs.existsSync(esPath)) {
  const es = JSON.parse(fs.readFileSync(esPath, 'utf8'));
  let n = 0;
  function walk(node) {
    if (!node || typeof node !== 'object') return;
    if (typeof node.question === 'string' && /2005/.test(node.question) && /junio|June/i.test(node.question) && !/2026/.test(node.question)) {
      console.log('ES DOB candidate:', node.question.slice(0, 120));
      n++;
    }
    for (const v of Object.values(node)) walk(v);
  }
  walk(es);
  console.log('ES DOB candidates without 2026:', n);
}

// Final sanity
const weak = [];
for (const q of exam.questions) {
  const bodies = q.options.map((o) => o.text.replace(/^[A-D]\.\s*/, '').toLowerCase());
  if (new Set(bodies).size !== 4) weak.push('dup options Q' + q.order + ': ' + bodies.join(' | '));
}
console.log(weak.length ? weak.join('\n') : 'No duplicate options');
console.log('Q55:', q55.options.map((o) => o.text).join(' || '));
