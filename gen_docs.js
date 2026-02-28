const { 
  Document, Packer, Paragraph, TextRun, AlignmentType, 
  LevelFormat, BorderStyle, UnderlineType, TabStopType, TabStopPosition,
  ExternalHyperlink
} = require('docx');
const fs = require('fs');

const args = JSON.parse(process.argv[2]);
const { role, company, jd, roleType, outputDir, isAI } = args;

// ─── PROFILE DATA ────────────────────────────────────────────
const CONTACT = {
  name: 'AMRETHA KARTHIKEYAN',
  address: '#02-321 153 Gangsa Road, Singapore-670153',
  mobile: '+65-90256503',
  email: 'amretha.ammu@gmail.com',
  linkedin: 'https://www.linkedin.com/in/amretha-nishanth-534b39101/'
};

// Determine which CV variant to use
function getCVVariant(roleType) {
  const rt = (roleType || '').toLowerCase();
  if (rt.includes('digital product') || rt.includes('dpm')) return 'DPM';
  if (rt.includes('product owner') || rt.includes(' po')) return 'PO';
  if (rt.includes('product manager') && !rt.includes('digital')) return 'PO';
  if (rt.includes('ai product') || rt.includes('ai/ml')) return 'DPM';
  return 'BA'; // default
}

const variant = getCVVariant(roleType);

