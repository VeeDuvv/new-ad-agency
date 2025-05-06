# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

# add a fifth grade level explanation of the code
# This code is like a recipe book for different helpers (agents) 
# that work together to make a cool project. 
# Each helper has its own special job, 
# and this code helps them understand what they need to do and how to do it.


from pydantic import BaseModel
from typing import List, Dict, Optional

#
# 1) IntakeAgent
#
class IntakeInput(BaseModel):
    client_brief: str
    goals: str
    budget: float
    KPIs: List[str]
    campaign_id: Optional[str]

class IntakeOutput(BaseModel):
    campaign_id: str
    objectives: str
    budget: float
    KPIs: List[str]
    notes: str

#
# 2) StrategyAgent
#
class StrategyInput(BaseModel):
    campaign_spec: Dict[str, Optional[str]]

class StrategyOutput(BaseModel):
    segments: List[str]
    themes: List[str]
    channel_mix: Dict[str, float]

#
# 3) FuncArchAgent
#
class FuncArchInput(BaseModel):
    function_name: str
    framework: str

class LevelItem(BaseModel):
    name: str
    role: str
    tools: List[str]
    deliverable: str
    time_estimate: str
    subitems: Optional[List["LevelItem"]] = None

LevelItem.update_forward_refs()

class FuncArchOutput(BaseModel):
    levels: Dict[str, List[LevelItem]]

#
# 4) MicroDecompAgent
#
class MicroDecompInput(BaseModel):
    name: str
    role: str
    tools: List[str]
    deliverable: str
    time_estimate: str

class Subtask(BaseModel):
    name: str
    role: str
    tools: List[str]
    deliverable: str
    time_estimate: str

class MicroDecompOutput(BaseModel):
    subtasks: List[Subtask]

#
# 5) ExecutionAgent (Planning)
#
class ExecuteInput(BaseModel):
    name: str
    role: str
    tools: List[str]
    deliverable: str
    time_estimate: str

class ExecuteDetails(BaseModel):
    steps_executed: List[str]

class ExecuteOutput(BaseModel):
    status: str
    details: ExecuteDetails

#
# 6) APICallerAgent
#
class APICallerInput(ExecuteInput):
    plan: List[str]

class APICallerOutput(BaseModel):
    status: str
    details: Dict[str, Dict]  # executed + responses

#
# 7) ReportingAgent
#
class ReportingInput(BaseModel):
    campaign_id: Optional[str]
    executions: List[ExecuteOutput]

class ReportKPIs(BaseModel):
    total_tasks: int
    successful: int
    failed: int

class ReportingDetails(BaseModel):
    summary: str
    KPIs: ReportKPIs
    tools_used: List[str]

class ReportingOutput(BaseModel):
    report: ReportingDetails
