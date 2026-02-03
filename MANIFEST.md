# Federal Trial Counsel Skill - MANIFEST

## Skill Overview

**Name:** federal-trial-counsel
**Version:** 1.1.0
**Court:** U.S. District Court, Middle District of Florida (Orlando Division)
**Circuit:** Eleventh Circuit Court of Appeals

## File Structure

```
federal-trial-counsel/
├── SKILL.md                           # Main skill definition
├── MANIFEST.md                        # This file
│
├── scripts/
│   └── courtlistener/                 # Case law research module
│       ├── index.ts                   # Main exports
│       ├── client.ts                  # API client with retry/backoff
│       ├── types.ts                   # TypeScript type definitions
│       ├── format.ts                  # Markdown formatting
│       ├── cli.ts                     # Command-line interface
│       ├── skill.json                 # Module metadata
│       ├── README.md                  # Module documentation
│       └── examples.md                # Usage examples
│
├── modules/
│   ├── board_risk_dashboard.md        # Executive risk briefing templates
│   ├── case_timeline_builder.md       # Litigation timeline generator
│   ├── case_analysis_engine.md        # Comprehensive case analysis (0-100 scoring)
│   ├── strategy_scoring_system.md     # Strategy scorecard with verdict probability
│   └── mandamus_engine.md             # Federal writ of mandamus litigation engine
│
└── assets/
    └── templates/
        ├── pleadings/
        │   ├── complaint_federal.md       # Federal complaint template
        │   ├── notice_of_removal.md       # Removal to federal court
        │   └── answer_federal.md          # Answer with affirmative defenses
        │
        ├── motions/
        │   ├── tro_motion.md              # TRO/emergency relief
        │   ├── preliminary_injunction.md  # Preliminary injunction
        │   ├── motion_to_dismiss.md       # Rule 12(b) motion
        │   ├── summary_judgment.md        # Rule 56 motion
        │   ├── motion_to_compel.md        # Rule 37(a) motion
        │   ├── motion_for_sanctions.md    # Rule 11/37/§1927/inherent power
        │   ├── motions_in_limine.md       # Pre-trial evidentiary motions
        │   └── post_trial_motions.md      # JMOL, new trial, alter judgment
        │
        ├── discovery/
        │   ├── initial_disclosures.md         # Rule 26(a)(1) disclosures
        │   ├── interrogatories_first_set.md   # Rule 33 interrogatories
        │   ├── requests_for_production.md     # Rule 34 document requests
        │   ├── requests_for_admission.md      # Rule 36 RFAs
        │   ├── deposition_notice.md           # Rule 30 deposition notices
        │   ├── subpoena_third_party.md        # Rule 45 subpoenas
        │   ├── expert_disclosure.md           # Rule 26(a)(2) expert disclosures
        │   └── discovery_response_template.md # Response templates & objections
        │
        └── workflows/
            ├── case_intake_workflow.md        # Initial case assessment
            ├── trial_preparation_workflow.md  # 90-day trial prep checklist
            └── appeal_workflow.md             # Post-judgment appeal process
```

## File Descriptions

### Core Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition with FRCP/FRE expertise, jurisdiction analysis, and procedural guidance |
| `MANIFEST.md` | Index of all files and their procedural purposes |

### CourtListener Research Module

| File | Purpose |
|------|---------|
| `scripts/courtlistener/index.ts` | Main entry point - `searchCourtListener()` function |
| `scripts/courtlistener/client.ts` | HTTP client with authentication, retry/backoff, pagination |
| `scripts/courtlistener/types.ts` | TypeScript interfaces for input/output |
| `scripts/courtlistener/format.ts` | Markdown formatting for search results |
| `scripts/courtlistener/cli.ts` | Command-line interface for manual searches |
| `scripts/courtlistener/skill.json` | Module metadata and configuration |
| `scripts/courtlistener/README.md` | Module documentation |
| `scripts/courtlistener/examples.md` | Research scenario examples |

### Litigation Intelligence Modules

| File | Purpose | Output |
|------|---------|--------|
| `modules/board_risk_dashboard.md` | Executive-level legal risk assessment | Board briefing (.md) |
| `modules/case_timeline_builder.md` | Automatic case chronology and deadline tracking | Timeline (.md) |
| `modules/case_analysis_engine.md` | Comprehensive case strength analysis with 0-100 scoring | Full analysis report (.md) |
| `modules/strategy_scoring_system.md` | Litigation strategy scorecard with verdict probability | Strategy scorecard (.md) |
| `modules/mandamus_engine.md` | Federal writ of mandamus litigation builder (28 U.S.C. § 1361) | Complete mandamus case workspace |

### Pleading Templates

| File | Rule | Purpose |
|------|------|---------|
| `complaint_federal.md` | FRCP 8 | Federal civil complaint with Twombly/Iqbal guidance |
| `notice_of_removal.md` | 28 U.S.C. § 1446 | Removal from state to federal court |
| `answer_federal.md` | FRCP 8(b), 12 | Answer with affirmative defenses and counterclaims |

### Motion Templates

| File | Rule | Purpose |
|------|------|---------|
| `tro_motion.md` | FRCP 65(b) | Emergency TRO with Winter factors |
| `preliminary_injunction.md` | FRCP 65(a) | Preliminary injunction with evidentiary hearing |
| `motion_to_dismiss.md` | FRCP 12(b) | Motion to dismiss (12(b)(1), 12(b)(6)) |
| `summary_judgment.md` | FRCP 56 | Summary judgment with Local Rule 3.01(c) |
| `motion_to_compel.md` | FRCP 37(a) | Compel discovery with meet-and-confer |
| `motion_for_sanctions.md` | Rule 11/37/§1927 | Sanctions for misconduct |
| `motions_in_limine.md` | FRE 104, 401-403 | Pre-trial evidentiary exclusions |
| `post_trial_motions.md` | FRCP 50, 59 | JMOL, new trial, alter judgment |

