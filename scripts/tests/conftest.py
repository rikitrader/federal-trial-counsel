"""Shared fixtures for FTC engine tests."""
import json
import pytest
from pathlib import Path


@pytest.fixture
def sample_case() -> dict:
    """Load the standard sample case (excessive force / Tampa PD)."""
    path = Path(__file__).parent.parent / "ftc_engine" / "sample_case.json"
    return json.loads(path.read_text())


@pytest.fixture
def minimal_case() -> dict:
    """Bare-minimum case for boundary testing."""
    return {
        "court": {"district": "Middle District of Florida", "division": "Tampa", "state": "Florida"},
        "parties": {
            "plaintiffs": [{"name": "Jane Doe", "entity_type": "individual", "citizenship": "Florida"}],
            "defendants": [{"name": "Corp Inc", "type": "private", "capacity": "individual",
                            "citizenship": "Delaware", "entity_type": "corporation"}],
        },
        "facts": [],
        "claims_requested": [],
        "relief_requested": [],
        "exhaustion": {},
        "limitations": {"key_dates": {}},
        "goals": {},
    }


@pytest.fixture
def federal_defendant_case(minimal_case) -> dict:
    """Case with a federal agency defendant."""
    minimal_case["parties"]["defendants"] = [
        {"name": "Department of Veterans Affairs", "type": "federal",
         "capacity": "official", "citizenship": "Federal", "entity_type": "federal_agency"}
    ]
    minimal_case["exhaustion"]["ftca_admin_claim_filed"] = True
    return minimal_case


@pytest.fixture
def employment_case(minimal_case) -> dict:
    """Employment discrimination case."""
    minimal_case["parties"]["defendants"] = [
        {"name": "MegaCorp LLC", "type": "private", "capacity": "individual",
         "citizenship": "Delaware", "entity_type": "corporation"}
    ]
    minimal_case["facts"] = [
        {"date": "2025-03-01", "event": "Plaintiff was fired after reporting age discrimination",
         "actors": ["MegaCorp LLC"], "harm": "Lost income and benefits",
         "location": "Tampa, FL", "documents": ["Termination letter"], "witnesses": ["HR Director"]},
    ]
    minimal_case["exhaustion"]["eeoc_charge_filed"] = True
    minimal_case["claims_requested"] = ["title_vii_disparate_treatment", "adea_age_discrimination"]
    minimal_case["relief_requested"] = ["money", "fees"]
    minimal_case["limitations"]["key_dates"]["injury_date"] = "2025-03-01"
    return minimal_case
