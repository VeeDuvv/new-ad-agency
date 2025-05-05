# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsiduvuri

from backend.agents.openai.execution_agent import ExecutionAgent
import json

def test_execution():
    agent = ExecutionAgent()
    task = {
        "name": "Upload banner to DSP",
        "role": "AdOps Manager",
        "tools": ["DSP API", "Creative CDN"],
        "deliverable": "Banner asset live in DSP",
        "time_estimate": "15 minutes"
    }
    result = agent.run(task)
    print("ExecutionAgent output:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_execution()
