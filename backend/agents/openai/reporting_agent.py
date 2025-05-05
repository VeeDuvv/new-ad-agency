# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

"""
File: backend/agents/openai/reporting_agent.py

Need for this file (5th‑grader explanation):
“Think of ReportingAgent as Frank’s calculator robot.  It gathers all the
execution results, adds up the numbers, computes the KPIs, and hands
you a little report card that says how well the campaign did.”
"""

from ..base import Agent

class ReportingAgent(Agent):
    def run(self, payload: dict) -> dict:
        # Dummy report so DirectorAgent can finish
        return {"report": {"summary": "all good", "KPIs": payload.get("executions", [])}}

if __name__ == "__main__":
    r = ReportingAgent()
    print(r.run({"executions":[{"status":"success"}]}))
