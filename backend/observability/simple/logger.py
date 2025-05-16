# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

"""
Simple implementation of the TaskMonitor interface using structured logging.
"""

import logging
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

from ..interfaces import TaskMonitor

class SimpleTaskMonitor(TaskMonitor):
    """
    Monitors agent tasks using structured logging.
    
    Each task event (start, completion, error) is logged as a JSON object
    to make parsing and analysis easier in the future.
    """
    
    def __init__(self, agent_name: str):
        """
        Initialize a task monitor for the specified agent.
        
        Args:
            agent_name: Identifier for the agent being monitored
        """
        self.agent_name = agent_name
        self.logger = logging.getLogger(f"agent.{agent_name}")
        
        # Ensure logs directory exists
        os.makedirs("logs", exist_ok=True)
        
        # Ensure logger is properly configured
        if not self.logger.handlers:
            # File handler - writes to agent-specific log file
            file_handler = logging.FileHandler(f"logs/{agent_name}.log")
            file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
            
            # Console handler for development visibility
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
            
            self.logger.setLevel(logging.INFO)
    
    def start_task(self, task_id: str, input_data: Any = None, attributes: Dict[str, Any] = None) -> None:
        """
        Record the start of a task with optional context.
        
        Args:
            task_id: Unique identifier for the task
            input_data: Input data provided to the task (will be summarized)
            attributes: Additional context attributes for the task
        """
        # Create a structured log entry as JSON
        log_entry = {
            "event": "task_start",
            "agent": self.agent_name,
            "task_id": task_id,
            "timestamp": datetime.now().isoformat(),
            "attributes": attributes or {}
        }
        
        # Add input summary if provided, but limit length
        if input_data is not None:
            input_str = str(input_data)
            log_entry["input_summary"] = (input_str[:100] + '...') if len(input_str) > 100 else input_str
        
        self.logger.info(json.dumps(log_entry))
    
    def end_task(self, task_id: str, status: str = "success", 
                output_data: Any = None, duration_ms: Optional[int] = None,
                attributes: Dict[str, Any] = None) -> None:
        """
        Record the end of a task with results.
        
        Args:
            task_id: Unique identifier for the task
            status: Completion status (success, failure, etc.)
            output_data: Output data from the task (will be summarized)
            duration_ms: Task execution duration in milliseconds
            attributes: Additional context attributes for the task
        """
        # Create a structured log entry as JSON
        log_entry = {
            "event": "task_complete",
            "agent": self.agent_name,
            "task_id": task_id,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "attributes": attributes or {}
        }
        
        # Add duration if provided
        if duration_ms is not None:
            log_entry["duration_ms"] = duration_ms
        
        # Add output summary if provided, but limit length
        if output_data is not None:
            output_str = str(output_data)
            log_entry["output_summary"] = (output_str[:100] + '...') if len(output_str) > 100 else output_str
        
        self.logger.info(json.dumps(log_entry))
    
    def record_error(self, task_id: str, error_message: str, 
                    attributes: Dict[str, Any] = None) -> None:
        """
        Record an error that occurred during task execution.
        
        Args:
            task_id: Unique identifier for the task
            error_message: Description of the error
            attributes: Additional context attributes
        """
        # Create a structured log entry as JSON
        log_entry = {
            "event": "task_error",
            "agent": self.agent_name,
            "task_id": task_id,
            "timestamp": datetime.now().isoformat(),
            "error": error_message,
            "attributes": attributes or {}
        }
        
        self.logger.error(json.dumps(log_entry))