# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

"""
Helper functions and decorators for integrating observability into agents.

These utilities make it easier to add monitoring to agent methods
without cluttering the core business logic.
"""

import time
import functools
import uuid
from typing import Callable, Any, Dict, Optional

from .factory import create_task_monitor, create_workflow_monitor
from .interfaces import TaskMonitor, WorkflowMonitor

def monitor_task(agent_name: str, task_name: str = None, 
                extract_campaign_id: Callable = None):
    """
    Decorator to monitor an agent task method.
    
    This decorator will automatically:
    1. Generate a unique task ID
    2. Record the start of the task
    3. Record the task completion (success or error)
    4. Track the task duration
    
    Args:
        agent_name: Name of the agent being monitored
        task_name: Optional name for the task (defaults to method name)
        extract_campaign_id: Optional function to extract campaign ID from method args
        
    Returns:
        Decorated method with monitoring
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create monitors
            task_monitor = create_task_monitor(agent_name)
            workflow_monitor = create_workflow_monitor()
            
            # Generate a unique task ID
            task_id = str(uuid.uuid4())
            
            # Determine task name
            method_name = task_name or func.__name__
            
            # Extract campaign ID if possible
            campaign_id = None
            if extract_campaign_id:
                try:
                    campaign_id = extract_campaign_id(*args, **kwargs)
                except Exception:
                    pass
            
            # Prepare attributes
            attributes = {
                "method_name": method_name
            }
            if campaign_id:
                attributes["campaign_id"] = campaign_id
            
            # Record task start
            task_monitor.start_task(
                task_id=task_id,
                input_data={"args": args[1:], "kwargs": kwargs} if len(args) > 0 else {"kwargs": kwargs},
                attributes=attributes
            )
            
            # Update agent status if we have a campaign ID
            if campaign_id:
                workflow_monitor.update_agent_status(
                    agent_id=agent_name,
                    status="processing",
                    current_task=campaign_id
                )
            
            # Record timing
            start_time = time.time()
            
            try:
                # Execute the original method
                result = func(*args, **kwargs)
                
                # Calculate duration
                duration_ms = int((time.time() - start_time) * 1000)
                
                # Record successful completion
                task_monitor.end_task(
                    task_id=task_id,
                    status="success",
                    duration_ms=duration_ms,
                    output_data=result,
                    attributes=attributes
                )
                
                # Return the original result
                return result
                
            except Exception as e:
                # Record error
                task_monitor.record_error(
                    task_id=task_id,
                    error_message=str(e),
                    attributes=attributes
                )
                
                # Re-raise the exception
                raise
                
            finally:
                # Update agent status
                if campaign_id:
                    workflow_monitor.update_agent_status(
                        agent_id=agent_name,
                        status="idle"
                    )
                    
        return wrapper
    return decorator

class AgentObserver:
    """
    Class to simplify observability integration into agents.
    
    This helper class provides a unified interface for monitoring agent
    activities and updating workflow state.
    """
    
    def __init__(self, agent_name: str):
        """
        Initialize an observer for the specified agent.
        
        Args:
            agent_name: Name of the agent to monitor
        """
        self.agent_name = agent_name
        self.task_monitor = create_task_monitor(agent_name)
        self.workflow_monitor = create_workflow_monitor()
    
    def track_task(self, campaign_id: Optional[str] = None, 
                  context: Optional[Dict[str, Any]] = None):
        """
        Create a context manager for tracking a task.
        
        Usage:
            with agent_observer.track_task(campaign_id="123") as task:
                # Do work
                task.add_metadata("key", "value")
                
        Args:
            campaign_id: Optional campaign ID associated with this task
            context: Additional context information
            
        Returns:
            A task tracking context manager
        """
        return TaskContext(
            self.task_monitor, 
            self.workflow_monitor,
            self.agent_name,
            campaign_id,
            context or {}
        )
    
    def update_campaign(self, campaign_id: str, status: str, 
                       metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Update campaign status in the workflow.
        
        Args:
            campaign_id: Campaign identifier
            status: New status to record
            metadata: Additional information about the state change
        """
        self.workflow_monitor.update_campaign_status(
            campaign_id=campaign_id,
            status=status,
            metadata=metadata
        )
        
    def update_status(self, status: str, current_task: Optional[str] = None) -> None:
        """
        Update this agent's status.
        
        Args:
            status: New agent status
            current_task: Optional task the agent is currently processing
        """
        self.workflow_monitor.update_agent_status(
            agent_id=self.agent_name,
            status=status,
            current_task=current_task
        )

class TaskContext:
    """Context manager for tracking a task with metadata."""
    
    def __init__(self, task_monitor: TaskMonitor, workflow_monitor: WorkflowMonitor,
                agent_name: str, campaign_id: Optional[str], context: Dict[str, Any]):
        """Initialize the task context."""
        self.task_monitor = task_monitor
        self.workflow_monitor = workflow_monitor
        self.agent_name = agent_name
        self.campaign_id = campaign_id
        self.context = context.copy()
        self.task_id = str(uuid.uuid4())
        self.start_time = None
        
        # Add campaign ID to context if available
        if campaign_id:
            self.context["campaign_id"] = campaign_id
    
    def __enter__(self):
        """Start tracking the task."""
        self.start_time = time.time()
        
        # Record task start
        self.task_monitor.start_task(
            task_id=self.task_id,
            attributes=self.context
        )
        
        # Update agent status
        if self.campaign_id:
            self.workflow_monitor.update_agent_status(
                agent_id=self.agent_name,
                status="processing",
                current_task=self.campaign_id
            )
            
            # Update campaign status
            self.workflow_monitor.update_campaign_status(
                campaign_id=self.campaign_id,
                status=f"{self.agent_name}_started",
                metadata={"task_id": self.task_id}
            )
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """End task tracking with success or error."""
        duration_ms = int((time.time() - self.start_time) * 1000)
        
        if exc_type is None:
            # Task completed successfully
            self.task_monitor.end_task(
                task_id=self.task_id,
                status="success",
                duration_ms=duration_ms,
                attributes=self.context
            )
            
            # Update campaign status on success
            if self.campaign_id:
                self.workflow_monitor.update_campaign_status(
                    campaign_id=self.campaign_id,
                    status=f"{self.agent_name}_completed",
                    metadata={"duration_ms": duration_ms}
                )
        else:
            # Task failed
            self.task_monitor.record_error(
                task_id=self.task_id,
                error_message=str(exc_val),
                attributes=self.context
            )
            
            # Update campaign status on failure
            if self.campaign_id:
                self.workflow_monitor.update_campaign_status(
                    campaign_id=self.campaign_id,
                    status=f"{self.agent_name}_failed",
                    metadata={"error": str(exc_val)}
                )
        
        # Reset agent status
        if self.campaign_id:
            self.workflow_monitor.update_agent_status(
                agent_id=self.agent_name,
                status="idle"
            )
        
        # Don't suppress exceptions
        return False
    
    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to the task context."""
        self.context[key] = value