// ─── CV CONTENT BY VARIANT ───────────────────────────────────
const CV_DATA = {
  DPM: {
    headline: 'Digital Product Manager | Product Owner (AI & Data Platforms)',
    summary: `Digital Product Manager / Product Owner with 5+ years of experience delivering large-scale digital platforms across financial services and enterprise environments. Proven expertise in owning product roadmaps, managing Agile delivery, translating user needs into scalable solutions, and driving data-informed product decisions. Experienced in partnering with UX, engineering and senior stakeholders to launch customer-centric digital products. Strong focus on AI-powered platforms, data-driven product growth and continuous improvement.`,
    kpmgTitle: 'Digital Product Manager',
    kpmgBullets: [
      'Led end-to-end product lifecycle from ideation to launch for large-scale digital transformation initiatives serving financial institutions',
      'Owned product vision, roadmap and backlog prioritisation, translating business objectives into clear user stories and sprint deliverables using Agile/SAFe methodology',
      'Partnered closely with UX designers, architects and engineering teams to deliver user-centric digital platforms and workflow enhancements',
      'Managed multiple cross-functional stakeholders and vendors across concurrent workstreams, ensuring alignment on timelines, scope and delivery outcomes',
      'Drove data-informed product decisions by defining KPIs, analysing performance metrics and identifying continuous product improvement opportunities',
      'Built business cases and executive presentations for new product features, securing stakeholder approval and contributing to a 5% increase in project profitability',
      'Acted as Product Lead for key roadmap initiatives, overseeing UAT, go-live planning and operational readiness across business units',
      'Supported automation and AI-enabled solution design, including API integrations, improving efficiency and reducing manual effort by up to 30 man-days',
    ],
    achievements: [
      'Performed accurate Impact Analysis and persuaded clients to approve Change Request items, generating additional profit of ~5% of Project Cost',
      'Delivered automation solution for Interest Computation (financial services), saving 30 man-days of manual work',
      'Led cross-functional team through critical Sprint-to-SIT transition, maintaining project delivery timeline',
    ],
    skills: 'AI-enabled Product Integration, MVP Definition & Go-To-Market, Management Consulting, Agile/SAFe 6.0, JIRA, Excel, Microsoft Project, Product Vision & Roadmapping, Business Analysis, Risk Mitigation & Change Management, Budget Forecasting & Variance Analysis, KPI Tracking & Dashboard Reporting, Tableau, Power BI, PSQL, Python, API Integrations, Stakeholder Management',
  },
  PO: {
    headline: 'Business Analyst Lead | Product Owner | Product Manager',
    summary: `Lead Business Analyst and Product Owner with 5+ years of experience driving digital product delivery, backlog ownership and cross-functional alignment across financial services and enterprise environments. SAFe 6.0 certified Product Owner with proven ability to translate business objectives into actionable roadmaps, manage stakeholder expectations and deliver measurable outcomes in Agile environments.`,
    kpmgTitle: 'Lead Business Analyst – Product Owner',
    kpmgBullets: [
      'Defined and drove product vision, roadmap and delivery strategy for large-scale digital transformation initiatives for financial institutions',
      'Owned and prioritised product backlog, ensuring alignment with business objectives, regulatory requirements and customer experience goals',
      'Collaborated with cross-regional stakeholders (UX, architecture, finance) to drive alignment across engineering and operations functions',
      'Facilitated sprint ceremonies including planning, reviews, retrospectives and PI Planning as SAFe 6.0 certified Product Owner',
      'Managed internal reporting cycles, change requests and approval workflows contributing to a 5% increase in project profitability',
      'Trained vendors and managed go-live execution plans, ensuring process continuity across business units',
      'Conducted internal workshops to drive operational readiness and team-wide coordination',
      'Designed, documented and executed end-to-end test scenarios on Loan IQ Product Applications (M&A, Trade, WCL, FA) with JIRA defect management',
    ],
    achievements: [
      'Performed accurate Impact Analysis and persuaded clients to approve Change Request items, generating additional profit of ~5% of Project Cost',
      'Analysed and provided solutioning for Automated Interest Computation (financial services), saving 30 man-days of work',
      'Led team through critical Sprint-to-SIT transition, maintaining project delivery timeline',
    ],
    skills: 'SAFe 6.0 Product Owner/PM, Agile, JIRA, Product Vision & Roadmapping, Backlog Management, Business Analysis, Risk Mitigation & Change Management, Stakeholder Management, Budget Forecasting & Variance Analysis, KPI Tracking & Dashboard Reporting, Tableau, Power BI, PSQL, Python, Excel, Microsoft Project, API Integrations, Data Migration, Workshop Facilitation',
  },
  BA: {
    headline: 'Business Analyst Lead | Product Owner | Sales & Operations Excellence',
    summary: `Lead Business Analyst with 5+ years of experience supporting senior leadership through business planning, financial operations and cross-functional project execution. Proven ability to streamline processes, manage executive stakeholder communications, track KPIs, drive operational alignment and cost profitability. SAFe 6.0 certified with strong background in fintech, banking and enterprise digital transformation.`,
    kpmgTitle: 'Lead Business Analyst – Functional Consultant',
    kpmgBullets: [
      'Partnered with Enterprise Singapore on large-scale digital transformation projects',
      'Supported executive decision-making through As-Is/To-Be analysis and streamlined documentation of strategic processes across finance teams',
      'Collaborated with cross-regional stakeholders (UX, architecture, finance) to drive alignment across engineering and operations functions',
      'Managed internal reporting cycles, change requests and approval workflows contributing to a 5% increase in project profitability',
      'Owned and prioritised product backlog, ensuring alignment with business objectives, regulatory requirements and customer experience goals',
      'Trained vendors and managed go-live execution plans, ensuring process continuity across business units',
      'Designed, documented and executed end-to-end test scenarios on Loan IQ Product Applications (M&A, Trade, WCL, FA)',
      'Led testers, interns and junior BAs for Scrum activities including Planning, Closure and Retrospectives',
    ],
    achievements: [
      'Performed accurate Impact Analysis and persuaded clients to approve Change Request items, generating additional profit of ~5% of Project Cost',
      'Analysed and provided solutioning for Automated Interest Computation (financial services), saving 30 man-days of work',
      'Led team through critical Sprint-to-SIT transition phase, maintaining project delivery timeline',
    ],
    skills: 'Management Consulting, Agile, JIRA, Excel, Microsoft Project, Product Vision & Roadmapping, Business Analysis, Risk Mitigation & Change Management, Budget Forecasting & Variance Analysis, KPI Tracking & Dashboard Reporting, Event & Workshop Facilitation, Tableau, Power BI, PSQL, Python, API Integrations, Stakeholder Management, Data Migration',
  }
};

const cv = CV_DATA[variant];

// AI project bullet (added when role is AI-related)
const AI_BULLET = 'Built 3 production web applications leveraging advanced AI prompting with Claude Opus 4.6 and Sonnet 4.6 (Anthropic) and GitHub Copilot, demonstrating hands-on AI product development from requirements through to deployment';

// Extract JD keywords to sprinkle into summary (simple keyword matching)
function getJDKeywords(jd) {
  if (!jd) return [];
  const keywords = [
    'agile','scrum','kanban','product roadmap','stakeholder','user story','sprint','backlog',
    'data-driven','analytics','api','ux','fintech','digital transformation','go-to-market',
    'saas','b2b','b2c','kpi','okr','sql','python','tableau','power bi','jira','confluence',
    'ai','machine learning','llm','generative ai','product-led','growth','payments','lending',
    'banking','insurance','govtech','ecommerce','platform','mobile','web','cloud','aws','azure'
  ];
  const jdLower = jd.toLowerCase();
  return keywords.filter(k => jdLower.includes(k)).slice(0, 8);
}

