# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

"""
Core interfaces for the observability system.

These interfaces define the contract for monitoring agent tasks and workflow state,
allowing for different implementations while maintaining a consistent API.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class TaskMonitor(ABC):
    """Interface for monitoring individual agent tasks"""
    
    @abstractmethod
    def start_task(self, task_id: str, input_data: Any = None, attributes: Dict[str, Any] = None) -> None:
        """Record the start of a task with optional context"""
        pass
    
    @abstractmethod
    def end_task(self, task_id: str, status: str = "success", 
                 output_data: Any = None, duration_ms: Optional[int] = None,
                 attributes: Dict[str, Any] = None) -> None:
        """Record the end of a task with results"""
        pass
    
    @abstractmethod
    def record_error(self, task_id: str, error_message: str, 
                    attributes: Dict[str, Any] = None) -> None:
        """Record an error that occurred during task execution"""
        pass


class WorkflowMonitor(ABC):
    """Interface for tracking workflow state across agents"""
    
    @abstractmethod
    def update_campaign_status(self, campaign_id: str, status: str, 
                              metadata: Dict[str, Any] = None) -> None:
        """Update the status of a campaign in the workflow"""
        pass
    
    @abstractmethod
    def update_agent_status(self, agent_id: str, status: str, 
                           current_task: Optional[str] = None) -> None:
        """Update the status of an agent"""
        pass
    
    @abstractmethod
    def get_campaign_status(self, campaign_id: Optional[str] = None) -> Any:
        """Get the current status of one or all campaigns"""
        pass
    
    @abstractmethod
    def get_agent_status(self, agent_id: Optional[str] = None) -> Any:
        """Get the current status of one or all agents"""
        pass