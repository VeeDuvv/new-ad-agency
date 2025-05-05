# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

"""
File: backend/agents/openai/strategy_agent.py

Need for this file (5th‑grader explanation):
“Think of StrategyAgent as our clever planner robot.  It takes the neat
campaign spec from IntakeAgent—things like audience, budget, and KPIs—
and turns them into a simple game plan: who we talk to, what messages
we use, and where we place our ads.  Then it hands that plan to Cathy’s
robot so she can break it into actual steps.”
"""

from ..base import Agent

class StrategyAgent(Agent):
    def run(self, payload: dict) -> dict:
        # For now return a dummy “strategy” so DirectorAgent can continue
        spec = payload.get("campaign_spec", {})
        return {
            "strategy": {
                "segments": ["default_segment"],
                "themes": ["default_theme"],
                "channel_mix": {"display": 0.5, "social": 0.5}
            }
        }

if __name__ == "__main__":
    a = StrategyAgent()
    print(a.run({"campaign_spec": {"objectives":"X","budget":1,"KPIs":["test"]}}))
