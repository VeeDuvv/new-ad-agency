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
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from agents.factory import get_agent

import uvicorn

from backend.agents.openai.func_decomp_agent import FuncArchAgent
from backend.agents.openai.micro_decomp_agent import MicroDecompAgent

load_dotenv()  # load OPENAI_API_KEY

app = FastAPI(title="Blueprint Maker API")

class AgentRequest(BaseModel):
    agent: str
    payload: dict

@app.post("/api/agent")
def call_agent(req: AgentRequest):
    try:
        agent = get_agent(req.agent)
    except KeyError:
        raise HTTPException(404, f"No such agent: {req.agent}")

    result = agent.run(req.payload)
    return {"result": result}

# ——— Static files (UI) ———
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# ——— Run server (dev only) ———
if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
