// SPDX-License-Identifier: MIT
// Copyright (c) 2025 Vamsi Duvvuri

import React, { useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const AgentWorkspace = () => {
  // Sample data (will be replaced with API calls later)
  const [agents, setAgents] = useState([
    {
      id: "intake_agent",
      name: "Intake Agent",
      status: "idle",
      tasksCompleted: 45,
      avgDuration: 2.5,
      errorRate: 0.02,
      lastActive: "2025-05-09T08:45:12Z",
    },
    {
      id: "strategy_agent",
      name: "Strategy Agent",
      status: "processing",
      tasksCompleted: 38,
      avgDuration: 15,
      errorRate: 0.05,
      lastActive: "2025-05-09T09:12:35Z",
    },
    {
      id: "func_arch_agent",
      name: "Functional Architecture Agent",
      status: "idle",
      tasksCompleted: 32,
      avgDuration: 8.5,
      errorRate: 0.01,
      lastActive: "2025-05-09T08:15:22Z",
    },
    {
      id: "micro_decomp_agent",
      name: "Micro Decomposition Agent",
      status: "idle",
      tasksCompleted: 120,
      avgDuration: 1.2,
      errorRate: 0.03,
      lastActive: "2025-05-09T08:30:45Z",
    },
    {
      id: "execution_agent",
      name: "Execution Agent",
      status: "processing",
      tasksCompleted: 58,
      avgDuration: 5.5,
      errorRate: 0.04,
      lastActive: "2025-05-09T09:15:03Z",
    },
    {
      id: "api_caller_agent",
      name: "API Caller Agent",
      status: "idle",
      tasksCompleted: 78,
      avgDuration: 3.2,
      errorRate: 0.02,
      lastActive: "2025-05-09T08:50:12Z",
    },
    {
      id: "reporting_agent",
      name: "Reporting Agent",
      status: "idle",
      tasksCompleted: 25,
      avgDuration: 6.8,
      errorRate: 0.01,
      lastActive: "2025-05-09T07:45:30Z",
    },
  ]);

  const [selectedAgent, setSelectedAgent] = useState(agents[0]);

  // Sample performance data for the selected agent
  const agentPerformanceData = [
    { date: "05/03", tasks: 5, errors: 0, duration: 2.3 },
    { date: "05/04", tasks: 8, errors: 1, duration: 2.5 },
    { date: "05/05", tasks: 12, errors: 0, duration: 2.1 },
    { date: "05/06", tasks: 10, errors: 0, duration: 2.4 },
    { date: "05/07", tasks: 15, errors: 1, duration: 2.6 },
    { date: "05/08", tasks: 20, errors: 0, duration: 2.2 },
    { date: "05/09", tasks: 18, errors: 0, duration: 2.3 },
  ];

  // Format timestamp to readable format
  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold mb-6">Agent Workspace</h2>

      {/* Agent Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Total Agents
          </h3>
          <p className="text-3xl font-bold text-primary-600">{agents.length}</p>
        </div>

        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Active Agents
          </h3>
          <p className="text-3xl font-bold text-green-600">
            {agents.filter((agent) => agent.status === "processing").length}
          </p>
        </div>

        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Tasks Completed
          </h3>
          <p className="text-3xl font-bold text-secondary-600">
            {agents.reduce((total, agent) => total + agent.tasksCompleted, 0)}
          </p>
        </div>

        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Avg. Error Rate
          </h3>
          <p className="text-3xl font-bold text-yellow-600">
            {(
              (agents.reduce((total, agent) => total + agent.errorRate, 0) /
                agents.length) *
              100
            ).toFixed(2)}
            %
          </p>
        </div>
      </div>

      {/* Agent Selection and Details */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Agent List */}
        <div className="card lg:col-span-1">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Agents</h3>
          <div className="space-y-2">
            {agents.map((agent) => (
              <div
                key={agent.id}
                className={`p-3 rounded-lg cursor-pointer transition-colors ${
                  selectedAgent.id === agent.id
                    ? "bg-primary-100 border border-primary-300"
                    : "bg-gray-50 hover:bg-gray-100"
                }`}
                onClick={() => setSelectedAgent(agent)}
              >
                <div className="flex justify-between items-center">
                  <div>
                    <p className="font-medium">{agent.name}</p>
                    <p className="text-xs text-gray-500">
                      Last active: {formatTimestamp(agent.lastActive)}
                    </p>
                  </div>
                  <span
                    className={`px-2 py-1 text-xs rounded-full ${
                      agent.status === "processing"
                        ? "bg-green-100 text-green-800"
                        : "bg-gray-100 text-gray-800"
                    }`}
                  >
                    {agent.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Agent Details and Performance */}
        <div className="lg:col-span-2 space-y-6">
          {/* Agent Details */}
          <div className="card">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              {selectedAgent.name} Details
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <p className="text-sm text-gray-500">Status</p>
                <p className="font-medium">{selectedAgent.status}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Tasks Completed</p>
                <p className="font-medium">{selectedAgent.tasksCompleted}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Avg. Duration (s)</p>
                <p className="font-medium">{selectedAgent.avgDuration}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Error Rate</p>
                <p className="font-medium">
                  {(selectedAgent.errorRate * 100).toFixed(2)}%
                </p>
              </div>
            </div>
          </div>

          {/* Performance Chart */}
          <div className="card">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              {selectedAgent.name} Performance
            </h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart
                  data={agentPerformanceData}
                  margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis yAxisId="left" />
                  <YAxis yAxisId="right" orientation="right" />
                  <Tooltip />
                  <Legend />
                  <Line
                    yAxisId="left"
                    type="monotone"
                    dataKey="tasks"
                    name="Tasks Completed"
                    stroke="#0284c7"
                    activeDot={{ r: 8 }}
                  />
                  <Line
                    yAxisId="left"
                    type="monotone"
                    dataKey="errors"
                    name="Errors"
                    stroke="#ef4444"
                  />
                  <Line
                    yAxisId="right"
                    type="monotone"
                    dataKey="duration"
                    name="Avg. Duration (s)"
                    stroke="#7c3aed"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Agent Controls */}
          <div className="flex space-x-4">
            <button className="btn-primary">Restart Agent</button>
            <button className="btn-secondary">View Logs</button>
            <button className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50">
              Configure
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AgentWorkspace;
