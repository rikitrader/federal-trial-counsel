/**
 * Federal Pleading Engine - Claim Library
 *
 * Comprehensive registry of federal causes of action with metadata
 * for jurisdiction, exhaustion, immunities, and typical defenses.
 */

import {
  ClaimMetadata,
  ClaimCategory,
  SourceType,
  ExhaustionType,
  ImmunityType,
  JurisdictionBasis,
} from './schema';

/**
 * Master claim library with metadata for each cause of action
 */
export const CLAIM_LIBRARY: Record<string, ClaimMetadata> = {
  // ============================================================================
  // A. CONSTITUTIONAL / CIVIL RIGHTS (42 U.S.C. § 1983)
  // ============================================================================

  '1983_first_amendment_retaliation': {
    name: 'First Amendment Retaliation (§ 1983)',
    category: 'constitutional_civil_rights',
    source: '42 U.S.C. § 1983; U.S. Const. amend. I',
    sourceType: 'constitutional',
    heightenedPleading: false,
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: ['qualified'],
    typicalDefenses: [
      'Qualified immunity - right not clearly established',
      'Same decision regardless of speech',
      'Speech not on matter of public concern',
      'Speech pursuant to official duties (Garcetti)',
      'Disruption to government operations',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: 'State personal injury SOL (typically 2-4 years)',
  },

  '1983_first_amendment_speech_restriction': {
    name: 'First Amendment Speech Restriction (§ 1983)',
    category: 'constitutional_civil_rights',
    source: '42 U.S.C. § 1983; U.S. Const. amend. I',
    sourceType: 'constitutional',
    heightenedPleading: false,
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: ['qualified'],
    typicalDefenses: [
      'Qualified immunity',
      'Viewpoint-neutral time/place/manner restriction',
      'Content-neutral regulation',
      'Compelling government interest (strict scrutiny)',
      'Traditional public forum vs limited forum',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: 'State personal injury SOL (typically 2-4 years)',
  },

  '1983_fourth_false_arrest': {
    name: 'Fourth Amendment False Arrest (§ 1983)',
    category: 'constitutional_civil_rights',
    source: '42 U.S.C. § 1983; U.S. Const. amend. IV',
    sourceType: 'constitutional',
    heightenedPleading: false,
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: ['qualified'],
    typicalDefenses: [
      'Qualified immunity',
      'Probable cause existed',
      'Arguable probable cause',
      'Good faith reliance on warrant',
      'Consent to encounter',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: 'State personal injury SOL (typically 2-4 years)',
  },

  '1983_fourth_unlawful_search_seizure': {
    name: 'Fourth Amendment Unlawful Search/Seizure (§ 1983)',
    category: 'constitutional_civil_rights',
    source: '42 U.S.C. § 1983; U.S. Const. amend. IV',
    sourceType: 'constitutional',
    heightenedPleading: false,
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: ['qualified'],
    typicalDefenses: [
      'Qualified immunity',
      'Valid warrant',
      'Consent',
      'Exigent circumstances',
      'Plain view doctrine',
      'Search incident to arrest',
      'Automobile exception',
      'Terry stop justified',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: 'State personal injury SOL (typically 2-4 years)',
  },

  '1983_fourth_excessive_force': {
    name: 'Fourth Amendment Excessive Force (§ 1983)',
    category: 'constitutional_civil_rights',
    source: '42 U.S.C. § 1983; U.S. Const. amend. IV',
    sourceType: 'constitutional',
    heightenedPleading: false,
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: ['qualified'],
    typicalDefenses: [
      'Qualified immunity - no clearly established right',
      'Force objectively reasonable under Graham v. Connor',
      'Severity of crime at issue',
      'Immediate threat to officers/others',
      'Active resistance or flight',
      'Tense/rapidly evolving situation',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: 'State personal injury SOL (typically 2-4 years)',
  },

  '1983_fourteenth_procedural_due_process': {
    name: 'Fourteenth Amendment Procedural Due Process (§ 1983)',
    category: 'constitutional_civil_rights',
    source: '42 U.S.C. § 1983; U.S. Const. amend. XIV',
    sourceType: 'constitutional',
    heightenedPleading: false,
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: ['qualified'],
    typicalDefenses: [
      'Qualified immunity',
      'No protected property/liberty interest',
      'Adequate post-deprivation remedies',
      'Random and unauthorized act (Parratt doctrine)',
      'Adequate pre-deprivation process provided',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: 'State personal injury SOL (typically 2-4 years)',
  },

  '1983_fourteenth_substantive_due_process': {
    name: 'Fourteenth Amendment Substantive Due Process (§ 1983)',
    category: 'constitutional_civil_rights',
    source: '42 U.S.C. § 1983; U.S. Const. amend. XIV',
    sourceType: 'constitutional',
    heightenedPleading: false,
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: ['qualified'],
    typicalDefenses: [
      'Qualified immunity',
      'Conduct does not shock the conscience',
      'Explicit textual source in Constitution (use that instead)',
      'Rational basis for government action',
      'No fundamental right implicated',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: 'State personal injury SOL (typically 2-4 years)',
  },

  '1983_fourteenth_equal_protection': {
    name: 'Fourteenth Amendment Equal Protection (§ 1983)',
    category: 'constitutional_civil_rights',
    source: '42 U.S.C. § 1983; U.S. Const. amend. XIV',
    sourceType: 'constitutional',
    heightenedPleading: false,
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: ['qualified'],
    typicalDefenses: [
      'Qualified immunity',
      'Rational basis for classification',
      'No discriminatory intent',
      'Similarly situated comparators not actually similar',
      'Legitimate non-discriminatory reason',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: 'State personal injury SOL (typically 2-4 years)',
  },

  '1983_monell_municipal_liability': {
    name: 'Monell Municipal Liability (§ 1983)',
    category: 'constitutional_civil_rights',
    source: '42 U.S.C. § 1983; Monell v. Dep\'t of Social Servs., 436 U.S. 658 (1978)',
    sourceType: 'constitutional',
    heightenedPleading: false,
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: [],  // Municipalities cannot claim qualified immunity
    typicalDefenses: [
      'No underlying constitutional violation',
      'No official policy or custom',
      'Policy did not cause the violation',
      'No final policymaker involvement',
      'No deliberate indifference to known pattern',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: 'State personal injury SOL (typically 2-4 years)',
  },

  '1985_conspiracy': {
    name: 'Conspiracy to Deprive Rights (42 U.S.C. § 1985)',
    category: 'constitutional_civil_rights',
    source: '42 U.S.C. § 1985(3)',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: ['qualified'],
    typicalDefenses: [
      'Qualified immunity',
      'No class-based animus',
      'No agreement between defendants',
      'No overt act in furtherance',
      'Intracorporate conspiracy doctrine',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: 'State personal injury SOL (typically 2-4 years)',
  },

  '1986_failure_to_prevent': {
    name: 'Failure to Prevent Conspiracy (42 U.S.C. § 1986)',
    category: 'constitutional_civil_rights',
    source: '42 U.S.C. § 1986',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: ['qualified'],
    typicalDefenses: [
      'No underlying § 1985 conspiracy',
      'No knowledge of conspiracy',
      'No power to prevent',
      'Reasonable diligence used',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: '1 year from commission of wrong',
  },

  // ============================================================================
  // B. BIVENS CLAIMS (Federal Actors)
  // ============================================================================

  'bivens_fourth_search_seizure': {
    name: 'Bivens Fourth Amendment (Search/Seizure)',
    category: 'bivens',
    source: 'Bivens v. Six Unknown Named Agents, 403 U.S. 388 (1971)',
    sourceType: 'constitutional',
    heightenedPleading: false,
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: ['qualified', 'sovereign'],
    typicalDefenses: [
      'Qualified immunity',
      'New context (Ziglar v. Abbasi factors)',
      'Special factors counseling hesitation',
      'Alternative remedies available',
      'National security implications',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: 'State personal injury SOL (typically 2-4 years)',
    viabilityWarning: 'VERIFY: Modern Bivens doctrine severely limited. Courts rarely extend to new contexts. See Ziglar v. Abbasi, 582 U.S. 120 (2017); Egbert v. Boule, 596 U.S. 482 (2022).',
  },

  'bivens_fifth_due_process': {
    name: 'Bivens Fifth Amendment (Due Process)',
    category: 'bivens',
    source: 'Davis v. Passman, 442 U.S. 228 (1979)',
    sourceType: 'constitutional',
    heightenedPleading: false,
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: ['qualified', 'sovereign'],
    typicalDefenses: [
      'Qualified immunity',
      'New context',
      'Special factors',
      'Alternative remedies',
      'CSRA preclusion (federal employees)',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: 'State personal injury SOL (typically 2-4 years)',
    viabilityWarning: 'VERIFY: Rarely extended beyond employment discrimination context. CSRA may provide exclusive remedy for federal employees.',
  },

  'bivens_eighth_deliberate_indifference': {
    name: 'Bivens Eighth Amendment (Deliberate Indifference)',
    category: 'bivens',
    source: 'Carlson v. Green, 446 U.S. 14 (1980)',
    sourceType: 'constitutional',
    heightenedPleading: false,
    exhaustionRequired: true,
    exhaustionType: null,  // PLRA exhaustion
    immunities: ['qualified', 'sovereign'],
    typicalDefenses: [
      'Qualified immunity',
      'PLRA exhaustion not complete',
      'No subjective knowledge of risk',
      'Reasonable response to risk',
      'BOP administrative remedies not exhausted',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: 'State personal injury SOL (typically 2-4 years)',
    viabilityWarning: 'VERIFY: Limited to federal prisoner medical care context. PLRA exhaustion required. New contexts rarely recognized.',
  },

  // ============================================================================
  // C. ADMINISTRATIVE / APA / MANDAMUS / HABEAS
  // ============================================================================

  'apa_arbitrary_capricious': {
    name: 'APA - Arbitrary and Capricious Agency Action',
    category: 'administrative',
    source: '5 U.S.C. § 706(2)(A)',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: true,
    exhaustionType: 'apa_final_action',
    immunities: ['sovereign'],  // Waived for non-monetary relief
    typicalDefenses: [
      'No final agency action',
      'Committed to agency discretion',
      'Plaintiff not within zone of interests',
      'Agency action reasonable',
      'Adequate explanation provided',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: '6 years (28 U.S.C. § 2401)',
  },

  'apa_unlawful_withholding_unreasonable_delay': {
    name: 'APA - Unlawful Withholding/Unreasonable Delay',
    category: 'administrative',
    source: '5 U.S.C. § 706(1)',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: true,
    exhaustionType: 'apa_final_action',
    immunities: ['sovereign'],
    typicalDefenses: [
      'No discrete action unlawfully withheld',
      'Agency proceeding reasonably',
      'Complex matter requiring time',
      'TRAC factors favor agency',
      'No statutory deadline',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: 'None (but laches may apply)',
  },

  'mandamus_compel_ministerial_duty': {
    name: 'Mandamus - Compel Ministerial Duty',
    category: 'administrative',
    source: '28 U.S.C. § 1361',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: ['sovereign'],
    typicalDefenses: [
      'Duty is discretionary, not ministerial',
      'No clear right to relief',
      'Adequate alternative remedy exists',
      'Plaintiff lacks standing',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: 'None (but laches may apply)',
  },

  'habeas_detention_challenge': {
    name: 'Habeas Corpus - Challenge to Detention',
    category: 'administrative',
    source: '28 U.S.C. § 2241',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: true,
    exhaustionType: null,  // BOP administrative remedies
    immunities: ['sovereign'],
    typicalDefenses: [
      'Failure to exhaust administrative remedies',
      'Improper custody',
      'AEDPA time bar (conviction challenges)',
      'Successive petition bar',
      'Procedural default',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: 'Varies; 1 year for conviction challenges',
  },

  // ============================================================================
  // D. EMPLOYMENT / CIVIL RIGHTS STATUTES
  // ============================================================================

  'title_vii_disparate_treatment': {
    name: 'Title VII - Disparate Treatment',
    category: 'employment',
    source: '42 U.S.C. § 2000e-2',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: true,
    exhaustionType: 'eeoc',
    immunities: ['eleventh_amendment'],  // For state employers
    typicalDefenses: [
      'Failure to exhaust (no EEOC charge)',
      'EEOC charge untimely (180/300 days)',
      'Legitimate non-discriminatory reason',
      'Same actor inference',
      'Comparators not similarly situated',
      'Insufficient evidence of pretext',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: '90 days from right-to-sue letter',
  },

  'title_vii_hostile_work_environment': {
    name: 'Title VII - Hostile Work Environment',
    category: 'employment',
    source: '42 U.S.C. § 2000e-2',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: true,
    exhaustionType: 'eeoc',
    immunities: ['eleventh_amendment'],
    typicalDefenses: [
      'Failure to exhaust',
      'Not severe or pervasive',
      'Not based on protected class',
      'Faragher/Ellerth defense (supervisor harassment)',
      'Prompt remedial action taken',
      'Plaintiff unreasonably failed to report',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: '90 days from right-to-sue letter',
  },

  'title_vii_retaliation': {
    name: 'Title VII - Retaliation',
    category: 'employment',
    source: '42 U.S.C. § 2000e-3',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: true,
    exhaustionType: 'eeoc',
    immunities: ['eleventh_amendment'],
    typicalDefenses: [
      'Failure to exhaust',
      'No protected activity',
      'No materially adverse action',
      'No causal connection',
      'Same decision regardless',
      'Temporal proximity insufficient alone',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: '90 days from right-to-sue letter',
  },

  'adea_age_discrimination': {
    name: 'ADEA - Age Discrimination',
    category: 'employment',
    source: '29 U.S.C. § 621 et seq.',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: true,
    exhaustionType: 'eeoc',
    immunities: ['eleventh_amendment'],
    typicalDefenses: [
      'Failure to exhaust',
      'Plaintiff under 40',
      'RFOA (reasonable factor other than age)',
      'Bona fide occupational qualification',
      'Same actor inference',
      'Legitimate non-discriminatory reason',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: '90 days from right-to-sue; 60 days after filing charge',
  },

  'ada_title_i_employment_disability': {
    name: 'ADA Title I - Disability Discrimination',
    category: 'employment',
    source: '42 U.S.C. § 12112',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: true,
    exhaustionType: 'eeoc',
    immunities: ['eleventh_amendment'],
    typicalDefenses: [
      'Failure to exhaust',
      'Not a qualified individual',
      'No disability under ADA',
      'Cannot perform essential functions',
      'Undue hardship for accommodation',
      'Direct threat defense',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: '90 days from right-to-sue letter',
  },

  'fmla_interference': {
    name: 'FMLA - Interference',
    category: 'employment',
    source: '29 U.S.C. § 2615(a)(1)',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: ['eleventh_amendment'],
    typicalDefenses: [
      'Employer has fewer than 50 employees',
      'Employee not eligible (1 year, 1,250 hours)',
      'Not a serious health condition',
      'Employee would have been terminated anyway',
      'Employee failed to provide adequate notice',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: '2 years (3 years for willful violations)',
  },

  'fmla_retaliation': {
    name: 'FMLA - Retaliation',
    category: 'employment',
    source: '29 U.S.C. § 2615(a)(2)',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: ['eleventh_amendment'],
    typicalDefenses: [
      'Employer has fewer than 50 employees',
      'Employee not eligible',
      'No causal connection',
      'Same decision regardless of FMLA use',
      'Legitimate non-retaliatory reason',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: '2 years (3 years for willful violations)',
  },

  'flsa_unpaid_wages_overtime': {
    name: 'FLSA - Unpaid Wages/Overtime',
    category: 'employment',
    source: '29 U.S.C. § 201 et seq.',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: ['eleventh_amendment'],
    typicalDefenses: [
      'Employee exempt (executive, administrative, professional)',
      'Independent contractor',
      'Not engaged in commerce',
      'Good faith defense (liquidated damages)',
      'SOL expired',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: '2 years (3 years for willful violations)',
  },

  // ============================================================================
  // E. FTCA (Federal Tort Claims)
  // ============================================================================

  'ftca_negligence': {
    name: 'FTCA - Negligence',
    category: 'tort_government',
    source: '28 U.S.C. § 1346(b)',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: true,
    exhaustionType: 'ftca_sf95',
    immunities: ['sovereign', 'discretionary_function'],
    typicalDefenses: [
      'Failure to exhaust (no SF-95 filed)',
      'Discretionary function exception',
      'Intentional tort exception',
      'Federal employee acting outside scope',
      'State law does not recognize claim',
      'Failure to file within 2 years',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: '2 years from accrual; 6 months from denial',
  },

  'ftca_medical_malpractice': {
    name: 'FTCA - Medical Malpractice',
    category: 'tort_government',
    source: '28 U.S.C. § 1346(b)',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: true,
    exhaustionType: 'ftca_sf95',
    immunities: ['sovereign', 'discretionary_function'],
    typicalDefenses: [
      'Failure to exhaust (no SF-95)',
      'Failure to meet state malpractice requirements',
      'No duty owed',
      'Standard of care met',
      'No causation',
      'Statute of repose',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: '2 years from accrual; 6 months from denial',
  },

  'ftca_wrongful_death': {
    name: 'FTCA - Wrongful Death',
    category: 'tort_government',
    source: '28 U.S.C. § 1346(b)',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: true,
    exhaustionType: 'ftca_sf95',
    immunities: ['sovereign', 'discretionary_function'],
    typicalDefenses: [
      'Failure to exhaust',
      'Discretionary function exception',
      'No state law wrongful death claim',
      'Plaintiff lacks standing',
      'Contributory/comparative negligence',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: '2 years from death; 6 months from denial',
  },

  // ============================================================================
  // F. FINANCIAL / CONSUMER
  // ============================================================================

  'fcra_inaccurate_reporting': {
    name: 'FCRA - Inaccurate Credit Reporting',
    category: 'financial_consumer',
    source: '15 U.S.C. § 1681 et seq.',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: [],
    typicalDefenses: [
      'Information was accurate',
      'Reasonable procedures followed',
      'No willfulness (statutory damages)',
      'Plaintiff failed to dispute',
      'No damages suffered',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: '2 years from discovery; 5 years absolute',
  },

  'fdcpa_prohibited_practices': {
    name: 'FDCPA - Prohibited Debt Collection Practices',
    category: 'financial_consumer',
    source: '15 U.S.C. § 1692 et seq.',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: [],
    typicalDefenses: [
      'Defendant is not a debt collector',
      'Plaintiff is not a consumer',
      'Not a consumer debt',
      'Bona fide error defense',
      'SOL expired (1 year)',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: '1 year from violation',
  },

  'tila_disclosure_violations': {
    name: 'TILA - Disclosure Violations',
    category: 'financial_consumer',
    source: '15 U.S.C. § 1601 et seq.',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: [],
    typicalDefenses: [
      'No material disclosure violation',
      'Bona fide error',
      'SOL expired (1 year for damages)',
      'No actual damages',
      'Right of rescission waived',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: '1 year for damages; 3 years for rescission',
  },

  // ============================================================================
  // G. COMMERCIAL / FRAUD / ANTITRUST / FCA / RICO / IP
  // ============================================================================

  'false_claims_act_qui_tam': {
    name: 'False Claims Act - Qui Tam',
    category: 'commercial',
    source: '31 U.S.C. § 3730(b)',
    sourceType: 'statute',
    heightenedPleading: true,  // Rule 9(b) applies
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: [],
    typicalDefenses: [
      'Public disclosure bar',
      'First-to-file bar',
      'No false claim submitted',
      'No scienter (knowledge)',
      'Government knowledge',
      'Materiality lacking',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: '6 years from violation; 3 years from discovery',
    viabilityWarning: 'VERIFY: Must file under seal. Government must be served. First-to-file and public disclosure bars apply.',
  },

  'rico_1962c': {
    name: 'RICO - Pattern of Racketeering (§ 1962(c))',
    category: 'commercial',
    source: '18 U.S.C. § 1962(c)',
    sourceType: 'statute',
    heightenedPleading: true,  // If predicate is fraud
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: [],
    typicalDefenses: [
      'No enterprise',
      'No pattern (continuity + relationship)',
      'No predicate acts',
      'No injury to business or property',
      'No proximate causation',
      'Rule 9(b) particularity lacking',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: '4 years from discovery of injury',
  },

  'rico_1962d_conspiracy': {
    name: 'RICO - Conspiracy (§ 1962(d))',
    category: 'commercial',
    source: '18 U.S.C. § 1962(d)',
    sourceType: 'statute',
    heightenedPleading: true,
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: [],
    typicalDefenses: [
      'No underlying RICO violation',
      'No agreement to participate',
      'No knowledge of pattern',
      'Withdrawal from conspiracy',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: '4 years from discovery of injury',
  },

  'antitrust_sherman_section_1': {
    name: 'Sherman Act § 1 - Restraint of Trade',
    category: 'commercial',
    source: '15 U.S.C. § 1',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: [],
    typicalDefenses: [
      'No agreement (unilateral conduct)',
      'Rule of reason analysis (procompetitive justification)',
      'No antitrust injury',
      'State action immunity',
      'Noerr-Pennington doctrine',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: '4 years',
  },

  'antitrust_sherman_section_2': {
    name: 'Sherman Act § 2 - Monopolization',
    category: 'commercial',
    source: '15 U.S.C. § 2',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: [],
    typicalDefenses: [
      'No monopoly power',
      'No anticompetitive conduct',
      'Superior product/skill/foresight',
      'No antitrust injury',
      'State action immunity',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: '4 years',
  },

  'lanham_trademark_infringement': {
    name: 'Lanham Act - Trademark Infringement',
    category: 'commercial',
    source: '15 U.S.C. § 1114',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: [],
    typicalDefenses: [
      'No likelihood of confusion',
      'Fair use (descriptive, nominative)',
      'Abandonment',
      'Laches/acquiescence',
      'First Amendment (expressive works)',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: 'None (but laches applies)',
  },

  'copyright_infringement': {
    name: 'Copyright Infringement',
    category: 'commercial',
    source: '17 U.S.C. § 501',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: false,
    exhaustionType: null,  // Registration required for suit
    immunities: ['eleventh_amendment'],
    typicalDefenses: [
      'No valid copyright',
      'No copying (independent creation)',
      'Fair use',
      'License/permission',
      'De minimis use',
      'Statute of limitations (3 years)',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: '3 years from infringement',
  },

  'patent_infringement': {
    name: 'Patent Infringement',
    category: 'commercial',
    source: '35 U.S.C. § 271',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: ['eleventh_amendment'],
    typicalDefenses: [
      'Invalidity (anticipation, obviousness)',
      'Non-infringement',
      'Exhaustion',
      'License/permission',
      'Inequitable conduct',
      'Laches/equitable estoppel',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: '6 years (damages limitation)',
    viabilityWarning: 'VERIFY: Special venue requirements under TC Heartland. Patent must be issued and valid.',
  },

  // ============================================================================
  // H. ERISA
  // ============================================================================

  'erisa_502a1b_benefits': {
    name: 'ERISA § 502(a)(1)(B) - Denial of Benefits',
    category: 'erisa',
    source: '29 U.S.C. § 1132(a)(1)(B)',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: true,
    exhaustionType: 'erisa_internal',
    immunities: [],
    typicalDefenses: [
      'Failure to exhaust internal appeals',
      'Plan interpretation reasonable',
      'Abuse of discretion standard',
      'No plan coverage',
      'Pre-existing condition exclusion',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: 'Plan terms or state limitations (varies)',
  },

  'erisa_502a3_equitable_relief': {
    name: 'ERISA § 502(a)(3) - Equitable Relief',
    category: 'erisa',
    source: '29 U.S.C. § 1132(a)(3)',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: true,
    exhaustionType: 'erisa_internal',
    immunities: [],
    typicalDefenses: [
      'Adequate remedy under § 502(a)(1)(B)',
      'Relief not equitable in nature',
      'No fiduciary breach',
      'Plan followed',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: 'Plan terms or state limitations (varies)',
  },

  // ============================================================================
  // I. TAX
  // ============================================================================

  'tax_refund_suit': {
    name: 'Tax Refund Suit',
    category: 'tax',
    source: '28 U.S.C. § 1346(a)(1)',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: true,
    exhaustionType: null,  // Full payment + admin claim
    immunities: ['sovereign'],
    typicalDefenses: [
      'Failure to pay full assessment',
      'No timely administrative claim',
      'Tax properly assessed',
      'Variance doctrine (new issues)',
      'SOL expired',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: '2 years from denial or 6 months deemed denial',
    viabilityWarning: 'VERIFY: Must pay full tax before suit. Administrative claim required. Complex jurisdictional rules.',
  },

  'tax_wrongful_levy': {
    name: 'Tax Wrongful Levy',
    category: 'tax',
    source: '26 U.S.C. § 7426',
    sourceType: 'statute',
    heightenedPleading: false,
    exhaustionRequired: false,
    exhaustionType: null,
    immunities: ['sovereign'],
    typicalDefenses: [
      'Proper levy procedures followed',
      'Plaintiff not owner of property',
      'No interest in property at time of levy',
      'SOL expired (9 months)',
    ],
    jurisdiction: 'federal_question',
    statuteOfLimitations: '9 months from levy',
    viabilityWarning: 'VERIFY: Very short SOL. Specific procedural requirements.',
  },
};

/**
 * Get all claim keys for a specific category
 */
export function getClaimsByCategory(category: ClaimCategory): string[] {
  return Object.entries(CLAIM_LIBRARY)
    .filter(([_, meta]) => meta.category === category)
    .map(([key, _]) => key);
}

/**
 * Get claims that require exhaustion
 */
export function getClaimsRequiringExhaustion(): string[] {
  return Object.entries(CLAIM_LIBRARY)
    .filter(([_, meta]) => meta.exhaustionRequired)
    .map(([key, _]) => key);
}

/**
 * Get claims with heightened pleading (Rule 9(b))
 */
export function getHeightenedPleadingClaims(): string[] {
  return Object.entries(CLAIM_LIBRARY)
    .filter(([_, meta]) => meta.heightenedPleading)
    .map(([key, _]) => key);
}

/**
 * Get claims with immunity concerns
 */
export function getClaimsWithImmunity(immunityType: ImmunityType): string[] {
  return Object.entries(CLAIM_LIBRARY)
    .filter(([_, meta]) => meta.immunities.includes(immunityType))
    .map(([key, _]) => key);
}

/**
 * Get all claim keys
 */
export function getAllClaimKeys(): string[] {
  return Object.keys(CLAIM_LIBRARY);
}

/**
 * Check if a claim key exists
 */
export function isValidClaimKey(key: string): boolean {
  return key in CLAIM_LIBRARY;
}

/**
 * Get claim metadata by key
 */
export function getClaimMetadata(key: string): ClaimMetadata | undefined {
  return CLAIM_LIBRARY[key];
}
