// Formatting authority for the House Style Spec. This builder exists for
// format only: its output is labeled DO NOT SUBMIT and is never uploaded.
// New builders copy its structure and spacing, then swap in real content that
// traces to documents/cv/approved-bullets.md or to a dated user answer.
//
//   npm install
//   node cv/build_resume_example.js
//   soffice --headless --convert-to pdf --outdir cv "cv/<file>.docx"
//   python3 cv/verify_resume_layout.py "cv/<file>.pdf" --docx "cv/<file>.docx"
const path = require("path");
const L = require(path.join(__dirname, "build_epsilon_lib.js"));
const profile = L.profile;
const c = [];
c.push(...L.header(profile.name));

c.push(L.heading("Education"));
c.push(L.eduSchool(profile.school, profile.location));
c.push(L.eduDegree("B.S. Example Engineering", "Expected June 20XX"));
c.push(L.plain("GPA: X.XX/4.0", { italics: true }));

c.push(L.heading("Skills"));
c.push(L.skill("Languages:", "Python, TypeScript, SQL"));
c.push(L.skill("Frontend:", "React, Next.js, HTML, CSS, accessibility"));
c.push(L.skill("Backend and Cloud:", "Node.js, PostgreSQL, Docker, REST"));
c.push(L.skill("Practice:", "pytest, GitHub Actions, code review"));

c.push(L.heading("Professional Experience"));

c.push(L.roleLine("Example Company", "Software Engineering Intern", "June 2026 - August 2026"));
c.push(L.bullet("Replace this bullet with a confirmed outcome: what changed, by how much, and how"));
c.push(L.bullet("Every bullet is one sentence, leads with the result, and names the stack that produced it"));
c.push(L.bullet("Each entry carries 2 to 5 bullets; the last one is marked final so it gets the 6pt gap", { final: true }));

c.push(L.heading("Projects"));

c.push(L.roleLine("Example Project", "Lead Developer", "March 2026 - June 2026"));
c.push(L.bullet("Name the users, the measured effect, and the technology, in that order"));
c.push(L.bullet("Do not put a repository URL in a bullet; the header GitHub link is the only one", { final: true }));

L.write(c, path.join(__dirname, `${profile.name} - EXAMPLE - DO NOT SUBMIT.docx`));
