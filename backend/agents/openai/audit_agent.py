# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsiduvvuri

"""
File: backend/agents/openai/audit_agent.py

Need for this file (5th-grader explanation):
“Before any robot starts or finishes its job, AuditAgent checks its
shopping list (input) or its receipt (output) to make sure everything
is there, spelled right, and nobody’s sneaking in weird stuff. It’s
our safety inspector so the whole pipeline runs cleanly!”
"""

import os, json
from jsonschema import validate, ValidationError
from ..base import Agent

class AuditAgent(Agent):
    def run(self, payload: dict) -> dict:
        """
        payload: {
          "phase": "input"|"output",
          "agent": "<agent_key>",
          "payload": <the data to validate>
        }
        returns: {"errors": []} or list of schema errors
        """
        phase = payload.get("phase")
        agent_key = payload.get("agent")
        data = payload.get("payload")

        schema_path = os.path.join(
            os.getcwd(),
            "schemas",
            f"{agent_key}_{phase}.json"
        )
        try:
            schema = json.load(open(schema_path))
        except FileNotFoundError:
            return {"errors": [f"Schema not found: {agent_key}_{phase}.json"]}

        try:
            validate(instance=data, schema=schema)
            return {"errors": []}
        except ValidationError as e:
            return {"errors": [e.message]}
