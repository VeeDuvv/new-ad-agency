# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsiduvvuri

from backend.agents.openai.strategy_agent import StrategyAgent
import json

def test_strategy():
    agent = StrategyAgent()
    spec = {
        "objectives": "Boost site visits by 20% for our eco-friendly shoes.",
        "budget": 25000,
        "KPIs": ["clicks", "bounce_rate"],
        "notes": "Target US urban women, age 18-30."
    }
    result = agent.run({"campaign_spec": spec})
    print("StrategyAgent output:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_strategy()
