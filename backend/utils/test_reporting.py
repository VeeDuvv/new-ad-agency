# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsiduvuri

from backend.agents.openai.reporting_agent import ReportingAgent
import json

def test_reporting():
    agent = ReportingAgent()
    executions = [
        {"status":"success", "details":{"executed":["A"], "responses":{}}},
        {"status":"error",   "details":{"executed":["B"], "responses":{}}},
        {"status":"success", "details":{"executed":["C"], "responses":{}}}
    ]
    result = agent.run({"campaign_id":"XYZ","executions":executions})
    print("ReportingAgent output:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_reporting()
