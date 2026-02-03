# Federal Trial Counsel - Claude Code Skill

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ███████╗███████╗██████╗ ███████╗██████╗  █████╗ ██╗                        ║
║   ██╔════╝██╔════╝██╔══██╗██╔════╝██╔══██╗██╔══██╗██║                        ║
║   █████╗  █████╗  ██║  ██║█████╗  ██████╔╝███████║██║                        ║
║   ██╔══╝  ██╔══╝  ██║  ██║██╔══╝  ██╔══██╗██╔══██║██║                        ║
║   ██║     ███████╗██████╔╝███████╗██║  ██║██║  ██║███████╗                   ║
║   ╚═╝     ╚══════╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝                   ║
║                                                                               ║
║   ████████╗██████╗ ██╗ █████╗ ██╗          ██████╗ ██████╗ ██╗   ██╗███╗  ██╗║
║   ╚══██╔══╝██╔══██╗██║██╔══██╗██║         ██╔════╝██╔═══██╗██║   ██║████╗ ██║║
║      ██║   ██████╔╝██║███████║██║         ██║     ██║   ██║██║   ██║██╔██╗██║║
║      ██║   ██╔══██╗██║██╔══██║██║         ██║     ██║   ██║██║   ██║██║╚████║║
║      ██║   ██║  ██║██║██║  ██║███████╗    ╚██████╗╚██████╔╝╚██████╔╝██║ ╚███║║
║      ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝     ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚══╝║
║                                                                               ║
║                    🦅  U.S. District Court Specialist  🦅                     ║
║                                                                               ║
║   ┌───────────────────────────────────────────────────────────────────────┐  ║
║   │  ⚖️  40+ Federal Claims  │  📊 MTD Risk Scoring  │  🎯 19 Engines    │  ║
║   │  📋 Twombly/Iqbal       │  🔍 Auto-Suggest      │  📁 FRCP Mastery  │  ║
║   └───────────────────────────────────────────────────────────────────────┘  ║
║                                                                               ║
║              Middle District of Florida │ 11th Circuit │ FRCP/FRE            ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

Elite United States federal trial attorney and strategic legal advisor for U.S. District Courts with comprehensive civil litigation expertise.

## Overview

This Claude Code skill transforms Claude into a senior federal trial attorney with deep expertise in federal civil litigation, from complaint drafting through appeal. It includes:

- **40+ Federal Causes of Action** with element-by-element analysis
- **19 Litigation Strategy Engines** for complete case management
- **Twombly/Iqbal Compliant** pleading generation
- **MTD Risk Scoring** (0-100) with vulnerability fixes
- **Auto-Trigger Workflow** for seamless case analysis

## Installation

### As Claude Code Skill

1. Copy this directory to `~/.claude/skills/federal-trial-counsel/`
2. The skill auto-activates when federal litigation topics are detected

### Build the Pleading Engine

```bash
cd scripts/federal_pleading_engine
npm install
npm run build
```

## Features

### Federal Pleading Engine

Location: `scripts/federal_pleading_engine/`

The engine generates Rule 12(b)(6)-resilient federal complaints with:

| Feature | Description |
|---------|-------------|
| **Elements Analysis** | Maps facts to required legal elements for each claim |
| **Plausibility Hardening** | Ensures Twombly/Iqbal compliance |
| **Rule 9(b) Detection** | Heightened pleading for fraud-based claims |
| **MTD Risk Scoring** | 0-100 vulnerability assessment with fixes |
| **Defense Anticipation** | Immunity, exhaustion, SOL analysis |
| **Fact Gap Detection** | Missing allegations identified |
| **Auto-Suggest** | Recommends claims based on facts |

#### Supported Claims (40+)

**Constitutional / Civil Rights (§ 1983)**
- `1983_first_amendment_retaliation`
- `1983_first_amendment_speech_restriction`
- `1983_fourth_false_arrest`
- `1983_fourth_unlawful_search_seizure`
- `1983_fourth_excessive_force`
- `1983_fourteenth_procedural_due_process`
- `1983_fourteenth_substantive_due_process`
- `1983_fourteenth_equal_protection`
- `1983_monell_municipal_liability`
- `1985_conspiracy`
- `1986_failure_to_prevent`

**Bivens Claims (Federal Actors)**
- `bivens_fourth_search_seizure`
- `bivens_fifth_due_process`
- `bivens_eighth_deliberate_indifference`

**Administrative / APA**
- `apa_arbitrary_capricious`
- `apa_unlawful_withholding_unreasonable_delay`
- `mandamus_compel_ministerial_duty`
- `habeas_detention_challenge`

