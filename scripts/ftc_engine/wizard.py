"""
Interactive Case Wizard — Step-by-step intake for new and existing federal cases.

Guides users through a 12-step workflow:
  court → plaintiffs → defendants → facts → claims → relief →
  exhaustion → limitations → goals → review → documents → generate

Usage:
  python3 -m ftc_engine.cli new       # Launch interactive wizard
  python3 -m ftc_engine.cli open X    # Resume existing case
  python3 -m ftc_engine.cli cases     # List all saved cases
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

from .case_manager import (
    CaseState,
    WORKFLOW_STEPS,
    STEP_KEYS,
    create_case,
    open_case,
    list_cases,
    save_state,
    save_case_data,
    load_case_data,
    advance_step,
    get_workflow_map,
    import_documents,
    get_output_path,
)


# ── Input helpers ───────────────────────────────────────────────────────────

def _prompt(label: str, *, required: bool = False, default: str = "",
            description: str = "") -> str:
    """Prompt user for a single text value."""
    parts = [f"  {label}"]
    if description:
        parts[0] += f" ({description})"
    if default:
        parts[0] += f" [{default}]"
    if not required:
        parts[0] += " (blank to skip)"
    parts[0] += ": "

    while True:
        val = input(parts[0]).strip()
        if not val and default:
            return default
        if not val and required:
            print("    → This field is required.")
            continue
        return val


def _prompt_choice(label: str, choices: list[str], *,
                   description: str = "", default: int = 1) -> str:
    """Prompt user to pick one option from a numbered list."""
    if description:
        print(f"\n  {label} — {description}")
    else:
        print(f"\n  {label}:")
    for i, ch in enumerate(choices, 1):
        marker = "*" if i == default else " "
        print(f"    {marker}{i}. {ch}")
    while True:
        raw = input(f"  Choice [{default}]: ").strip()
        if not raw:
            return choices[default - 1]
        if raw.isdigit() and 1 <= int(raw) <= len(choices):
            return choices[int(raw) - 1]
        print(f"    → Enter 1-{len(choices)}")


def _prompt_multi_choice(label: str, choices: list[str], *,
                         preselected: Optional[list[int]] = None) -> list[str]:
    """Prompt user to select multiple items (toggle on/off)."""
    selected = set(preselected or [])
    print(f"\n  {label}:")
    for i, ch in enumerate(choices, 1):
        mark = "X" if i in selected else " "
        print(f"    [{mark}] {i}. {ch}")
    print("  Enter numbers to toggle, 'a' for all, 'done' to confirm:")
    while True:
        raw = input("  > ").strip().lower()
        if raw == "done":
            return [choices[i - 1] for i in sorted(selected)]
        if raw == "a":
            selected = set(range(1, len(choices) + 1))
        elif raw.isdigit() and 1 <= int(raw) <= len(choices):
            n = int(raw)
            selected.symmetric_difference_update({n})
        else:
            print(f"    → Enter 1-{len(choices)}, 'a', or 'done'")
        # Reprint
        for i, ch in enumerate(choices, 1):
            mark = "X" if i in selected else " "
            print(f"    [{mark}] {i}. {ch}")


def _prompt_yes_no(label: str, *, default: bool = False) -> bool:
    """Prompt yes/no question."""
    hint = "Y/n" if default else "y/N"
    raw = input(f"  {label} [{hint}]: ").strip().lower()
    if not raw:
        return default
    return raw.startswith("y")


def _prompt_date(label: str, *, required: bool = False) -> str:
    """Prompt for a date in YYYY-MM-DD format."""
    while True:
        raw = input(f"  {label} (YYYY-MM-DD): ").strip()
        if not raw and not required:
            return ""
        if not raw and required:
            print("    → Date is required.")
            continue
        # Basic validation
        parts = raw.split("-")
        if len(parts) == 3 and all(p.isdigit() for p in parts):
            return raw
        print("    → Format: YYYY-MM-DD")


def _print_header(text: str) -> None:
    """Print a section header."""
    print()
    print("=" * 70)
    print(f"  {text}")
    print("=" * 70)


def _print_table(headers: list[str], rows: list[list[str]]) -> None:
    """Print a simple aligned table."""
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], len(str(cell)))
    fmt = "  ".join(f"{{:<{w}}}" for w in widths)
    print("  " + fmt.format(*headers))
    print("  " + "  ".join("-" * w for w in widths))
    for row in rows:
        padded = [str(row[i]) if i < len(row) else "" for i in range(len(headers))]
        print("  " + fmt.format(*padded))


# ── Section collectors ──────────────────────────────────────────────────────

def collect_court(state: CaseState, case_data: dict) -> dict:
    """Collect court and jurisdiction information."""
    _print_header("STEP 1: COURT & JURISDICTION")

    from .districts import list_districts
    districts = list_districts()
    district_names = [f"{d.name} ({d.code})" for d in districts]
    district_names.append("Other (enter manually)")

    choice = _prompt_choice("Select district", district_names)
    if "Other" in choice:
        district = _prompt("District name", required=True,
                           description="e.g. Middle District of Florida")
        state_name = _prompt("State", required=True)
    else:
        # Parse selected district
        idx = district_names.index(choice)
        d = districts[idx]
        district = d.name
        state_name = d.state

    division = _prompt("Division", description="e.g. Tampa, Orlando")

    case_data["court"] = {
        "district": district,
        "division": division,
        "state": state_name,
    }
    save_case_data(state.case_number, case_data)
    advance_step(state, "court")
    return case_data


def collect_plaintiffs(state: CaseState, case_data: dict) -> dict:
    """Collect plaintiff information — one or more."""
    _print_header("STEP 2: PLAINTIFF INFORMATION")
    plaintiffs: list[dict] = []
    adding = True

    while adding:
        print(f"\n  --- Plaintiff #{len(plaintiffs) + 1} ---")
        p: dict = {}
        p["name"] = _prompt("Full name", required=True)
        entity_choice = _prompt_choice("Entity type", [
            "individual", "corporation", "llc", "partnership", "municipality",
        ])
        p["entity_type"] = entity_choice

        p["citizenship"] = _prompt("Citizenship / State of domicile", required=True)

        if entity_choice in ("corporation", "llc"):
            p["state_of_incorporation"] = _prompt("State of incorporation")
            p["principal_place_of_business"] = _prompt("Principal place of business")

        p["address"] = _prompt("Address")
        p["phone"] = _prompt("Phone")
        p["email"] = _prompt("Email")

        plaintiffs.append(p)
        adding = _prompt_yes_no("Add another plaintiff?")

    case_data["parties"]["plaintiffs"] = plaintiffs
    save_case_data(state.case_number, case_data)
    advance_step(state, "plaintiffs")
    return case_data


def collect_defendants(state: CaseState, case_data: dict) -> dict:
    """Collect defendant information — one or more."""
    _print_header("STEP 3: DEFENDANT INFORMATION")
    defendants: list[dict] = []
    adding = True

    while adding:
        print(f"\n  --- Defendant #{len(defendants) + 1} ---")
        d: dict = {}
        d["name"] = _prompt("Full name", required=True)
        d["entity_type"] = _prompt_choice("Entity type", [
            "individual", "corporation", "llc", "municipality",
            "federal_agency", "state_agency",
        ])
        d["type"] = _prompt_choice("Defendant type", [
            "officer", "local", "federal", "state", "private",
        ])
        d["capacity"] = _prompt_choice("Capacity sued in", [
            "individual", "official", "both",
        ])
        d["citizenship"] = _prompt("Citizenship / State", required=True)
        d["role_title"] = _prompt("Role/title", description="e.g. police officer")

        if d["entity_type"] in ("corporation", "llc"):
            d["state_of_incorporation"] = _prompt("State of incorporation")
            d["principal_place_of_business"] = _prompt("Principal place of business")

        defendants.append(d)
        adding = _prompt_yes_no("Add another defendant?")

    case_data["parties"]["defendants"] = defendants
    save_case_data(state.case_number, case_data)
    advance_step(state, "defendants")
    return case_data


def collect_facts(state: CaseState, case_data: dict) -> dict:
    """Collect factual allegations — one or more."""
    _print_header("STEP 4: FACTUAL ALLEGATIONS")
    facts: list[dict] = case_data.get("facts", [])
    adding = True

    while adding:
        print(f"\n  --- Fact #{len(facts) + 1} ---")
        f: dict = {}
        f["date"] = _prompt_date("Date of event")
        f["location"] = _prompt("Location")
        f["event"] = _prompt("What happened?", required=True,
                             description="Describe the event")
        actors = _prompt("Who was involved?", description="comma-separated")
        f["actors"] = [a.strip() for a in actors.split(",") if a.strip()] if actors else []
        f["harm"] = _prompt("What harm resulted?")
        docs = _prompt("Supporting documents?", description="comma-separated")
        f["documents"] = [d.strip() for d in docs.split(",") if d.strip()] if docs else []
        witnesses = _prompt("Witnesses?", description="comma-separated")
        f["witnesses"] = [w.strip() for w in witnesses.split(",") if w.strip()] if witnesses else []
        evidence = _prompt("Evidence?", description="comma-separated")
        f["evidence"] = [e.strip() for e in evidence.split(",") if e.strip()] if evidence else []
        f["damages_estimate"] = _prompt("Damages estimate?", description="e.g. $150,000")

        facts.append(f)
        adding = _prompt_yes_no("Add another fact?")

    case_data["facts"] = facts
    save_case_data(state.case_number, case_data)
    advance_step(state, "facts")
    return case_data


def collect_claims(state: CaseState, case_data: dict) -> dict:
    """Suggest and select claims based on case facts."""
    _print_header("STEP 5: CLAIMS SELECTION")

    from .suggest import suggest_claims
    from .claims import CLAIM_LIBRARY, list_categories, get_claims_by_category

    # Auto-suggest
    suggestions = suggest_claims(case_data)
    if suggestions:
        print("\n  Auto-suggested claims based on your facts:\n")
        for i, s in enumerate(suggestions, 1):
            print(f"    {i}. [{s.score:.0f}] {s.claim_key} — {s.claim_name}")
        print()

        if _prompt_yes_no("Accept these suggestions?", default=True):
            case_data["claims_requested"] = [s.claim_key for s in suggestions]
        else:
            case_data["claims_requested"] = []
    else:
        print("\n  No claims auto-suggested from facts. Select manually.")
        case_data["claims_requested"] = []

    # Manual addition
    if _prompt_yes_no("Browse claim categories to add more?"):
        categories = list_categories()
        while True:
            cat_choice = _prompt_choice("Category", categories + ["Done — finish selection"])
            if "Done" in cat_choice:
                break
            claims = get_claims_by_category(cat_choice)
            keys = list(claims.keys())
            names = [f"{k} — {claims[k].name}" for k in keys]
            selected = _prompt_multi_choice(f"Claims in {cat_choice}", names)
            for sel in selected:
                key = sel.split(" — ")[0]
                if key not in case_data["claims_requested"]:
                    case_data["claims_requested"].append(key)

    print(f"\n  Selected {len(case_data['claims_requested'])} claim(s).")
    save_case_data(state.case_number, case_data)
    advance_step(state, "claims")
    return case_data


def collect_relief(state: CaseState, case_data: dict) -> dict:
    """Select relief types."""
    _print_header("STEP 6: RELIEF REQUESTED")
    options = [
        "money — Compensatory and/or punitive damages",
        "injunction — Court order to stop/require action",
        "declaratory — Declaration of rights",
        "fees — Attorney fees and costs",
        "restoration — Reinstatement / position restoration",
    ]
    selected = _prompt_multi_choice("Select relief types", options,
                                    preselected=[1, 4])
    case_data["relief_requested"] = [s.split(" — ")[0] for s in selected]
    save_case_data(state.case_number, case_data)
    advance_step(state, "relief")
    return case_data


def collect_exhaustion(state: CaseState, case_data: dict) -> dict:
    """Check administrative exhaustion based on selected claims."""
    _print_header("STEP 7: ADMINISTRATIVE EXHAUSTION")
    claims = case_data.get("claims_requested", [])
    exhaustion: dict = {}

    # Check what's needed
    needs_eeoc = any(c.startswith(("title_vii", "adea", "ada_")) for c in claims)
    needs_ftca = any(c.startswith("ftca_") for c in claims)
    needs_erisa = any(c.startswith("erisa_") for c in claims)
    needs_apa = any(c.startswith("apa_") for c in claims)

    if not any([needs_eeoc, needs_ftca, needs_erisa, needs_apa]):
        print("\n  No exhaustion requirements for your selected claims.")
    else:
        if needs_eeoc:
            exhaustion["eeoc_charge_filed"] = _prompt_yes_no(
                "EEOC charge filed? (required for Title VII/ADEA/ADA)")
            if exhaustion["eeoc_charge_filed"]:
                exhaustion["eeoc_right_to_sue"] = _prompt_yes_no(
                    "Right-to-sue letter received?")
        if needs_ftca:
            exhaustion["ftca_admin_claim_filed"] = _prompt_yes_no(
                "SF-95 administrative claim filed? (required for FTCA)")
        if needs_erisa:
            exhaustion["erisa_appeal_done"] = _prompt_yes_no(
                "Internal ERISA appeal completed?")
        if needs_apa:
            exhaustion["agency_final_action"] = _prompt_yes_no(
                "Agency final action received?")

    case_data["exhaustion"] = exhaustion
    save_case_data(state.case_number, case_data)
    advance_step(state, "exhaustion")
    return case_data


def collect_limitations(state: CaseState, case_data: dict) -> dict:
    """Collect statute of limitations info."""
    _print_header("STEP 8: STATUTE OF LIMITATIONS")
    key_dates: dict = {}

    injury_date = _prompt_date("Date of injury/incident")
    if injury_date:
        key_dates["injury_date"] = injury_date

    tolling = _prompt("Tolling factors?",
                      description="comma-separated, e.g. minority, mental incapacity")
    tolling_list = [t.strip() for t in tolling.split(",") if t.strip()] if tolling else []

    case_data["limitations"] = {
        "key_dates": key_dates,
        "tolling_factors": tolling_list,
    }
    save_case_data(state.case_number, case_data)
    advance_step(state, "limitations")
    return case_data


def collect_goals(state: CaseState, case_data: dict) -> dict:
    """Collect case goals."""
    _print_header("STEP 9: CASE GOALS")
    goals: dict = {}
    goals["primary"] = _prompt("Primary goal",
                               description="e.g. Obtain compensation for injuries")
    goals["secondary"] = _prompt("Secondary goal",
                                 description="e.g. Hold officer accountable")
    case_data["goals"] = goals
    save_case_data(state.case_number, case_data)
    advance_step(state, "goals")
    return case_data


# ── Case summary review ────────────────────────────────────────────────────

def show_case_summary(case_data: dict) -> None:
    """Display complete case summary for review."""
    _print_header("STEP 10: CASE SUMMARY REVIEW")

    court = case_data.get("court", {})
    parties = case_data.get("parties", {})
    facts = case_data.get("facts", [])
    claims = case_data.get("claims_requested", [])
    relief = case_data.get("relief_requested", [])
    exhaustion = case_data.get("exhaustion", {})
    limitations = case_data.get("limitations", {})
    goals = case_data.get("goals", {})

    print(f"\n  Court:       {court.get('district', '—')} / {court.get('division', '—')}")
    print(f"  State:       {court.get('state', '—')}")
    print()

    # Plaintiffs
    pls = parties.get("plaintiffs", [])
    for p in pls:
        print(f"  Plaintiff:   {p.get('name', '—')} ({p.get('entity_type', '—')}, {p.get('citizenship', '—')})")

    # Defendants
    defs = parties.get("defendants", [])
    for d in defs:
        cap = d.get("capacity", "—")
        print(f"  Defendant:   {d.get('name', '—')} ({d.get('type', '—')}, {cap}, {d.get('citizenship', '—')})")

    print(f"\n  Facts:       {len(facts)} allegation(s)")
    print(f"  Claims:      {', '.join(claims) if claims else '—'}")
    print(f"  Relief:      {', '.join(relief) if relief else '—'}")

    # Exhaustion
    if exhaustion:
        exh_items = [f"{k}={'Y' if v else 'N'}" for k, v in exhaustion.items()]
        print(f"  Exhaustion:  {', '.join(exh_items)}")
    else:
        print("  Exhaustion:  N/A")

    # SOL
    injury = limitations.get("key_dates", {}).get("injury_date", "")
    print(f"  Injury date: {injury or '—'}")

    # Goals
    print(f"  Primary:     {goals.get('primary', '—')}")
    print(f"  Secondary:   {goals.get('secondary', '—')}")
    print()


def review_case(state: CaseState, case_data: dict) -> dict:
    """Show summary, let user go back to fix sections."""
    show_case_summary(case_data)

    if _prompt_yes_no("Is this correct?", default=True):
        advance_step(state, "review")
        return case_data

    # Let user go back
    step_labels = [f"{k} — {label}" for k, label in WORKFLOW_STEPS[:9]]
    choice = _prompt_choice("Go back to which section?", step_labels)
    go_back = choice.split(" — ")[0]
    # Remove from completed so it gets re-run
    if go_back in state.completed_steps:
        state.completed_steps.remove(go_back)
    state.current_step = go_back
    if go_back not in state.pending_steps:
        state.pending_steps.append(go_back)
    save_state(state)
    return case_data


# ── Document selection ──────────────────────────────────────────────────────

AVAILABLE_DOCUMENTS = [
    {"key": "complaint", "name": "Complaint Draft"},
    {"key": "analysis", "name": "Full Case Analysis Report"},
    {"key": "js44", "name": "JS-44 Civil Cover Sheet"},
    {"key": "summons", "name": "Summons (per defendant)"},
    {"key": "disclosure", "name": "FRCP 7.1 Corporate Disclosure"},
    {"key": "calendar", "name": "Filing Calendar / Document Map"},
    {"key": "monitor", "name": "Rule 11 Monitor Report"},
    {"key": "risk", "name": "MTD Risk Scores"},
    {"key": "sol", "name": "SOL Report"},
    {"key": "exhibits", "name": "Exhibit Index"},
    {"key": "deposition", "name": "Deposition Outlines"},
    {"key": "questions", "name": "Verification Questions"},
]


def _filter_available_docs(case_data: dict) -> list[dict]:
    """Filter documents to only those possible given the case data."""
    docs = list(AVAILABLE_DOCUMENTS)
    parties = case_data.get("parties", {})
    defs = parties.get("defendants", [])
    all_parties = parties.get("plaintiffs", []) + defs

    # Corporate disclosure only if corporate parties exist
    has_corp = any(
        p.get("entity_type", "").lower() in ("corporation", "llc", "corporate")
        for p in all_parties
    )
    if not has_corp:
        docs = [d for d in docs if d["key"] != "disclosure"]

    # Deposition only if there are witnesses/defendants
    if not defs:
        docs = [d for d in docs if d["key"] != "deposition"]

    return docs


def collect_document_selection(state: CaseState, case_data: dict) -> dict:
    """Let user select which documents to generate."""
    _print_header("STEP 11: DOCUMENT SELECTION")

    available = _filter_available_docs(case_data)
    names = [d["name"] for d in available]
    # Default: select all
    preselected = list(range(1, len(names) + 1))

    selected = _prompt_multi_choice("Select documents to generate", names,
                                    preselected=preselected)
    selected_keys = []
    for sel in selected:
        for d in available:
            if d["name"] == sel:
                selected_keys.append(d["key"])
                break

    state.documents_selected = selected_keys

    # Output format
    fmt = _prompt_choice("Output format", [
        "terminal — Display output only",
        "markdown — Save as .md files",
        "docx — Court-formatted Word documents",
        "both — Markdown + Word",
    ])
    state.output_format = fmt.split(" — ")[0]

    save_state(state)
    advance_step(state, "documents")
    return case_data


# ── Pipeline executor ───────────────────────────────────────────────────────

def execute_pipeline(state: CaseState, case_data: dict) -> list[str]:
    """Generate selected documents, save to case folder, display progress."""
    _print_header("STEP 12: GENERATING DOCUMENTS")
    selected = state.documents_selected
    fmt = state.output_format
    generated: list[str] = []
    total = len(selected)

    for i, key in enumerate(selected, 1):
        label = next((d["name"] for d in AVAILABLE_DOCUMENTS if d["key"] == key), key)
        print(f"\n  [{i}/{total}] {label}...", end=" ", flush=True)

        try:
            text = _generate_document(key, case_data, state)
            if text:
                # Save to disk if not terminal-only
                if fmt in ("markdown", "both"):
                    out = get_output_path(state.case_number, key)
                    out_md = out.with_suffix(".md")
                    out_md.write_text(text)
                    generated.append(str(out_md))

                if fmt in ("docx", "both"):
                    try:
                        from .exporter import export_text
                        out = get_output_path(state.case_number, key)
                        out_docx = str(out.with_suffix(".docx"))
                        export_text(text, out_docx)
                        generated.append(out_docx)
                    except Exception:
                        pass  # docx export is optional

                if fmt == "terminal":
                    print("done")
                    print(text)
                else:
                    print("done")
            else:
                print("skipped (no output)")
        except Exception as e:
            print(f"ERROR: {e}")

    advance_step(state, "generate")

    # Summary
    _print_header("GENERATION COMPLETE")
    print(f"\n  Generated {len(generated)} file(s):")
    for g in generated:
        print(f"    → {g}")
    print(f"\n  Case folder: {state.case_path}")
    print()

    return generated


def _generate_document(key: str, case_data: dict, state: CaseState) -> str:
    """Generate a single document by key. Returns formatted text."""
    if key == "complaint":
        from .drafter import generate_complaint
        return generate_complaint(case_data)

    elif key == "analysis":
        from .suggest import suggest_claims
        from .risk import calculate_mtd_risk
        from .sol import calculate_sol
        from .drafter import analyze_jurisdiction

        lines: list[str] = []
        lines.append("=" * 70)
        lines.append("  FULL CASE ANALYSIS REPORT")
        lines.append("=" * 70)

        jx = analyze_jurisdiction(case_data)
        lines.append(f"\n  Jurisdiction: {jx.basis}")
        lines.append(f"  Venue: {jx.venue}")

        suggestions = suggest_claims(case_data)
        lines.append(f"\n  Suggested Claims ({len(suggestions)}):")
        for s in suggestions:
            lines.append(f"    [{s.score:.0f}] {s.claim_key}")

        claims = case_data.get("claims_requested", [])
        if claims and claims != ["auto_suggest"]:
            lines.append("\n  MTD Risk Scores:")
            for c in claims:
                r = calculate_mtd_risk(case_data, c)
                lines.append(f"    {c}: {r.overall_score}/100")

        injury = case_data.get("limitations", {}).get("key_dates", {}).get("injury_date")
        if injury and claims:
            lines.append("\n  SOL Check:")
            for c in claims:
                if c == "auto_suggest":
                    continue
                sol = calculate_sol(c, injury)
                lines.append(f"    {c}: {sol.days_remaining}d remaining ({sol.status})")

        return "\n".join(lines)

    elif key == "js44":
        from .pacer_meta import generate_js44, format_js44
        return format_js44(generate_js44(case_data))

    elif key == "summons":
        from .pacer_meta import generate_summons, format_summons
        defs = case_data.get("parties", {}).get("defendants", [])
        parts: list[str] = []
        for idx in range(len(defs)):
            s = generate_summons(case_data, idx)
            parts.append(format_summons(s))
        return "\n\n".join(parts)

    elif key == "disclosure":
        from .pacer_meta import generate_corporate_disclosure
        parties = case_data.get("parties", {})
        all_p = parties.get("plaintiffs", []) + parties.get("defendants", [])
        corp = [p for p in all_p
                if p.get("entity_type", "").lower() in ("corporation", "llc", "corporate")]
        if not corp:
            return ""
        parts = []
        for p in corp:
            cd = generate_corporate_disclosure(case_data, p)
            parts.append(f"  FRCP 7.1 Disclosure: {cd.party_name}\n"
                         f"  Parent: {cd.parent_corporation}\n"
                         f"  10%+ Holder: {cd.publicly_held_10pct}")
        return "\n\n".join(parts)

    elif key == "calendar":
        from .filing_calendar import generate_filing_calendar, format_filing_calendar
        cal = generate_filing_calendar(case_data)
        return format_filing_calendar(cal)

    elif key == "monitor":
        from .rule11_monitor import generate_monitor_report, format_monitor_report
        report = generate_monitor_report(case_data)
        return format_monitor_report(report, verbose=True)

    elif key == "risk":
        from .risk import calculate_mtd_risk
        claims = case_data.get("claims_requested", [])
        lines = ["  MTD RISK SCORES", "  " + "-" * 40]
        for c in claims:
            if c == "auto_suggest":
                continue
            r = calculate_mtd_risk(case_data, c)
            lines.append(f"    {c}: {r.overall_score}/100")
        return "\n".join(lines) if len(lines) > 2 else ""

    elif key == "sol":
        from .sol import calculate_sol
        injury = case_data.get("limitations", {}).get("key_dates", {}).get("injury_date")
        claims = case_data.get("claims_requested", [])
        if not injury or not claims:
            return ""
        lines = ["  STATUTE OF LIMITATIONS REPORT", "  " + "-" * 40]
        for c in claims:
            if c == "auto_suggest":
                continue
            result = calculate_sol(c, injury)
            lines.append(f"    {c}: {result.days_remaining}d remaining "
                         f"({result.status}) — deadline {result.deadline}")
        return "\n".join(lines) if len(lines) > 2 else ""

    elif key == "exhibits":
        from .exhibits import generate_exhibit_index, format_exhibit_index
        idx = generate_exhibit_index(case_data)
        return format_exhibit_index(idx, fmt="detailed")

    elif key == "deposition":
        from .deposition import generate_deposition_outline, format_deposition_outline
        defs = case_data.get("parties", {}).get("defendants", [])
        parts = []
        for d in defs:
            outline = generate_deposition_outline(
                case_data, witness_name=d["name"], dep_type="cross")
            parts.append(format_deposition_outline(outline, verbose=True))
        return "\n\n".join(parts)

    elif key == "questions":
        from .questions import generate_questions, format_questions
        qs = generate_questions(case_data)
        return format_questions(qs, verbose=True)

    return ""


# ── Main wizard entry points ───────────────────────────────────────────────

STEP_COLLECTORS = {
    "court": collect_court,
    "plaintiffs": collect_plaintiffs,
    "defendants": collect_defendants,
    "facts": collect_facts,
    "claims": collect_claims,
    "relief": collect_relief,
    "exhaustion": collect_exhaustion,
    "limitations": collect_limitations,
    "goals": collect_goals,
    "review": review_case,
    "documents": collect_document_selection,
    "generate": execute_pipeline,
}


def run_case_wizard(state: CaseState, case_data: dict) -> None:
    """Run the wizard from the current step onwards."""
    print(get_workflow_map(state))

    while state.current_step != "done":
        step = state.current_step
        collector = STEP_COLLECTORS.get(step)
        if collector is None:
            break

        if step == "generate":
            execute_pipeline(state, case_data)
            break
        else:
            case_data = collector(state, case_data)


def start_wizard() -> None:
    """Main wizard entry — asks new vs existing, routes accordingly."""
    _print_header("FEDERAL TRIAL COUNSEL — CASE WIZARD")

    choice = _prompt_choice("Case type", [
        "New case (start from scratch)",
        "Existing case (resume or import documents)",
    ])

    if choice.startswith("New"):
        case_number = _prompt("Case number", required=True,
                              description="e.g. 6:24-cv-01234-ABC-DEF, or 'pending' for pre-filing")
        state = create_case(case_number)
        case_data = load_case_data(case_number)

        # Document intake
        if _prompt_yes_no("Do you have documents to provide for this case?"):
            doc_path = _prompt("Path to documents folder or file", required=True)
            try:
                imported = import_documents(state.case_number, doc_path)
                print(f"  Imported {len(imported)} document(s)")
            except FileNotFoundError as e:
                print(f"  Warning: {e}")

        run_case_wizard(state, case_data)
    else:
        # Existing case
        cases = list_cases()
        if cases:
            print("\n  Saved cases:")
            for i, c in enumerate(cases, 1):
                print(f"    {i}. {c.case_number} — {c.case_name} [{c.status}] step={c.current_step}")

            raw = input("\n  Select case number (or enter new case number): ").strip()
            if raw.isdigit() and 1 <= int(raw) <= len(cases):
                selected = cases[int(raw) - 1]
                state, case_data = open_case(selected.case_number)
            else:
                # Treat as new case number
                try:
                    state, case_data = open_case(raw)
                except FileNotFoundError:
                    state = create_case(raw)
                    case_data = load_case_data(raw)
        else:
            print("\n  No saved cases found.")
            case_number = _prompt("Case number", required=True)
            try:
                state, case_data = open_case(case_number)
            except FileNotFoundError:
                state = create_case(case_number)
                case_data = load_case_data(case_number)

        # Document intake for existing
        if _prompt_yes_no("Do you have documents to provide?"):
            doc_path = _prompt("Path to documents folder or file", required=True)
            try:
                imported = import_documents(state.case_number, doc_path)
                print(f"  Imported {len(imported)} document(s)")
            except FileNotFoundError as e:
                print(f"  Warning: {e}")

        run_case_wizard(state, case_data)
