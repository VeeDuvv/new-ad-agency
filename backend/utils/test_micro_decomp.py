# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsiduvuri

from backend.agents.openai.micro_decomp_agent import MicroDecompAgent
import json

def test_micro():
    agent = MicroDecompAgent()
    task = {
        "name": "Develop creative brief",
        "role": "Creative Director",
        "tools": ["Google Docs", "Brand Guidelines"],
        "deliverable": "Creative brief document",
        "time_estimate": "2 days"
    }
    result = agent.run(task)
    print("MicroDecompAgent subtasks:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_micro()
