import uuid
from ..base import Agent
from ..factory import get_agent
from .audit_agent import AuditAgent
import logging
logger = logging.getLogger("blueprint_maker.director_agent")


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

        audit = AuditAgent()

        
        
        intake_payload = { **payload, "campaign_id": campaign_id }

        # Before IntakeAgent
        errs = audit.run({"phase": "input", "agent": "intake","payload": intake_payload})["errors"]
        if errs:
            logger.error(f"Input errors: {errs}")
            raise RuntimeError(f"Intake input invalid: {errs}")

        # 1) Intake 
        spec = get_agent("intake").run({intake_payload})

        # After IntakeAgent returns:
        errs = audit.run({"phase": "output","agent": "intake","payload": spec})["errors"]
        if errs:
            logger.error(f"Output errors: {errs}")
            raise RuntimeError(f"Intake output invalid: {errs}")







        # Before StrategyAgent
        errs = audit.run({"phase": "input", "agent": "strategy","payload": spec})["errors"]
        if errs:
            logger.error(f"Input errors: {errs}")
            raise RuntimeError(f"Intake input invalid: {errs}")

        # 2) Strategy
        strategy = get_agent("strategy").run({"campaign_spec": spec})["strategy"]

        # After StrategyAgent returns:
        errs = audit.run({"phase": "output","agent": "strategy","payload": strategy})["errors"]
        if errs:
            logger.error(f"Output errors: {errs}")
            raise RuntimeError(f"Strategy output invalid: {errs}")




        # Before BlueprintAgent
        errs = audit.run({"phase": "input", "agent": "blueprint","payload": strategy})["errors"]
        if errs:
            logger.error(f"Input errors: {errs}")
            raise RuntimeError(f"Blueprint input invalid: {errs}")
        

        # 3) Blueprint (L0–L4)
        blueprint = get_agent("decomp").run({
            "function_name": strategy.get("strategy_name", "Campaign Execution"),
            "framework": strategy.get("framework", "APQC")
        })

        # After BlueprintAgent returns:
        errs = audit.run({"phase": "output","agent": "blueprint","payload": blueprint})["errors"]
        if errs:
            logger.error(f"Output errors: {errs}")
            raise RuntimeError(f"Blueprint output invalid: {errs}")




        # Before MicroDecompAgent
        errs = audit.run({"phase": "input", "agent": "micro_decomp","payload": blueprint})["errors"]
        if errs:
            logger.error(f"Input errors: {errs}")
            raise RuntimeError(f"MicroDecomp input invalid: {errs}")
        
        # 4) Micro-decompose each L3 task
        tasks = blueprint["levels"]["L3"]
        subtasks = []
        for task in tasks:
            subtasks.extend(get_agent("micro_decomp").run(task)["subtasks"])

        # After MicroDecompAgent returns:
        errs = audit.run({"phase": "output","agent": "micro_decomp","payload": subtasks})["errors"]
        if errs:
            logger.error(f"Output errors: {errs}")
            raise RuntimeError(f"MicroDecomp output invalid: {errs}")
        
        
        
        
        
        # Before ExecuteAgent
        errs = audit.run({"phase": "input", "agent": "execute","payload": subtasks})["errors"]
        if errs:    
            logger.error(f"Input errors: {errs}")
            raise RuntimeError(f"Execute input invalid: {errs}")
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

        # After ExecuteAgent returns:
        errs = audit.run({"phase": "output","agent": "execute","payload": apicaller_res})["errors"]
        if errs:
            logger.error(f"Output errors: {errs}")
            raise RuntimeError(f"Execute output invalid: {errs}")


        # Before ReportAgent
        errs = audit.run({"phase": "input", "agent": "report","payload": real_executions})["errors"]
        if errs:    
            logger.error(f"Input errors: {errs}")
            raise RuntimeError(f"Report input invalid: {errs}")
        # 6) Final report
        report = get_agent("report").run({
            "campaign_id": campaign_id,
            "executions": real_executions
        })["report"]

        # After ReportAgent returns:
        errs = audit.run({"phase": "output","agent": "report","payload": report})["errors"] 
        if errs:
            logger.error(f"Output errors: {errs}")
            raise RuntimeError(f"Report output invalid: {errs}")

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
