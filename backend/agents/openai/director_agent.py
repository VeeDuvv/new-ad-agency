import uuid
from ..base import Agent
from ..factory import get_agent
from .audit_agent import AuditAgent
import logging
logger = logging.getLogger("blueprint_maker.director_agent")

audit_agent = AuditAgent()

def _audit_or_raise(phase: str, agent_name: str, payload: dict):
    """
    Run the audit for a given phase/agent/payload.
    Raises RuntimeError if audit.errors is non‐empty.
    """
    result = audit_agent.run({
        "phase":   phase,
        "agent":   agent_name,
        "payload": payload
    })
    errs = result.get("errors", [])
    if errs:
        logger.error(f"{agent_name} {phase} invalid: {errs}")
        raise RuntimeError(f"{agent_name.capitalize()} {phase} invalid: {errs}")

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

        # ——— Normalize numeric fields ———
        # If budget came in as a string like "1" or "1000.5", convert it:
        if "budget" in payload and isinstance(payload["budget"], str):
            try:
                payload["budget"] = float(payload["budget"])
            except ValueError:
                # leave it be and let the audit/schema catch it
                pass

        # 0) Stamp a unique campaign ID
        campaign_id = str(uuid.uuid4())

        intake_payload = { **payload, "campaign_id": campaign_id }

        _audit_or_raise("input", "intake", intake_payload)
        spec = get_agent("intake").run(intake_payload)
        _audit_or_raise("output", "intake", spec)

        # build the payload the StrategyAgent expects
        strategy_input = {"campaign_spec": spec}

        _audit_or_raise("input", "strategy", strategy_input)
        strategy_res = get_agent("strategy").run(strategy_input)
        strategy = strategy_res["strategy"]
        _audit_or_raise("output", "strategy", strategy)

        blueprint_input = {
            "function_name": strategy.get("strategy_name", "Campaign Execution"),
            "framework":     strategy.get("framework",     "APQC")
        }

        _audit_or_raise("input", "decomp", blueprint_input)
        blueprint = get_agent("decomp").run(blueprint_input)
        _audit_or_raise("output", "decomp", blueprint)

        campaign_package = {
            "campaign_id": campaign_id,
            "campaign_spec": spec,
            "strategy":     strategy,
            "blueprint":    blueprint
        }

        # ——— 4) Micro-Decomposition ———
        micro = get_agent("micro_decomp")
        micro_results = []

        # Grab every L3 task from the blueprint
        tasks = blueprint.get("levels", {}).get("L3", [])
        if not tasks:
            raise RuntimeError("No tasks (L3) found in blueprint")

        for task in tasks:
            # Build the exact payload our MicroDecompAgent schema expects
            task_input = {
                "name":           task.get("name"),
                "role":           task.get("role"),
                "tools":          task.get("tools"),
                "deliverable":    task.get("deliverable"),
                "time_estimate":  task.get("time_estimate")
            }

            _audit_or_raise("input", "micro_decomp", task_input)
            res = micro.run(task_input)
            subtasks = res.get("subtasks", [])
            _audit_or_raise("output", "micro_decomp", res)
            # _audit_or_raise("output", "micro_decomp", subtasks)

            # Collect for the campaign package
            micro_results.append({**task_input, "subtasks": subtasks})

        campaign_package["micro_decomposition"] = micro_results
        
        exec_agent = get_agent("execute")
        api_agent  = get_agent("apicaller")
        execution_results = []

        # Loop over each L3 task’s subtasks
        for micro_entry in campaign_package["micro_decomposition"]:
            for subtask in micro_entry.get("subtasks", []):
                # 5a) Build the single-subtask payload
                exec_input = {
                    "name":          subtask["name"],
                    "role":          subtask["role"],
                    "tools":         subtask["tools"],
                    "deliverable":   subtask["deliverable"],
                    "time_estimate": subtask["time_estimate"]
                }
                _audit_or_raise("input", "execute", exec_input)
                exec_res = exec_agent.run(exec_input)
                _audit_or_raise("output", "execute", exec_res)

                # 5e) Build & audit APICallerAgent input
                api_input = {**exec_input, "plan": exec_res["details"]["steps_executed"]}
                
                _audit_or_raise("input", "apicaller", api_input)
                api_res = api_agent.run(api_input)
                # print("🔍 DEBUG api_res:", api_res)

                # normalize list → object
                normalized = {
                    "status": api_res["status"],
                    "details": {
                        "executed": {
                            step["tool"]: step
                            for step in api_res["details"]["executed"]
                        },
                        "responses": api_res["details"]["responses"]
                    }
                }
                _audit_or_raise("output", "apicaller", normalized)
                api_res = normalized     

                execution_results.append({
                    "subtask": exec_input,
                    "plan":    exec_res["details"]["steps_executed"],
                    "api":     api_res
                })

        # Finally, attach all executions to the campaign package
        campaign_package["execution"] = execution_results

        # assuming execution_results is a list of run-dicts like you showed above
        step_names = [ r["subtask"]["name"] for r in execution_results ]

        single_exec = {
            "status": "success",
            "details": {
            "steps_executed": step_names
            # You might still want to include your runs data:
            # "runs": execution_results
            }
        }
        report_input = {
            "campaign_id": campaign_id,
            "executions": [ single_exec ]
        }
        
        _audit_or_raise("input", "report", report_input)
        report_output = get_agent("report").run(report_input)
        print("DEBUG: Actual report_output from ReportingAgent:") # ADD THIS
        import json                                              # ADD THIS
        print(json.dumps(report_output, indent=2))               # ADD THIS

        _audit_or_raise("output", "report", report_output)

        # 7) Package everything
        campaign_package = {
            "campaign_id":     campaign_id,
            "spec":            spec,
            "strategy":        strategy,
            "blueprint":       blueprint,
            "executions":      micro_results,
            "real_executions": execution_results,
            "report":          report_output
        }

        return {"campaign_package": campaign_package}
