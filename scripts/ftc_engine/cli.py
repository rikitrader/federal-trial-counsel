#!/usr/bin/env python3
"""
Federal Trial Counsel - Local Execution CLI

Achieves 90-99% token reduction by running case analysis, claim suggestion,
risk scoring, SOL calculation, and document generation locally in Python.

Usage:
  python3 -m ftc_engine.cli <command> [options]

Commands:
  analyze   - Full case analysis from JSON input
  suggest   - Auto-suggest claims from case facts
  risk      - MTD risk scoring for specific claims
  sol       - Statute of limitations calculator
  draft     - Generate complaint skeleton
  export    - Export to court-formatted .docx (Word/Google Docs/PDF)
  claims    - List all available federal claims
  info      - Show claim metadata

Flags:
  -q, --questions  Show post-generation verification questions
  -v, --verbose    Show detailed context for each question
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from datetime import date


def cmd_analyze(args):
    """Full case analysis: suggest claims, score risk, check SOL, generate draft."""
    from .suggest import suggest_claims
    from .risk import calculate_mtd_risk
    from .sol import calculate_sol
    from .drafter import analyze_jurisdiction, generate_complaint

    case_data = _load_case(args.input)

    print("=" * 70)
    print("         FEDERAL TRIAL COUNSEL - CASE ANALYSIS")
    print("=" * 70)

    # 1. Jurisdiction
    jx = analyze_jurisdiction(case_data)
    print(f"\n## Jurisdiction")
    print(f"   Basis:     {jx.basis}")
    print(f"   Satisfied: {jx.satisfied}")
    print(f"   Analysis:  {jx.analysis}")
    print(f"   Venue:     {jx.venue_analysis}")
    print(f"   Standing:  injury={jx.standing_injury} causation={jx.standing_causation} redress={jx.standing_redressability}")

    # 2. Claim suggestions
    suggestions = suggest_claims(case_data)
    print(f"\n## Suggested Claims ({len(suggestions)})")
    for s in suggestions:
        flag = " [SHOWSTOPPERS]" if s.showstoppers else ""
        print(f"   [{s.match_score:3d}] {s.claim_key}{flag}")
        print(f"         {s.claim_name}")
        for r in s.reasons[:3]:
            print(f"         + {r}")
        for ss in s.showstoppers:
            print(f"         ! {ss}")

    # 3. Risk scoring
    claims = case_data.get("claims_requested", [])
    if not claims or claims == ["auto_suggest"]:
        claims = [s.claim_key for s in suggestions[:3] if not s.showstoppers]

    print(f"\n## MTD Risk Scores")
    for ck in claims:
        risk = calculate_mtd_risk(case_data, ck)
        bar = _risk_bar(risk.overall_score)
        print(f"   {ck}")
        print(f"     Score: {risk.overall_score}/100 [{risk.risk_level.upper()}] {bar}")
        for v in risk.top_vulnerabilities[:3]:
            print(f"     ! {v}")
        for f in risk.prioritized_fixes[:2]:
            print(f"     > {f}")

    # 4. SOL
    injury_date = case_data.get("limitations", {}).get("key_dates", {}).get("injury_date")
    if injury_date:
        print(f"\n## Statute of Limitations (injury: {injury_date})")
        for ck in claims:
            try:
                sol = calculate_sol(ck, injury_date)
                icon = {"safe": "OK", "urgent": "!!", "expired": "XX"}.get(sol.status, "??")
                print(f"   [{icon}] {ck}: {sol.days_remaining}d remaining (deadline: {sol.deadline})")
            except Exception as e:
                print(f"   [??] {ck}: {e}")

    # 5. Draft to file if output specified
    if args.output:
        complaint = generate_complaint(case_data)
        out_path = Path(args.output)
        out_path.mkdir(parents=True, exist_ok=True)

        (out_path / "complaint_draft.md").write_text(complaint)
        print(f"\n## Draft written to {out_path / 'complaint_draft.md'}")

        # Also write JSON report
        report = {
            "jurisdiction": {"basis": jx.basis, "satisfied": jx.satisfied, "analysis": jx.analysis},
            "suggestions": [{"key": s.claim_key, "score": s.match_score, "reasons": s.reasons, "showstoppers": s.showstoppers} for s in suggestions],
            "risk_scores": {ck: {"score": (r := calculate_mtd_risk(case_data, ck)).overall_score, "level": r.risk_level} for ck in claims},
            "generated": str(date.today()),
        }
        (out_path / "analysis_report.json").write_text(json.dumps(report, indent=2, default=str))
        print(f"   Report written to {out_path / 'analysis_report.json'}")

    print("\n" + "=" * 70)

    # 6. Post-generation questions
    if getattr(args, "questions", False):
        from .questions import generate_questions, format_questions

        suggestion_dicts = [{"key": s.claim_key, "score": s.match_score, "showstoppers": s.showstoppers} for s in suggestions]
        risk_dict = {ck: {"score": calculate_mtd_risk(case_data, ck).overall_score, "level": calculate_mtd_risk(case_data, ck).risk_level} for ck in claims}

        sol_dicts = None
        if injury_date:
            sol_dicts = []
            for ck in claims:
                try:
                    sol = calculate_sol(ck, injury_date)
                    sol_dicts.append({"claim_key": ck, "status": sol.status, "days_remaining": sol.days_remaining})
                except Exception:
                    pass

        qs = generate_questions(case_data, doc_type="analyze", suggestions=suggestion_dicts, risk_scores=risk_dict, sol_results=sol_dicts)
        print(format_questions(qs, verbose=getattr(args, "verbose", False)))


def cmd_suggest(args):
    """Auto-suggest claims based on case facts."""
    from .suggest import suggest_claims
    case_data = _load_case(args.input)
    suggestions = suggest_claims(case_data, args.max if args.max is not None else 10)

    print(f"{'Score':>5}  {'Claim Key':<45} {'Name'}")
    print("-" * 100)
    for s in suggestions:
        flag = " *" if s.showstoppers else ""
        print(f"{s.match_score:>5}  {s.claim_key:<45} {s.claim_name}{flag}")
        if args.verbose:
            for r in s.reasons:
                print(f"       + {r}")
            for ss in s.showstoppers:
                print(f"       ! {ss}")


def cmd_risk(args):
    """MTD risk scoring."""
    from .risk import calculate_mtd_risk
    case_data = _load_case(args.input)
    claims = args.claims.split(",") if args.claims else case_data.get("claims_requested", [])

    for ck in claims:
        ck = ck.strip()
        risk = calculate_mtd_risk(case_data, ck)
        bar = _risk_bar(risk.overall_score)
        print(f"\n## {ck}")
        print(f"   Overall: {risk.overall_score}/100 [{risk.risk_level.upper()}] {bar}")
        print(f"   Factors:")
        for f in risk.factors:
            fbar = _risk_bar(f.score)
            print(f"     {f.category:<15} {f.score:>3}/100 {fbar} {f.issue}")
        if risk.prioritized_fixes:
            print(f"   Fixes:")
            for fix in risk.prioritized_fixes:
                print(f"     > {fix}")


def cmd_sol(args):
    """Statute of limitations calculator."""
    from .sol import calculate_sol, calculate_all_sol
    claims = args.claims.split(",")
    try:
        results = calculate_all_sol([c.strip() for c in claims], args.date)
    except Exception as e:
        print(f"Error calculating SOL: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"{'Status':<8} {'Claim':<45} {'Deadline':<12} {'Remaining':>10}")
    print("-" * 80)
    for r in results:
        icon = {"safe": "OK", "urgent": "URGENT", "expired": "EXPIRED"}.get(r.status, "UNKNOWN")
        print(f"{icon:<8} {r.claim_key:<45} {r.deadline} {r.days_remaining:>7}d")
        if args.verbose:
            for note in r.tolling_notes[:2]:
                print(f"         * {note}")


def cmd_draft(args):
    """Generate complaint skeleton."""
    from .drafter import generate_complaint
    case_data = _load_case(args.input)
    complaint = generate_complaint(case_data)

    if args.output:
        Path(args.output).write_text(complaint)
        print(f"Complaint written to {args.output}")
    else:
        print(complaint)

    if getattr(args, "questions", False):
        from .questions import generate_questions, format_questions
        qs = generate_questions(case_data, doc_type="draft")
        print(format_questions(qs, verbose=getattr(args, "verbose", False)))


def cmd_claims(args):
    """List all available federal claims."""
    from .claims import CLAIM_LIBRARY, list_categories
    for cat in list_categories():
        print(f"\n## {cat.upper().replace('_', ' ')}")
        for key, meta in CLAIM_LIBRARY.items():
            if meta.category == cat:
                flags = []
                if meta.heightened_pleading:
                    flags.append("9(b)")
                if meta.exhaustion_required:
                    flags.append(f"exhaust:{meta.exhaustion_type}")
                if meta.immunities:
                    flags.append(f"imm:{','.join(meta.immunities)}")
                flag_str = f" [{'; '.join(flags)}]" if flags else ""
                print(f"  {key:<45} {meta.name}{flag_str}")


def cmd_export(args):
    """Export to court-formatted .docx (Word/Google Docs/PDF-ready)."""
    from .exporter import export_draft, export_template, export_text, list_templates

    if args.list_templates:
        templates = list_templates()
        print(f"{'Category':<15} {'Template Name':<40} {'Path'}")
        print("-" * 80)
        for t in templates:
            print(f"{t['category']:<15} {t['name']:<40} {t['path']}")
        return

    output = args.output or "output.docx"

    if args.draft:
        case_data = _load_case(args.input)
        result = export_draft(case_data, output)
        print(f"Complaint draft exported to: {result.output_path}")
        print(f"  Format: .docx (Times New Roman 12pt, double-spaced, 1\" margins)")
        print(f"  Sections: {result.sections}")
        print(f"  Open in: Microsoft Word, Google Docs, or LibreOffice")
        print(f"  To PDF: File > Export/Print as PDF from any of the above")
    elif args.template:
        case_data = _load_case(args.input) if args.input else {}
        result = export_template(args.template, case_data, output)
        print(f"Template exported to: {result.output_path}")
        print(f"  Template: {args.template}")
        print(f"  Format: .docx (Times New Roman 12pt, double-spaced, 1\" margins)")
        print(f"  Sections: {result.sections}")
    elif args.text:
        from pathlib import Path as P
        text = P(args.text).read_text()
        result = export_text(text, output)
        print(f"Text exported to: {result.output_path}")
        print(f"  Format: .docx (court-formatted)")
    else:
        print("Error: specify --draft, --template, --text, or --list-templates", file=sys.stderr)
        sys.exit(1)

    if getattr(args, "questions", False) and hasattr(args, "input") and args.input:
        from .questions import generate_questions, format_questions
        case_data = _load_case(args.input)
        qs = generate_questions(case_data, doc_type="export")
        print(format_questions(qs, verbose=getattr(args, "verbose", False)))


def cmd_info(args):
    """Show detailed claim metadata."""
    from .claims import get_claim
    meta = get_claim(args.claim)
    if not meta:
        print(f"Unknown claim: {args.claim}")
        sys.exit(1)
    print(f"Name:           {meta.name}")
    print(f"Category:       {meta.category}")
    print(f"Source:         {meta.source}")
    print(f"Jurisdiction:   {meta.jurisdiction}")
    print(f"SOL:            {meta.statute_of_limitations}")
    print(f"Heightened 9b:  {meta.heightened_pleading}")
    print(f"Exhaustion:     {meta.exhaustion_required} ({meta.exhaustion_type or 'N/A'})")
    print(f"Immunities:     {', '.join(meta.immunities) or 'None'}")
    print(f"Defenses:       {'; '.join(meta.typical_defenses[:5])}")
    if meta.viability_warning:
        print(f"WARNING:        {meta.viability_warning}")


def _load_case(path: str) -> dict:
    """Load case JSON file."""
    try:
        return json.loads(Path(path).read_text())
    except FileNotFoundError:
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {path}: {e}", file=sys.stderr)
        sys.exit(1)


def _risk_bar(score: int) -> str:
    """Generate ASCII risk bar."""
    score = max(0, min(100, score))
    filled = score // 5
    empty = 20 - filled
    return f"[{'#' * filled}{'.' * empty}]"


def main():
    parser = argparse.ArgumentParser(
        prog="ftc",
        description="Federal Trial Counsel - Local Execution Engine",
    )
    sub = parser.add_subparsers(dest="command", help="Command")

    # analyze
    p = sub.add_parser("analyze", help="Full case analysis")
    p.add_argument("-i", "--input", required=True, help="Case JSON file")
    p.add_argument("-o", "--output", help="Output directory")
    p.add_argument("-q", "--questions", action="store_true", help="Show post-generation verification questions")
    p.add_argument("-v", "--verbose", action="store_true", help="Show detailed context for questions")

    # suggest
    p = sub.add_parser("suggest", help="Auto-suggest claims")
    p.add_argument("-i", "--input", required=True, help="Case JSON file")
    p.add_argument("-m", "--max", type=int, default=10, help="Max results")
    p.add_argument("-v", "--verbose", action="store_true")

    # risk
    p = sub.add_parser("risk", help="MTD risk scoring")
    p.add_argument("-i", "--input", required=True, help="Case JSON file")
    p.add_argument("-c", "--claims", help="Comma-separated claim keys")

    # sol
    p = sub.add_parser("sol", help="Statute of limitations")
    p.add_argument("-c", "--claims", required=True, help="Comma-separated claim keys")
    p.add_argument("-d", "--date", required=True, help="Injury date (YYYY-MM-DD)")
    p.add_argument("-v", "--verbose", action="store_true")

    # draft
    p = sub.add_parser("draft", help="Generate complaint")
    p.add_argument("-i", "--input", required=True, help="Case JSON file")
    p.add_argument("-o", "--output", help="Output file path")
    p.add_argument("-q", "--questions", action="store_true", help="Show post-generation verification questions")
    p.add_argument("-v", "--verbose", action="store_true", help="Show detailed context for questions")

    # claims
    sub.add_parser("claims", help="List all claims")

    # export
    p = sub.add_parser("export", help="Export to .docx (Word/Google Docs/PDF)")
    p.add_argument("--draft", action="store_true", help="Export generated complaint draft")
    p.add_argument("-t", "--template", help="Template path (e.g. motions/motion_to_dismiss)")
    p.add_argument("--text", help="Path to markdown/text file to convert")
    p.add_argument("-i", "--input", help="Case JSON file (for placeholder filling)")
    p.add_argument("-o", "--output", help="Output .docx file path")
    p.add_argument("--list-templates", action="store_true", help="List all available templates")
    p.add_argument("-q", "--questions", action="store_true", help="Show post-generation verification questions")
    p.add_argument("-v", "--verbose", action="store_true", help="Show detailed context for questions")

    # info
    p = sub.add_parser("info", help="Claim metadata")
    p.add_argument("claim", help="Claim key")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmd_map = {
        "analyze": cmd_analyze,
        "suggest": cmd_suggest,
        "risk": cmd_risk,
        "sol": cmd_sol,
        "draft": cmd_draft,
        "export": cmd_export,
        "claims": cmd_claims,
        "info": cmd_info,
    }
    cmd_map[args.command](args)


if __name__ == "__main__":
    main()
