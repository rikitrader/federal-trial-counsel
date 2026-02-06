"""
Rule 11 Duty Monitor — Monitors claim viability against current case law.

Works in dual mode:
- OFFLINE (default): Uses built-in VIABILITY_KNOWLEDGE dict covering major
  Supreme Court and Circuit decisions. Zero external calls. Self-sufficient.
- ONLINE (opt-in): When COURTLISTENER_API_TOKEN env var is set and --mode online
  is used, queries CourtListener API v4 via urllib.request (stdlib).
  Graceful fallback to offline on failure.

Produces:
- Per-claim viability checks (viable/warning/questionable/non_viable)
- Overall compliance report (compliant/review_needed/non_compliant)
- Actionable recommendations with citations

Usage:
  ftc monitor -i case.json
  ftc monitor -i case.json --claims key1,key2 --mode online -v
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class ViabilityIssue:
    severity: str  # critical | high | medium | low
    category: str  # scotus_decision | circuit_decision | statutory_amendment | bivens_limitation | exhaustion_change | immunity_expansion
    description: str
    citation: str = ""
    date: str = ""
    recommendation: str = ""


@dataclass
class ViabilityCheck:
    claim_key: str
    claim_name: str
    status: str  # viable | warning | questionable | non_viable
    confidence: float = 0.0  # 0.0-1.0
    issues: list[ViabilityIssue] = field(default_factory=list)
    data_source: str = "built_in"  # built_in | courtlistener


@dataclass
class MonitorReport:
    case_name: str
    claims_checked: int
    checks: list[ViabilityCheck] = field(default_factory=list)
    overall_compliance: str = "compliant"  # compliant | review_needed | non_compliant
    critical_flags: list[str] = field(default_factory=list)
    next_review_recommended: str = ""
    generated_at: str = ""


# ── Built-in Viability Knowledge ────────────────────────────────────────────

VIABILITY_KNOWLEDGE: dict[str, list[ViabilityIssue]] = {
    # Bivens claims — post-Egbert severe restrictions
    "bivens_fourth_search_seizure": [
        ViabilityIssue(
            severity="critical",
            category="scotus_decision",
            description="Bivens extension effectively frozen after Egbert v. Boule. New contexts almost certainly barred.",
            citation="Egbert v. Boule, 596 U.S. 482 (2022)",
            date="2022-06-08",
            recommendation="Verify this is a recognized Bivens context (Bivens itself, Davis, Carlson). If new context, consider § 1983 or FTCA alternative.",
        ),
        ViabilityIssue(
            severity="high",
            category="scotus_decision",
            description="Even in recognized Fourth Amendment Bivens context, courts increasingly find 'special factors' counsel hesitation.",
            citation="Ziglar v. Abbasi, 582 U.S. 120 (2017)",
            date="2017-06-19",
            recommendation="Plead within the exact factual contours of Bivens v. Six Unknown Named Agents, 403 U.S. 388 (1971).",
        ),
    ],
    "bivens_fifth_due_process": [
        ViabilityIssue(
            severity="critical",
            category="scotus_decision",
            description="Fifth Amendment Bivens claims face near-certain dismissal in new contexts post-Egbert.",
            citation="Egbert v. Boule, 596 U.S. 482 (2022)",
            date="2022-06-08",
            recommendation="Only viable in exact Davis v. Passman context (employment discrimination by congressional staffer). Consider FTCA or APA alternatives.",
        ),
    ],
    "bivens_eighth_deliberate_indifference": [
        ViabilityIssue(
            severity="critical",
            category="scotus_decision",
            description="Eighth Amendment Bivens for prisoner conditions may be limited to Carlson v. Green facts.",
            citation="Egbert v. Boule, 596 U.S. 482 (2022)",
            date="2022-06-08",
            recommendation="Plead within Carlson v. Green, 446 U.S. 14 (1980) contours (failure to provide medical treatment). Consider FTCA.",
        ),
    ],

    # Section 1983 — qualified immunity strictness
    "1983_fourth_excessive_force": [
        ViabilityIssue(
            severity="medium",
            category="circuit_decision",
            description="11th Circuit applies strict 'clearly established' standard; factually identical precedent often required.",
            citation="Mercado v. City of Orlando, 407 F.3d 1152 (11th Cir. 2005)",
            date="2005-05-16",
            recommendation="Cite factually analogous 11th Circuit or Supreme Court decisions when opposing qualified immunity.",
        ),
    ],
    "1983_fourth_false_arrest": [
        ViabilityIssue(
            severity="medium",
            category="circuit_decision",
            description="Qualified immunity grants common for false arrest; courts broadly interpret 'arguable probable cause'.",
            citation="Grider v. City of Auburn, 618 F.3d 1240 (11th Cir. 2010)",
            date="2010-08-20",
            recommendation="Show officer lacked even arguable probable cause and cite analogous precedent.",
        ),
    ],
    "1983_monell_municipal_liability": [
        ViabilityIssue(
            severity="medium",
            category="circuit_decision",
            description="Monell pleading standards require specific policy/custom allegations; cannot rely solely on respondeat superior.",
            citation="McDowell v. Brown, 392 F.3d 1283 (11th Cir. 2004)",
            date="2004-12-15",
            recommendation="Plead specific policy, widespread custom, or deliberate indifference to training. Obtain FOIA records of prior complaints.",
        ),
    ],

    # Employment — procedural traps
    "title_vii_disparate_treatment": [
        ViabilityIssue(
            severity="high",
            category="exhaustion_change",
            description="Failure to file EEOC charge within 180/300 days bars claim. Right-to-sue letter required before filing.",
            citation="Fort Bend County v. Davis, 587 U.S. 541 (2019)",
            date="2019-06-03",
            recommendation="Verify EEOC charge was timely filed and right-to-sue letter received. 90-day filing window from receipt is jurisdictional-like.",
        ),
    ],
    "title_vii_hostile_work_environment": [
        ViabilityIssue(
            severity="medium",
            category="circuit_decision",
            description="Continuing violation doctrine may save late-filed claims, but discrete acts still require timely EEOC charge.",
            citation="Nat'l R.R. Passenger Corp. v. Morgan, 536 U.S. 101 (2002)",
            date="2002-06-10",
            recommendation="Distinguish between discrete acts (timely charge required) and hostile environment pattern (continuing violation doctrine applies).",
        ),
    ],
    "adea_age_discrimination": [
        ViabilityIssue(
            severity="medium",
            category="exhaustion_change",
            description="ADEA exhaustion parallels Title VII but mixed motive framework is more limited per Gross v. FBL.",
            citation="Gross v. FBL Financial Services, 557 U.S. 167 (2009)",
            date="2009-06-18",
            recommendation="Plead 'but-for' causation, not merely motivating factor. ADEA requires stronger causal link than Title VII.",
        ),
    ],

    # FTCA
    "ftca_negligence": [
        ViabilityIssue(
            severity="high",
            category="exhaustion_change",
            description="SF-95 administrative claim must be filed within 2 years. Failure is jurisdictional — cannot be waived.",
            citation="McNeil v. United States, 508 U.S. 106 (1993)",
            date="1993-05-17",
            recommendation="Verify SF-95 filed within 2 years of accrual. After denial, file suit within 6 months.",
        ),
        ViabilityIssue(
            severity="medium",
            category="immunity_expansion",
            description="Discretionary function exception (28 U.S.C. 2680(a)) bars many government negligence claims.",
            citation="Berkovitz v. United States, 486 U.S. 531 (1988)",
            date="1988-06-13",
            recommendation="Show government employee violated a mandatory duty (not discretionary judgment).",
        ),
    ],
    "ftca_medical_malpractice": [
        ViabilityIssue(
            severity="high",
            category="exhaustion_change",
            description="SF-95 administrative claim required. State law governs standard of care under FTCA.",
            citation="28 U.S.C. 2674",
            recommendation="File SF-95 within 2 years. Apply forum state's medical malpractice standard (not federal).",
        ),
    ],

    # APA
    "apa_arbitrary_capricious": [
        ViabilityIssue(
            severity="medium",
            category="scotus_decision",
            description="Post-Loper Bright, Chevron deference overruled. Courts now exercise independent judgment on statutory interpretation.",
            citation="Loper Bright Enterprises v. Raimondo, 603 U.S. ___ (2024)",
            date="2024-06-28",
            recommendation="APA challenges may be more viable post-Loper Bright. Argue statutory text independently — Chevron deference no longer applies.",
        ),
    ],

    # PLRA — prisoner claims
    "1983_eighth_deliberate_indifference": [
        ViabilityIssue(
            severity="high",
            category="exhaustion_change",
            description="PLRA requires exhaustion of all available administrative remedies before filing. No exceptions.",
            citation="Ross v. Blake, 578 U.S. 632 (2016)",
            date="2016-06-06",
            recommendation="Exhaust all available prison grievance procedures. If unavailable, document why (Ross v. Blake three exceptions).",
        ),
    ],
}


# ── Viability Checkers ──────────────────────────────────────────────────────

def _check_built_in_viability(claim_key: str) -> list[ViabilityIssue]:
    """Check claim against built-in knowledge base."""
    return VIABILITY_KNOWLEDGE.get(claim_key, [])


def _check_exhaustion_compliance(case_data: dict, claim_key: str) -> list[ViabilityIssue]:
    """Check exhaustion requirements are met."""
    from .claims import get_claim
    meta = get_claim(claim_key)
    if not meta or not meta.exhaustion_required:
        return []

    issues = []
    exhaustion = case_data.get("exhaustion", {})
    etype = meta.exhaustion_type or ""

    # Check EEOC exhaustion
    if "eeoc" in etype:
        if exhaustion.get("eeoc_charge_filed") is False:
            issues.append(ViabilityIssue(
                severity="critical",
                category="exhaustion_change",
                description="EEOC charge NOT filed. Title VII / ADEA / ADA claims require administrative exhaustion.",
                recommendation="File EEOC charge immediately. If 180/300-day deadline passed, analyze tolling options.",
            ))
        elif exhaustion.get("eeoc_charge_filed") is None:
            issues.append(ViabilityIssue(
                severity="high",
                category="exhaustion_change",
                description="EEOC filing status unknown. Must verify before proceeding.",
                recommendation="Confirm EEOC charge was filed and right-to-sue letter was received.",
            ))

    # Check FTCA exhaustion
    if "ftca" in etype:
        if exhaustion.get("ftca_admin_claim_filed") is False:
            issues.append(ViabilityIssue(
                severity="critical",
                category="exhaustion_change",
                description="SF-95 administrative claim NOT filed. FTCA requires exhaustion — jurisdictional bar.",
                citation="28 U.S.C. 2675(a)",
                recommendation="File SF-95 immediately. This is a jurisdictional prerequisite.",
            ))

    # Check PLRA exhaustion
    if "plra" in etype:
        if exhaustion.get("plra_exhaustion_done") is False:
            issues.append(ViabilityIssue(
                severity="critical",
                category="exhaustion_change",
                description="PLRA exhaustion NOT completed. All available administrative remedies must be exhausted.",
                citation="42 U.S.C. 1997e(a); Ross v. Blake, 578 U.S. 632 (2016)",
                recommendation="Complete prison grievance process. Document if unavailable.",
            ))

    return issues


def _check_sol_compliance(case_data: dict, claim_key: str) -> list[ViabilityIssue]:
    """Cross-check SOL status."""
    injury_date_str = case_data.get("limitations", {}).get("key_dates", {}).get("injury_date")
    if not injury_date_str:
        return []

    try:
        from .sol import calculate_sol
        sol = calculate_sol(claim_key, injury_date_str)
        if sol.status == "expired":
            return [ViabilityIssue(
                severity="critical",
                category="exhaustion_change",
                description=f"Statute of limitations EXPIRED. Deadline was {sol.deadline}, {abs(sol.days_remaining)} days ago.",
                recommendation="Analyze tolling doctrines: discovery rule, equitable tolling, fraudulent concealment. If no tolling, drop claim.",
            )]
        if sol.status == "urgent":
            return [ViabilityIssue(
                severity="high",
                category="exhaustion_change",
                description=f"SOL expires in {sol.days_remaining} days (deadline: {sol.deadline}).",
                recommendation="File immediately. Consider filing with leave to amend if investigation is incomplete.",
            )]
    except Exception:
        pass

    return []


def _check_immunity_exposure(case_data: dict, claim_key: str) -> list[ViabilityIssue]:
    """Check immunity risks."""
    from .claims import get_claim
    meta = get_claim(claim_key)
    if not meta:
        return []

    issues = []
    defendants = case_data.get("parties", {}).get("defendants", [])

    if "qualified" in meta.immunities:
        officers = [d for d in defendants if d.get("type") == "officer" or d.get("capacity") == "individual"]
        if officers:
            issues.append(ViabilityIssue(
                severity="medium",
                category="immunity_expansion",
                description="Qualified immunity defense expected. Must identify clearly established law at time of conduct.",
                recommendation="Research factually analogous circuit precedent. Officers are immune unless clearly established law was violated.",
            ))

    if "sovereign" in meta.immunities:
        fed_defs = [d for d in defendants if d.get("type") == "federal"]
        if fed_defs:
            issues.append(ViabilityIssue(
                severity="high",
                category="immunity_expansion",
                description="Sovereign immunity applies to federal defendants unless waived by statute (e.g., FTCA, Tucker Act).",
                recommendation="Identify specific statutory waiver of sovereign immunity.",
            ))

    if "eleventh_amendment" in meta.immunities:
        state_defs = [d for d in defendants if d.get("type") == "state"]
        if state_defs:
            issues.append(ViabilityIssue(
                severity="high",
                category="immunity_expansion",
                description="Eleventh Amendment bars damages claims against states. Ex parte Young exception limited to injunctive relief against officials.",
                citation="Ex parte Young, 209 U.S. 123 (1908)",
                recommendation="Sue state officials in individual capacity or seek only injunctive/declaratory relief.",
            ))

    return issues


def _check_courtlistener(claim_key: str) -> list[ViabilityIssue]:
    """Query CourtListener for recent decisions affecting claim viability (online mode only)."""
    token = os.environ.get("COURTLISTENER_API_TOKEN")
    if not token:
        return []

    try:
        import urllib.request
        import json

        # Map claim to search terms
        search_terms = {
            "bivens_fourth_search_seizure": "Bivens fourth amendment",
            "bivens_fifth_due_process": "Bivens fifth amendment due process",
            "bivens_eighth_deliberate_indifference": "Bivens eighth amendment",
            "1983_fourth_excessive_force": "section 1983 excessive force qualified immunity",
            "1983_monell_municipal_liability": "Monell municipal liability",
            "title_vii_disparate_treatment": "Title VII disparate treatment",
            "apa_arbitrary_capricious": "APA arbitrary capricious chevron",
        }

        query = search_terms.get(claim_key, claim_key.replace("_", " "))
        url = f"https://www.courtlistener.com/api/rest/v4/search/?q={urllib.parse.quote(query)}&type=o&court=scotus,ca11&filed_after=2023-01-01&order_by=dateFiled desc&page_size=3"

        req = urllib.request.Request(url, headers={"Authorization": f"Token {token}"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())

        issues = []
        for result in data.get("results", [])[:3]:
            case_name = result.get("caseName", "Unknown case")
            filed = result.get("dateFiled", "")
            snippet = result.get("snippet", "")[:200]

            issues.append(ViabilityIssue(
                severity="medium",
                category="circuit_decision",
                description=f"Recent decision: {case_name} ({filed}) — {snippet}",
                citation=case_name,
                date=filed,
                recommendation="Review this decision for impact on current claim viability.",
            ))

        return issues

    except Exception:
        # Graceful fallback — online mode is best-effort
        return []


# ── Main API ────────────────────────────────────────────────────────────────

def check_claim_viability(
    case_data: dict,
    claim_key: str,
    mode: str = "offline",
) -> ViabilityCheck:
    """Check viability of a single claim.

    Args:
        case_data: The case JSON data
        claim_key: The claim key to check
        mode: "offline" (built-in only) or "online" (+ CourtListener)

    Returns:
        ViabilityCheck with status, confidence, and issues
    """
    from .claims import get_claim
    meta = get_claim(claim_key)
    claim_name = meta.name if meta else claim_key

    issues: list[ViabilityIssue] = []

    # Built-in knowledge
    issues.extend(_check_built_in_viability(claim_key))

    # Exhaustion compliance
    issues.extend(_check_exhaustion_compliance(case_data, claim_key))

    # SOL compliance
    issues.extend(_check_sol_compliance(case_data, claim_key))

    # Immunity exposure
    issues.extend(_check_immunity_exposure(case_data, claim_key))

    # Online mode
    data_source = "built_in"
    if mode == "online":
        online_issues = _check_courtlistener(claim_key)
        if online_issues:
            issues.extend(online_issues)
            data_source = "courtlistener"

    # Determine status
    critical_count = sum(1 for i in issues if i.severity == "critical")
    high_count = sum(1 for i in issues if i.severity == "high")

    if critical_count >= 2:
        status = "non_viable"
        confidence = 0.9
    elif critical_count >= 1:
        status = "questionable"
        confidence = 0.7
    elif high_count >= 2:
        status = "warning"
        confidence = 0.6
    elif high_count >= 1 or len(issues) >= 3:
        status = "warning"
        confidence = 0.5
    else:
        status = "viable"
        confidence = 0.8 if not issues else 0.6

    return ViabilityCheck(
        claim_key=claim_key,
        claim_name=claim_name,
        status=status,
        confidence=confidence,
        issues=issues,
        data_source=data_source,
    )


def generate_monitor_report(
    case_data: dict,
    claim_keys: list[str] | None = None,
    mode: str = "offline",
) -> MonitorReport:
    """Generate a comprehensive viability monitor report.

    Args:
        case_data: The case JSON data
        claim_keys: Claims to check (auto-detects if None)
        mode: "offline" or "online"

    Returns:
        MonitorReport with all checks and overall compliance
    """
    # Determine claims
    if not claim_keys:
        claim_keys = case_data.get("claims_requested", [])
        if not claim_keys or claim_keys == ["auto_suggest"]:
            from .suggest import suggest_claims
            suggestions = suggest_claims(case_data, max_results=5)
            claim_keys = [s.claim_key for s in suggestions if not s.showstoppers]

    # Run checks
    checks = [check_claim_viability(case_data, ck, mode) for ck in claim_keys]

    # Overall compliance
    non_viable = [c for c in checks if c.status == "non_viable"]
    questionable = [c for c in checks if c.status == "questionable"]
    warnings = [c for c in checks if c.status == "warning"]

    if non_viable:
        overall = "non_compliant"
    elif questionable:
        overall = "review_needed"
    elif warnings:
        overall = "review_needed"
    else:
        overall = "compliant"

    # Critical flags
    critical_flags = []
    for c in checks:
        for issue in c.issues:
            if issue.severity == "critical":
                critical_flags.append(f"[{c.claim_key}] {issue.description[:100]}")

    # Case name
    parties = case_data.get("parties", {})
    plaintiffs = parties.get("plaintiffs", [])
    defendants = parties.get("defendants", [])
    p_name = plaintiffs[0]["name"] if plaintiffs else "Plaintiff"
    d_name = defendants[0]["name"] if defendants else "Defendant"
    case_name = f"{p_name} v. {d_name}"

    return MonitorReport(
        case_name=case_name,
        claims_checked=len(checks),
        checks=checks,
        overall_compliance=overall,
        critical_flags=critical_flags,
        next_review_recommended="30 days" if overall != "compliant" else "90 days",
        generated_at=str(date.today()),
    )


def format_monitor_report(report: MonitorReport, verbose: bool = False) -> str:
    """Format monitor report for CLI output."""
    lines = []

    lines.append("")
    lines.append("=" * 70)
    lines.append("         RULE 11 DUTY MONITOR — CLAIM VIABILITY REPORT")
    lines.append("=" * 70)
    lines.append(f"  Case:       {report.case_name}")
    lines.append(f"  Claims:     {report.claims_checked}")
    lines.append(f"  Compliance: {report.overall_compliance.upper().replace('_', ' ')}")
    lines.append(f"  Review in:  {report.next_review_recommended}")

    if report.critical_flags:
        lines.append("")
        lines.append("  CRITICAL FLAGS:")
        for flag in report.critical_flags:
            lines.append(f"    [!!] {flag}")

    status_icons = {
        "viable": "OK",
        "warning": "??",
        "questionable": "!?",
        "non_viable": "XX",
    }

    lines.append("")
    for check in report.checks:
        icon = status_icons.get(check.status, "??")
        lines.append(f"  [{icon}] {check.claim_key}")
        lines.append(f"       Status: {check.status} (confidence: {check.confidence:.0%})")
        lines.append(f"       Source: {check.data_source}")

        if check.issues:
            for issue in check.issues:
                sev_icon = {"critical": "!!", "high": ">>", "medium": "..", "low": "  "}.get(issue.severity, "  ")
                lines.append(f"       [{sev_icon}] {issue.description[:100]}")
                if verbose:
                    if issue.citation:
                        lines.append(f"            Citation: {issue.citation}")
                    if issue.recommendation:
                        lines.append(f"            Action:   {issue.recommendation}")
        else:
            lines.append("       No known viability issues")
        lines.append("")

    lines.append("=" * 70)
    lines.append(f"  Generated: {report.generated_at}")
    lines.append(f"  Mode: {report.checks[0].data_source if report.checks else 'offline'}")
    lines.append("")

    return "\n".join(lines)
