/**
 * Federal Pleading Engine - Fact to Element Mapper
 *
 * Maps case facts to required legal elements using keyword matching,
 * actor analysis, and date proximity heuristics.
 */

import {
  CaseInput,
  FactEntry,
  ClaimMappingResult,
  FactElementMapping,
  FactGap,
  ClaimPrecondition,
} from './schema';
import { getClaimMetadata, CLAIM_LIBRARY } from './claim_library';
import { getElements, getPreconditions, CLAIM_ELEMENTS } from './elements';

/**
 * Keywords associated with each element type for matching
 */
const ELEMENT_KEYWORDS: Record<string, string[]> = {
  // Constitutional elements
  'protected_activity': ['speech', 'spoke', 'said', 'wrote', 'published', 'protest', 'complaint', 'petition', 'assembly', 'religion', 'criticized', 'reported', 'whistleblow'],
  'adverse_action': ['fired', 'terminated', 'demoted', 'suspended', 'transferred', 'disciplined', 'denied', 'rejected', 'retaliated', 'punished'],
  'state_actor': ['officer', 'police', 'deputy', 'agent', 'government', 'municipal', 'city', 'county', 'state', 'federal', 'official', 'badge', 'uniform'],
  'seizure': ['arrest', 'detained', 'seized', 'stopped', 'handcuffed', 'custody', 'taken into'],
  'force': ['force', 'struck', 'hit', 'shot', 'tased', 'pepper spray', 'beat', 'punched', 'kicked', 'slammed', 'thrown', 'choked'],
  'search': ['search', 'warrant', 'entered', 'seized property', 'took', 'confiscated'],
  'probable_cause': ['without cause', 'no reason', 'wrongful', 'false', 'baseless', 'groundless'],
  'unreasonable': ['excessive', 'unnecessary', 'unreasonable', 'disproportionate', 'brutal'],

  // Employment elements
  'protected_class': ['race', 'color', 'sex', 'gender', 'religion', 'national origin', 'age', 'disability', 'pregnant', 'LGBTQ', 'African American', 'Hispanic', 'Asian', 'Muslim', 'Jewish', 'Christian'],
  'qualified': ['qualified', 'performed well', 'good reviews', 'met expectations', 'experienced', 'competent'],
  'harassment': ['harassed', 'hostile', 'offensive', 'comments', 'jokes', 'slurs', 'groping', 'inappropriate', 'unwelcome', 'intimidation'],
  'severe_pervasive': ['constant', 'ongoing', 'repeated', 'daily', 'frequently', 'multiple incidents', 'pattern', 'pervasive'],

  // FTCA elements
  'federal_employee': ['federal', 'VA', 'military', 'IRS', 'FBI', 'ICE', 'CBP', 'postal', 'USPS', 'government employee', 'agency'],
  'negligence': ['negligent', 'careless', 'failed to', 'should have', 'breached duty', 'malpractice', 'error', 'mistake'],

  // Damages elements
  'injury': ['injury', 'injured', 'hurt', 'harm', 'damage', 'suffered', 'pain', 'broken', 'fractured', 'bruise', 'contusion', 'trauma'],
  'damages': ['medical', 'hospital', 'treatment', 'lost wages', 'lost income', 'expenses', 'bills', 'costs', 'emotional distress', 'PTSD', 'anxiety', 'depression'],

  // RICO elements
  'enterprise': ['organization', 'company', 'business', 'group', 'association', 'network', 'scheme'],
  'pattern': ['pattern', 'repeated', 'ongoing', 'continuous', 'multiple', 'scheme', 'series'],
  'racketeering': ['fraud', 'bribery', 'extortion', 'mail fraud', 'wire fraud', 'money laundering'],

  // Contract elements
  'agreement': ['contract', 'agreement', 'promised', 'deal', 'terms', 'signed'],
  'breach': ['breach', 'violated', 'failed to perform', 'did not deliver', 'broke'],

  // Monell elements
  'policy': ['policy', 'custom', 'practice', 'training', 'supervision', 'pattern', 'widespread', 'deliberate indifference'],
};

/**
 * Map facts to elements for a specific claim
 */
export function mapFactsToElements(
  caseInput: CaseInput,
  claimKey: string
): ClaimMappingResult {
  const claimMetadata = getClaimMetadata(claimKey);
  const elements = getElements(claimKey);
  const preconditions = getPreconditions(claimKey);

  if (!claimMetadata || !elements) {
    return {
      claimKey,
      claimName: claimMetadata?.name || 'Unknown Claim',
      elements: [],
      overallCoverage: 0,
      factGaps: [{
        elementNumber: 0,
        elementName: 'Claim Definition',
        missingInfo: 'No element definitions found for this claim',
        priority: 'critical',
        suggestedSources: ['Legal research'],
      }],
      preconditions: [],
    };
  }

  const elementMappings: FactElementMapping[] = [];
  const factGaps: FactGap[] = [];

  // Map each element to relevant facts
  for (const element of elements) {
    const mapping = mapElementToFacts(element, caseInput.facts);
    elementMappings.push(mapping);

    // Identify gaps
    if (mapping.coverage === 'none') {
      factGaps.push({
        elementNumber: element.number,
        elementName: element.name,
        missingInfo: element.mustAllege,
        priority: 'critical',
        suggestedSources: element.typicalEvidence,
      });
    } else if (mapping.coverage === 'partial') {
      factGaps.push({
        elementNumber: element.number,
        elementName: element.name,
        missingInfo: `Partial support for: ${element.mustAllege}`,
        priority: 'important',
        suggestedSources: element.typicalEvidence,
      });
    }
  }

  // Calculate overall coverage
  const coveredElements = elementMappings.filter(m => m.coverage !== 'none').length;
  const overallCoverage = Math.round((coveredElements / elements.length) * 100);

  // Evaluate preconditions
  const evaluatedPreconditions = evaluatePreconditions(preconditions, caseInput);

  return {
    claimKey,
    claimName: claimMetadata.name,
    elements: elementMappings,
    overallCoverage,
    factGaps,
    preconditions: evaluatedPreconditions,
  };
}

