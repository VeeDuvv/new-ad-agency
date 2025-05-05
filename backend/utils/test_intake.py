# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

from backend.agents.openai.intake_agent import IntakeAgent
import json

def test_intake():
    agent = IntakeAgent()
    sample = {
        "client_brief": "We want to boost awareness of our new electric bike among city commuters.",
        "goals": "Increase test-ride signups by 15% in Q3.",
        "budget": "30000",
        "KPIs": ["test_ride_signups", "website_visits"]
    }
    result = agent.run(sample)
    print("IntakeAgent output:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_intake()
