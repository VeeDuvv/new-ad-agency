# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

"""
API endpoints for accessing observability data.

This module provides FastAPI endpoints for retrieving campaign and agent
status information from the observability system.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends

from .factory import create_workflow_monitor
from .interfaces import WorkflowMonitor

# Create a router for workflow endpoints
workflow_router = APIRouter(prefix="/api/workflow", tags=["Workflow"])

# Dependency to get workflow monitor
def get_workflow_monitor() -> WorkflowMonitor:
    """Dependency to get a workflow monitor instance."""
    return create_workflow_monitor()

@workflow_router.get("/campaigns")
async def get_workflow_campaigns(
    workflow_monitor: WorkflowMonitor = Depends(get_workflow_monitor)
) -> List[Dict[str, Any]]:
    """
    Get all campaign workflow statuses.
    
    Returns a list of campaign status objects, each including:
    - ID
    - Current status
    - Status history
    - Timestamps
    """
    return workflow_monitor.get_campaign_status()

@workflow_router.get("/campaign/{campaign_id}")
async def get_campaign_workflow(
    campaign_id: str,
    workflow_monitor: WorkflowMonitor = Depends(get_workflow_monitor)
) -> Dict[str, Any]:
    """
    Get detailed workflow status for a specific campaign.
    
    Args:
        campaign_id: ID of the campaign to retrieve
    
    Returns:
        Campaign status object with history
        
    Raises:
        HTTPException: If the campaign is not found
    """
    campaign = workflow_monitor.get_campaign_status(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@workflow_router.get("/agents")
async def get_workflow_agents(
    workflow_monitor: WorkflowMonitor = Depends(get_workflow_monitor)
) -> Dict[str, Dict[str, Any]]:
    """
    Get all agent statuses.
    
    Returns a dictionary mapping agent IDs to their status objects, including:
    - Current status (idle, processing)
    - Current task (if any)
    - Last update timestamp
    """
    return workflow_monitor.get_agent_status()

@workflow_router.get("/agent/{agent_id}")
async def get_agent_status(
    agent_id: str,
    workflow_monitor: WorkflowMonitor = Depends(get_workflow_monitor)
) -> Dict[str, Any]:
    """
    Get status for a specific agent.
    
    Args:
        agent_id: ID of the agent to retrieve
    
    Returns:
        Agent status object
        
    Raises:
        HTTPException: If the agent is not found
    """
    agent = workflow_monitor.get_agent_status(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

def add_observability_endpoints(app):
    """
    Add observability endpoints to a FastAPI application.
    
    This function adds all the workflow endpoints to an existing
    FastAPI application to expose observability data.
    
    Args:
        app: The FastAPI application to add endpoints to
    """
    app.include_router(workflow_router)