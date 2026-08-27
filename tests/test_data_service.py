import os
import unittest

os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("LANGSMITH_TRACING", "false")

from gtm_agent import data_service
from gtm_agent.gtm_agent import build_prospect_profile


class UpdateProspectInfoTest(unittest.TestCase):
    def test_technology_update_persists_to_stack_and_profile(self):
        prospect_id = "LEAD-71001"
        record = data_service.get_prospect_record(prospect_id)
        original_stack = list(record["tech_stack"])

        try:
            data_service._PROFILES.pop(prospect_id, None)
            result = data_service.update_prospect_info(prospect_id, "Kafka")

            self.assertIn("Kafka", result["tech_stack"])
            self.assertIn("Kafka", data_service.fetch_tech_stack(prospect_id))
            profile = build_prospect_profile.invoke({"prospect_id": prospect_id})["prospect_profile"]
            self.assertIn("Kafka", profile["tech_stack"])
        finally:
            record["tech_stack"] = original_stack
            data_service._PROFILES.pop(prospect_id, None)


if __name__ == "__main__":
    unittest.main()
