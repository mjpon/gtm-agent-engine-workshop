import os
import unittest

os.environ.setdefault("OPENAI_API_KEY", "test-key")
from gtm_agent.gtm_agent import send_prospect_email


class SendProspectEmailTests(unittest.TestCase):
    def test_disqualified_prospect_is_blocked_without_message_id(self):
        result = send_prospect_email.func(
            prospect={
                "prospect_id": "LEAD-50002",
                "name": "Liam O'Brien",
                "email": "liam.obrien@meridiansystems.com",
            },
            subject="Technical deep dive",
            body="Please let me know your availability.",
            runtime=type("Runtime", (), {"config": {}})(),
            from_rep={"name": "Ola Adeyemi", "email": "ola.adeyemi@northpoint.com"},
        )

        self.assertEqual(
            result,
            {
                "status": "blocked",
                "reason": "Prospect is marked disqualified in the CRM; sending requires an explicit override from the rep.",
                "prospect_id": "LEAD-50002",
            },
        )
        self.assertNotIn("message_id", result)


if __name__ == "__main__":
    unittest.main()
