# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

"""
File: backend/agents/openai/reporting_agent.py

Need for this file (5th-grader explanation):
“ReportingAgent is Frank’s trusty tallybot. It takes all the actual API call
results from APICallerAgent, counts wins vs. losses, notes which tools we used,
and writes a quick summary sentence plus KPI numbers, all in clean JSON.”
"""

import re, json
from ..base import Agent
from ...utils.openai_client import chat_completion

class ReportingAgent(Agent):
    def run(self, payload: dict) -> dict:
        """
        :param payload: {
            "campaign_id": Optional[str],
            "executions": [ 
                { "status": str, "details": { "executed": [str], "responses": {...} } }, 
                … 
            ]
        }
        :return: {
            "report": {
              "summary": str,
              "KPIs": {
                "total_tasks": int,
                "successful": int,
                "failed": int
              },
              "tools_used": [ str, … ]
            }
        }
        """
        executions = payload.get("executions", [])
        prompt = (
            "You are a data‐savvy reporting assistant.\n"
            "Given these execution results, produce JSON with exactly:\n"
            "• summary: one sentence overview\n"
            "• KPIs: total_tasks, successful, failed\n"
            "• tools_used: unique list of all tools invoked\n\n"
            f"Executions:\n{json.dumps(executions, indent=2)}\n\n"
            "Return ONLY a JSON object with key “report”."
        )

        messages = [
            {"role":"system", "content":"You are a helpful reporting agent."},
            {"role":"user",   "content":prompt}
        ]
        resp = chat_completion(messages, model="gpt-4o", temperature=0)
        content = resp.choices[0].message.content.strip()
        content = re.sub(r"^```(?:json)?\s*","",content)
        content = re.sub(r"\s*```$","",content)

        try:
            data = json.loads(content)
            return {"report": data.get("report", {})}
        except json.JSONDecodeError as e:
            return {
                "report": {
                    "summary": "Error generating report",
                    "KPIs": {
                        "total_tasks": len(executions),
                        "successful": sum(1 for ex in executions if ex.get("status")=="success"),
                        "failed": sum(1 for ex in executions if ex.get("status")!="success")
                    },
                    "tools_used": [],
                    "raw_response": content,
                    "error": str(e)
                }
            }
