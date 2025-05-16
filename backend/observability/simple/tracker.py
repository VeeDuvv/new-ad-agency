# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

"""
Simple implementation of the WorkflowMonitor interface using JSON files.

This implementation stores campaign and agent status information in JSON files,
making it easy to visualize the workflow state without complex infrastructure.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, List, Union

from ..interfaces import WorkflowMonitor

class SimpleWorkflowMonitor(WorkflowMonitor):
    """
    Monitors workflow state using JSON files for storage.
    
    Campaign status and agent status are stored in separate files,
    enabling simple querying and visualization of workflow progress.
    """
    
    def __init__(self, storage_dir: str = "data/workflow"):
        """
        Initialize a workflow monitor with the specified storage directory.
        
        Args:
            storage_dir: Directory where workflow state files will be stored
        """
        self.storage_dir = storage_dir
        
        # Ensure storage directory exists
        os.makedirs(self.storage_dir, exist_ok=True)
        
        # Define file paths
        self.campaigns_file = os.path.join(self.storage_dir, "campaigns.json")
        self.agents_file = os.path.join(self.storage_dir, "agents.json")
        
        # Initialize files if they don't exist
        if not os.path.exists(self.campaigns_file):
            with open(self.campaigns_file, "w") as f:
                json.dump([], f)
        
        if not os.path.exists(self.agents_file):
            with open(self.agents_file, "w") as f:
                json.dump({}, f)
    
    def update_campaign_status(self, campaign_id: str, status: str, 
                              metadata: Dict[str, Any] = None) -> None:
        """
        Update the status of a campaign in the workflow.
        
        Args:
            campaign_id: Unique identifier for the campaign
            status: New status for the campaign
            metadata: Additional context information
        """
        # Read current campaigns data
        try:
            with open(self.campaigns_file, "r") as f:
                campaigns = json.load(f)
        except json.JSONDecodeError:
            # Handle corrupted file by starting fresh
            campaigns = []
        
        # Find campaign or create new entry
        campaign = next((c for c in campaigns if c["id"] == campaign_id), None)
        if campaign is None:
            campaign = {
                "id": campaign_id, 
                "history": [],
                "created_at": datetime.now().isoformat()
            }
            campaigns.append(campaign)
        
        # Add status update
        campaign["current_status"] = status
        campaign["updated_at"] = datetime.now().isoformat()
        campaign["history"].append({
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        })
        
        # Save updated data
        with open(self.campaigns_file, "w") as f:
            json.dump(campaigns, f, indent=2)
    
    def update_agent_status(self, agent_id: str, status: str, 
                           current_task: Optional[str] = None) -> None:
        """
        Update the status of an agent.
        
        Args:
            agent_id: Unique identifier for the agent
            status: New status for the agent (idle, processing, etc.)
            current_task: Identifier of the task the agent is working on (if any)
        """
        # Read current agents data
        try:
            with open(self.agents_file, "r") as f:
                agents = json.load(f)
        except json.JSONDecodeError:
            # Handle corrupted file by starting fresh
            agents = {}
        
        # Update agent status
        agents[agent_id] = {
            "status": status,
            "current_task": current_task,
            "last_updated": datetime.now().isoformat()
        }
        
        # Save updated data
        with open(self.agents_file, "w") as f:
            json.dump(agents, f, indent=2)
    
    def get_campaign_status(self, campaign_id: Optional[str] = None) -> Union[Dict, List[Dict], None]:
        """
        Get the current status of one or all campaigns.
        
        Args:
            campaign_id: Optional ID to get status of a specific campaign
            
        Returns:
            Campaign status information as a dict for a specific campaign
            or a list of dicts for all campaigns
        """
        try:
            with open(self.campaigns_file, "r") as f:
                campaigns = json.load(f)
        except json.JSONDecodeError:
            # Handle corrupted file
            campaigns = []
        
        if campaign_id:
            # Return specific campaign if requested
            return next((c for c in campaigns if c["id"] == campaign_id), None)
        
        # Otherwise return all campaigns
        return campaigns
    
    def get_agent_status(self, agent_id: Optional[str] = None) -> Union[Dict, Dict[str, Dict], None]:
        """
        Get the current status of one or all agents.
        
        Args:
            agent_id: Optional ID to get status of a specific agent
            
        Returns:
            Agent status information as a dict for a specific agent
            or a dict of dicts for all agents
        """
        try:
            with open(self.agents_file, "r") as f:
                agents = json.load(f)
        except json.JSONDecodeError:
            # Handle corrupted file
            agents = {}
        
        if agent_id:
            # Return specific agent if requested
            return agents.get(agent_id)
        
        # Otherwise return all agents
        return agents