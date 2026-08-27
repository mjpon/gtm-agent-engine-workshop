import json
import os

os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ["LANGSMITH_TRACING"] = "false"
from gtm_agent.gtm_agent import build_prospect_profile, get_prospect


def test_prospect_tools_exclude_billing_identifiers():
    prospect = get_prospect.invoke({"prospect_id": "LEAD-50003"})
    profile = build_prospect_profile.invoke({"prospect_id": "LEAD-50003"})

    for result in (prospect, profile):
        serialized = json.dumps(result)
        assert "tax_id" not in serialized
        assert "card_on_file" not in serialized
        assert "date_of_birth" not in serialized
