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
            "details": {
                "steps_executed": [ <tool names> ]
            }
        }
        """
        prompt = (
            "You are ExecutionAgent for an AI-native ad agency.\n"
            "Your ONLY job is to list which tools you would invoke to complete this subtask.\n"
            "Return a JSON object with exactly two keys:\n"
            "  \"status\": \"success\" or \"error\",\n"
            "  \"details\": { \"steps_executed\": [ <tool names as strings> ] }\n"
            "Do NOT include any other fields, nested objects, comments, or example code.\n\n"
            "Subtask:\n"
            f"{json.dumps(payload, indent=2)}\n"
        )

        messages = [
            {"role": "system", "content": "You are a precise execution planner."},
            {"role": "user",   "content": prompt}
        ]

        resp = chat_completion(messages, model="gpt-4o", temperature=0)
        content = resp.choices[0].message.content.strip()

        # Strip markdown fences
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            # Last-resort error structure
            return {
                "status": "error",
                "details": {
                    "raw_response": content,
                    "error": str(e)
                }
            }

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
