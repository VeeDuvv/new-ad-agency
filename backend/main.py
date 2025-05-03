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

from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn

load_dotenv()  # load OPENAI_API_KEY

from backend.agents.func_decomp_agent import FuncArchAgent

app = FastAPI(title="Blueprint Maker API")

agent = FuncArchAgent()

class DecomposeRequest(BaseModel):
    function_name: str
    framework: str = "APQC"  # either "APQC" or "eTOM"

@app.post("/decompose")
async def decompose(req: DecomposeRequest):
    """
    Accepts JSON:
      {
        "function_name": "...",
        "framework": "APQC"  // or "eTOM"
      }
    Returns the decomposition JSON aligned to the chosen framework.
    """
    blueprint = agent.decompose(req.function_name, req.framework)
    return blueprint

# Serve frontend
from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
