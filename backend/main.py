# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

"""
File: backend/main.py

Need for this file (5th-grader explanation):
"Think of this as the front door to our Blueprint Maker house. 
We made a special mailbox (/decompose) where you drop a letter 
with two things: the name of the toy set (function) and which 
map book (APQC or eTOM) you want to follow. Inside, our blueprint 
robot reads that letter, makes the plan, and sends it back out 
the door in JSON format!

We added even more mailboxes for our AI-Native Ad Agency dashboard,
so now you can also get information about campaigns, agents, and analytics!"
"""

from typing import List, Optional
import logging
import os
import mimetypes
from datetime import datetime, timedelta

# FastAPI imports
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Application-specific imports
from dotenv import load_dotenv
from backend.agents.factory import get_agent

import uvicorn

# Load environment variables
load_dotenv()  # load OPENAI_API_KEY

# Initialize FastAPI app
app = FastAPI(title="AI-Native Ad Agency API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)s %(levelname)s %(message)s"
)
logger = logging.getLogger("ai_ad_agency")

# Ensure proper MIME types
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('application/json', '.json')

# ========== MODEL DEFINITIONS ==========

class AgentRequest(BaseModel):
    agent: str
    payload: dict

class Campaign(BaseModel):
    id: str
    name: str
    client: str
    status: str
    impressions: int
    clicks: int
    ctr: float

class Agent(BaseModel):
    id: str
    name: str
    status: str
    tasksCompleted: int
    avgDuration: float
    errorRate: float
    lastActive: str

class OverviewMetrics(BaseModel):
    activeCampaigns: int
    completedCampaigns: int
    totalImpressions: int
    totalClicks: int
    averageCTR: float
    totalConversions: int

class TimeSeriesPoint(BaseModel):
    name: str
    impressions: int
    clicks: int
    conversions: int

# ========== SAMPLE DATA (REPLACE WITH DATABASE IN PRODUCTION) ==========

# Sample campaign data
campaigns = [
    {
        "id": "cam_1",
        "name": "Summer Promotion 2025",
        "client": "SunFun Co.",
        "status": "active",
        "impressions": 750000,
        "clicks": 32000,
        "ctr": 4.27
    },
    {
        "id": "cam_2",
        "name": "Product Launch X200",
        "client": "TechGiant",
        "status": "active",
        "impressions": 500000,
        "clicks": 18500,
        "ctr": 3.7
    },
    {
        "id": "cam_3",
        "name": "Fall Collection Preview",
        "client": "Fashion Forward",
        "status": "planning",
        "impressions": 0,
        "clicks": 0,
        "ctr": 0
    },
    {
        "id": "cam_4",
        "name": "Holiday Season Special",
        "client": "Gifty",
        "status": "planning",
        "impressions": 0,
        "clicks": 0,
        "ctr": 0
    },
    {
        "id": "cam_5",
        "name": "Back to School",
        "client": "EduSupplies",
        "status": "active",
        "impressions": 1200000,
        "clicks": 37000,
        "ctr": 3.08
    }
]

# Sample agent data
agents_data = [
    {
        "id": "intake_agent", 
        "name": "Intake Agent",
        "status": "idle", 
        "tasksCompleted": 45, 
        "avgDuration": 2.5, 
        "errorRate": 0.02,
        "lastActive": (datetime.now() - timedelta(minutes=15)).isoformat()
    },
    {
        "id": "strategy_agent", 
        "name": "Strategy Agent",
        "status": "processing", 
        "tasksCompleted": 38, 
        "avgDuration": 15, 
        "errorRate": 0.05,
        "lastActive": datetime.now().isoformat()
    },
    {
        "id": "func_arch_agent", 
        "name": "Functional Architecture Agent",
        "status": "idle", 
        "tasksCompleted": 32, 
        "avgDuration": 8.5, 
        "errorRate": 0.01,
        "lastActive": (datetime.now() - timedelta(minutes=45)).isoformat()
    },
    {
        "id": "micro_decomp_agent", 
        "name": "Micro Decomposition Agent",
        "status": "idle", 
        "tasksCompleted": 120, 
        "avgDuration": 1.2, 
        "errorRate": 0.03,
        "lastActive": (datetime.now() - timedelta(minutes=30)).isoformat()
    },
    {
        "id": "execution_agent", 
        "name": "Execution Agent",
        "status": "processing", 
        "tasksCompleted": 58, 
        "avgDuration": 5.5, 
        "errorRate": 0.04,
        "lastActive": datetime.now().isoformat()
    },
    {
        "id": "api_caller_agent", 
        "name": "API Caller Agent",
        "status": "idle", 
        "tasksCompleted": 78, 
        "avgDuration": 3.2, 
        "errorRate": 0.02,
        "lastActive": (datetime.now() - timedelta(minutes=10)).isoformat()
    },
    {
        "id": "reporting_agent", 
        "name": "Reporting Agent",
        "status": "idle", 
        "tasksCompleted": 25, 
        "avgDuration": 6.8, 
        "errorRate": 0.01,
        "lastActive": (datetime.now() - timedelta(hours=2)).isoformat()
    }
]

