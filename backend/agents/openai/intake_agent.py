# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

"""
File: backend/agents/openai/intake_agent.py

Need for this file (5th-grader explanation):
“Think of IntakeAgent as our friendly receptionist robot. When a client
drops off a messy letter full of goals, budgets, and ideas, IntakeAgent
opens it up, double‑checks that everything is there, and arranges all the
pieces into neat boxes labeled ‘audience’, ‘budget’, ‘KPIs’, etc. Then it
hands that neat package to the next robot so no one ever loses a note!”
"""

import re, json
from ..base import Agent
from ...utils.openai_client import chat_completion

class IntakeAgent(Agent):
    def run(self, payload: dict) -> dict:
        """
        :param payload: {
            "client_brief": str,
            "goals": str,
            "budget": str,
            "KPIs": List[str]
        }
        :return: {
            "campaign_spec": {
               "objectives": str,
               "budget": float,
               "KPIs": List[str],
               "notes": str
            }
        }
        """
        prompt = (
            "You are the IntakeAgent for an AI-native ad agency. "
            "Below is a raw client brief. Parse it into a JSON object "
            "with keys: objectives, budget, KPIs, and notes. "
            "Ensure budget is a number (in USD) and KPIs is a list of strings.\n\n"
            f"Client brief:\n{payload.get('client_brief')}\n"
            f"Goals: {payload.get('goals')}\n"
            f"Budget: {payload.get('budget')}\n"
            f"KPIs: {json.dumps(payload.get('KPIs', []))}\n\n"
            "Return ONLY the JSON object."
        )

        messages = [
            {"role": "system",  "content": "You are a helpful intake assistant."},
            {"role": "user",    "content": prompt}
        ]
        resp = chat_completion(messages, model="gpt-4o", temperature=0)
        content = resp.choices[0].message.content.strip()
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)

        spec = json.loads(content)
        return {"campaign_spec": spec}


if __name__ == "__main__":
    agent = IntakeAgent()
    test = {
      "client_brief": "We want to increase brand awareness among young adults.",
      "goals": "Improve recall by 20%",
      "budget": "50000",
      "KPIs": ["impressions", "video_views"]
    }
    print(agent.run(test))
