const fs = require('fs');
const exam = require('../final-exam.sc.json');

for (const q of exam.questions) {
  if (q.text.endsWith('?.')) q.text = q.text.replace(/\?\.$/, '?');
  if (/June 5,\s*2005/.test(q.text) && /June 1/.test(q.text) && !/2026/.test(q.text)) {
    q.text =
      "Today's date is June 1, 2026. A customer's date of birth is June 5, 2005. What should you do?";
  }
}

const optionPatches = [
  {
    qIncludes: 'looks under 21',
    from: 'Ask another employee for their opinion and serve',
    to: 'Serve them if a coworker says they look old enough',
  },
  {
    qIncludes: 'I know the owner',
    from: 'Ignore them and walk away without telling anyone',
    to: 'Walk away without repeating the refusal or notifying anyone',
  },
  {
    qIncludes: 'several drinks over a short period',
    from: 'Ignore the behavior and let a coworker handle it',
    to: 'Leave the decision to a coworker while you continue serving',
  },
  {
    qIncludes: 'coworker continues serving a customer who appears intoxicated',
    from: 'Ignore the situation and focus on your own tables',
    to: 'Stay focused on your own tables and assume they will handle it',
  },
  {
    qIncludes: 'refused alcohol due to intoxication. What is the best next step',
    from: 'Ask another server to serve them',
    to: 'Ask another server to resume alcohol service for them',
  },
  {
    qIncludes: 'slurred speech and poor balance',
    from: 'Ask another server to handle it',
    to: 'Pass the decision to another server so you avoid conflict',
  },
  {
    qIncludes: 'forgot their ID but insist they are 21',
    from: 'Ask them to come back later and serve now',
    to: 'Serve now and ask them to bring ID next time',
  },
  {
    qIncludes: 'poor judgment and risk-taking',
    from: 'Continue service because they say they feel fine',
    to: 'Continue normal service because they still seem alert',
  },
  {
    qIncludes: 'visible firearm',
    from: 'Ask other customers what to do',
    to: 'Wait until closing and report it then',
  },
  {
    qIncludes: 'slurring their speech and struggling to stay balanced',
    from: 'Serve them quickly',
    to: 'Serve quickly so they leave sooner',
  },
  {
    qIncludes: 'slurring their speech and struggling to stay balanced',
    from: 'Ask them if they feel okay and serve',
    to: 'Ask if they feel okay, and serve if they say yes',
  },
  {
    qIncludes: 'photo hair and face look different',
    from: 'Sell; the card is probably fine',
    to: 'Sell if they seem confident the card is theirs',
  },
  {
    qIncludes: 'photo hair and face look different',
    from: 'Sell but only beer',
    to: 'Sell beer only, since it is lower risk than liquor',
  },
  {
    qIncludes: 'photo hair and face look different',
    from: 'Ask them to sign for it',
    to: 'Have them sign a note confirming their age and serve',
  },
  {
    qIncludes: 'slides it to a visibly underage',
    from: 'Nothing; the adult bought it legally',
    to: 'Allow it because the adult purchased the drink legally',
  },
  {
    qIncludes: 'slides it to a visibly underage',
    from: 'Charge the underage guest for it',
    to: 'Warn them once, then allow the transfer if they stay quiet',
  },
  {
    qIncludes: 'slides it to a visibly underage',
    from: 'Ask them to move tables',
    to: 'Ask them to move farther from the bar and continue service',
  },
];

let applied = 0;
for (const q of exam.questions) {
  for (const p of optionPatches) {
    if (!q.text.toLowerCase().includes(p.qIncludes.toLowerCase())) continue;
    for (const o of q.options) {
      const body = o.text.replace(/^[A-D]\.\s*/, '');
      if (body === p.from || o.text.includes(p.from)) {
        const letter = o.text.match(/^([A-D])\./)[1];
        o.text = `${letter}. ${p.to}`;
        applied++;
      }
    }
  }
}

const leftovers = [];
for (const q of exam.questions) {
  for (const o of q.options) {
    if (o.correct) continue;
    if (/^(A-D)\. Ignore |Ignore it$|Ask another customer|Join in|Change the story|Encourage speed/i.test(o.text) ||
        /\bIgnore\b/i.test(o.text) ||
        /Ask another customer/i.test(o.text)) {
      leftovers.push(`Q${q.order}: ${o.text}`);
    }
  }
}

fs.writeFileSync(
  require('path').join(__dirname, '..', 'final-exam.sc.json'),
  JSON.stringify(exam, null, 2) + '\n'
);

console.log('Applied option patches:', applied);
console.log('Leftover weak distractors:', leftovers.length);
leftovers.forEach((l) => console.log(' ', l));
console.log(
  'June DOB item:',
  exam.questions.find((q) => /June 5,\s*2005/.test(q.text))?.text
);
