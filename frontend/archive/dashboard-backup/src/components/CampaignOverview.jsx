// SPDX-License-Identifier: MIT
// Copyright (c) 2025 Vamsi Duvvuri

import React, { useState, useEffect } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { campaignService, analyticsService } from "../services/api";

const CampaignOverview = () => {
  const [metrics, setMetrics] = useState({
    activeCampaigns: 0,
    completedCampaigns: 0,
    totalImpressions: 0,
    totalClicks: 0,
    averageCTR: 0,
    totalConversions: 0,
  });

  const [campaigns, setCampaigns] = useState([]);
  const [performanceData, setPerformanceData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);

        // Fetch overview metrics and campaigns in parallel
        const [metricsData, campaignsData, performanceData] = await Promise.all(
          [
            analyticsService.getOverviewMetrics(),
            campaignService.getAllCampaigns(),
            analyticsService.getTimeSeriesData(
              "campaign_performance",
              "weekly"
            ),
          ]
        );

        setMetrics(metricsData);
        setCampaigns(campaignsData);
        setPerformanceData(performanceData);
        setError(null);
      } catch (err) {
        console.error("Error fetching dashboard data:", err);
        setError("Failed to load dashboard data. Please try again later.");

        // Set fallback demo data if API fails
        setMetrics({
          activeCampaigns: 5,
          completedCampaigns: 12,
          totalImpressions: 2450000,
          totalClicks: 87500,
          averageCTR: 3.57,
          totalConversions: 4320,
        });

        setCampaigns([
          {
            id: "cam_1",
            name: "Summer Promotion 2025",
            client: "SunFun Co.",
            status: "active",
            impressions: 750000,
            clicks: 32000,
            ctr: 4.27,
          },
          {
            id: "cam_2",
            name: "Product Launch X200",
            client: "TechGiant",
            status: "active",
            impressions: 500000,
            clicks: 18500,
            ctr: 3.7,
          },
          {
            id: "cam_3",
            name: "Fall Collection Preview",
            client: "Fashion Forward",
            status: "planning",
            impressions: 0,
            clicks: 0,
            ctr: 0,
          },
          {
            id: "cam_4",
            name: "Holiday Season Special",
            client: "Gifty",
            status: "planning",
            impressions: 0,
            clicks: 0,
            ctr: 0,
          },
          {
            id: "cam_5",
            name: "Back to School",
            client: "EduSupplies",
            status: "active",
            impressions: 1200000,
            clicks: 37000,
            ctr: 3.08,
          },
        ]);

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

    // Set up polling every 30 seconds
    const intervalId = setInterval(fetchData, 30000);

    // Clean up on component unmount
    return () => clearInterval(intervalId);
  }, []);

  // Handle creating a new campaign
  const handleCreateCampaign = () => {
    // You could implement a modal or navigation to a campaign creation form
    alert("Create campaign functionality will be implemented here");
  };

  // Handle viewing a campaign
  const handleViewCampaign = (campaignId) => {
    // You could implement navigation to campaign details page
    alert(`View campaign ${campaignId}`);
  };

  // Handle editing a campaign
  const handleEditCampaign = (campaignId) => {
    // You could implement a modal or navigation to campaign edit form
    alert(`Edit campaign ${campaignId}`);
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold mb-6">Campaign Overview</h2>

      {loading && (
        <div className="flex justify-center items-center py-8">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
          <span className="ml-4 text-gray-600">Loading dashboard data...</span>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg
                className="h-5 w-5 text-red-400"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">{error}</p>
              <p className="text-xs text-red-500">
                Using demo data for display.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Key metrics section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-2">Campaigns</h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-gray-500">Active</p>
              <p className="text-3xl font-bold text-primary-600">
                {metrics.activeCampaigns}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Completed</p>
              <p className="text-3xl font-bold text-secondary-600">
                {metrics.completedCampaigns}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Performance
          </h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-gray-500">Impressions</p>
              <p className="text-3xl font-bold text-primary-600">
                {metrics.totalImpressions.toLocaleString()}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Clicks</p>
              <p className="text-3xl font-bold text-secondary-600">
                {metrics.totalClicks.toLocaleString()}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-2">Conversion</h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-gray-500">Avg. CTR</p>
              <p className="text-3xl font-bold text-primary-600">
                {metrics.averageCTR}%
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Conversions</p>
              <p className="text-3xl font-bold text-secondary-600">
                {metrics.totalConversions.toLocaleString()}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Performance chart section */}
      <div className="card">
        <h3 className="text-lg font-medium text-gray-900 mb-4">
          Campaign Performance Trend
        </h3>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={performanceData}
              margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="impressions" name="Impressions" fill="#0284c7" />
              <Bar dataKey="clicks" name="Clicks" fill="#7c3aed" />
              <Bar dataKey="conversions" name="Conversions" fill="#16a34a" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Campaign list section */}
      <div className="card">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-medium text-gray-900">
            Active Campaigns
          </h3>
          <button className="btn-primary" onClick={handleCreateCampaign}>
            New Campaign
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Campaign
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Client
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Status
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Impressions
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Clicks
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  CTR
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {campaigns.map((campaign) => (
                <tr key={campaign.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {campaign.name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {campaign.client}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        campaign.status === "active"
                          ? "bg-green-100 text-green-800"
                          : campaign.status === "planning"
                          ? "bg-yellow-100 text-yellow-800"
                          : "bg-gray-100 text-gray-800"
                      }`}
                    >
                      {campaign.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {campaign.impressions.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {campaign.clicks.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {campaign.ctr > 0 ? `${campaign.ctr}%` : "-"}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <button
                      className="text-primary-600 hover:text-primary-900 mr-3"
                      onClick={() => handleViewCampaign(campaign.id)}
                    >
                      View
                    </button>
                    <button
                      className="text-secondary-600 hover:text-secondary-900"
                      onClick={() => handleEditCampaign(campaign.id)}
                    >
                      Edit
                    </button>
                  </td>
                </tr>
              ))}
              {campaigns.length === 0 && !loading && (
                <tr>
                  <td
                    colSpan="7"
                    className="px-6 py-4 text-center text-sm text-gray-500"
                  >
                    No campaigns found. Click "New Campaign" to create one.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default CampaignOverview;
