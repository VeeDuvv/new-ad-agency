# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsiduvvuri

"""
File: backend/agents/openai/execution_agent.py

Need for this file (5th-grader explanation):
“ExecutionAgent is Amy’s robot arms. It takes each tiny task—like
‘Upload banner to DSP’—and either actually calls the right ad-platform
API, or explains exactly which API call to make with what parameters.
Then it reports back ‘success’ and any IDs or URLs it created.”
"""

import re, json
from ..base import Agent
from ...utils.openai_client import chat_completion

class ExecutionAgent(Agent):
    def run(self, payload: dict) -> dict:
        """
        :param payload: {
            "name": str,
            "role": str,
            "tools": List[str],
            "deliverable": str,
            "time_estimate": str
        }
        :return: {
            "status": "success"|"error",
            "details": { ... }
        }
        """
        prompt = (
            "You are ExecutionAgent for an AI-native ad agency.\n"
            "Below is a single subtask, plus a list of tools you can call.\n"
            "For each tool in `tools`, describe exactly how you would invoke it "
            "(e.g. API endpoint, method, params) to complete this task. "
            "Return ONLY a JSON object with keys:\n"
            "  • status: \"success\" or \"error\"\n"
            "  • details: an object describing any IDs or outputs produced\n\n"
            f"Subtask:\n{json.dumps(payload, indent=2)}\n\n"
        )

        messages = [
            {"role": "system",  "content": "You are a helpful execution assistant."},
            {"role": "user",    "content": prompt}
        ]

        resp = chat_completion(messages, model="gpt-4o", temperature=0)
        content = resp.choices[0].message.content.strip()
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)

        result = json.loads(content)
        return result


# Self-test
if __name__ == "__main__":
    agent = ExecutionAgent()
    sample = {
        "name": "Upload banner to DSP",
        "role": "AdOps Manager",
        "tools": ["DSP API", "Creative CDN"],
        "deliverable": "Banner asset live in DSP",
        "time_estimate": "15 minutes"
    }
    print(json.dumps(agent.run(sample), indent=2))
