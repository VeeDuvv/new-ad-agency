# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

"""
File: backend/agents/openai/apicaller_agent.py

Need for this file (5th-grader explanation):
“APICallerAgent is like Amy’s super-fast helper hands. It takes the list of tools
that ExecutionAgent said to run and actually calls each one (or pretends to for now),
then gathers back any answers or IDs and packs them up so ReportingAgent can crunch
the numbers. It makes sure each API call happens correctly and tells us what came back!”
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
                "executed": List[str],
                "responses": { tool_name: { ...mock response... } }
            }
        }
        """
        plan = payload.get("plan", [])
        responses = {}
        for tool in plan:
            # In a real agent, we'd call the tool's SDK or HTTP API here.
            # For now, mock a successful response.
            responses[tool] = {"result": "ok", "tool": tool}

        return {
            "status": "success",
            "details": {
                "executed": plan,
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