// ─── STYLING HELPERS ─────────────────────────────────────────
const FONT = 'Times New Roman';
const NAME_SIZE = 32;
const SECTION_SIZE = 24;
const BODY_SIZE = 22;
const SMALL_SIZE = 20;

function nameRun(text) {
  return new TextRun({ text, font: FONT, size: NAME_SIZE, bold: true });
}
function sectionHeader(text) {
  return new Paragraph({
    spacing: { before: 160, after: 60 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: '000000', space: 1 } },
    children: [new TextRun({ text, font: FONT, size: SECTION_SIZE, bold: true, allCaps: true })]
  });
}
function boldPara(text, size = BODY_SIZE) {
  return new Paragraph({
    spacing: { before: 80, after: 20 },
    children: [new TextRun({ text, font: FONT, size, bold: true })]
  });
}
function normalPara(text, size = BODY_SIZE, spacing = { before: 40, after: 20 }) {
  return new Paragraph({ spacing, children: [new TextRun({ text, font: FONT, size })] });
}
function bulletPara(text) {
  return new Paragraph({
    numbering: { reference: 'bullets', level: 0 },
    spacing: { before: 30, after: 30 },
    children: [new TextRun({ text, font: FONT, size: BODY_SIZE })]
  });
}
function twoColPara(left, right) {
  return new Paragraph({
    spacing: { before: 40, after: 20 },
    tabStops: [{ type: TabStopType.RIGHT, position: 9360 }],
    children: [
      new TextRun({ text: left, font: FONT, size: BODY_SIZE, bold: true }),
      new TextRun({ text: '\t', font: FONT, size: BODY_SIZE }),
      new TextRun({ text: right, font: FONT, size: BODY_SIZE, bold: true }),
    ]
  });
}

