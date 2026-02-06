"""
Document Analyzer — Intake, Parse, Classify, and Route legal documents.

Reads user-provided documents (PDF, DOCX, TXT), classifies them as legal
document types, extracts parties/dates/claims/court info, and auto-routes
to the correct workflow.

Layers:
  1. Text Extraction   — read_document()
  2. Classification     — classify_legal_document()
  3. Entity Extraction  — extract_parties(), extract_dates(), etc.
  4. Analysis Pipeline  — analyze_document(), analyze_intake_docs()
  5. Workflow Routing   — determine_workflow(), build_auto_populated_data()

Usage:
  from ftc_engine.doc_analyzer import analyze_intake_docs, format_analysis_report
  report = analyze_intake_docs("6:24-cv-01234")
  print(format_analysis_report(report))
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


# ── Dataclasses ────────────────────────────────────────────────────────────

@dataclass
class ExtractedEntity:
    entity_type: str    # "plaintiff", "defendant", "date", "case_number", "court", "claim"
    value: str
    confidence: float   # 0.0–1.0
    context: str        # surrounding text snippet


@dataclass
class DocumentAnalysis:
    filename: str
    file_path: str
    document_category: str     # from LEGAL_DOCUMENT_CATEGORIES
    confidence_score: float
    extracted_text: str        # first 5000 chars
    text_length: int
    parties: list[ExtractedEntity] = field(default_factory=list)
    dates: list[ExtractedEntity] = field(default_factory=list)
    case_numbers: list[ExtractedEntity] = field(default_factory=list)
    claims: list[ExtractedEntity] = field(default_factory=list)
    courts: list[ExtractedEntity] = field(default_factory=list)
    key_phrases: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


@dataclass
class IntakeAnalysisReport:
    case_number: str
    analyzed_at: str
    total_documents: int
    successful_analyses: int
    failed_analyses: int
    documents: list[DocumentAnalysis] = field(default_factory=list)
    suggested_workflow: str = "new_case"
    auto_populated: dict = field(default_factory=dict)
    recommendations: list[str] = field(default_factory=list)


# ── Layer 1: Text Extraction ──────────────────────────────────────────────

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt", ".md"}


def read_pdf(path: Path) -> str:
    """Extract text from a PDF file using PyPDF2."""
    from PyPDF2 import PdfReader
    reader = PdfReader(str(path))
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    return "\n".join(pages)


def read_docx(path: Path) -> str:
    """Extract text from a DOCX file."""
    from docx import Document
    doc = Document(str(path))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def read_text(path: Path) -> str:
    """Read plain text or markdown files."""
    return path.read_text(encoding="utf-8", errors="replace")


def read_document(path: Path) -> str:
    """Read any supported document format. Dispatches by extension."""
    ext = path.suffix.lower()
    if ext == ".pdf":
        return read_pdf(path)
    elif ext in (".docx", ".doc"):
        return read_docx(path)
    elif ext in (".txt", ".md"):
        return read_text(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


# ── Layer 2: Legal Document Classification ────────────────────────────────

LEGAL_DOCUMENT_CATEGORIES: dict[str, list[str]] = {
    # Evidence types (aligned with exhibits.py)
    "medical_records": [
        "medical", "hospital", "doctor", "nurse", "diagnosis", "treatment",
        "radiology", "x-ray", "mri", "emergency room", "discharge", "prescription",
    ],
    "police_report": [
        "police", "arrest", "incident report", "use of force", "booking",
        "officer", "body camera", "body cam", "dash cam", "patrol",
    ],
    "financial": [
        "invoice", "receipt", "bank", "check", "payment", "billing", "wage",
        "payroll", "w-2", "tax return", "1099",
    ],
    "correspondence": [
        "letter", "email", "correspondence", "memo", "notice", "demand letter",
    ],
    "photograph": [
        "photo", "image", "picture", "screenshot", "photograph",
    ],
    "employment": [
        "termination", "evaluation", "performance", "handbook", "policy",
        "job description", "offer letter", "employment agreement",
    ],
    "government_record": [
        "foia", "public record", "certificate", "license", "permit",
        "government", "agency", "eeoc", "charge of discrimination",
    ],
    "contract": [
        "contract", "agreement", "lease", "deed", "settlement", "release",
    ],

    # Legal procedural documents (NEW — extends exhibits.py)
    "complaint": [
        "complaint", "civil complaint", "comes now", "jurisdiction",
        "cause of action", "count i", "prayer for relief", "wherefore",
        "plaintiff respectfully", "this action arises",
    ],
    "answer": [
        "answer", "affirmative defense", "general denial", "admits", "denies",
        "defendant answers", "first affirmative defense",
    ],
    "motion_dismiss": [
        "motion to dismiss", "12(b)(6)", "rule 12(b)", "failure to state",
        "plausibility", "iqbal", "twombly", "12(b)(1)",
    ],
    "motion_summary_judgment": [
        "summary judgment", "rule 56", "no genuine issue",
        "material fact", "undisputed", "statement of undisputed facts",
    ],
    "motion_other": [
        "motion to", "motion for", "memorandum in support",
        "respectfully moves", "good cause",
    ],
    "discovery_request": [
        "interrogatories", "request for production", "rfp", "rfa",
        "request for admission", "you are requested", "rule 33", "rule 34",
    ],
    "court_order": [
        "it is ordered", "the court orders", "so ordered",
        "scheduling order", "show cause", "hereby orders",
    ],
    "subpoena": [
        "subpoena", "subpoena duces tecum", "command", "appear and testify",
    ],
    "notice": [
        "notice of removal", "notice of appeal", "notice of filing",
        "hereby give notice", "notice is hereby given",
    ],
    "deposition_transcript": [
        "deposition", "transcript", "testimony", "q.", "a.",
        "direct examination", "cross examination",
    ],
}


_GENERIC_CATEGORIES = {"motion_other"}


def classify_legal_document(text: str, filename: str = "") -> tuple[str, float]:
    """Classify document text into a legal category.

    Returns (category, confidence) where confidence is 0.0–1.0.
    Scoring: keyword count in text + 2x bonus for filename matches.
    Generic catch-all categories (motion_other) only win if no specific
    category scored at all.
    """
    text_lower = text.lower()
    fn_lower = filename.lower()

    best_cat = "other"
    best_score = 0
    best_generic_cat = "other"
    best_generic_score = 0

    for category, keywords in LEGAL_DOCUMENT_CATEGORIES.items():
        score = 0
        for kw in keywords:
            if kw in text_lower:
                score += 1
            if kw in fn_lower:
                score += 2  # filename match is strong signal
        if category in _GENERIC_CATEGORIES:
            if score > best_generic_score:
                best_generic_score = score
                best_generic_cat = category
        else:
            if score > best_score:
                best_score = score
                best_cat = category

    # Prefer specific match; fall back to generic only when nothing specific scored
    if best_score == 0 and best_generic_score > 0:
        best_cat = best_generic_cat
        best_score = best_generic_score

    confidence = min(1.0, best_score / 10.0)
    return best_cat, confidence


# ── Layer 3: Entity Extraction (regex, no ML) ─────────────────────────────

def _snippet(text: str, match: re.Match, window: int = 60) -> str:
    """Extract a text snippet around a regex match."""
    start = max(0, match.start() - window)
    end = min(len(text), match.end() + window)
    return text[start:end].replace("\n", " ").strip()


def extract_parties(text: str) -> list[ExtractedEntity]:
    """Extract plaintiff/defendant names from document text."""
    entities: list[ExtractedEntity] = []

    # Pattern: "Name v. Name" or "Name vs. Name"
    # Length capped at {0,80} to prevent regex backtracking on long inputs
    vs_pat = re.compile(
        r"([A-Z][A-Za-z\s,.']{0,80}?)\s+(?:v\.|vs\.?)\s+([A-Z][A-Za-z\s,.']{0,80}?)(?:[,\n;]|$)",
        re.MULTILINE,
    )
    for m in vs_pat.finditer(text):
        p_name = m.group(1).strip().rstrip(",")
        d_name = m.group(2).strip().rstrip(",")
        if len(p_name) > 2 and len(d_name) > 2:
            entities.append(ExtractedEntity("plaintiff", p_name, 0.8, _snippet(text, m)))
            entities.append(ExtractedEntity("defendant", d_name, 0.8, _snippet(text, m)))

    # Pattern: "Plaintiff: Name" or "Defendant: Name"
    role_pat = re.compile(
        r"(plaintiff|defendant)[s]?\s*[:]\s*([A-Z][A-Za-z\s,.']{0,80}?)(?:\n|$)",
        re.IGNORECASE | re.MULTILINE,
    )
    for m in role_pat.finditer(text):
        role = m.group(1).lower().rstrip("s")
        name = m.group(2).strip().rstrip(",")
        if len(name) > 2:
            entities.append(ExtractedEntity(role, name, 0.7, _snippet(text, m)))

    return entities


def extract_dates(text: str) -> list[ExtractedEntity]:
    """Extract dates in various formats from text."""
    entities: list[ExtractedEntity] = []
    seen: set[str] = set()

    patterns = [
        (r"\b(\d{4}-\d{2}-\d{2})\b", "ISO"),
        (r"\b(\d{2}/\d{2}/\d{4})\b", "US"),
        (r"\b((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4})\b", "written"),
    ]

    for pat, fmt_name in patterns:
        for m in re.finditer(pat, text):
            val = m.group(1)
            if val not in seen:
                seen.add(val)
                entities.append(ExtractedEntity("date", val, 0.9, _snippet(text, m)))

    return entities


def extract_case_number(text: str) -> list[ExtractedEntity]:
    """Extract federal case numbers (e.g. Case No. 6:24-cv-01234)."""
    entities: list[ExtractedEntity] = []
    seen: set[str] = set()

    pat = re.compile(
        r"(?:Case\s+(?:No\.|Number|#)\s*)(\d{1,2}:\d{2}-[a-z]{2}-\d{4,6}(?:-[A-Z]{2,4}(?:-[A-Z]{2,4})?)?)",
        re.IGNORECASE,
    )
    for m in pat.finditer(text):
        val = m.group(1)
        if val not in seen:
            seen.add(val)
            entities.append(ExtractedEntity("case_number", val, 0.95, _snippet(text, m)))

    # Also match standalone case-number patterns without "Case No."
    standalone = re.compile(r"\b(\d{1,2}:\d{2}-cv-\d{4,6}(?:-[A-Z]{2,4}(?:-[A-Z]{2,4})?)?)\b")
    for m in standalone.finditer(text):
        val = m.group(1)
        if val not in seen:
            seen.add(val)
            entities.append(ExtractedEntity("case_number", val, 0.7, _snippet(text, m)))

    return entities


def extract_claims(text: str) -> list[ExtractedEntity]:
    """Extract statutory references and legal claims."""
    entities: list[ExtractedEntity] = []
    seen: set[str] = set()

    claim_patterns = [
        (r"42\s*U\.?S\.?C\.?\s*(?:§|Section)\s*1983", "42 U.S.C. § 1983"),
        (r"Title\s+VII", "Title VII"),
        (r"28\s*U\.?S\.?C\.?\s*(?:§|Section)\s*1331", "28 U.S.C. § 1331 (Federal Question)"),
        (r"28\s*U\.?S\.?C\.?\s*(?:§|Section)\s*1332", "28 U.S.C. § 1332 (Diversity)"),
        (r"28\s*U\.?S\.?C\.?\s*(?:§|Section)\s*1441", "28 U.S.C. § 1441 (Removal)"),
        (r"Federal\s+Tort\s+Claims\s+Act|FTCA", "FTCA"),
        (r"18\s*U\.?S\.?C\.?\s*(?:§|Section)\s*1961|RICO", "RICO"),
        (r"Americans?\s+with\s+Disabilities\s+Act|ADA", "ADA"),
        (r"Age\s+Discrimination\s+in\s+Employment\s+Act|ADEA", "ADEA"),
        (r"Family\s+(?:and\s+)?Medical\s+Leave\s+Act|FMLA", "FMLA"),
        (r"Fair\s+Labor\s+Standards\s+Act|FLSA", "FLSA"),
        (r"False\s+Claims\s+Act|FCA", "FCA"),
    ]

    for pat, label in claim_patterns:
        for m in re.finditer(pat, text, re.IGNORECASE):
            if label not in seen:
                seen.add(label)
                entities.append(ExtractedEntity("claim", label, 0.85, _snippet(text, m)))

    return entities


def extract_court(text: str) -> list[ExtractedEntity]:
    """Extract court information from document text."""
    entities: list[ExtractedEntity] = []

    # Federal district court pattern
    pat = re.compile(
        r"(?:UNITED\s+STATES\s+DISTRICT\s+COURT|U\.?S\.?\s+District\s+Court)[,\s]*"
        r"(?:for\s+the\s+)?(.+?(?:DISTRICT|District)\s+(?:of|OF)\s+[A-Z][a-zA-Z\s]+?)(?:\n|$)",
        re.IGNORECASE | re.MULTILINE,
    )
    for m in pat.finditer(text):
        val = m.group(1).strip()
        if len(val) > 5:
            entities.append(ExtractedEntity("court", val, 0.9, _snippet(text, m)))

    # Fallback: just "District of Florida" etc.
    fallback = re.compile(
        r"((?:Northern|Southern|Middle|Eastern|Western|Central)\s+District\s+of\s+[A-Z][a-zA-Z]+)",
        re.IGNORECASE,
    )
    if not entities:
        for m in fallback.finditer(text):
            entities.append(ExtractedEntity("court", m.group(1).strip(), 0.7, _snippet(text, m)))

    return entities


# ── Layer 4: Analysis Pipeline ────────────────────────────────────────────

def analyze_document(file_path: Path) -> DocumentAnalysis:
    """Analyze a single document: read, classify, extract entities."""
    analysis = DocumentAnalysis(
        filename=file_path.name,
        file_path=str(file_path),
        document_category="other",
        confidence_score=0.0,
        extracted_text="",
        text_length=0,
    )

    try:
        text = read_document(file_path)
    except Exception as e:
        analysis.errors.append(f"Read error: {e}")
        return analysis

    analysis.extracted_text = text[:5000]
    analysis.text_length = len(text)

    # Classify
    cat, conf = classify_legal_document(text, file_path.name)
    analysis.document_category = cat
    analysis.confidence_score = conf

    # Extract entities
    analysis.parties = extract_parties(text)
    analysis.dates = extract_dates(text)
    analysis.case_numbers = extract_case_number(text)
    analysis.claims = extract_claims(text)
    analysis.courts = extract_court(text)

    # Key phrases (top keywords found)
    phrases: list[str] = []
    if cat in LEGAL_DOCUMENT_CATEGORIES:
        text_lower = text.lower()
        for kw in LEGAL_DOCUMENT_CATEGORIES[cat]:
            if kw in text_lower and kw not in phrases:
                phrases.append(kw)
    analysis.key_phrases = phrases[:10]

    return analysis


def analyze_intake_docs(case_number: str) -> IntakeAnalysisReport:
    """Analyze all documents in a case's intake_docs/ folder."""
    from .case_manager import get_case_path

    intake_dir = get_case_path(case_number) / "intake_docs"
    report = IntakeAnalysisReport(
        case_number=case_number,
        analyzed_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
        total_documents=0,
        successful_analyses=0,
        failed_analyses=0,
    )

    if not intake_dir.exists():
        report.recommendations.append("No intake_docs folder found. Import documents first.")
        return report

    files = [
        f for f in sorted(intake_dir.rglob("*"))
        if f.is_file() and not f.name.startswith(".") and f.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    report.total_documents = len(files)

    if not files:
        report.recommendations.append("No supported documents found. Supported: PDF, DOCX, TXT, MD")
        return report

    for fpath in files:
        analysis = analyze_document(fpath)
        report.documents.append(analysis)
        if analysis.errors:
            report.failed_analyses += 1
        else:
            report.successful_analyses += 1

    # Determine workflow and build auto-populated data
    report.suggested_workflow = determine_workflow(report.documents)
    report.auto_populated = build_auto_populated_data(report.documents)
    report.recommendations = generate_recommendations(report.documents)

    return report


# ── Layer 5: Workflow Routing ─────────────────────────────────────────────

WORKFLOW_ROUTING: dict[str, str] = {
    # Procedural documents → specific workflows
    "complaint":                "complaint_defense",
    "answer":                   "existing_litigation",
    "motion_dismiss":           "motion_response",
    "motion_summary_judgment":  "motion_response",
    "motion_other":             "motion_response",
    "discovery_request":        "discovery_response",
    "court_order":              "compliance",
    "subpoena":                 "compliance",
    "notice":                   "existing_litigation",
    "deposition_transcript":    "existing_litigation",
    # Evidence types → standard new case
    "medical_records":          "new_case",
    "police_report":            "new_case",
    "financial":                "new_case",
    "correspondence":           "new_case",
    "photograph":               "new_case",
    "employment":               "new_case",
    "government_record":        "new_case",
    "contract":                 "new_case",
}

# Priority order for routing (higher priority = first match wins)
_ROUTING_PRIORITY = [
    "complaint", "motion_dismiss", "motion_summary_judgment", "motion_other",
    "discovery_request", "court_order", "subpoena", "notice", "answer",
    "deposition_transcript",
]


def determine_workflow(analyses: list[DocumentAnalysis]) -> str:
    """Determine the best workflow based on document classifications.

    Priority: complaint > motion > discovery > order > evidence.
    """
    if not analyses:
        return "new_case"

    categories = {a.document_category for a in analyses if not a.errors}

    for cat in _ROUTING_PRIORITY:
        if cat in categories:
            return WORKFLOW_ROUTING.get(cat, "new_case")

    return "new_case"


def build_auto_populated_data(analyses: list[DocumentAnalysis]) -> dict:
    """Merge extracted entities into a case_data-compatible structure."""
    auto: dict = {}

    all_parties_p: list[dict] = []
    all_parties_d: list[dict] = []
    all_dates: list[str] = []
    court_info: dict = {}
    claims_found: list[str] = []
    case_nums: list[str] = []

    seen_names: set[str] = set()

    for a in analyses:
        if a.errors:
            continue

        for entity in a.parties:
            name = entity.value
            if name in seen_names:
                continue
            seen_names.add(name)
            party = {"name": name, "entity_type": "individual", "citizenship": ""}
            if entity.entity_type == "plaintiff":
                all_parties_p.append(party)
            else:
                all_parties_d.append(party)

        for entity in a.dates:
            if entity.value not in all_dates:
                all_dates.append(entity.value)

        for entity in a.courts:
            if not court_info:
                court_info = {"district": entity.value, "division": "", "state": ""}

        for entity in a.claims:
            if entity.value not in claims_found:
                claims_found.append(entity.value)

        for entity in a.case_numbers:
            if entity.value not in case_nums:
                case_nums.append(entity.value)

    if all_parties_p or all_parties_d:
        auto["parties"] = {
            "plaintiffs": all_parties_p,
            "defendants": all_parties_d,
        }

    if court_info:
        auto["court"] = court_info

    if claims_found:
        auto["claims_extracted"] = claims_found

    if all_dates:
        auto["dates_extracted"] = all_dates

    if case_nums:
        auto["case_numbers_extracted"] = case_nums

    return auto


_WORKFLOW_LABELS: dict[str, str] = {
    "new_case":             "New Case Intake",
    "complaint_defense":    "Complaint Defense (Answer/MTD)",
    "existing_litigation":  "Existing Litigation Management",
    "motion_response":      "Motion Response",
    "discovery_response":   "Discovery Response",
    "compliance":           "Court Order Compliance",
}


def generate_recommendations(analyses: list[DocumentAnalysis]) -> list[str]:
    """Generate actionable recommendations based on the analysis."""
    recs: list[str] = []
    categories = [a.document_category for a in analyses if not a.errors]

    if "complaint" in categories:
        recs.append("Complaint detected — Answer or MTD due within 21 days of service")

    if "motion_dismiss" in categories:
        recs.append("Motion to Dismiss detected — Response due within 21 days")

    if "motion_summary_judgment" in categories:
        recs.append("Summary Judgment motion detected — Response due per local rule")

    if "discovery_request" in categories:
        recs.append("Discovery requests detected — Responses due within 30 days")

    if "court_order" in categories:
        recs.append("Court order detected — Check compliance deadlines immediately")

    if "subpoena" in categories:
        recs.append("Subpoena detected — Compliance or motion to quash required")

    # Claims detected
    all_claims: list[str] = []
    for a in analyses:
        for e in a.claims:
            if e.value not in all_claims:
                all_claims.append(e.value)
    if all_claims:
        recs.append(f"Statutory references found: {', '.join(all_claims)}")

    if not recs:
        recs.append("Evidence documents detected — proceed with standard case intake")

    return recs


# ── Formatting ─────────────────────────────────────────────────────────────

def format_analysis_report(report: IntakeAnalysisReport) -> str:
    """Format the analysis report for CLI display."""
    lines: list[str] = []
    sep = "\u2550" * 70  # ═

    lines.append("")
    lines.append(f"  {sep}")
    lines.append("    DOCUMENT ANALYSIS REPORT")
    lines.append(f"  {sep}")
    lines.append(f"    Case:     {report.case_number}")
    lines.append(f"    Analyzed: {report.analyzed_at}")
    lines.append(f"    Total:    {report.total_documents} documents")
    lines.append(f"    Success:  {report.successful_analyses}  |  Failed: {report.failed_analyses}")
    lines.append("")

    if report.documents:
        lines.append(f"    {'File':<30} {'Category':<25} {'Conf.':<8} {'Entities'}")
        lines.append("    " + "-" * 66)
        for doc in report.documents:
            entity_count = (
                len(doc.parties) + len(doc.dates) + len(doc.case_numbers)
                + len(doc.claims) + len(doc.courts)
            )
            conf_pct = f"{doc.confidence_score:.0%}"
            err = " [ERR]" if doc.errors else ""
            lines.append(
                f"    {doc.filename[:30]:<30} {doc.document_category:<25} {conf_pct:<8} {entity_count}{err}"
            )

    if report.auto_populated:
        lines.append("")
        lines.append("    AUTO-EXTRACTED DATA:")
        if "parties" in report.auto_populated:
            p = report.auto_populated["parties"]
            if p.get("plaintiffs"):
                names = ", ".join(x["name"] for x in p["plaintiffs"])
                lines.append(f"      Plaintiffs: {names}")
            if p.get("defendants"):
                names = ", ".join(x["name"] for x in p["defendants"])
                lines.append(f"      Defendants: {names}")
        if "court" in report.auto_populated:
            lines.append(f"      Court:      {report.auto_populated['court'].get('district', '')}")
        if "claims_extracted" in report.auto_populated:
            lines.append(f"      Claims:     {', '.join(report.auto_populated['claims_extracted'])}")
        if "case_numbers_extracted" in report.auto_populated:
            lines.append(f"      Case No.:   {', '.join(report.auto_populated['case_numbers_extracted'])}")

    # Workflow suggestion
    wf_label = _WORKFLOW_LABELS.get(report.suggested_workflow, report.suggested_workflow)
    lines.append("")
    lines.append(f"    SUGGESTED WORKFLOW: {wf_label}")

    if report.recommendations:
        lines.append("")
        lines.append("    RECOMMENDATIONS:")
        for rec in report.recommendations:
            lines.append(f"      -> {rec}")

    lines.append("")
    lines.append(f"  {sep}")
    lines.append("")

    return "\n".join(lines)
