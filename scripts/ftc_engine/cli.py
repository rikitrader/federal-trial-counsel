#!/usr/bin/env python3
"""
Federal Trial Counsel - Local Execution CLI

Achieves 90-99% token reduction by running case analysis, claim suggestion,
risk scoring, SOL calculation, and document generation locally in Python.

Usage:
  python3 -m ftc_engine.cli <command> [options]

Commands:
  analyze    - Full case analysis from JSON input
  suggest    - Auto-suggest claims from case facts
  risk       - MTD risk scoring for specific claims
  sol        - Statute of limitations calculator
  draft      - Generate complaint skeleton
  export     - Export to court-formatted .docx (Word/Google Docs/PDF)
  claims     - List all available federal claims
  info       - Show claim metadata
  district   - Manage district configuration
  deposition - Generate deposition question outlines
  exhibits   - Generate exhibit index with authentication checklist
  pacer      - Generate PACER/ECF filing package (JS-44, summons, disclosure)
  monitor    - Rule 11 duty monitor — claim viability report
  calendar   - Generate case filing calendar / document map
  new        - Interactive case wizard (new or existing case)
  open       - Open/resume an existing case
  cases      - List all saved cases
  setup      - Auto-install dependencies and configure environment
  doctor     - Diagnostic health check

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


def cmd_district(args):
    """Manage district configuration."""
    from .districts import (
        get_district, list_districts, get_active_district, set_active_district,
        format_district_info, format_district_list,
    )

    action = args.action

    if action == "list":
        print(format_district_list())
    elif action == "current":
        ctx = get_active_district()
        print(f"Active: {ctx.config.code} — {ctx.config.name}")
        if ctx.division:
            print(f"Division: {ctx.division}")
    elif action == "set":
        if not args.code:
            print("Error: district code required for 'set'", file=sys.stderr)
            sys.exit(1)
        ctx = set_active_district(args.code, args.division)
        print(f"Active district set to: {ctx.config.code} — {ctx.config.name}")
        if ctx.division:
            print(f"Division: {ctx.division}")
    elif action == "info":
        code = args.code or get_active_district().config.code
        config = get_district(code)
        if not config:
            print(f"Unknown district: {code}", file=sys.stderr)
            sys.exit(1)
        print(format_district_info(config))
    else:
        print("Usage: ftc district [list|current|set <code>|info <code>]", file=sys.stderr)
        sys.exit(1)


def cmd_deposition(args):
    """Generate deposition question outlines."""
    from .deposition import generate_deposition_outline, format_deposition_outline
    case_data = _load_case(args.input)

    claim_keys = args.claims.split(",") if args.claims else None
    outline = generate_deposition_outline(
        case_data,
        witness_name=args.witness,
        exam_type=args.type,
        claim_keys=claim_keys,
        max_questions=args.max or 50,
    )

    output_text = format_deposition_outline(outline, verbose=args.verbose)

    if args.output:
        Path(args.output).write_text(output_text)
        print(f"Deposition outline written to {args.output}")
    else:
        print(output_text)


def cmd_exhibits(args):
    """Generate exhibit index."""
    from .exhibits import generate_exhibit_index, format_exhibit_index
    case_data = _load_case(args.input)

    index = generate_exhibit_index(
        case_data,
        scan_directory=args.scan,
        numbering=args.numbering,
        prefix=args.prefix or "",
    )

    output_text = format_exhibit_index(index, fmt=args.format)

    if args.output:
        Path(args.output).write_text(output_text)
        print(f"Exhibit index written to {args.output}")
    else:
        print(output_text)


def cmd_pacer(args):
    """Generate PACER/ECF filing package."""
    from .pacer_meta import (
        generate_filing_package, generate_js44, generate_all_summonses,
        generate_all_disclosures, format_js44, format_summons, format_filing_package,
    )
    case_data = _load_case(args.input)

    if args.all:
        pkg = generate_filing_package(case_data)
        print(format_filing_package(pkg))
    elif args.js44:
        sheet = generate_js44(case_data)
        print(format_js44(sheet))
    elif args.summons:
        summonses = generate_all_summonses(case_data)
        for s in summonses:
            print(format_summons(s))
            print()
    elif args.disclosure:
        disclosures = generate_all_disclosures(case_data)
        if not disclosures:
            print("No corporate parties requiring FRCP 7.1 disclosure.")
        for d in disclosures:
            print(f"{d.party_name} ({d.party_type})")
            print(f"  Parent: {d.parent_corporation}")
            print(f"  10%+ Holder: {d.publicly_held_10pct}")
            print()
    else:
        pkg = generate_filing_package(case_data)
        print(format_filing_package(pkg))


def cmd_monitor(args):
    """Rule 11 duty monitor."""
    from .rule11_monitor import generate_monitor_report, format_monitor_report
    case_data = _load_case(args.input)

    claim_keys = args.claims.split(",") if args.claims else None
    report = generate_monitor_report(case_data, claim_keys=claim_keys, mode=args.mode)

    output_text = format_monitor_report(report, verbose=args.verbose)

    if args.output:
        Path(args.output).write_text(output_text)
        print(f"Monitor report written to {args.output}")
    else:
        print(output_text)


def cmd_calendar(args):
    """Generate case filing calendar."""
    from .filing_calendar import generate_filing_calendar, format_filing_calendar
    case_data = _load_case(args.input)

    calendar = generate_filing_calendar(
        case_data,
        filing_date_str=args.filing_date,
        district_code=args.district,
    )

    output_text = format_filing_calendar(calendar, fmt=args.format)

    if args.output:
        Path(args.output).write_text(output_text)
        print(f"Filing calendar written to {args.output}")
    else:
        print(output_text)


def cmd_setup(args):
    """Auto-install dependencies and configure environment."""
    import subprocess

    print("=" * 70)
    print("         FEDERAL TRIAL COUNSEL — SETUP")
    print("=" * 70)

    # 1. Check Python version
    print(f"\n  Python: {sys.version.split()[0]}", end="")
    if sys.version_info >= (3, 9):
        print(" [OK]")
    else:
        print(" [WARN] Python 3.9+ recommended")

    # 2. Check/install python-docx
    print("  python-docx: ", end="")
    try:
        import docx
        print(f"{docx.__version__} [OK]")
    except ImportError:
        print("not found — installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "python-docx"], check=True)
        print("  python-docx: installed [OK]")

    # 3. Create config directory
    config_dir = Path.home() / ".ftc"
    config_dir.mkdir(exist_ok=True)
    print(f"  Config dir: {config_dir} [OK]")

    # 4. Write default config
    config_file = config_dir / "config.json"
    if not config_file.exists():
        config_file.write_text(json.dumps({"active_district": "mdfl", "division": "Orlando"}, indent=2))
        print(f"  Config file: created [OK]")
    else:
        print(f"  Config file: exists [OK]")

    # 5. Smoke test
    print("\n  Running smoke test...")
    try:
        from .claims import CLAIM_LIBRARY
        from .districts import list_districts
        print(f"  Claims loaded: {len(CLAIM_LIBRARY)} [OK]")
        print(f"  Districts loaded: {len(list_districts())} [OK]")
        print("\n  Setup complete!")
    except Exception as e:
        print(f"  Smoke test failed: {e}")

    print("=" * 70)


def cmd_new(args):
    """Interactive case wizard — new or existing case."""
    from .wizard import start_wizard
    start_wizard()


def cmd_open(args):
    """Open/resume an existing case."""
    from .case_manager import open_case, get_workflow_map
    from .wizard import run_case_wizard
    try:
        state, case_data = open_case(args.case_number)
    except FileNotFoundError:
        print(f"Error: Case not found: {args.case_number}", file=sys.stderr)
        sys.exit(1)

    if args.step:
        # Jump to specific step
        if args.step in state.completed_steps:
            state.completed_steps.remove(args.step)
        state.current_step = args.step
        if args.step not in state.pending_steps:
            state.pending_steps.append(args.step)
        from .case_manager import save_state
        save_state(state)

    print(get_workflow_map(state))
    if state.current_step != "done":
        run_case_wizard(state, case_data)
    else:
        print("\n  All steps complete. Use --step to revisit a section.\n")


def cmd_cases(args):
    """List all saved cases."""
    from .case_manager import list_cases
    cases = list_cases()
    if not cases:
        print("  No saved cases found. Run 'ftc new' to start one.")
        return

    print("=" * 70)
    print("  SAVED CASES")
    print("=" * 70)
    for c in cases:
        print(f"  {c.case_number}")
        print(f"    Name:     {c.case_name}")
        print(f"    Status:   {c.status}")
        print(f"    Step:     {c.current_step}")
        print(f"    Modified: {c.last_modified}")
        print()


def cmd_doctor(args):
    """Diagnostic health check."""
    print("=" * 70)
    print("         FEDERAL TRIAL COUNSEL — DIAGNOSTICS")
    print("=" * 70)

    checks_passed = 0
    checks_total = 0

    # 1. Python version
    checks_total += 1
    py_ok = sys.version_info >= (3, 9)
    icon = "OK" if py_ok else "!!"
    print(f"  [{icon}] Python version: {sys.version.split()[0]}")
    if py_ok:
        checks_passed += 1

    # 2. python-docx
    checks_total += 1
    try:
        import docx
        print(f"  [OK] python-docx: {docx.__version__}")
        checks_passed += 1
    except ImportError:
        print("  [!!] python-docx: NOT INSTALLED — run 'ftc setup'")

    # 3. Config directory
    checks_total += 1
    config_dir = Path.home() / ".ftc"
    if config_dir.exists():
        print(f"  [OK] Config dir: {config_dir}")
        checks_passed += 1
    else:
        print(f"  [!!] Config dir: {config_dir} NOT FOUND — run 'ftc setup'")

    # 4. Active district
    checks_total += 1
    try:
        from .districts import get_active_district
        ctx = get_active_district()
        print(f"  [OK] Active district: {ctx.config.code} — {ctx.config.name}")
        checks_passed += 1
    except Exception as e:
        print(f"  [!!] Active district: error — {e}")

    # 5. Claims library
    checks_total += 1
    try:
        from .claims import CLAIM_LIBRARY
        print(f"  [OK] Claims library: {len(CLAIM_LIBRARY)} claims loaded")
        checks_passed += 1
    except Exception as e:
        print(f"  [!!] Claims library: error — {e}")

    # 6. Templates
    checks_total += 1
    templates_dir = Path(__file__).parent.parent.parent / "assets" / "templates"
    if templates_dir.exists():
        count = sum(1 for _ in templates_dir.rglob("*.md"))
        print(f"  [OK] Templates: {count} templates found")
        checks_passed += 1
    else:
        print(f"  [..] Templates: directory not found (encrypted?)")

    # 7. Sample case
    checks_total += 1
    sample = Path(__file__).parent / "sample_case.json"
    if sample.exists():
        print(f"  [OK] Sample case: {sample.name}")
        checks_passed += 1
    else:
        print(f"  [!!] Sample case: not found")

    # 8. CourtListener token
    checks_total += 1
    import os
    token = os.environ.get("COURTLISTENER_API_TOKEN")
    if token:
        print(f"  [OK] CourtListener API token: configured")
        checks_passed += 1
    else:
        print(f"  [..] CourtListener API token: not set (optional — online monitor mode)")
        checks_passed += 1  # Optional, so still passes

    print(f"\n  Result: {checks_passed}/{checks_total} checks passed")
    print("=" * 70)


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

    # district
    p = sub.add_parser("district", help="Manage district configuration")
    p.add_argument("action", choices=["list", "current", "set", "info"], help="Action")
    p.add_argument("code", nargs="?", help="District code (e.g., sdfl, ndcal)")
    p.add_argument("--division", help="Division within district")

    # deposition
    p = sub.add_parser("deposition", help="Generate deposition question outline")
    p.add_argument("-i", "--input", required=True, help="Case JSON file")
    p.add_argument("-w", "--witness", required=True, help="Witness name")
    p.add_argument("--type", choices=["direct", "cross"], default="cross", help="Exam type")
    p.add_argument("-c", "--claims", help="Comma-separated claim keys")
    p.add_argument("-m", "--max", type=int, default=50, help="Max questions")
    p.add_argument("-o", "--output", help="Output file path")
    p.add_argument("-v", "--verbose", action="store_true")

    # exhibits
    p = sub.add_parser("exhibits", help="Generate exhibit index")
    p.add_argument("-i", "--input", required=True, help="Case JSON file")
    p.add_argument("--scan", help="Directory to scan for documents")
    p.add_argument("--numbering", choices=["alpha", "numeric", "bates"], default="alpha")
    p.add_argument("--prefix", help="Bates prefix (e.g., SMITH)")
    p.add_argument("--format", choices=["table", "detailed"], default="table")
    p.add_argument("-o", "--output", help="Output file path")

    # pacer
    p = sub.add_parser("pacer", help="Generate PACER/ECF filing package")
    p.add_argument("-i", "--input", required=True, help="Case JSON file")
    p.add_argument("--all", action="store_true", help="Generate complete filing package")
    p.add_argument("--js44", action="store_true", help="Generate JS-44 only")
    p.add_argument("--summons", action="store_true", help="Generate summonses only")
    p.add_argument("--disclosure", action="store_true", help="Generate corporate disclosures only")
    p.add_argument("-o", "--output", help="Output directory")

    # monitor
    p = sub.add_parser("monitor", help="Rule 11 duty monitor — claim viability")
    p.add_argument("-i", "--input", required=True, help="Case JSON file")
    p.add_argument("-c", "--claims", help="Comma-separated claim keys")
    p.add_argument("--mode", choices=["offline", "online"], default="offline")
    p.add_argument("-o", "--output", help="Output report file")
    p.add_argument("-v", "--verbose", action="store_true")

    # calendar
    p = sub.add_parser("calendar", help="Generate case filing calendar / document map")
    p.add_argument("-i", "--input", required=True, help="Case JSON file")
    p.add_argument("--filing-date", help="Filing date (YYYY-MM-DD, default: today)")
    p.add_argument("--district", help="District code for timing rules")
    p.add_argument("--format", choices=["table", "detailed"], default="table")
    p.add_argument("-o", "--output", help="Output file path")

    # new (wizard)
    p = sub.add_parser("new", help="Interactive case wizard")
    p.add_argument("-o", "--output", help="Override output directory")

    # open (resume)
    p = sub.add_parser("open", help="Open/resume existing case")
    p.add_argument("case_number", help="Case number (e.g., 6:24-cv-01234-ABC-DEF)")
    p.add_argument("--step", help="Jump to specific step")

    # cases (list)
    sub.add_parser("cases", help="List all saved cases")

    # setup
    sub.add_parser("setup", help="Auto-install dependencies and configure")

    # doctor
    sub.add_parser("doctor", help="Diagnostic health check")

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
        "district": cmd_district,
        "deposition": cmd_deposition,
        "exhibits": cmd_exhibits,
        "pacer": cmd_pacer,
        "monitor": cmd_monitor,
        "calendar": cmd_calendar,
        "new": cmd_new,
        "open": cmd_open,
        "cases": cmd_cases,
        "setup": cmd_setup,
        "doctor": cmd_doctor,
    }
    cmd_map[args.command](args)


if __name__ == "__main__":
    main()