// ─── BUILD RESUME ─────────────────────────────────────────────
function buildResume() {
  const jdKw = getJDKeywords(jd);
  const isAIRole = isAI || (jd && /(ai|machine learning|llm|generative|artificial intelligence)/i.test(jd));
  
  // Enhance summary with JD keywords if relevant
  let summary = cv.summary;

  const bullets = [...cv.kpmgBullets];
  if (isAIRole) bullets.push(AI_BULLET);

  const children = [
    // ── HEADER ──
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 40 },
      children: [nameRun(CONTACT.name)]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 20 },
      children: [new TextRun({ text: CONTACT.address, font: FONT, size: BODY_SIZE, bold: true })]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 20 },
      children: [
        new TextRun({ text: `Mobile: ${CONTACT.mobile}, email:`, font: FONT, size: BODY_SIZE, bold: true }),
        new TextRun({ text: CONTACT.email, font: FONT, size: BODY_SIZE, bold: true }),
      ]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 40 },
      children: [new TextRun({ text: CONTACT.linkedin, font: FONT, size: BODY_SIZE, bold: true, color: '0000FF' })]
    }),
    // Role headline
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 80 },
      children: [new TextRun({ text: cv.headline, font: FONT, size: BODY_SIZE, bold: true })]
    }),

    // ── SUMMARY ──
    sectionHeader('SUMMARY:'),
    normalPara(summary, BODY_SIZE, { before: 60, after: 60 }),

    // ── ACADEMIC QUALIFICATION ──
    sectionHeader('ACADEMIC QUALIFICATION:'),
    twoColPara('Master of Science Engineering Business Management', 'July 2019 – Nov 2020'),
    normalPara('Coventry University, UK'),
    twoColPara('Bachelor of Engineering', 'July 2012 – June 2016'),
    normalPara('Electronics & Communication Engineering'),
    normalPara('Anna University, India'),

    // ── SKILL SET ──
    sectionHeader('SKILL SET:'),
    new Paragraph({
      spacing: { before: 40, after: 20 },
      children: [
        new TextRun({ text: 'Data visualization tools: ', font: FONT, size: BODY_SIZE, bold: true }),
        new TextRun({ text: 'Tableau, Power BI', font: FONT, size: BODY_SIZE }),
      ]
    }),
    new Paragraph({
      spacing: { before: 40, after: 20 },
      children: [
        new TextRun({ text: 'Programming: ', font: FONT, size: BODY_SIZE, bold: true }),
        new TextRun({ text: 'PSQL, Python basics', font: FONT, size: BODY_SIZE }),
      ]
    }),
    new Paragraph({
      spacing: { before: 40, after: 20 },
      children: [
        new TextRun({ text: 'Others: ', font: FONT, size: BODY_SIZE, bold: true }),
        new TextRun({ text: cv.skills, font: FONT, size: BODY_SIZE }),
      ]
    }),
    new Paragraph({
      spacing: { before: 40, after: 40 },
      children: [
        new TextRun({ text: 'Certification: ', font: FONT, size: BODY_SIZE, bold: true }),
        new TextRun({ text: 'Scaled Agile Framework 6.0 Product Owner/Product Management', font: FONT, size: BODY_SIZE }),
      ]
    }),

    // ── PROFESSIONAL EXPERIENCE ──
    sectionHeader('PROFESSIONAL EXPERIENCE:'),
    twoColPara('KPMG, Singapore', 'Feb 2021 – Present'),
    boldPara(cv.kpmgTitle),
    normalPara('Roles and Responsibilities:', BODY_SIZE, { before: 60, after: 20 }),
    ...bullets.map(b => bulletPara(b)),
    normalPara('Key Achievements:', BODY_SIZE, { before: 60, after: 20 }),
    ...cv.achievements.map(a => bulletPara(a)),

    // J.P. Morgan
    new Paragraph({ spacing: { before: 80, after: 0 }, children: [] }),
    twoColPara('J.P. Morgan', ''),
    boldPara('Asset Management Virtual Internship                            Oct 2023 – Jan 2024'),
    normalPara('Roles and Responsibilities:', BODY_SIZE, { before: 40, after: 20 }),
    bulletPara('Helped Traders and clients build stronger investment portfolios with market-leading solutions'),
    bulletPara('Gathered business requirements from end users; built robust investor profiles through structured questionnaires'),
    bulletPara('Performed quantitative fundamental analysis of 5 stocks and recommended to 2 clients based on risk appetite metrics'),
    bulletPara('Measured investment success via KPIs: Annual Portfolio Return, Portfolio Variance, Portfolio Standard Deviation'),

    // Amazon
    new Paragraph({ spacing: { before: 80, after: 0 }, children: [] }),
    twoColPara('Amazon Inc, India', 'Mar 2018 – Mar 2019'),
    boldPara('Business Analyst'),
    normalPara('Roles and Responsibilities:', BODY_SIZE, { before: 40, after: 20 }),
    bulletPara('Analysed and translated business requirements into functional and non-functional specifications'),
    bulletPara('Worked closely with stakeholders to understand needs, scope problems and develop business cases from data'),
    normalPara('Key Achievements:', BODY_SIZE, { before: 40, after: 20 }),
    bulletPara('Developed real-time monitoring quality metrics using Power BI importing data from SQL Server and MS Excel'),
    bulletPara('Analysed and visualised data using Tableau/Power BI model building'),
    bulletPara('Analysed customer engagement patterns on e-commerce platform, contributing to 5% increase in customer retention'),
  ];

  const doc = new Document({
    numbering: {
      config: [{
        reference: 'bullets',
        levels: [{ level: 0, format: LevelFormat.BULLET, text: '\u2022', alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 360, hanging: 260 } } } }]
      }]
    },
    styles: {
      default: { document: { run: { font: FONT, size: BODY_SIZE } } },
      paragraphStyles: [
        { id: 'Title', name: 'Title', basedOn: 'Normal', next: 'Normal',
          run: { font: FONT, size: NAME_SIZE, bold: true },
          paragraph: { alignment: AlignmentType.CENTER, spacing: { before: 0, after: 40 } } },
        { id: 'Normal', name: 'Normal', basedOn: 'Normal',
          run: { font: FONT, size: BODY_SIZE },
          paragraph: { spacing: { before: 40, after: 20 } } },
      ]
    },
    sections: [{
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 720, right: 900, bottom: 720, left: 900 }
        }
      },
      children
    }]
  });

  return doc;
}

