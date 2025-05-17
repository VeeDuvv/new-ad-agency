# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

import uuid
import json
import time
from typing import Dict, Any, List

from ..base import Agent
from ..factory import get_agent
from .audit_agent import AuditAgent
import logging
from backend.observability.factory import create_logger, create_tracker
from backend.observability.interfaces import Logger, Tracker

# Initialize the audit agent
audit_agent = AuditAgent()

class DirectorAgent(Agent):
    """
    Need for this file (5th-grader explanation):
    "This is our campaign conductor! It gives every new campaign a special name tag (a UUID),
    then asks each robot in turn—Intake, Strategy, Blueprint, Micro-Decomp, Execution, API Caller,
    and Reporting—to do its part, always carrying that name tag along. At the end, it hands you
    one big packet with everything labeled by that same name tag so you can track it from start
    to finish."
    """

    def __init__(self, config=None):
        """Initialize the Director Agent with observability tools."""
        super().__init__(config)
        
        # Initialize observability components
        self.agent_name = "director_agent"
        self.logger = create_logger(self.agent_name)
        self.tracker = create_tracker(self.agent_name)
        
        # Legacy logger for backward compatibility
        self.legacy_logger = logging.getLogger("blueprint_maker.director_agent")

    def _audit_or_raise(self, phase: str, agent_name: str, payload: dict):
        """
        Run the audit for a given phase/agent/payload.
        Raises RuntimeError if audit.errors is non‐empty.
        """
        with self.tracker.start_span(f"audit.{agent_name}.{phase}", 
                                   {"agent": agent_name, "phase": phase}):
            self.logger.debug(f"Auditing {agent_name} {phase}")
            
            try:
                result = audit_agent.run({
                    "phase":   phase,
                    "agent":   agent_name,
                    "payload": payload
                })
                
                errs = result.get("errors", [])
                if errs:
                    error_msg = f"{agent_name.capitalize()} {phase} invalid: {errs}"
                    self.logger.error(error_msg)
                    self.legacy_logger.error(f"{agent_name} {phase} invalid: {errs}")
                    self.tracker.add_event("audit_failure", {
                        "agent": agent_name,
                        "phase": phase,
                        "errors": errs
                    })
                    raise RuntimeError(error_msg)
                
                self.logger.debug(f"Audit passed for {agent_name} {phase}")
                return result
            except Exception as e:
                if not isinstance(e, RuntimeError):  # Avoid double logging for audit errors
                    self.logger.error(f"Audit error for {agent_name} {phase}: {str(e)}")
                    self.tracker.record_exception(e)
                raise

    def run(self, payload: dict) -> dict:
        """
        Process a campaign through the entire workflow, coordinating all agents.
        
        Args:
            payload: Input data for the campaign
            
        Returns:
            Dict containing the complete campaign results
        """
        # Generate a campaign ID
        campaign_id = str(uuid.uuid4())
        
        # Start tracking the campaign with observability
        with self.tracker.start_span(f"campaign.{campaign_id}", 
                                    {"campaign_id": campaign_id}) as campaign_span:
            self.logger.info(f"Starting campaign processing for campaign {campaign_id}")
            
            try:
                # Track campaign status
                self.tracker.add_event("campaign_status_change", 
                                     {"campaign_id": campaign_id, "status": "started"})
                
                # Execute the workflow and return results
                campaign_package = self._execute_workflow(campaign_id, payload, campaign_span)
                
                # Update final status
                self.tracker.add_event("campaign_status_change", 
                                     {"campaign_id": campaign_id, "status": "completed"})
                
                self.logger.info(f"Successfully completed campaign {campaign_id}")
                return {"campaign_package": campaign_package}
                
            except Exception as e:
                # Update status on error
                self.tracker.add_event("campaign_status_change", 
                                     {"campaign_id": campaign_id, "status": "failed"})
                
                self.logger.error(f"Error processing campaign {campaign_id}: {str(e)}")
                self.tracker.record_exception(e)
                raise
    
    def _execute_workflow(self, campaign_id: str, payload: dict, parent_span) -> Dict[str, Any]:
        """
        Execute the complete workflow by running each agent in sequence.
        
        Args:
            campaign_id: Unique identifier for the campaign
            payload: Input data for the campaign
            parent_span: Parent span for tracking
            
        Returns:
            Dict containing the complete campaign package
        """
        # ——— Normalize numeric fields ———
        # If budget came in as a string like "1" or "1000.5", convert it:
        if "budget" in payload and isinstance(payload["budget"], str):
            try:
                payload["budget"] = float(payload["budget"])
            except ValueError:
                # leave it be and let the audit/schema catch it
                pass

        # Add campaign_id to payload
        intake_payload = {**payload, "campaign_id": campaign_id}

        # 1. Intake Agent
        with self.tracker.start_span(f"intake_agent.{campaign_id}", 
                                   {"campaign_id": campaign_id, "agent": "intake"}) as span:
            start_time = time.time()
            self.logger.info(f"Running intake agent for campaign {campaign_id}")
            
            try:
                self._audit_or_raise("input", "intake", intake_payload)
                spec = get_agent("intake").run(intake_payload)
                self._audit_or_raise("output", "intake", spec)
                
                # Record metrics
                exec_time = time.time() - start_time
                span.add_attribute("execution_time", exec_time)
                span.add_attribute("success", True)
                self.logger.info(f"Intake agent completed for campaign {campaign_id} in {exec_time:.2f}s")
            except Exception as e:
                span.add_attribute("success", False)
                self.tracker.record_exception(e)
                raise

        # 2. Strategy Agent
        with self.tracker.start_span(f"strategy_agent.{campaign_id}", 
                                   {"campaign_id": campaign_id, "agent": "strategy"}) as span:
            start_time = time.time()
            self.logger.info(f"Running strategy agent for campaign {campaign_id}")
            
            # build the payload the StrategyAgent expects
            strategy_input = {"campaign_spec": spec}
            
            try:
                self._audit_or_raise("input", "strategy", strategy_input)
                strategy_res = get_agent("strategy").run(strategy_input)
                strategy = strategy_res["strategy"]
                self._audit_or_raise("output", "strategy", strategy)
                
                # Record metrics
                exec_time = time.time() - start_time
                span.add_attribute("execution_time", exec_time)
                span.add_attribute("success", True)
                self.logger.info(f"Strategy agent completed for campaign {campaign_id} in {exec_time:.2f}s")
            except Exception as e:
                span.add_attribute("success", False)
                self.tracker.record_exception(e)
                raise

        # 3. Functional Decomposition (Blueprint) Agent
        with self.tracker.start_span(f"decomp_agent.{campaign_id}", 
                                   {"campaign_id": campaign_id, "agent": "decomp"}) as span:
            start_time = time.time()
            self.logger.info(f"Running functional decomposition agent for campaign {campaign_id}")
            
            blueprint_input = {
                "function_name": strategy.get("strategy_name", "Campaign Execution"),
                "framework":     strategy.get("framework", "APQC")
            }
            
            try:
                self._audit_or_raise("input", "decomp", blueprint_input)
                blueprint = get_agent("decomp").run(blueprint_input)
                self._audit_or_raise("output", "decomp", blueprint)
                
                # Record metrics
                exec_time = time.time() - start_time
                span.add_attribute("execution_time", exec_time)
                span.add_attribute("success", True)
                self.logger.info(f"Functional decomposition completed for campaign {campaign_id} in {exec_time:.2f}s")
            except Exception as e:
                span.add_attribute("success", False)
                self.tracker.record_exception(e)
                raise

        # Create initial campaign package
        campaign_package = {
            "campaign_id": campaign_id,
            "campaign_spec": spec,
            "strategy": strategy,
            "blueprint": blueprint
        }

        # 4. Micro-Decomposition Agent
        with self.tracker.start_span(f"micro_decomp_agent.{campaign_id}", 
                                   {"campaign_id": campaign_id, "agent": "micro_decomp"}) as span:
            start_time = time.time()
            self.logger.info(f"Running micro decomposition agent for campaign {campaign_id}")
            
            micro = get_agent("micro_decomp")
            micro_results = []

            try:
                # Grab every L3 task from the blueprint
                tasks = blueprint.get("levels", {}).get("L3", [])
                if not tasks:
                    error_msg = "No tasks (L3) found in blueprint"
                    self.logger.error(error_msg)
                    raise RuntimeError(error_msg)
                
                span.add_attribute("task_count", len(tasks))
                
                for task_idx, task in enumerate(tasks):
                    # Create child span for each task
                    with self.tracker.start_span(f"micro_decomp_task.{task_idx}.{campaign_id}", 
                                             {"campaign_id": campaign_id, "task_idx": task_idx}) as task_span:
                        # Build the exact payload our MicroDecompAgent schema expects
                        task_input = {
                            "name":           task.get("name"),
                            "role":           task.get("role"),
                            "tools":          task.get("tools"),
                            "deliverable":    task.get("deliverable"),
                            "time_estimate":  task.get("time_estimate")
                        }
                        
                        task_span.add_attribute("task_name", task.get("name", "unnamed"))
                        
                        self._audit_or_raise("input", "micro_decomp", task_input)
                        res = micro.run(task_input)
                        subtasks = res.get("subtasks", [])
                        self._audit_or_raise("output", "micro_decomp", res)
                        
                        # Collect for the campaign package
                        micro_results.append({**task_input, "subtasks": subtasks})
                        task_span.add_attribute("subtask_count", len(subtasks))
                
                # Add micro decomposition results to campaign package
                campaign_package["micro_decomposition"] = micro_results
                
                # Record metrics
                exec_time = time.time() - start_time
                span.add_attribute("execution_time", exec_time)
                span.add_attribute("success", True)
                span.add_attribute("total_subtasks", sum(len(task.get("subtasks", [])) for task in micro_results))
                self.logger.info(f"Micro decomposition completed for campaign {campaign_id} in {exec_time:.2f}s")
            except Exception as e:
                span.add_attribute("success", False)
                self.tracker.record_exception(e)
                raise

        # 5. Execution and API Caller Agents
        with self.tracker.start_span(f"execution_phase.{campaign_id}", 
                                   {"campaign_id": campaign_id}) as exec_phase_span:
            start_time = time.time()
            self.logger.info(f"Starting execution phase for campaign {campaign_id}")
            
            exec_agent = get_agent("execute")
            api_agent = get_agent("apicaller")
            execution_results = []
            
            try:
                total_subtasks = sum(len(task.get("subtasks", [])) for task in campaign_package["micro_decomposition"])
                exec_phase_span.add_attribute("total_subtasks", total_subtasks)
                
                # Loop over each L3 task's subtasks
                for micro_idx, micro_entry in enumerate(campaign_package["micro_decomposition"]):
                    for subtask_idx, subtask in enumerate(micro_entry.get("subtasks", [])):
                        # Create span for this subtask execution
                        with self.tracker.start_span(f"subtask.{micro_idx}.{subtask_idx}.{campaign_id}", 
                                                 {"campaign_id": campaign_id, 
                                                  "micro_idx": micro_idx, 
                                                  "subtask_idx": subtask_idx}) as subtask_span:
                            subtask_name = subtask.get("name", "unnamed")
                            subtask_span.add_attribute("subtask_name", subtask_name)
                            self.logger.debug(f"Executing subtask: {subtask_name}")
                            
                            # 5a) Execute subtask
                            with self.tracker.start_span(f"execute.{subtask_name}", 
                                                     {"campaign_id": campaign_id, 
                                                      "subtask": subtask_name}) as execute_span:
                                # Build the single-subtask payload
                                exec_input = {
                                    "name":          subtask["name"],
                                    "role":          subtask["role"],
                                    "tools":         subtask["tools"],
                                    "deliverable":   subtask["deliverable"],
                                    "time_estimate": subtask["time_estimate"]
                                }
                                self._audit_or_raise("input", "execute", exec_input)
                                exec_res = exec_agent.run(exec_input)
                                self._audit_or_raise("output", "execute", exec_res)
                                execute_span.add_attribute("steps_count", len(exec_res["details"]["steps_executed"]))
                            
                            # 5b) Call API for this subtask
                            with self.tracker.start_span(f"apicaller.{subtask_name}", 
                                                     {"campaign_id": campaign_id, 
                                                      "subtask": subtask_name}) as api_span:
                                # Build & audit APICallerAgent input
                                api_input = {**exec_input, "plan": exec_res["details"]["steps_executed"]}
                                
                                self._audit_or_raise("input", "apicaller", api_input)
                                api_res = api_agent.run(api_input)
                                
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
                                self._audit_or_raise("output", "apicaller", normalized)
                                api_res = normalized
                                api_span.add_attribute("api_status", api_res["status"])
                            
                            # Add results to collection
                            execution_results.append({
                                "subtask": exec_input,
                                "plan":    exec_res["details"]["steps_executed"],
                                "api":     api_res
                            })
                
                # Record metrics for full execution phase
                exec_time = time.time() - start_time
                exec_phase_span.add_attribute("execution_time", exec_time)
                exec_phase_span.add_attribute("success", True)
                self.logger.info(f"Execution phase completed for campaign {campaign_id} in {exec_time:.2f}s")
            except Exception as e:
                exec_phase_span.add_attribute("success", False)
                self.tracker.record_exception(e)
                raise

        # Add execution results to campaign package
        campaign_package["execution"] = execution_results

        # 6. Reporting Agent
        with self.tracker.start_span(f"reporting_agent.{campaign_id}", 
                                   {"campaign_id": campaign_id, "agent": "report"}) as span:
            start_time = time.time()
            self.logger.info(f"Running reporting agent for campaign {campaign_id}")
            
            try:
                # Prepare input for reporting agent
                step_names = [r["subtask"]["name"] for r in execution_results]
                
                single_exec = {
                    "status": "success",
                    "details": {
                        "steps_executed": step_names
                    }
                }
                
                report_input = {
                    "campaign_id": campaign_id,
                    "executions": [single_exec]
                }
                
                self._audit_or_raise("input", "report", report_input)
                report_output = get_agent("report").run(report_input)
                
                # Log the report output for debugging
                self.logger.debug(f"Report output for campaign {campaign_id}: {json.dumps(report_output, indent=2)}")
                
                self._audit_or_raise("output", "report", report_output)
                
                # Record metrics
                exec_time = time.time() - start_time
                span.add_attribute("execution_time", exec_time)
                span.add_attribute("success", True)
                self.logger.info(f"Reporting agent completed for campaign {campaign_id} in {exec_time:.2f}s")
            except Exception as e:
                span.add_attribute("success", False)
                self.tracker.record_exception(e)
                raise

        # 7. Package everything
        final_campaign_package = {
            "campaign_id":      campaign_id,
            "spec":             spec,
            "strategy":         strategy,
            "blueprint":        blueprint,
            "executions":       micro_results,
            "real_executions":  execution_results,
            "report":           report_output
        }
        
        # Record overall campaign metrics
        parent_span.add_attribute("agent_count", 7)  # Number of distinct agents used
        parent_span.add_attribute("task_count", len(micro_results))
        parent_span.add_attribute("subtask_count", len(execution_results))
        
        return final_campaign_package