**Employment**
- `title_vii_disparate_treatment`
- `title_vii_hostile_work_environment`
- `title_vii_retaliation`
- `adea_age_discrimination`
- `ada_title_i_employment_disability`
- `fmla_interference`
- `fmla_retaliation`
- `flsa_unpaid_wages_overtime`

**FTCA (Federal Tort Claims)**
- `ftca_negligence`
- `ftca_medical_malpractice`
- `ftca_wrongful_death`

**Financial / Consumer**
- `fcra_inaccurate_reporting`
- `fdcpa_prohibited_practices`
- `tila_disclosure_violations`

**Commercial / RICO / Antitrust / IP**
- `false_claims_act_qui_tam`
- `rico_1962c`
- `rico_1962d_conspiracy`
- `antitrust_sherman_section_1`
- `antitrust_sherman_section_2`
- `lanham_trademark_infringement`
- `copyright_infringement`
- `patent_infringement`

**ERISA**
- `erisa_502a1b_benefits`
- `erisa_502a3_equitable_relief`

**Tax**
- `tax_refund_suit`
- `tax_wrongful_levy`

#### CLI Usage

```bash
# Generate complaint from case input
node dist/cli.js --input case.json --out ./output

# Auto-suggest claims based on facts
node dist/cli.js --input case.json --suggest

# List all available claims
node dist/cli.js --list

# Specify output format
node dist/cli.js --input case.json --format markdown
```

#### Input Format (CASE_INPUT)

```json
{
  "court": {
    "district": "Middle District of Florida",
    "division": "Orlando",
    "state": "FL"
  },
  "parties": {
    "plaintiffs": [{
      "name": "John Doe",
      "citizenship": "Florida",
      "entity_type": "individual",
      "residence": "Orlando, FL"
    }],
    "defendants": [{
      "name": "City of Orlando",
      "type": "local",
      "capacity": "official",
      "citizenship": "Florida",
      "entity_type": "municipality",
      "role_title": "Municipal Corporation"
    }]
  },
  "facts": [{
    "date": "2025-06-15",
    "location": "Orlando, FL",
    "actors": ["Officer Smith", "John Doe"],
    "event": "Description of what happened",
    "documents": ["body cam footage", "medical records"],
    "harm": "injuries suffered",
    "damages_estimate": "$250,000",
    "evidence": ["video", "photos"],
    "witnesses": ["Jane Doe"]
  }],
  "claims_requested": ["1983_fourth_excessive_force"],
  "relief_requested": ["money", "injunction", "fees", "costs"],
  "exhaustion": {
    "ftca_admin_claim_filed": false,
    "eeoc_charge_filed": false,
    "erisa_appeal_done": false,
    "agency_final_action": false
  },
  "limitations": {
    "key_dates": {
      "injury_date": "2025-06-15"
    }
  },
  "goals": {
    "settlement_target": "$500,000",
    "non_monetary_goals": ["policy change"]
  }
}
```

#### Output Generated

For each claim, the engine produces:

1. **Elements Table** - Required allegations for each element
2. **Preconditions** - Exhaustion, standing, timing requirements
3. **Defense Warnings** - Anticipated immunity/procedural defenses
4. **Pleading Checklist** - Fact-to-element mapping status
5. **Draft Count** - Complaint-ready cause of action
6. **Fact Gaps** - Missing allegations with suggested sources
7. **MTD Risk Score** - 0-100 vulnerability with prioritized fixes

### 19 Litigation Strategy Engines

Location: `references/federal_litigation_engines.md`

| # | Engine | Purpose |
|---|--------|---------|
| 1 | **Defense Matrix** | Identify all Rule 12(b) and substantive defenses with counter-strategies |
| 2 | **Jurisdictional Trap Detector** | Standing, exhaustion, abstention, removal defects |
| 3 | **Complaint Structure Generator** | Rule 8 compliant pleading templates |
| 4 | **MTD Counter-Strike** | Strategies to defeat motions to dismiss |
| 5 | **Case Survival Probability** | Weighted outcome modeling (MTD/SJ/Trial %) |
| 6 | **Judge Risk Model** | Judicial tendencies and strategy adaptation |
| 7 | **Discovery Strategy** | Phase planning, ESI, depositions, expert strategy |
| 8 | **Summary Judgment Builder** | SUMF, element analysis, burden shifting |
| 9 | **Trial Strategy** | Theme, witnesses, exhibits, jury psychology |
| 10 | **Appellate Strategy** | Preservation audit, standards of review, brief structure |
| 11 | **Settlement Optimization** | Case valuation, timing, negotiation psychology |
| 12 | **Jury Persuasion** | Narrative framing, cognitive bias leverage |
| 13 | **Damages Modeling** | Economic/non-economic quantification |
| 14 | **Evidence Credibility** | Admissibility, authentication, Daubert analysis |
| 15 | **Pretrial Motions** | MIL, Daubert, procedural motion strategy |
| 16 | **Sanctions Analyzer** | Spoliation exposure, Rule 37(e), ethical issues |
| 17 | **Jury Instruction Builder** | Elements instructions, verdict forms |
| 18 | **Judge Behavior Profiler** | Detailed judicial tendency profiles |
| 19 | **Voir Dire Strategy** | Jury selection, bias detection, strike strategy |

