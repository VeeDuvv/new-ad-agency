# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsiduvvuri

"""
File: backend/agents/openai/strategy_agent.py

Need for this file (5th-grader explanation):
“StrategyAgent is our clever planner robot. It takes the neat campaign spec—things
like objectives, budget, and KPIs—from IntakeAgent, and turns them into a simple game
plan: who to talk to (segments), what big ideas to use (themes), and where to place
our ads (channel_mix). Then it hands that plan to Cathy’s robot so she can break it
into actual steps.”
"""

import re, json
from ..base import Agent
from ...utils.openai_client import chat_completion

class StrategyAgent(Agent):
    def run(self, payload: dict) -> dict:
        """
        :param payload: {
            "campaign_spec": {
               "objectives": str,
               "budget": float,
               "KPIs": List[str],
               "notes": str
            }
        }
        :return: {
            "strategy": {
               "segments": List[str],
               "themes": List[str],
               "channel_mix": { channel_name: float }
            }
        }
        """
        spec = payload.get("campaign_spec", {})
        prompt = (
            "You are the StrategyAgent for an AI-native ad agency.\n"
            "Based on this campaign spec, produce a JSON object with exactly:\n"
            "  • segments: an array of 2–4 distinct audience segments\n"
            "  • themes: an array of 2–3 creative themes (short phrases)\n"
            "  • channel_mix: an object mapping channel names to percentage splits (sum to 1.0)\n\n"
            f"Campaign spec:\n{json.dumps(spec, indent=2)}\n\n"
            "Return ONLY the JSON object—no extra text or markdown."
        )

        messages = [
            {"role": "system", "content": "You are a smart marketing strategist."},
            {"role": "user",   "content": prompt}
        ]
        resp = chat_completion(messages, model="gpt-4o", temperature=0.7)
        content = resp.choices[0].message.content.strip()
        # strip fences
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)

        strategy = json.loads(content)
        return {"strategy": strategy}


if __name__ == "__main__":
    agent = StrategyAgent()
    test_spec = {
        "objectives": "Increase test-ride signups by 15% in Q3.",
        "budget": 30000,
        "KPIs": ["test_ride_signups", "website_visits"],
        "notes": "Focus on urban riders aged 25-35."
    }
    print(json.dumps(agent.run({"campaign_spec": test_spec}), indent=2))
