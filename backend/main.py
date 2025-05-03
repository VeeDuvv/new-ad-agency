# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

"""
File: backend/main.py

Need for this file (5th-grader explanation):
“Think of this as the front door to our Blueprint Maker house. 
We made a special mailbox (/decompose) where you drop a letter 
with two things: the name of the toy set (function) and which 
map book (APQC or eTOM) you want to follow. Inside, our blueprint 
robot reads that letter, makes the plan, and sends it back out 
the door in JSON format!”
"""

from typing import List
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn

from backend.agents.func_decomp_agent import FuncArchAgent
from backend.agents.micro_decomp_agent import MicroDecompAgent

load_dotenv()  # load OPENAI_API_KEY

app = FastAPI(title="Blueprint Maker API")

# ——— Decomposition endpoint ———
class DecomposeRequest(BaseModel):
    function_name: str
    framework: str = "APQC"  # either "APQC" or "eTOM"

@app.post("/decompose")
async def decompose(req: DecomposeRequest):
    """
    Accepts:
      { function_name: str, framework: str }
    Returns:
      L0–L4 decomposition JSON
    """
    agent = FuncArchAgent()
    return agent.decompose(req.function_name, req.framework)

# ——— Drill-down endpoint ———
class DrillRequest(BaseModel):
    name: str
    role: str
    tools: List[str]
    deliverable: str
    time_estimate: str

@app.post("/drilldown")
async def drill_down(req: DrillRequest):
    """
    Accepts:
      { name, role, tools, deliverable, time_estimate }
    Returns:
      { subtasks: [...] }
    """
    micro = MicroDecompAgent()
    subtasks = micro.drill_down(req.dict())
    return {"subtasks": subtasks}

# ——— Static files (UI) ———
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# ——— Run server (dev only) ———
if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
