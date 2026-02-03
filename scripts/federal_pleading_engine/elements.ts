/**
 * Federal Pleading Engine - Elements Definitions
 *
 * Comprehensive element definitions for each federal cause of action.
 * Each element includes what must be alleged, typical evidence, and pitfalls.
 */

import { ClaimElement, ClaimPrecondition } from './schema';

/**
 * Element definitions for all supported claims
 */
export const CLAIM_ELEMENTS: Record<string, ClaimElement[]> = {
  // ============================================================================
  // CONSTITUTIONAL / CIVIL RIGHTS (42 U.S.C. § 1983)
  // ============================================================================

  '1983_first_amendment_retaliation': [
    {
      number: 1,
      name: 'Protected Activity',
      mustAllege: 'Plaintiff engaged in constitutionally protected speech or conduct (petition, assembly, religion)',
      typicalEvidence: ['Speech transcript', 'Emails', 'Meeting records', 'Witness testimony'],
      pitfalls: 'Speech pursuant to official duties is NOT protected (Garcetti). Must be on matter of public concern.',
    },
    {
      number: 2,
      name: 'Adverse Action',
      mustAllege: 'Defendant took an action that would chill a person of ordinary firmness from continuing to engage in protected activity',
      typicalEvidence: ['Termination letter', 'Disciplinary records', 'Demotion notice', 'Transfer orders'],
      pitfalls: 'De minimis actions may not qualify. Must deter reasonable person.',
    },
    {
      number: 3,
      name: 'Causation',
      mustAllege: 'The protected activity was a substantial or motivating factor in the adverse action',
      typicalEvidence: ['Timeline/temporal proximity', 'Defendant statements', 'Comparative treatment', 'Pattern evidence'],
      pitfalls: 'Temporal proximity alone usually insufficient. Need additional evidence of retaliatory motive.',
    },
    {
      number: 4,
      name: 'State Action',
      mustAllege: 'Defendant acted under color of state law',
      typicalEvidence: ['Employment records', 'Badge/uniform', 'Policy invocation', 'Official capacity evidence'],
      pitfalls: 'Private actors require state involvement. Off-duty conduct may not qualify.',
    },
  ],

  '1983_fourth_excessive_force': [
    {
      number: 1,
      name: 'Seizure Occurred',
      mustAllege: 'Defendant seized plaintiff through intentional application of physical force or show of authority that terminated movement',
      typicalEvidence: ['Arrest records', 'Body camera', 'Witness statements', 'Medical records'],
      pitfalls: 'Accidental force may not constitute seizure. Must be intentional.',
    },
    {
      number: 2,
      name: 'Force Applied',
      mustAllege: 'Defendant applied physical force to plaintiff\'s person',
      typicalEvidence: ['Medical records', 'Photos of injuries', 'Video evidence', 'Use of force reports'],
      pitfalls: 'Minimal force may not suffice. Document all force used.',
    },
    {
      number: 3,
      name: 'Objective Unreasonableness',
      mustAllege: 'The force used was objectively unreasonable under the circumstances, considering: (a) severity of crime; (b) immediate threat to safety; (c) active resistance/flight (Graham v. Connor factors)',
      typicalEvidence: ['Video showing events', 'Witness testimony on threat level', 'Use of force policy', 'Training records'],
      pitfalls: 'Must analyze from perspective of reasonable officer on scene, not hindsight. Tense situations favor officers.',
    },
    {
      number: 4,
      name: 'State Action',
      mustAllege: 'Defendant acted under color of state law',
      typicalEvidence: ['On-duty status', 'Uniform/badge', 'Invocation of authority'],
      pitfalls: 'Off-duty officers may still act under color of law if invoking authority.',
    },
    {
      number: 5,
      name: 'Injury/Damages',
      mustAllege: 'Plaintiff suffered injury as a result of the force',
      typicalEvidence: ['Medical records', 'Photos', 'Bills', 'Expert testimony'],
      pitfalls: 'Some circuits require more than de minimis injury for damages.',
    },
  ],

  '1983_fourth_false_arrest': [
    {
      number: 1,
      name: 'Arrest/Detention',
      mustAllege: 'Defendant caused plaintiff to be detained against plaintiff\'s will',
      typicalEvidence: ['Arrest records', 'Booking records', 'Witness statements'],
      pitfalls: 'Brief investigative stops (Terry) have different standard.',
    },
    {
      number: 2,
      name: 'Lack of Probable Cause',
      mustAllege: 'Defendant lacked probable cause to believe plaintiff committed a crime',
      typicalEvidence: ['Arrest report deficiencies', 'Witness testimony', 'Video evidence', 'Lack of investigation'],
      pitfalls: 'Only need arguable probable cause for qualified immunity. Low bar.',
    },
    {
      number: 3,
      name: 'State Action',
      mustAllege: 'Defendant acted under color of state law',
      typicalEvidence: ['Official capacity', 'Badge/uniform', 'Authority invocation'],
      pitfalls: 'Private security generally not state actors.',
    },
    {
      number: 4,
      name: 'Causation',
      mustAllege: 'Defendant\'s actions were proximate cause of plaintiff\'s detention',
      typicalEvidence: ['Chain of events', 'Defendant decisions', 'Timing'],
      pitfalls: 'Intervening actors (prosecutors, judges) may break chain.',
    },
  ],

  '1983_monell_municipal_liability': [
    {
      number: 1,
      name: 'Constitutional Violation',
      mustAllege: 'A municipal employee violated plaintiff\'s constitutional rights',
      typicalEvidence: ['Same evidence as underlying § 1983 claim'],
      pitfalls: 'Must first establish an underlying violation. No vicarious liability.',
    },
    {
      number: 2,
      name: 'Official Policy or Custom',
      mustAllege: 'The violation resulted from: (a) official policy; (b) widespread practice so persistent as to constitute custom; (c) decision by final policymaker; or (d) failure to train amounting to deliberate indifference',
      typicalEvidence: ['Written policies', 'Training manuals', 'Prior incident records', 'Pattern evidence', 'Policymaker directives'],
      pitfalls: 'Single incident rarely sufficient. Must show policy/custom, not just respondeat superior.',
    },
    {
      number: 3,
      name: 'Moving Force Causation',
      mustAllege: 'The policy or custom was the "moving force" behind the constitutional violation',
      typicalEvidence: ['Link between policy and specific violation', 'Failure to train evidence', 'Deliberate indifference to known risk'],
      pitfalls: 'Must show direct causation between policy and harm. Not just "but for" causation.',
    },
    {
      number: 4,
      name: 'Municipal Defendant',
      mustAllege: 'Defendant is a municipality or local government entity',
      typicalEvidence: ['Municipal charter', 'Organizational documents'],
      pitfalls: 'States and state agencies have Eleventh Amendment immunity. Municipalities do not.',
    },
  ],

  '1983_fourteenth_procedural_due_process': [
    {
      number: 1,
      name: 'Protected Interest',
      mustAllege: 'Plaintiff possessed a protected property or liberty interest',
      typicalEvidence: ['Employment contract', 'Statute creating entitlement', 'Tenured status', 'Professional license'],
      pitfalls: 'At-will employment generally no property interest. Need objective source.',
    },
    {
      number: 2,
      name: 'Deprivation',
      mustAllege: 'Defendant deprived plaintiff of that interest',
      typicalEvidence: ['Termination records', 'License revocation', 'Benefit denial'],
      pitfalls: 'Must be actual deprivation, not just threatened.',
    },
    {
      number: 3,
      name: 'Inadequate Process',
      mustAllege: 'Defendant failed to provide adequate procedural protections before or after the deprivation',
      typicalEvidence: ['Lack of notice', 'No opportunity to be heard', 'Biased decisionmaker'],
      pitfalls: 'Post-deprivation remedies may satisfy due process. Check Parratt/Hudson doctrine.',
    },
    {
      number: 4,
      name: 'State Action',
      mustAllege: 'Defendant acted under color of state law',
      typicalEvidence: ['Government employment', 'State power invocation'],
      pitfalls: 'Private entities generally not covered unless state action nexus.',
    },
  ],

  '1983_fourteenth_equal_protection': [
    {
      number: 1,
      name: 'Discriminatory Treatment',
      mustAllege: 'Defendant treated plaintiff differently from similarly situated individuals',
      typicalEvidence: ['Comparative treatment evidence', 'Statistical data', 'Policy documents'],
      pitfalls: 'Comparators must be genuinely similarly situated in all material respects.',
    },
    {
      number: 2,
      name: 'Discriminatory Intent',
      mustAllege: 'Defendant acted with intent to discriminate based on protected class (or irrational basis for class-of-one)',
      typicalEvidence: ['Statements by decisionmakers', 'Pattern of discrimination', 'Departures from procedure'],
      pitfalls: 'Disparate impact alone insufficient. Must show intent.',
    },
    {
      number: 3,
      name: 'Protected Class or Class of One',
      mustAllege: 'Discrimination was based on protected class (race, religion, national origin, sex) or plaintiff was intentionally singled out for different treatment without rational basis',
      typicalEvidence: ['Class membership', 'Comparative treatment', 'Lack of rational basis'],
      pitfalls: 'Different scrutiny levels apply to different classes.',
    },
    {
      number: 4,
      name: 'State Action',
      mustAllege: 'Defendant acted under color of state law',
      typicalEvidence: ['Government capacity', 'State power exercise'],
      pitfalls: 'Private discrimination generally not covered.',
    },
  ],

  // ============================================================================
  // EMPLOYMENT
  // ============================================================================

  'title_vii_disparate_treatment': [
    {
      number: 1,
      name: 'Protected Class',
      mustAllege: 'Plaintiff is a member of a protected class (race, color, religion, sex, national origin)',
      typicalEvidence: ['Self-identification', 'Personnel records', 'Witness testimony'],
      pitfalls: 'Must identify specific protected characteristic.',
    },
    {
      number: 2,
      name: 'Qualification',
      mustAllege: 'Plaintiff was qualified for the position or performing job adequately',
      typicalEvidence: ['Performance reviews', 'Qualifications vs. job requirements', 'Commendations'],
      pitfalls: 'Defendant will attack qualifications. Document all accomplishments.',
    },
    {
      number: 3,
      name: 'Adverse Employment Action',
      mustAllege: 'Plaintiff suffered an adverse employment action (termination, demotion, failure to hire, etc.)',
      typicalEvidence: ['Termination letter', 'Demotion records', 'Rejection letter', 'Wage records'],
      pitfalls: 'Lateral transfers or minor changes may not qualify. Must be materially adverse.',
    },
    {
      number: 4,
      name: 'Circumstances Suggesting Discrimination',
      mustAllege: 'Circumstances give rise to an inference of discrimination',
      typicalEvidence: ['Comparative treatment', 'Discriminatory comments', 'Timing', 'Statistical evidence'],
      pitfalls: 'Stray remarks by non-decisionmakers have limited weight.',
    },
    {
      number: 5,
      name: 'Causation',
      mustAllege: 'Protected characteristic was a motivating factor in the adverse action',
      typicalEvidence: ['Decisionmaker statements', 'Pattern evidence', 'Departure from procedure'],
      pitfalls: 'Same-actor inference may undercut claim if same person hired and fired.',
    },
  ],

  'title_vii_hostile_work_environment': [
    {
      number: 1,
      name: 'Protected Class',
      mustAllege: 'Plaintiff is a member of a protected class',
      typicalEvidence: ['Self-identification', 'Personnel records'],
      pitfalls: 'Harassment must be "because of" protected status.',
    },
    {
      number: 2,
      name: 'Unwelcome Conduct',
      mustAllege: 'Plaintiff was subjected to unwelcome conduct',
      typicalEvidence: ['Complaints made', 'Witness testimony', 'Documented objections'],
      pitfalls: 'Participation in conduct may undercut "unwelcome" showing.',
    },
    {
      number: 3,
      name: 'Based on Protected Class',
      mustAllege: 'Conduct was based on plaintiff\'s protected characteristic',
      typicalEvidence: ['Nature of comments', 'Target selection', 'Comparative treatment'],
      pitfalls: 'General rudeness or harassment not based on protected status insufficient.',
    },
    {
      number: 4,
      name: 'Severe or Pervasive',
      mustAllege: 'Conduct was sufficiently severe or pervasive to alter conditions of employment and create abusive environment',
      typicalEvidence: ['Frequency of incidents', 'Severity documentation', 'Physical threats', 'Interference with work'],
      pitfalls: 'Single incident rarely sufficient unless extremely severe. Consider totality.',
    },
    {
      number: 5,
      name: 'Employer Liability',
      mustAllege: 'Basis for employer liability (supervisor with tangible action, or negligence for co-worker harassment)',
      typicalEvidence: ['Supervisor status', 'Complaints to HR', 'Employer response', 'Policy failures'],
      pitfalls: 'Faragher/Ellerth defense available if no tangible employment action by supervisor.',
    },
  ],

  'flsa_unpaid_wages_overtime': [
    {
      number: 1,
      name: 'Employment Relationship',
      mustAllege: 'Plaintiff was an employee of defendant (not independent contractor)',
      typicalEvidence: ['W-2 forms', 'Employment agreement', 'Control factors analysis'],
      pitfalls: 'FLSA uses "economic reality" test. Misclassification is common.',
    },
    {
      number: 2,
      name: 'Coverage',
      mustAllege: 'Defendant is covered by FLSA (enterprise coverage or individual coverage)',
      typicalEvidence: ['Annual sales > $500K', 'Interstate commerce activity'],
      pitfalls: 'Small employers may not be covered. Check both enterprise and individual coverage.',
    },
    {
      number: 3,
      name: 'Hours Worked',
      mustAllege: 'Plaintiff worked hours in excess of 40 per week (overtime) or was not paid minimum wage',
      typicalEvidence: ['Time records', 'Schedules', 'Testimony', 'Electronic records'],
      pitfalls: 'Records often controlled by employer. Employee estimates may suffice initially.',
    },
    {
      number: 4,
      name: 'Non-Exempt Status',
      mustAllege: 'Plaintiff was not exempt from overtime requirements',
      typicalEvidence: ['Job duties', 'Salary level', 'Discretion exercised', 'Management duties'],
      pitfalls: 'Executive, administrative, professional exemptions common. Analyze actual duties.',
    },
    {
      number: 5,
      name: 'Failure to Pay',
      mustAllege: 'Defendant failed to pay required wages or overtime premium',
      typicalEvidence: ['Pay stubs', 'Bank records', 'Comparison of hours to pay'],
      pitfalls: 'Must show actual hours worked vs. pay received.',
    },
  ],

  // ============================================================================
  // FTCA
  // ============================================================================

  'ftca_negligence': [
    {
      number: 1,
      name: 'Federal Employee',
      mustAllege: 'Negligent actor was a federal employee acting within scope of employment',
      typicalEvidence: ['Employment records', 'Job description', 'Scope of duties'],
      pitfalls: 'Contractors are generally not covered. Scope must be analyzed.',
    },
    {
      number: 2,
      name: 'State Law Tort',
      mustAllege: 'Conduct would constitute a tort under the law of the state where it occurred',
      typicalEvidence: ['State tort law analysis', 'Duty analysis', 'Standard of care'],
      pitfalls: 'FTCA adopts state substantive law. Research specific state requirements.',
    },
    {
      number: 3,
      name: 'Duty',
      mustAllege: 'Federal employee owed plaintiff a duty of care',
      typicalEvidence: ['Relationship', 'Foreseeability', 'State law duty analysis'],
      pitfalls: 'Many federal functions have no private analog (discretionary function).',
    },
    {
      number: 4,
      name: 'Breach',
      mustAllege: 'Federal employee breached the duty of care',
      typicalEvidence: ['Deviation from standard', 'Expert testimony', 'Policy violations'],
      pitfalls: 'Discretionary function exception may bar claim.',
    },
    {
      number: 5,
      name: 'Causation',
      mustAllege: 'Breach was proximate cause of plaintiff\'s injury',
      typicalEvidence: ['Medical causation', 'Expert testimony', 'Timeline'],
      pitfalls: 'Must establish both cause-in-fact and proximate cause.',
    },
    {
      number: 6,
      name: 'Damages',
      mustAllege: 'Plaintiff suffered cognizable damages',
      typicalEvidence: ['Medical bills', 'Lost wages', 'Pain and suffering documentation'],
      pitfalls: 'Punitive damages not available under FTCA.',
    },
  ],

  // ============================================================================
  // COMMERCIAL / RICO
  // ============================================================================

  'rico_1962c': [
    {
      number: 1,
      name: 'Enterprise',
      mustAllege: 'An enterprise exists (association-in-fact or legal entity)',
      typicalEvidence: ['Organizational structure', 'Ongoing relationships', 'Common purpose'],
      pitfalls: 'Enterprise must be distinct from defendant in some circuits. Association-in-fact requires ongoing structure.',
    },
    {
      number: 2,
      name: 'Pattern of Racketeering',
      mustAllege: 'Defendant engaged in a pattern of racketeering activity (at least 2 predicate acts within 10 years showing continuity and relationship)',
      typicalEvidence: ['Evidence of each predicate act', 'Timeline', 'Connection between acts'],
      pitfalls: 'Continuity requires either closed-ended (substantial period) or open-ended (threat of continuity). Isolated fraud schemes may fail.',
    },
    {
      number: 3,
      name: 'Conduct or Participation',
      mustAllege: 'Defendant conducted or participated in the conduct of the enterprise\'s affairs through the pattern',
      typicalEvidence: ['Role in enterprise', 'Decision-making power', 'Direction of predicate acts'],
      pitfalls: 'Mere association insufficient. Must have operation or management role (Reves test).',
    },
    {
      number: 4,
      name: 'Interstate Commerce',
      mustAllege: 'Enterprise engaged in or affected interstate commerce',
      typicalEvidence: ['Multi-state operations', 'Use of interstate communications', 'Impact on commerce'],
      pitfalls: 'Low threshold but must be alleged specifically.',
    },
    {
      number: 5,
      name: 'Injury to Business or Property',
      mustAllege: 'Plaintiff suffered injury to business or property by reason of the violation',
      typicalEvidence: ['Financial losses', 'Property damage', 'Business interruption'],
      pitfalls: 'Personal injuries alone insufficient. Must be business or property injury.',
    },
    {
      number: 6,
      name: 'Proximate Causation',
      mustAllege: 'Violation was proximate cause of injury (direct relation, no independent factors)',
      typicalEvidence: ['Direct harm chain', 'No intervening causes', 'Foreseeability'],
      pitfalls: 'Derivative injuries may not be compensable. Anza v. Ideal Steel Supply Corp.',
    },
  ],

  'false_claims_act_qui_tam': [
    {
      number: 1,
      name: 'False or Fraudulent Claim',
      mustAllege: 'Defendant submitted or caused to be submitted a false or fraudulent claim for payment to the government',
      typicalEvidence: ['Invoices', 'Claims submissions', 'Certifications', 'Billing records'],
      pitfalls: 'Rule 9(b) requires who/what/when/where/how. Specificity essential.',
    },
    {
      number: 2,
      name: 'Scienter',
      mustAllege: 'Defendant acted knowingly (actual knowledge, deliberate ignorance, or reckless disregard)',
      typicalEvidence: ['Internal communications', 'Audit findings', 'Prior warnings', 'Training records'],
      pitfalls: 'Innocent mistakes not actionable. Must show knowledge standard met.',
    },
    {
      number: 3,
      name: 'Materiality',
      mustAllege: 'The false statement or claim was material to the government\'s payment decision',
      typicalEvidence: ['Contract requirements', 'Government policies', 'Evidence of what government would have done'],
      pitfalls: 'Universal Health Services v. Escobar raised materiality bar. Government continued payment may undercut.',
    },
    {
      number: 4,
      name: 'Government Funds',
      mustAllege: 'Claim was for money or property from the United States',
      typicalEvidence: ['Federal contract', 'Grant documents', 'Medicare/Medicaid billing'],
      pitfalls: 'State-only funds may not qualify. Must trace to federal money.',
    },
  ],

  // ============================================================================
  // ERISA
  // ============================================================================

  'erisa_502a1b_benefits': [
    {
      number: 1,
      name: 'ERISA Plan',
      mustAllege: 'A plan exists that is governed by ERISA',
      typicalEvidence: ['Plan documents', 'SPD', 'Form 5500'],
      pitfalls: 'Governmental and church plans may be exempt.',
    },
    {
      number: 2,
      name: 'Participant or Beneficiary',
      mustAllege: 'Plaintiff is a participant or beneficiary of the plan',
      typicalEvidence: ['Enrollment records', 'Plan eligibility provisions', 'Employment records'],
      pitfalls: 'Former employees may lose participant status for some purposes.',
    },
    {
      number: 3,
      name: 'Denial of Benefits',
      mustAllege: 'Benefits were denied or not paid as required by the plan',
      typicalEvidence: ['Denial letter', 'Claim records', 'Plan terms', 'Correspondence'],
      pitfalls: 'Must identify specific benefit and how plan entitles claimant.',
    },
    {
      number: 4,
      name: 'Proper Under Plan Terms',
      mustAllege: 'Benefits are due under the terms of the plan',
      typicalEvidence: ['Plan language', 'SPD provisions', 'Coverage analysis'],
      pitfalls: 'Plan interpretation may be reviewed for abuse of discretion if plan grants discretion.',
    },
  ],

  // ============================================================================
  // APA
  // ============================================================================

  'apa_arbitrary_capricious': [
    {
      number: 1,
      name: 'Final Agency Action',
      mustAllege: 'The challenged action is final agency action',
      typicalEvidence: ['Agency decision letter', 'Order', 'Regulation', 'Denial of petition'],
      pitfalls: 'Must mark consummation of decision-making process and determine rights/obligations.',
    },
    {
      number: 2,
      name: 'Agency Action',
      mustAllege: 'The agency took "action" as defined by the APA',
      typicalEvidence: ['Rule', 'Order', 'License', 'Sanction', 'Relief'],
      pitfalls: 'Inaction may require § 706(1) unreasonable delay claim instead.',
    },
    {
      number: 3,
      name: 'Within Zone of Interests',
      mustAllege: 'Plaintiff\'s interests are arguably within the zone of interests protected by the statute',
      typicalEvidence: ['Statutory purposes', 'Legislative history', 'Relationship to regulated activity'],
      pitfalls: 'Prudential standing requirement. Must be more than marginally related.',
    },
    {
      number: 4,
      name: 'Arbitrary and Capricious',
      mustAllege: 'Agency action was arbitrary, capricious, an abuse of discretion, or otherwise not in accordance with law',
      typicalEvidence: ['Administrative record gaps', 'Failure to consider relevant factors', 'Departure from prior policy without explanation'],
      pitfalls: 'Highly deferential standard. Must show agency failed to consider important aspect, offered implausible explanation, or acted contrary to evidence.',
    },
  ],
};

