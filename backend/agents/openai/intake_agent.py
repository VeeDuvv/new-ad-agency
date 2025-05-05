# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

"""
File: backend/agents/openai/intake_agent.py

Need for this file (5th-grader explanation):
“Think of IntakeAgent as our friendly receptionist robot. When a client
drops off a messy letter full of goals, budgets, and ideas, IntakeAgent
opens it up, double-checks that everything is there, and arranges all the
pieces into neat boxes labeled ‘objectives’, ‘budget’, ‘KPIs’, and ‘notes’.
Then it hands that neat package to the next robot so no one ever loses a note!”
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
        # Build the LLM prompt
        prompt = (
            "You are the IntakeAgent for an AI-native ad agency.\n"
            "Your job is to take this raw client brief and turn it into a JSON object "
            "with exactly these fields:\n"
            "  • objectives: a clear description of what the client wants to achieve\n"
            "  • budget: a number (in USD)\n"
            "  • KPIs: an array of strings\n"
            "  • notes: any extra details or constraints\n\n"
            f"Client brief:\n{payload.get('client_brief')}\n\n"
            f"Goals:\n{payload.get('goals')}\n\n"
            f"Budget:\n{payload.get('budget')}\n\n"
            f"KPIs:\n{json.dumps(payload.get('KPIs', []))}\n\n"
            "Return ONLY the JSON object—no extra text or markdown."
        )

        messages = [
            {"role": "system", "content": "You are a helpful intake assistant."},
            {"role": "user",   "content": prompt}
        ]

        # Call OpenAI
        resp = chat_completion(messages, model="gpt-4o", temperature=0)
        content = resp.choices[0].message.content.strip()

        # Strip code fences if any
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)

        # Parse into dict
        spec = json.loads(content)
        return {"campaign_spec": spec}


# Quick local test
if __name__ == "__main__":
    agent = IntakeAgent()
    sample = {
      "client_brief": "We want to increase brand awareness for our new running shoes among 25–35 year-olds in New York.",
      "goals": "Improve ad recall by 20% and drive 1,000 site visits per week.",
      "budget": "50000",
      "KPIs": ["ad_recall", "site_visits"]
    }
    print(json.dumps(agent.run(sample), indent=2))
