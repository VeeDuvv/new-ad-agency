# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

"""
File: backend/agents/openai/director_agent.py

Need for this file (5th‑grader explanation):
“Think of DirectorAgent as the stage director in a play.  It doesn’t
act in the scenes itself—it tells each actor (the IntakeAgent, the
StrategyAgent, Cathy’s DecompAgent, Amy’s ExecutionAgent, Frank’s
ReportingAgent) exactly when to go on and what lines (data) to use.
At the end it collects all the scenes and hands you the whole
recording of the play (the completed campaign package).”
"""

import logging
from ..base import Agent
from ..factory import get_agent

logger = logging.getLogger(__name__)

class DirectorAgent(Agent):
    def run(self, payload: dict) -> dict:
        """
        payload: {
          client_brief: str,
          goals: str,
          budget: str,
          KPIs: List[str]
        }
        returns: {
          campaign_package: {
            spec: …,
            strategy: …,
            blueprint: …,
            executions: […],
            report: …
          }
        }
        """
        logger.debug("DirectorAgent starting with payload: %s", payload)

        # 1) Intake
        intake = get_agent("intake").run(payload)
        spec = intake["campaign_spec"]
        logger.debug("Spec: %s", spec)

        # 2) Strategy
        strategy = get_agent("strategy").run({"campaign_spec": spec})["strategy"]
        logger.debug("Strategy: %s", strategy)

        # 3) Blueprint (L0–L4)
        blueprint = get_agent("decomp").run({
            "function_name": "Launch Campaign",
            "framework": payload.get("framework", "APQC")
        })
        logger.debug("Blueprint: %s", blueprint)

        # 4) Micro‑decompose each L3 task into subtasks (handle both list or dict return)
        l3_tasks = blueprint["levels"].get("L3", [])
        subtasks = []
        for task in l3_tasks:
            result = get_agent("micro_decomp").run(task)
            # result may be a list of subtasks, or a dict { "subtasks": [...] }
            if isinstance(result, list):
                subtasks.extend(result)
            else:
                subtasks.extend(result.get("subtasks", []))
        logger.debug("All subtasks: %s", subtasks)

        # 5) Execute each subtask (planning) and then call the APIs
        executions = []
        real_executions = []
        for st in subtasks:
            # a) Plan the execution
            exec_res = get_agent("execute").run(st)
            executions.append(exec_res)
            # logger.debug("Executions: %s", executions)

            # b) Actually invoke each planned tool
            plan = exec_res["details"]["steps_executed"]
            apicaller_res = get_agent("apicaller").run({
                **st,
                "plan": plan
            })
            real_executions.append(apicaller_res)
            # logger.debug("Real (API Called) Executions: %s", real_executions)

        # 6) Reporting
        report = get_agent("report").run({
            "campaign_id": spec.get("campaign_id"),
            "executions": executions
        })["report"]
        logger.debug("Report: %s", report)

        package = {
            "spec": spec,
            "strategy": strategy,
            "blueprint": blueprint,
            "executions": executions,
            "real_executions": real_executions,
            "report": report
        }
        return {"campaign_package": package}


# self‑test
if __name__ == "__main__":
    agent = DirectorAgent()
    sample = {
      "client_brief": "Grow awareness for our new running shoe among 25–35 year‑olds.",
      "goals": "Increase web visits by 30%",
      "budget": "10000",
      "KPIs": ["impressions","clicks","CTR"],
      "framework": "APQC"
    }
    result = agent.run(sample)
    print("Campaign package:", result)
