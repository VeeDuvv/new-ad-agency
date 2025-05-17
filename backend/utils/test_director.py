# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

"""
Need for this file (5th-grader explanation):
"This is our campaign detective! It watches our campaign conductor (Director Agent) while it works and writes down everything that happens. It's like having a special notebook that keeps track of how long each robot takes to do its job, if they run into any problems, and how well they work together. At the end, it shows us a report card with all the important information so we can see if our robots are doing a good job or if they need help to work better."
"""

import json
import logging
import time
from typing import Dict, Any

# Import DirectorAgent
from backend.agents.openai.director_agent import DirectorAgent

# Import observability components
from backend.observability.factory import initialize_observability, get_logger, get_tracker

def setup_observability(log_level=logging.INFO):
    """
    Set up the observability framework for testing.
    
    Args:
        log_level: Logging level to use for the test
    """
    # Initialize basic logging
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)-8s %(name)s %(message)s"
    )
    
    # Initialize the observability framework
    initialize_observability(
        enable_console=True,  # Output to console for testing
        enable_file=True,     # Save to file for later analysis
        log_level=log_level,
        log_dir="./logs/tests"
    )
    
    # Get the test logger
    logger = get_logger("test_director")
    logger.info("Observability framework initialized for testing")
    
    return logger

def print_campaign_metrics(campaign_package: Dict[str, Any], logger):
    """
    Print metrics from the campaign execution.
    
    Args:
        campaign_package: The campaign package returned by the DirectorAgent
        logger: Logger instance for output
    """
    campaign_id = campaign_package.get("campaign_id", "unknown")
    
    logger.info(f"Campaign {campaign_id} execution complete")
    
    # Print basic metrics
    blueprint = campaign_package.get("blueprint", {})
    executions = campaign_package.get("executions", [])
    real_executions = campaign_package.get("real_executions", [])
    
    # Count the tasks at different levels
    l0_tasks = len(blueprint.get("levels", {}).get("L0", []))
    l1_tasks = len(blueprint.get("levels", {}).get("L1", []))
    l2_tasks = len(blueprint.get("levels", {}).get("L2", []))
    l3_tasks = len(blueprint.get("levels", {}).get("L3", []))
    
    # Count subtasks
    subtask_count = sum(len(task.get("subtasks", [])) for task in executions)
    
    logger.info(f"Blueprint hierarchy: L0={l0_tasks}, L1={l1_tasks}, L2={l2_tasks}, L3={l3_tasks}")
    logger.info(f"Total L3 tasks: {l3_tasks}")
    logger.info(f"Total subtasks: {subtask_count}")
    logger.info(f"Total executions: {len(real_executions)}")
    
    # Calculate some timing metrics (this would come from spans in a real implementation)
    # But for this test, we're just printing what we can extract from the campaign package
    return {
        "l0_tasks": l0_tasks,
        "l1_tasks": l1_tasks,
        "l2_tasks": l2_tasks,
        "l3_tasks": l3_tasks,
        "subtasks": subtask_count,
        "executions": len(real_executions)
    }

def test_director():
    """Test the DirectorAgent with observability."""
    # Set up observability
    logger = setup_observability(logging.INFO)
    
    start_time = time.time()
    logger.info("Starting DirectorAgent test")
    
    # Create agent with configuration that enables observability
    config = {
        "observability": {
            "enabled": True,
            "log_level": logging.INFO,
            "metrics_enabled": True
        }
    }
    
    agent = DirectorAgent(config)
    
    # Prepare test input
    inp = {
        "client_brief": "Test campaign for AI-powered ad agency with observability.",
        "goals": "Validate end-to-end flow with observability tracking",
        "budget": "1000",
        "KPIs": ["test", "observability", "tracking"],
        "framework": "APQC"
    }
    
    # Run the agent
    try:
        logger.info("Executing campaign with DirectorAgent")
        result = agent.run(inp)
        
        # Extract the campaign package
        campaign_package = result.get("campaign_package", {})
        
        # Print basic output information
        logger.info("DirectorAgent execution completed successfully")
        logger.info(f"DirectorAgent output keys: {result.keys()}")
        
        # Calculate and print metrics
        metrics = print_campaign_metrics(campaign_package, logger)
        
        # Print execution time
        exec_time = time.time() - start_time
        logger.info(f"Total execution time: {exec_time:.2f} seconds")
        
        # For observability analysis, save the full output to a file
        with open("./logs/tests/director_output.json", "w") as f:
            json.dump(result, f, indent=2)
            logger.info("Saved detailed output to ./logs/tests/director_output.json")
        
        # Print a summary of the campaign execution
        print("\n----- Campaign Execution Summary -----")
        print(f"Campaign ID: {campaign_package.get('campaign_id', 'unknown')}")
        print(f"Tasks: L0={metrics['l0_tasks']}, L1={metrics['l1_tasks']}, L2={metrics['l2_tasks']}, L3={metrics['l3_tasks']}")
        print(f"Subtasks: {metrics['subtasks']}")
        print(f"Executions: {metrics['executions']}")
        print(f"Execution time: {exec_time:.2f} seconds")
        print("-------------------------------------\n")
        
        # Pretty-print the output for manual verification
        print("DirectorAgent output preview:")
        # Only print a subset to keep output manageable
        preview = {
            "campaign_id": campaign_package.get("campaign_id"),
            "spec": campaign_package.get("spec"),
            "strategy": campaign_package.get("strategy"),
            # Omitting larger parts
            "execution_count": len(campaign_package.get("real_executions", [])),
            "report": campaign_package.get("report")
        }
        print(json.dumps(preview, indent=2))
        
    except Exception as e:
        logger.error(f"Error during DirectorAgent execution: {str(e)}", exc_info=True)
        raise

def view_observability_data():
    """
    Utility function to view collected observability data.
    This would typically connect to your observability platform.
    """
    print("\n----- Observability Data -----")
    print("To view detailed observability data:")
    print("1. Check the logs directory: ./logs/tests/")
    print("2. If using a monitoring dashboard, visit: http://localhost:8080/dashboard")
    print("3. For OpenTelemetry data: http://localhost:16686/search")
    print("-----------------------------\n")

if __name__ == "__main__":
    try:
        test_director()
        view_observability_data()
    except Exception as e:
        print(f"Test failed: {str(e)}")