/**
 * Map a single element to matching facts
 */
function mapElementToFacts(
  element: { number: number; name: string; mustAllege: string; typicalEvidence: string[]; pitfalls: string },
  facts: FactEntry[]
): FactElementMapping {
  const matchingFactIndices: number[] = [];
  const supportingFacts: string[] = [];
  const gaps: string[] = [];

  // Get keywords for this element type
  const keywords = getKeywordsForElement(element.name);

  // Check each fact for matches
  facts.forEach((fact, index) => {
    const factText = `${fact.event} ${fact.harm} ${fact.actors.join(' ')} ${fact.documents.join(' ')}`.toLowerCase();

    const hasMatch = keywords.some(keyword => factText.includes(keyword.toLowerCase()));

    if (hasMatch) {
      matchingFactIndices.push(index);
      supportingFacts.push(fact.event);
    }
  });

  // Determine coverage level
  let coverage: 'full' | 'partial' | 'none';
  if (matchingFactIndices.length >= 2) {
    coverage = 'full';
  } else if (matchingFactIndices.length === 1) {
    coverage = 'partial';
  } else {
    coverage = 'none';
    gaps.push(element.mustAllege);
  }

  return {
    elementNumber: element.number,
    elementName: element.name,
    factIndices: matchingFactIndices,
    coverage,
    supportingFacts,
    gaps,
  };
}

/**
 * Get keywords associated with an element name
 */
function getKeywordsForElement(elementName: string): string[] {
  const normalizedName = elementName.toLowerCase().replace(/[^a-z]/g, '_');

  // Check direct matches
  for (const [key, keywords] of Object.entries(ELEMENT_KEYWORDS)) {
    if (normalizedName.includes(key) || key.includes(normalizedName.substring(0, 5))) {
      return keywords;
    }
  }

  // Fallback: extract key terms from element name
  const terms = elementName.toLowerCase().split(/\s+/);
  const relevantTerms: string[] = [];

  for (const term of terms) {
    if (term.length > 3 && !['the', 'and', 'for', 'was', 'were', 'that', 'with'].includes(term)) {
      relevantTerms.push(term);
    }
  }

  return relevantTerms;
}

/**
 * Evaluate claim preconditions against case input
 */
function evaluatePreconditions(
  preconditions: ClaimPrecondition[],
  caseInput: CaseInput
): ClaimPrecondition[] {
  return preconditions.map(precondition => {
    let satisfied: boolean | 'unknown' = 'unknown';

    switch (precondition.type) {
      case 'exhaustion':
        // Check exhaustion status
        if (precondition.requirement.toLowerCase().includes('eeoc')) {
          satisfied = caseInput.exhaustion.eeoc_charge_filed;
        } else if (precondition.requirement.toLowerCase().includes('sf-95') ||
                   precondition.requirement.toLowerCase().includes('ftca')) {
          satisfied = caseInput.exhaustion.ftca_admin_claim_filed;
        } else if (precondition.requirement.toLowerCase().includes('erisa')) {
          satisfied = caseInput.exhaustion.erisa_appeal_done;
        } else if (precondition.requirement.toLowerCase().includes('agency')) {
          satisfied = caseInput.exhaustion.agency_final_action;
        }
        break;

      case 'timing':
        // Check if key dates are provided
        if (caseInput.limitations.key_dates.injury_date) {
          satisfied = 'unknown'; // Would need SOL calculation
        }
        break;

      case 'standing':
        // Check if facts indicate injury
        const hasInjury = caseInput.facts.some(f =>
          f.harm && f.harm.length > 0
        );
        satisfied = hasInjury;
        break;

      default:
        satisfied = 'unknown';
    }

    return {
      ...precondition,
      satisfied,
    };
  });
}

/**
 * Auto-suggest claims based on facts
 */
