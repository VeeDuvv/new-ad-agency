# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

from backend.agents.openai.apicaller_agent import APICallerAgent
import json

def test_apicaller():
    agent = APICallerAgent()
    payload = {
        "name": "Upload banner to DSP",
        "role": "AdOps Manager",
        "tools": ["Creative CDN", "DSP API"],
        "deliverable": "Banner asset live in DSP",
        "time_estimate": "15 minutes",
        "plan": ["Creative CDN", "DSP API"]
    }
    result = agent.run(payload)
    print("APICallerAgent output:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_apicaller()