### 7-Phase Master Workflow

The skill automatically executes this workflow when federal cases are detected:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FEDERAL MASTER CASE WORKFLOW                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  PHASE 1: INTAKE & CLASSIFICATION                                   │
│  ├── Federal case questionnaire                                     │
│  ├── A/B/C System classification                                    │
│  ├── Jurisdiction analysis (diversity/federal question)            │
│  └── Federal Pleading Engine: Auto-suggest claims                  │
│                                                                     │
│  PHASE 2: STATUS DETERMINATION                                      │
│  ├── FRCP timeline analysis                                         │
│  ├── Deadline calculation (21-day answer, 90-day service)          │
│  └── Rule 26(f) conference scheduling                              │
│                                                                     │
│  PHASE 3: DOCUMENT ANALYSIS (existing cases)                        │
│  ├── Pleadings review (Twombly/Iqbal compliance)                   │
│  ├── Discovery status (Rule 26 disclosures)                        │
│  └── Federal Pleading Engine: MTD risk assessment                  │
│                                                                     │
│  PHASE 4: LEGAL RESEARCH                                            │
│  ├── 11th Circuit precedent research                               │
│  ├── Supreme Court controlling authority                           │
│  └── CourtListener integration                                      │
│                                                                     │
│  PHASE 5: STRATEGIC BLUEPRINT GENERATION (.bd)                      │
│  ├── Litigation Engines: Full case analysis                        │
│  ├── Timeline & cost estimates                                     │
│  ├── Judge profile and risk adjustments                            │
│  └── Settlement valuation                                           │
│                                                                     │
│  PHASE 6: DOCUMENT DRAFTING QUEUE                                   │
│  ├── Federal Pleading Engine: Generate complaints                  │
│  ├── Priority-ranked document generation                           │
│  └── Element-by-element drafting                                   │
│                                                                     │
│  PHASE 7: QUALITY CONTROL & FILING                                  │
│  ├── FRCP/FRE citation verification                                │
│  ├── M.D. Fla. Local Rules compliance                              │
│  └── CM/ECF formatting check                                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
federal-trial-counsel/
├── SKILL.md                          # Main skill definition
├── README.md                         # This documentation
├── MANIFEST.md                       # File index
│
├── scripts/
│   ├── federal_pleading_engine/      # Elements-based pleading engine
│   │   ├── skill.json               # Package configuration
│   │   ├── README.md                # Engine documentation
│   │   ├── schema.ts                # Type definitions
│   │   ├── claim_library.ts         # 40+ causes of action
│   │   ├── elements.ts              # Element definitions
│   │   ├── mapper.ts                # Fact-to-element mapping
│   │   ├── drafter.ts               # Complaint generation
│   │   ├── risk.ts                  # MTD risk scoring
│   │   ├── cli.ts                   # Command-line interface
│   │   └── examples/
│   │       ├── sample_case_input.json
│   │       └── sample_output.md
│   │
│   └── courtlistener/                # Case law research integration
│       ├── client.ts
│       ├── types.ts
│       └── cli.ts
│
├── references/
│   ├── federal_litigation_engines.md # 19 litigation strategy modules
│   └── case_strategy_system.md       # A/B/C classification system
│
├── workflows/
│   └── 00-master-case-analysis.md    # 7-phase master workflow
│
├── modules/
│   ├── case_analysis_engine.md
│   ├── strategy_scoring_system.md
│   ├── board_risk_dashboard.md
│   ├── case_timeline_builder.md
│   └── mandamus_engine.md
│
└── assets/templates/
    ├── pleadings/
    │   ├── complaint_federal.md
    │   ├── answer_federal.md
    │   └── notice_of_removal.md
    ├── motions/
    │   ├── motion_to_dismiss.md
    │   ├── summary_judgment.md
    │   ├── tro_motion.md
    │   ├── preliminary_injunction.md
    │   └── motions_in_limine.md
    └── discovery/
        ├── initial_disclosures.md
        ├── interrogatories_first_set.md
        ├── requests_for_production.md
        └── deposition_notice.md
