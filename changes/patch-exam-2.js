const fs = require('fs');
const path = require('path');
const exam = require('../final-exam.sc.json');

function setOpt(qOrder, letter, text) {
  const q = exam.questions.find((x) => x.order === qOrder);
  const o = q.options.find((x) => x.text.startsWith(letter + '.'));
  o.text = `${letter}. ${text}`;
}

// Q3 — replace cartoon "serve as a test"
setOpt(3, 'C', 'Accept a photo of their ID on a phone');

// Q7 — replace "serve one drink and monitor"
setOpt(7, 'D', 'Serve one drink while you wait for them to find an ID');

// Q27 — differentiate A/B distractors (both were "almost 21")
setOpt(27, 'B', 'Complete the sale if they show any secondary card, even if expired');

// Q33 — polish remaining weak distractors
setOpt(33, 'A', 'Serve one more drink since they are still seated and ordering');
setOpt(33, 'D', 'Move them to a quieter seat and continue alcohol service');

// Q70 — soft-ignore rewrite did not fit the stem
setOpt(70, 'B', 'Serve them because they asked you instead of your coworker');

// Q9 — polish
setOpt(9, 'A', 'Serve quickly so they leave sooner');

// Q21 — friend confirmation is fine as a distractor; just make A more specific
setOpt(21, 'A', 'Complete the sale quickly to keep the line moving');
setOpt(21, 'C', 'Skip the ID check because they insist they are 21');

// Q42 — improve "No risk" cartoon
setOpt(42, 'B', 'No special risk beyond a normal table');

// Clean zero-width / weird whitespace in all text
for (const q of exam.questions) {
  q.text = q.text.replace(/[\u200b\u00a0]/g, '').replace(/\s+/g, ' ').trim();
  for (const o of q.options) {
    o.text = o.text.replace(/[\u200b\u00a0]/g, '').replace(/\s+/g, ' ').trim();
  }
}

// Ensure orders are sequential
exam.questions.forEach((q, i) => {
  q.order = i + 1;
  q.options.forEach((o, j) => {
    o.order = j;
  });
});

fs.writeFileSync(path.join(__dirname, '..', 'final-exam.sc.json'), JSON.stringify(exam, null, 2) + '\n');

// Final limp check
const weak = [];
for (const q of exam.questions) {
  const bodies = q.options.map((o) => o.text.replace(/^[A-D]\.\s*/, '').toLowerCase());
  if (new Set(bodies).size !== 4) weak.push('dup options Q' + q.order);
  const corrects = q.options.filter((o) => o.correct);
  if (corrects.length !== 1) weak.push('correct Q' + q.order);
  for (const o of q.options) {
    if (!o.correct && /as a test|ask another customer|join in|change the story|encourage speed|wait until they fall|serve a double/i.test(o.text)) {
      weak.push(`Q${q.order}: ${o.text}`);
    }
  }
}
console.log(weak.length ? weak.join('\n') : 'Clean');
console.log('Done, questions=', exam.questions.length);
