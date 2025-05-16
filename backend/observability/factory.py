# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

"""
Factory for creating observability components.

This module provides functions for creating TaskMonitor and WorkflowMonitor 
instances with the specified backend implementation, allowing for easy 
switching between different observability approaches.
"""

from typing import Dict, Any, Optional, Literal

from .interfaces import TaskMonitor, WorkflowMonitor
from .simple.logger import SimpleTaskMonitor
from .simple.tracker import SimpleWorkflowMonitor

# Type for the observability backend - will include 'opentelemetry' in the future
ObservabilityBackend = Literal["simple"]

def create_task_monitor(agent_name: str, backend: ObservabilityBackend = "simple") -> TaskMonitor:
    """
    Create a task monitor for the specified agent using the given backend.
    
    Args:
        agent_name: Name of the agent being monitored
        backend: Observability backend to use
        
    Returns:
        A TaskMonitor instance for the specified agent
        
    Raises:
        ValueError: If the specified backend is unknown
    """
    if backend == "simple":
        return SimpleTaskMonitor(agent_name)
    
    # Future: Add OpenTelemetry implementation
    # if backend == "opentelemetry":
    #     return OpenTelemetryTaskMonitor(agent_name)
    
    raise ValueError(f"Unknown observability backend: {backend}")

def create_workflow_monitor(backend: ObservabilityBackend = "simple", **kwargs) -> WorkflowMonitor:
    """
    Create a workflow monitor using the given backend.
    
    Args:
        backend: Observability backend to use
        **kwargs: Additional configuration options for the specific backend
        
    Returns:
        A WorkflowMonitor instance
        
    Raises:
        ValueError: If the specified backend is unknown
    """
    if backend == "simple":
        return SimpleWorkflowMonitor(**kwargs)
    
    # Future: Add OpenTelemetry implementation
    # if backend == "opentelemetry":
    #     return OpenTelemetryWorkflowMonitor(**kwargs)
    
    raise ValueError(f"Unknown observability backend: {backend}")