// ─── BUILD COVER LETTER ───────────────────────────────────────
function buildCoverLetter() {
  const isAIRole = isAI || (jd && /(ai|machine learning|llm|generative|artificial intelligence)/i.test(jd));
  const today = new Date().toLocaleDateString('en-SG', { day: 'numeric', month: 'long', year: 'numeric' });

  // Determine key skills emphasis by variant
  const variantHighlight = {
    DPM: 'product roadmap ownership, AI-enabled platform delivery and data-driven decision making',
    PO: 'SAFe 6.0 product ownership, backlog management and Agile delivery leadership',
    BA: 'business analysis, process optimisation and cross-functional stakeholder management'
  }[variant];

  const aiLine = isAIRole
    ? ` I have also independently built three production web applications using advanced AI prompting with Claude Opus 4.6 and Sonnet 4.6 and GitHub Copilot, which speaks directly to my hands-on experience with AI product development.`
    : '';

  const body1 = `I am writing to express my strong interest in the ${role} role at ${company}. With over 5 years of experience in ${variantHighlight} within fintech and enterprise environments, I am confident in my ability to contribute meaningfully from day one.`;

  const body2 = `In my current role at KPMG Singapore, I have served as Lead Business Analyst and de-facto Product Owner for Loan IQ — a core banking platform — leading cross-functional squads across engineering, UX and QA. Key highlights include: delivering a 5% increase in project profitability through rigorous impact analysis and stakeholder management; saving 30 man-days through automation of interest computation workflows; and maintaining delivery timelines through critical Sprint-to-SIT transitions.${aiLine}`;

  const body3 = `I am particularly drawn to ${company} because it represents the kind of in-house product environment where I can own outcomes end-to-end — from discovery through to scale — rather than in a consulting capacity. My SAFe 6.0 certification, combined with hands-on experience in backlog ownership, vendor management, data migration and API integrations, positions me well for this role.`;

  const body4 = `I would welcome the opportunity to discuss how my background aligns with your team's goals. Thank you for your consideration.`;

  const children = [
    // Header
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 40 },
      children: [new TextRun({ text: CONTACT.name, font: FONT, size: NAME_SIZE, bold: true })]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 20 },
      children: [new TextRun({ text: `${CONTACT.mobile} | ${CONTACT.email}`, font: FONT, size: BODY_SIZE, bold: true })]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 60 },
      children: [new TextRun({ text: CONTACT.linkedin, font: FONT, size: BODY_SIZE, color: '0000FF' })]
    }),

    // Date + salutation
    normalPara(today, BODY_SIZE, { before: 0, after: 80 }),
    normalPara(`Hiring Manager`, BODY_SIZE, { before: 0, after: 20 }),
    boldPara(company),
    new Paragraph({ spacing: { before: 60, after: 60 }, children: [] }),

    // RE line
    new Paragraph({
      spacing: { before: 0, after: 80 },
      children: [
        new TextRun({ text: 'Re: ', font: FONT, size: BODY_SIZE, bold: true }),
        new TextRun({ text: `Application for ${role}`, font: FONT, size: BODY_SIZE }),
      ]
    }),

    normalPara('Dear Hiring Manager,', BODY_SIZE, { before: 0, after: 80 }),
    normalPara(body1, BODY_SIZE, { before: 0, after: 160 }),
    normalPara(body2, BODY_SIZE, { before: 0, after: 160 }),
    normalPara(body3, BODY_SIZE, { before: 0, after: 160 }),
    normalPara(body4, BODY_SIZE, { before: 0, after: 160 }),
    normalPara('Yours sincerely,', BODY_SIZE, { before: 80, after: 120 }),
    boldPara(CONTACT.name),
  ];

  const doc = new Document({
    styles: {
      default: { document: { run: { font: FONT, size: BODY_SIZE } } },
    },
    sections: [{
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 }
        }
      },
      children
    }]
  });

  return doc;
}

// ─── WRITE FILES ─────────────────────────────────────────────
async function main() {
  const safeCompany = company.replace(/[^a-zA-Z0-9]/g, '_').substring(0, 30);
  const resumePath = `${outputDir}/Resume_${safeCompany}.docx`;
  const coverPath = `${outputDir}/CoverLetter_${safeCompany}.docx`;

  const [resumeBuf, coverBuf] = await Promise.all([
    Packer.toBuffer(buildResume()),
    Packer.toBuffer(buildCoverLetter())
  ]);

  fs.writeFileSync(resumePath, resumeBuf);
  fs.writeFileSync(coverPath, coverBuf);

  console.log(JSON.stringify({ resume: resumePath, cover: coverPath, variant }));
}

main().catch(e => { console.error(e.message); process.exit(1); });