```

## Auto-Trigger Conditions

The skill activates automatically when detecting:

| Trigger | Example |
|---------|---------|
| Federal case description | "I have a diversity case in the Middle District..." |
| Case number reference | "Case 6:24-cv-01234-ABC-DEF..." |
| Federal document drafting | "Draft a motion to dismiss under Rule 12(b)(6)..." |
| Jurisdiction analysis | "Can we remove this case to federal court..." |
| FRCP/FRE reference | Mentions of federal rules or procedures |
| 11th Circuit appeal | "We need to appeal to the Eleventh Circuit..." |

## Pleading Standards Applied

### FRCP Rule 8(a)
- Short and plain statement of jurisdiction
- Short and plain statement of claim
- Demand for judgment

### Twombly/Iqbal Plausibility
- Each element supported by factual allegations
- "Who, what, when, where, how" for material facts
- Legal conclusions disregarded
- Plausibility = more than possible, less than probable

### Rule 9(b) Heightened Pleading (Fraud)
- Specific identification of false statements
- Who made them, when, where, how
- Why statements were false
- Reliance and causation

### Immunity Considerations
- **Qualified Immunity**: Clearly established law analysis
- **Sovereign Immunity**: Waiver identification
- **Eleventh Amendment**: State agency protection

## MTD Risk Scoring Categories

| Category | Weight | Factors |
|----------|--------|---------|
| Standing | 15% | Injury, causation, redressability |
| Immunity | 20% | Qualified, sovereign, Eleventh Amendment |
| Exhaustion | 15% | EEOC, FTCA SF-95, ERISA, APA |
| SOL | 15% | Statute of limitations compliance |
| Rule 9(b) | 10% | Fraud pleading particularity |
| Monell | 10% | Municipal liability sufficiency |
| Causation | 10% | Direct and proximate cause |
| Damages | 5% | Quantification and proof |

## Examples

### Example 1: Excessive Force Case

```bash
# Create case input file
cat > case.json << 'EOF'
{
  "court": {"district": "Middle District of Florida", "division": "Orlando", "state": "FL"},
  "parties": {
    "plaintiffs": [{"name": "John Doe", "citizenship": "Florida", "entity_type": "individual"}],
    "defendants": [
      {"name": "Officer Smith", "type": "officer", "capacity": "both", "citizenship": "Florida", "entity_type": "individual"},
      {"name": "City of Orlando", "type": "local", "capacity": "official", "citizenship": "Florida", "entity_type": "municipality"}
    ]
  },
  "facts": [{
    "date": "2025-06-15",
    "location": "Orlando, FL",
    "actors": ["Officer Smith", "John Doe"],
    "event": "Officer used excessive force during traffic stop",
    "harm": "broken arm, contusions",
    "damages_estimate": "$250,000"
  }],
  "claims_requested": ["auto_suggest"],
  "relief_requested": ["money", "injunction", "fees"]
}
EOF

# Generate complaint
node dist/cli.js --input case.json --out ./output
```

### Example 2: Employment Discrimination

```bash
node dist/cli.js --input employment_case.json --claims "title_vii_disparate_treatment,title_vii_retaliation"
```

## Adding New Claims

To add a new federal cause of action:

### 1. Add to claim_library.ts

```typescript
'new_claim_key': {
  name: 'New Claim Name',
  category: 'category_name',
  source: '42 U.S.C. § XXXX',
  sourceType: 'statute',
  heightenedPleading: false,
  exhaustionRequired: false,
  exhaustionType: null,
  immunities: ['qualified'],
  typicalDefenses: ['defense1', 'defense2'],
  jurisdiction: 'federal_question',
  statuteOfLimitations: '2 years'
}
```

### 2. Add Elements to elements.ts

```typescript
'new_claim_key': [
  {
    number: 1,
    name: 'Element Name',
    mustAllege: 'What must be specifically alleged',
    typicalEvidence: ['evidence1', 'evidence2'],
    pitfalls: 'Common mistakes'
  }
]
```

### 3. Test

```bash
node dist/cli.js --input test_case.json --claims "new_claim_key"
```

## Legal Disclaimer

This tool assists with legal drafting but does not constitute legal advice. All output should be reviewed by a licensed attorney before filing. The engine does NOT fabricate facts - it only uses facts provided in the input.

## License

Private - For use with Claude Code skills system.

## Version

1.0.0 - Initial release with 40+ claims and 19 litigation engines.