export function autoSuggestClaims(caseInput: CaseInput): {
  claimKey: string;
  claimName: string;
  matchScore: number;
  reasons: string[];
  showstoppers: string[];
}[] {
  const suggestions: {
    claimKey: string;
    claimName: string;
    matchScore: number;
    reasons: string[];
    showstoppers: string[];
  }[] = [];

  const allFacts = caseInput.facts.map(f =>
    `${f.event} ${f.harm} ${f.actors.join(' ')}`
  ).join(' ').toLowerCase();

  // Check each claim for relevance
  for (const [claimKey, metadata] of Object.entries(CLAIM_LIBRARY)) {
    const elements = getElements(claimKey);
    if (!elements) continue;

    const reasons: string[] = [];
    const showstoppers: string[] = [];
    let matchScore = 0;

    // Check defendant types
    const hasStateActor = caseInput.parties.defendants.some(d =>
      ['state', 'local', 'federal', 'officer'].includes(d.type)
    );
    const hasPrivateDefendant = caseInput.parties.defendants.some(d =>
      d.type === 'private'
    );

    // Constitutional claims need state actors
    if (metadata.category === 'constitutional_civil_rights' || metadata.category === 'bivens') {
      if (hasStateActor) {
        matchScore += 20;
        reasons.push('State actor defendant identified');
      } else {
        showstoppers.push('No state actor defendant - § 1983 requires action under color of law');
        continue; // Skip this claim
      }
    }

    // Check fact patterns
    if (allFacts.includes('force') || allFacts.includes('beat') || allFacts.includes('shot')) {
      if (claimKey.includes('excessive_force')) {
        matchScore += 30;
        reasons.push('Force-related facts detected');
      }
    }

    if (allFacts.includes('arrest') || allFacts.includes('detained')) {
      if (claimKey.includes('false_arrest')) {
        matchScore += 30;
        reasons.push('Arrest/detention facts detected');
      }
    }

    if (allFacts.includes('fired') || allFacts.includes('terminated') || allFacts.includes('demoted')) {
      if (metadata.category === 'employment') {
        matchScore += 25;
        reasons.push('Employment action detected');
      }
    }

    if (allFacts.includes('discrimination') || allFacts.includes('because of') ||
        allFacts.includes('race') || allFacts.includes('gender')) {
      if (claimKey.includes('title_vii') || claimKey.includes('equal_protection')) {
        matchScore += 25;
        reasons.push('Discrimination language detected');
      }
    }

    // Check exhaustion requirements
    if (metadata.exhaustionRequired) {
      if (metadata.exhaustionType === 'eeoc' && caseInput.exhaustion.eeoc_charge_filed !== true) {
        showstoppers.push('EEOC charge not filed - administrative exhaustion required');
      }
      if (metadata.exhaustionType === 'ftca_sf95' && caseInput.exhaustion.ftca_admin_claim_filed !== true) {
        showstoppers.push('SF-95 administrative claim not filed - FTCA exhaustion required');
      }
    }

    // Check for viability warnings (Bivens)
    if (metadata.viabilityWarning) {
      showstoppers.push(metadata.viabilityWarning);
    }

    // Map facts to elements for scoring
    if (matchScore > 0 || reasons.length > 0) {
      const mapping = mapFactsToElements(caseInput, claimKey);
      matchScore += mapping.overallCoverage * 0.5;

      if (mapping.overallCoverage >= 50) {
        reasons.push(`${mapping.overallCoverage}% element coverage`);
      }
    }

    if (matchScore > 20 || reasons.length > 0) {
      suggestions.push({
        claimKey,
        claimName: metadata.name,
        matchScore: Math.min(100, Math.round(matchScore)),
        reasons,
        showstoppers,
      });
    }
  }

  // Sort by match score
  suggestions.sort((a, b) => b.matchScore - a.matchScore);

  return suggestions.slice(0, 10); // Top 10 suggestions
}

/**
 * Generate fact gap analysis for multiple claims
 */
export function generateFactGapReport(
  caseInput: CaseInput,
  claimKeys: string[]
): FactGap[] {
  const allGaps: FactGap[] = [];
  const seenGaps = new Set<string>();

  for (const claimKey of claimKeys) {
    const mapping = mapFactsToElements(caseInput, claimKey);

    for (const gap of mapping.factGaps) {
      const gapId = `${gap.elementName}-${gap.missingInfo}`;
      if (!seenGaps.has(gapId)) {
        seenGaps.add(gapId);
        allGaps.push(gap);
      }
    }
  }

  // Sort by priority
  const priorityOrder = { critical: 0, important: 1, helpful: 2 };
  allGaps.sort((a, b) => priorityOrder[a.priority] - priorityOrder[b.priority]);

  return allGaps;
}

/**
 * Check if all critical preconditions are met for a claim
 */
export function checkPreconditionsMet(
  caseInput: CaseInput,
  claimKey: string
): { met: boolean; issues: string[] } {
  const preconditions = getPreconditions(claimKey);
  const evaluated = evaluatePreconditions(preconditions, caseInput);

  const issues: string[] = [];

  for (const precondition of evaluated) {
    if (precondition.satisfied === false) {
      issues.push(`${precondition.requirement} - NOT SATISFIED`);
    } else if (precondition.satisfied === 'unknown') {
      issues.push(`${precondition.requirement} - STATUS UNKNOWN`);
    }
  }

  return {
    met: issues.filter(i => i.includes('NOT SATISFIED')).length === 0,
    issues,
  };
}