# ========== API ENDPOINTS ==========

# Agent endpoint
@app.post("/api/agent")
def call_agent(req: AgentRequest):
    try:
        agent = get_agent(req.agent)
    except KeyError:
        logger.error("No such agent registered: %s", req.agent)
        raise HTTPException(status_code=404, detail=f"No such agent: {req.agent}")

    try:
        result = agent.run(req.payload)
    except Exception as e:
        logger.exception("Agent %s raised exception", req.agent)
        raise HTTPException(status_code=500, detail=str(e))

    return {"result": result}

# Campaign related endpoints
@app.get("/api/campaigns", response_model=List[Campaign])
def get_campaigns():
    return campaigns

@app.get("/api/campaigns/{campaign_id}", response_model=Campaign)
def get_campaign(campaign_id: str):
    campaign = next((c for c in campaigns if c['id'] == campaign_id), None)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

# Agent related endpoints
@app.get("/api/agents", response_model=List[Agent])
def get_agents():
    return agents_data

@app.get("/api/agents/{agent_id}", response_model=Agent)
def get_agent_by_id(agent_id: str):
    agent = next((a for a in agents_data if a['id'] == agent_id), None)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@app.get("/api/agents/{agent_id}/logs")
def get_agent_logs(agent_id: str):
    # In a real implementation, this would fetch logs from a database or log file
    return [
        {"timestamp": (datetime.now() - timedelta(minutes=5)).isoformat(), "level": "INFO", "message": "Task completed successfully"},
        {"timestamp": (datetime.now() - timedelta(minutes=10)).isoformat(), "level": "INFO", "message": "Started processing task"},
        {"timestamp": (datetime.now() - timedelta(hours=1)).isoformat(), "level": "WARN", "message": "API rate limit approaching"}
    ]

# Analytics related endpoints
@app.get("/api/analytics/overview", response_model=OverviewMetrics)
def get_overview_metrics():
    # Calculate overview metrics from the campaigns data
    active_campaigns = sum(1 for c in campaigns if c['status'] == 'active')
    completed_campaigns = sum(1 for c in campaigns if c['status'] == 'completed')
    total_impressions = sum(c['impressions'] for c in campaigns)
    total_clicks = sum(c['clicks'] for c in campaigns)
    avg_ctr = round(total_clicks / total_impressions * 100, 2) if total_impressions > 0 else 0
    total_conversions = int(total_clicks * 0.05)  # Assuming 5% conversion rate
    
    return {
        "activeCampaigns": active_campaigns,
        "completedCampaigns": completed_campaigns,
        "totalImpressions": total_impressions,
        "totalClicks": total_clicks,
        "averageCTR": avg_ctr,
        "totalConversions": total_conversions
    }

@app.get("/api/analytics/timeseries/{metric}", response_model=List[TimeSeriesPoint])
def get_timeseries_data(metric: str, period: str = Query("weekly", description="Time period (weekly, monthly)")):
    # Sample time series data for performance metrics
    if period == "weekly":
        return [
            {"name": "Week 1", "impressions": 450000, "clicks": 15750, "conversions": 810},
            {"name": "Week 2", "impressions": 520000, "clicks": 18200, "conversions": 940},
            {"name": "Week 3", "impressions": 680000, "clicks": 23800, "conversions": 1230},
            {"name": "Week 4", "impressions": 800000, "clicks": 29750, "conversions": 1340}
        ]
    elif period == "monthly":
        return [
            {"name": "Jan", "impressions": 1800000, "clicks": 63000, "conversions": 3240},
            {"name": "Feb", "impressions": 2100000, "clicks": 73500, "conversions": 3780},
            {"name": "Mar", "impressions": 2450000, "clicks": 85750, "conversions": 4410},
            {"name": "Apr", "impressions": 2720000, "clicks": 95200, "conversions": 4900},
            {"name": "May", "impressions": 2450000, "clicks": 87500, "conversions": 4320}
        ]
    
    return []  # Return empty data for unknown periods

# ========== STATIC FILE SERVING ==========

# Serve the frontend directory (Blueprint Maker and dashboard)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# ========== SERVER STARTUP ==========

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=5000, reload=True)