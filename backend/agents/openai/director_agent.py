import uuid
from ..base import Agent
from ..factory import get_agent

class DirectorAgent(Agent):
    """
    Need for this file (5th-grader explanation):
    “This is our campaign conductor! It gives every new campaign a special name tag (a UUID),
    then asks each robot in turn—Intake, Strategy, Blueprint, Micro-Decomp, Execution, API Caller,
    and Reporting—to do its part, always carrying that name tag along. At the end, it hands you
    one big packet with everything labeled by that same name tag so you can track it from start
    to finish.”
    """

    def run(self, payload: dict) -> dict:
        # 0) Stamp a unique campaign ID
        campaign_id = str(uuid.uuid4())

        # 1) Intake
        spec = get_agent("intake").run({**payload, "campaign_id": campaign_id})

        # 2) Strategy
        strategy = get_agent("strategy").run({"campaign_spec": spec})["strategy"]

        # 3) Blueprint (L0–L4)
        blueprint = get_agent("decomp").run({
            "function_name": strategy.get("strategy_name", "Campaign Execution"),
            "framework": strategy.get("framework", "APQC")
        })

        # 4) Micro-decompose each L3 task
        tasks = blueprint["levels"]["L3"]
        subtasks = []
        for task in tasks:
            subtasks.extend(get_agent("micro_decomp").run(task)["subtasks"])

        # 5) Plan & actual execution
        executions = []
        real_executions = []
        for st in subtasks:
            # a) Planning
            plan_res = get_agent("execute").run(st)
            executions.append(plan_res)

            # b) Real API calls
            apicaller_res = get_agent("apicaller").run({
                **st,
                "plan": plan_res["details"]["steps_executed"]
            })
            real_executions.append(apicaller_res)

        # 6) Final report
        report = get_agent("report").run({
            "campaign_id": campaign_id,
            "executions": real_executions
        })["report"]

        # 7) Package everything
        campaign_package = {
            "campaign_id":     campaign_id,
            "spec":            spec,
            "strategy":        strategy,
            "blueprint":       blueprint,
            "executions":      executions,
            "real_executions": real_executions,
            "report":          report
        }

        return {"campaign_package": campaign_package}
