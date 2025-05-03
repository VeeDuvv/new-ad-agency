# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

"""
File: backend/main.py

Need for this file (5th-grader explanation):
“Imagine our Blueprint Maker lives in a house with a little door called ‘/decompose.’ 
Anyone can knock on that door (send a request) with the name of a toy set (function), 
and it will open up and give them the step-by-step plan in return. 
This file builds that little door so our robot helpers can talk to our Blueprint Maker over the web.”
"""

from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn

# Load environment (API key)
load_dotenv()

# Import our Blueprint Maker
from backend.agents.func_decomp_agent import FuncArchAgent

app = FastAPI(title="Blueprint Maker API")

agent = FuncArchAgent()

class DecomposeRequest(BaseModel):
    function_name: str

@app.post("/decompose")
async def decompose(req: DecomposeRequest):
    """
    Accepts JSON {"function_name": "..."} and returns the decomposition JSON.
    """
    blueprint = agent.decompose(req.function_name)
    return blueprint

# Serve frontend folder at root
from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    # Run with: python backend/main.py
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
