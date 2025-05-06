# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

"""
File: backend/agents/openai/apicaller_agent.py

Need for this file (5th-grader explanation):
“APICallerAgent is like Amy’s super-fast helper hands. It takes the plan of steps
(which tool to call in which order) and actually calls each one (or pretends to),
then wraps each tool’s name and its response into neat little boxes so
ReportingAgent can easily read them. Every executed step is its own object,
not just a string, so nothing gets lost in translation!”
"""

from ..base import Agent

class APICallerAgent(Agent):
    def run(self, payload: dict) -> dict:
        """
        :param payload: {
            "name": str,
            "role": str,
            "tools": List[str],
            "deliverable": str,
            "time_estimate": str,
            "plan": List[str]
        }
        :return: {
            "status": "success"|"error",
            "details": {
                "executed": List[ { "tool": str } ],
                "responses": { tool_name: { ...mock response... } }
            }
        }
        """
        plan = payload.get("plan", [])
        executed = []
        responses = {}

        for tool in plan:
            # Record the tool as an object
            executed.append({"tool": tool})

            # In a real agent, you'd call the tool’s SDK or HTTP API here.
            # For now, we mock a successful response.
            responses[tool] = {
                "result": "ok",
                "tool":   tool
            }

        return {
            "status": "success",
            "details": {
                "executed":  executed,
                "responses": responses
            }
        }

# Self-test
if __name__ == "__main__":
    agent = APICallerAgent()
    sample = {
        "name": "Upload banner to DSP",
        "role": "AdOps Manager",
        "tools": ["Creative CDN", "DSP API"],
        "deliverable": "Banner asset live in DSP",
        "time_estimate": "15 minutes",
        "plan": ["Creative CDN", "DSP API"]
    }
    import json
    print(json.dumps(agent.run(sample), indent=2))
