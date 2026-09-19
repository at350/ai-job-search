const fs = require("fs");
const path = require("path");

// Resolve `docx` from the workspace install by default. Set NODE_MODULES_DIR
// when the dependency lives outside this repo.
const docxModule = process.env.NODE_MODULES_DIR
  ? path.join(process.env.NODE_MODULES_DIR, "docx")
  : "docx";

const {
  AlignmentType,
  BorderStyle,
  Document,
  ExternalHyperlink,
  LevelFormat,
  LevelSuffix,
  Packer,
  Paragraph,
  TabStopType,
  TextRun,
} = require(docxModule);

// Candidate identity lives in cv/candidate.json so no script hard-codes a
// name, email, phone, or handle. /setup writes it; edit it by hand otherwise.
const profilePath =
  process.env.CANDIDATE_PROFILE ||
  (fs.existsSync(path.join(__dirname, "candidate.json"))
    ? path.join(__dirname, "candidate.json")
    : path.join(__dirname, "candidate.example.json"));
const profile = JSON.parse(fs.readFileSync(profilePath, "utf8"));

const FONT = "Times New Roman";
const BODY = 22;
const HEAD = 24;
const NAME = 40;
const WARNING = 18;
const WARNING_COLOR = "9C0006";
const RIGHT_TAB = 10440;
const LINE = { after: 0, line: 240, lineRule: "auto" };
// Density rule (spacing-only move toward Jake's Resume white space).
// Bullet paragraphs keep the slightly looser 1.04 line spacing (250/240) and
// now carry 1pt (20 twips) after each ordinary bullet. The final bullet of
// each entry carries 6pt (120 twips) after it to separate entries. Body,
// role, education, and skills lines remain 1.00 with after: 0.
const BULLET_LINE = { ...LINE, line: 250, after: 20 };
const FINAL_BULLET_LINE = { ...BULLET_LINE, after: 120 };

const run = (text, opts = {}) =>
  new TextRun({ text, font: FONT, size: BODY, ...opts });

const center = (children, spacing = LINE) =>
  new Paragraph({ alignment: AlignmentType.CENTER, spacing, children });

const heading = (text) =>
  new Paragraph({
    // Section headers: 8pt (160 twips) before, 2pt (40 twips) after the
    // rule (house style density update).
    spacing: { before: 160, after: 40, line: 240, lineRule: "auto" },
    border: {
      bottom: { style: BorderStyle.SINGLE, size: 4, color: "000000", space: 1 },
    },
    children: [run(text.toUpperCase(), { size: HEAD })],
  });

const roleLine = (organization, role, dates) =>
  new Paragraph({
    spacing: { before: 0, ...LINE },
    tabStops: [{ type: TabStopType.RIGHT, position: RIGHT_TAB }],
    children: [
      run(organization, { bold: true }),
      run(" | "),
      run(role, { italics: true }),
      run("\t"),
      run(dates),
    ],
  });

const eduSchool = (school, location) =>
  new Paragraph({
    spacing: { before: 0, ...LINE },
    tabStops: [{ type: TabStopType.RIGHT, position: RIGHT_TAB }],
    children: [run(school, { bold: true }), run("\t"), run(location)],
  });

const eduDegree = (degree, date) =>
  new Paragraph({
    spacing: LINE,
    tabStops: [{ type: TabStopType.RIGHT, position: RIGHT_TAB }],
    children: [run(degree), run("\t"), run(date)],
  });

const bullet = (text, { final = false, before = 0 } = {}) =>
  new Paragraph({
    style: "Normal",
    numbering: { reference: "bullets", level: 0 },
    spacing: {
      ...(final ? FINAL_BULLET_LINE : BULLET_LINE),
      ...(before ? { before } : {}),
    },
    indent: { left: 720, hanging: 360 },
    children: [run(text)],
  });

const plain = (text, opts = {}) =>
  new Paragraph({ spacing: LINE, children: [run(text, opts)] });

const skill = (label, keywords) =>
  new Paragraph({
    spacing: LINE,
    children: [run(`${label} `, { bold: true }), run(keywords)],
  });

const warningBanner = (text) =>
  center(
    [
      new TextRun({
        text,
        font: FONT,
        size: WARNING,
        bold: true,
        color: WARNING_COLOR,
      }),
    ],
    LINE,
  );

const header = (name) => {
  const out = [];
  out.push(center([run(name, { size: NAME })]));
  out.push(
    center([
      run(
        `${profile.location}  //  ${profile.email}  //  ${profile.phone}  //  `,
      ),
      new ExternalHyperlink({
        link: profile.linkedin_url,
        children: [
          new TextRun({
            text: profile.linkedin,
            font: FONT,
            size: BODY,
            color: "0563C1",
            underline: {},
          }),
        ],
      }),
      run("  //  "),
      new ExternalHyperlink({
        link: profile.github_url,
        children: [
          new TextRun({
            text: profile.github,
            font: FONT,
            size: BODY,
            color: "0563C1",
            underline: {},
          }),
        ],
      }),
    ]),
  );
  return out;
};

const DEFAULT_PAGE_MARGIN = { top: 648, right: 864, bottom: 648, left: 864 };

const buildDocument = (children, { pageMargin = DEFAULT_PAGE_MARGIN } = {}) =>
  new Document({
    numbering: {
      config: [
        {
          reference: "bullets",
          levels: [
            {
              level: 0,
              format: LevelFormat.BULLET,
              text: "●",
              alignment: AlignmentType.LEFT,
              suffix: LevelSuffix.TAB,
              style: {
                run: { font: FONT, size: BODY },
                paragraph: {
                  indent: { left: 720, hanging: 360 },
                  tabStops: [{ type: TabStopType.LEFT, position: 720 }],
                },
              },
            },
          ],
        },
      ],
    },
    styles: {
      default: {
        document: {
          run: { font: FONT, size: BODY },
          paragraph: { spacing: LINE },
        },
      },
      paragraphStyles: [
        {
          id: "Normal",
          name: "Normal",
          basedOn: "Normal",
          next: "Normal",
          run: { font: FONT, size: BODY },
          paragraph: { spacing: LINE },
        },
      ],
    },
    sections: [
      {
        properties: {
          page: {
            size: { width: 12240, height: 15840 },
            margin: pageMargin,
          },
        },
        children,
      },
    ],
  });

const write = (children, outputPath, options = {}) =>
  Packer.toBuffer(buildDocument(children, options)).then((buffer) => {
    fs.writeFileSync(outputPath, buffer);
    console.log(`written ${outputPath}`);
  });

module.exports = {
  profile,
  bullet,
  buildDocument,
  center,
  eduDegree,
  eduSchool,
  header,
  heading,
  plain,
  roleLine,
  run,
  skill,
  warningBanner,
  write,
};