### Discovery Templates

| File | Rule | Purpose |
|------|------|---------|
| `initial_disclosures.md` | FRCP 26(a)(1) | Mandatory initial disclosures |
| `interrogatories_first_set.md` | FRCP 33 | 25 interrogatories with verification |
| `requests_for_production.md` | FRCP 34 | 30 RFPs with ESI protocol |
| `requests_for_admission.md` | FRCP 36 | 30 RFAs with strategic guidance |
| `deposition_notice.md` | FRCP 30 | Individual and 30(b)(6) corporate notices |
| `subpoena_third_party.md` | FRCP 45 | Third-party subpoenas (banks, carriers, social media) |
| `expert_disclosure.md` | FRCP 26(a)(2) | Retained and non-retained expert disclosures |
| `discovery_response_template.md` | FRCP 33, 34, 36 | Response templates with common objections |

### Workflow Templates

| File | Phase | Purpose |
|------|-------|---------|
| `case_intake_workflow.md` | Pre-litigation | 7-phase intake with jurisdiction analysis |
| `trial_preparation_workflow.md` | Pre-trial | 90-day trial prep with trial notebook |
| `appeal_workflow.md` | Post-judgment | 11th Circuit appeal process |

## Capabilities

### Document Generation
- Federal complaints (diversity, federal question, CAFA)
- Answers with affirmative defenses
- Removal notices with jurisdiction analysis
- TRO/preliminary injunction motions (Winter factors)
- Motions to dismiss (12(b)(1), 12(b)(6))
- Summary judgment motions
- Motions to compel discovery
- Sanctions motions (Rule 11, 37, § 1927)
- Motions in limine (7 categories)
- Post-trial motions (JMOL, new trial)
- Complete discovery packages
- Proposed orders for all motions

### Legal Research
- CourtListener API integration for case law
- Middle District of Florida precedent
- Eleventh Circuit controlling authority
- Supreme Court foundational cases

### Case Analysis & Strategy
- **Case Analysis Engine**: Comprehensive 0-100 scoring
  - Jurisdiction strength (10%)
  - Claims/defenses viability (25%)
  - Evidence quality (20%)
  - Damages/exposure (15%)
  - Procedural posture (10%)
  - Settlement factors (10%)
  - Trial factors (10%)
- **Strategy Scoring System**: Verdict probability modeling
- **Risk Dashboard**: Board-level risk assessment
- **Timeline Builder**: Automatic chronology generation
- **Mandamus Engine**: Complete mandamus case builder
  - Three-element test analysis
  - TRAC factors for unreasonable delay
  - Viability scoring (0-100)
  - Defense preemption analysis
  - Full pleading generation

### Expertise Areas
- Federal jurisdiction (diversity, federal question, supplemental)
- Removal and remand
- Emergency injunction practice (TRO, PI)
- **Mandamus practice (28 U.S.C. § 1361, All Writs Act)**
- Discovery procedure and disputes
- Expert witness practice (Daubert)
- Motions practice
- Class action defense
- White-collar defense
- Regulatory enforcement
- Administrative law and agency inaction
- Appeals (11th Circuit)

## Usage

### Invoke the Skill

```
/federal-trial-counsel
```

### Example Commands

```
"Draft a TRO motion to stop defendant from [conduct]"
"Analyze whether this case can be removed to federal court"
"Search for qualified immunity cases in the Middle District of Florida"
"Generate a board-level risk assessment for this matter"
"Create a case timeline from these documents"
"Analyze my case and provide a full strategy report"
"Draft interrogatories for a breach of contract case"
"Prepare a motion for sanctions under Rule 11"
"Build Mandamus Case: [case name]"
"Draft a mandamus petition against USCIS for visa delay"
"Analyze mandamus viability for agency inaction"
```

### CourtListener Search (CLI)

```bash
cd scripts/courtlistener
npx ts-node cli.ts --q "preliminary injunction" --court flmd --after 2023-01-01
```

## Analysis Output Format

When generating case analysis or responding to discovery/motions, the skill produces comprehensive .md reports including:

1. **Case Summary** - Parties, claims, procedural history
2. **Jurisdiction Analysis** - Subject matter and personal jurisdiction
3. **Claims/Defenses Assessment** - Element-by-element analysis
4. **Evidence Inventory** - Available evidence with strength ratings
5. **Damages Analysis** - Compensatory, punitive, statutory
6. **Strategic Assessment** - SWOT analysis
7. **Scoring** - 0-100 overall score with component breakdown
8. **Recommendations** - Prioritized action items
9. **Risk Assessment** - Verdict probability and settlement range

## Dependencies

- Node.js 18+ (for CourtListener module)
- TypeScript (for CourtListener module)
- No external npm dependencies (uses native fetch)

## Environment Variables

| Variable | Purpose | Required |
|----------|---------|----------|
| `COURTLISTENER_API_TOKEN` | API token for higher rate limits | Optional |

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025 | Initial release |
| 1.1.0 | 2026 | Complete template library, case analysis engine, strategy scoring |
| 1.2.0 | 2026 | Federal Writ of Mandamus Engine (28 U.S.C. § 1361, All Writs Act) |

---

*This skill is designed for the U.S. District Court, Middle District of Florida. Adapt templates for other districts as needed.*