/**
 * Preconditions for filing various claims
 */
export const CLAIM_PRECONDITIONS: Record<string, ClaimPrecondition[]> = {
  'title_vii_disparate_treatment': [
    {
      type: 'exhaustion',
      requirement: 'EEOC charge filed within 180/300 days of adverse action',
      notes: '300 days if state has FEP agency. Must wait 180 days or receive right-to-sue letter.',
    },
    {
      type: 'timing',
      requirement: 'Suit filed within 90 days of right-to-sue letter',
      notes: 'Strict deadline. No equitable tolling in most circuits.',
    },
  ],

  'ftca_negligence': [
    {
      type: 'exhaustion',
      requirement: 'SF-95 administrative claim filed with appropriate agency',
      notes: 'Must include sum certain. Claim must be finally denied or 6 months pass.',
    },
    {
      type: 'timing',
      requirement: 'Administrative claim within 2 years of accrual; suit within 6 months of denial',
      notes: 'If no final denial, must wait 6 months but can sue any time after.',
    },
  ],

  'erisa_502a1b_benefits': [
    {
      type: 'exhaustion',
      requirement: 'Complete internal appeal process under the plan',
      notes: 'Usually one or two levels of internal appeal. Futility exception narrow.',
    },
  ],

  'apa_arbitrary_capricious': [
    {
      type: 'exhaustion',
      requirement: 'Final agency action',
      notes: 'Must be consummation of decision-making. Preliminary steps don\'t qualify.',
    },
  ],

  '1983_fourth_excessive_force': [
    {
      type: 'standing',
      requirement: 'Actual injury from use of force',
      notes: 'Some circuits require more than de minimis injury for compensatory damages.',
    },
  ],
};

/**
 * Get elements for a specific claim
 */
export function getElements(claimKey: string): ClaimElement[] | undefined {
  return CLAIM_ELEMENTS[claimKey];
}

/**
 * Get preconditions for a specific claim
 */
export function getPreconditions(claimKey: string): ClaimPrecondition[] {
  return CLAIM_PRECONDITIONS[claimKey] || [];
}

/**
 * Get element count for a claim
 */
export function getElementCount(claimKey: string): number {
  const elements = CLAIM_ELEMENTS[claimKey];
  return elements ? elements.length : 0;
}

/**
 * Check if elements are defined for a claim
 */
export function hasElements(claimKey: string): boolean {
  return claimKey in CLAIM_ELEMENTS;
}

/**
 * Get all claims with defined elements
 */
export function getClaimsWithElements(): string[] {
  return Object.keys(CLAIM_ELEMENTS);
}
