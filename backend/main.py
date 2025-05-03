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
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from backend.agents.factory import get_agent

import uvicorn

load_dotenv()  # load OPENAI_API_KEY

app = FastAPI(title="Blueprint Maker API")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)s %(levelname)s %(message)s"
)
logger = logging.getLogger("blueprint_maker")
class AgentRequest(BaseModel):
    agent: str
    payload: dict

@app.post("/api/agent")
def call_agent(req: AgentRequest):
    logger.debug("Received /api/agent request: agent=%s payload=%s", req.agent, req.payload)
    try:
        agent = get_agent(req.agent)
    except KeyError:
        logger.error("No such agent registered: %s", req.agent)
        raise HTTPException(status_code=404, detail=f"No such agent: {req.agent}")

    try:
        result = agent.run(req.payload)
        logger.debug("Agent %s returned: %s", req.agent, result)
    except Exception as e:
        logger.exception("Agent %s raised exception", req.agent)
        raise HTTPException(status_code=500, detail=str(e))

    return {"result": result}

# ——— Static files (UI) ———
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# ——— Run server (dev only) ———
if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
