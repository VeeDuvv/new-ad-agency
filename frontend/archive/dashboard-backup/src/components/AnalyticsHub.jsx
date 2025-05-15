// SPDX-License-Identifier: MIT
// Copyright (c) 2025 Vamsi Duvvuri

import React, { useState, useEffect } from "react";
import { analyticsService } from "../services/api";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const AnalyticsHub = () => {
  const [performanceData, setPerformanceData] = useState([]);
  const [periodFilter, setPeriodFilter] = useState("weekly");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Sample channel distribution data
  const channelData = [
    { name: "Social Media", value: 35 },
    { name: "Search", value: 25 },
    { name: "Display", value: 20 },
    { name: "Email", value: 15 },
    { name: "Other", value: 5 },
  ];

  const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#9E77F0"];

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const data = await analyticsService.getTimeSeriesData(
          "campaign_performance",
          periodFilter
        );
        setPerformanceData(data);
        setError(null);
      } catch (err) {
        console.error("Error fetching analytics data:", err);
        setError("Failed to load analytics data. Please try again later.");
        // Fallback data
        setPerformanceData([
          {
            name: "Week 1",
            impressions: 450000,
            clicks: 15750,
            conversions: 810,
          },
          {
            name: "Week 2",
            impressions: 520000,
            clicks: 18200,
            conversions: 940,
          },
          {
            name: "Week 3",
            impressions: 680000,
            clicks: 23800,
            conversions: 1230,
          },
          {
            name: "Week 4",
            impressions: 800000,
            clicks: 29750,
            conversions: 1340,
          },
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [periodFilter]);

  const handlePeriodChange = (period) => {
    setPeriodFilter(period);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Analytics Hub</h2>
        <div className="flex space-x-2">
          <button
            onClick={() => handlePeriodChange("weekly")}
            className={`px-3 py-1 rounded-md ${
              periodFilter === "weekly"
                ? "bg-primary-600 text-white"
                : "bg-gray-200 text-gray-700"
            }`}
          >
            Weekly
          </button>
          <button
            onClick={() => handlePeriodChange("monthly")}
            className={`px-3 py-1 rounded-md ${
              periodFilter === "monthly"
                ? "bg-primary-600 text-white"
                : "bg-gray-200 text-gray-700"
            }`}
          >
            Monthly
          </button>
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
          <span className="ml-4 text-gray-600">Loading analytics data...</span>
        </div>
      ) : error ? (
        <div className="bg-red-50 border-l-4 border-red-500 p-4">
          <p className="text-red-700">{error}</p>
        </div>
      ) : (
        <>
          {/* Campaign Performance Chart */}
          <div className="card">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              Campaign Performance
            </h3>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart
                  data={performanceData}
                  margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="impressions"
                    name="Impressions"
                    stroke="#0284c7"
                  />
                  <Line
                    type="monotone"
                    dataKey="clicks"
                    name="Clicks"
                    stroke="#7c3aed"
                  />
                  <Line
                    type="monotone"
                    dataKey="conversions"
                    name="Conversions"
                    stroke="#16a34a"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Channel Distribution Chart */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Channel Distribution
              </h3>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={channelData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                      label={({ name, percent }) =>
                        `${name} ${(percent * 100).toFixed(0)}%`
                      }
                    >
                      {channelData.map((entry, index) => (
                        <Cell
                          key={`cell-${index}`}
                          fill={COLORS[index % COLORS.length]}
                        />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Agent Efficiency Chart */}
            <div className="card">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Agent Efficiency
              </h3>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={[
                      { name: "Intake", tasks: 45, time: 2.5 },
                      { name: "Strategy", tasks: 38, time: 15 },
                      { name: "FuncArch", tasks: 32, time: 8.5 },
                      { name: "MicroDecomp", tasks: 120, time: 1.2 },
                      { name: "Execution", tasks: 58, time: 5.5 },
                      { name: "APICaller", tasks: 78, time: 3.2 },
                      { name: "Reporting", tasks: 25, time: 6.8 },
                    ]}
                    margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis yAxisId="left" orientation="left" stroke="#0284c7" />
                    <YAxis
                      yAxisId="right"
                      orientation="right"
                      stroke="#7c3aed"
                    />
                    <Tooltip />
                    <Legend />
                    <Bar
                      yAxisId="left"
                      dataKey="tasks"
                      name="Tasks Completed"
                      fill="#0284c7"
                    />
                    <Bar
                      yAxisId="right"
                      dataKey="time"
                      name="Avg. Time (s)"
                      fill="#7c3aed"
                    />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        </>
      )}

      {/* Analytics Configuration */}
      <div className="card">
        <h3 className="text-lg font-medium text-gray-900 mb-4">
          Analytics Settings
        </h3>
        <p className="text-gray-600 mb-4">
          Configure which metrics are displayed and how they're calculated.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Conversion Attribution Model
            </label>
            <select className="w-full border border-gray-300 rounded-md px-3 py-2">
              <option>Last Click</option>
              <option>First Click</option>
              <option>Linear</option>
              <option>Time Decay</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Default Time Period
            </label>
            <select className="w-full border border-gray-300 rounded-md px-3 py-2">
              <option>Last 7 Days</option>
              <option>Last 30 Days</option>
              <option>Last Quarter</option>
              <option>Year to Date</option>
            </select>
          </div>
        </div>
        <div className="mt-4">
          <button className="btn-primary">Save Settings</button>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsHub;
