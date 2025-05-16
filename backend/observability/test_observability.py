# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

"""
Test script for the observability system.

This script creates some sample data in the observability system
and then prints it out using the API endpoints.
"""

import time
import uuid
from backend.observability.factory import create_task_monitor, create_workflow_monitor
from backend.observability.helpers import AgentObserver

def main():
    """Run a simple test of the observability system."""
    print("Testing observability system...")
    
    # Create some sample data
    workflow_monitor = create_workflow_monitor()
    
    # Create a test campaign
    campaign_id = f"test_campaign_{uuid.uuid4()}"
    print(f"Created test campaign: {campaign_id}")
    
    # Update campaign status
    workflow_monitor.update_campaign_status(
        campaign_id=campaign_id,
        status="intake_started",
        metadata={"test": True}
    )
    
    # Create an observer for the intake agent
    intake_observer = AgentObserver("intake_agent")
    
    # Update agent status
    intake_observer.update_status("idle")
    
    # Track a task using the context manager
    with intake_observer.track_task(campaign_id=campaign_id) as task:
        print("Running intake task...")
        time.sleep(1)  # Simulate work
        task.add_metadata("processed_items", 42)
    
    # Create an observer for the strategy agent
    strategy_observer = AgentObserver("strategy_agent")
    
    # Update agent status
    strategy_observer.update_status("idle")
    
    # Simulate a task with an error
    try:
        with strategy_observer.track_task(campaign_id=campaign_id) as task:
            print("Running strategy task...")
            time.sleep(1)  # Simulate work
            raise ValueError("Test error in strategy task")
    except ValueError:
        print("Caught expected test error")
    
    print("\nData created successfully!")
    print("\nYou can now check the following API endpoints:")
    print("- GET /api/workflow/campaigns")
    print("- GET /api/workflow/campaign/" + campaign_id)
    print("- GET /api/workflow/agents")
    print("- GET /api/workflow/agent/intake_agent")
    print("- GET /api/workflow/agent/strategy_agent")

if __name__ == "__main__":
    main()