// SPDX-License-Identifier: MIT
// Copyright (c) 2025 Vamsi Duvvuri

import React, { useState } from "react";
import { Routes, Route, useNavigate, useLocation } from "react-router-dom";
import Sidebar from "./Sidebar";
import CampaignOverview from "./CampaignOverview";
import AgentWorkspace from "./AgentWorkspace";
import AnalyticsHub from "./AnalyticsHub";
import BlueprintIntegration from "./BlueprintIntegration";

const Dashboard = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const pathSegments = location.pathname.split("/").filter(Boolean);
  const currentPath = pathSegments.length > 1 ? pathSegments[1] : "overview";

  const handleTabChange = (tabId) => {
    navigate(tabId === "overview" ? "/" : `/${tabId}`);
  };

  return (
    <div className="flex">
      <Sidebar activeTab={currentPath} setActiveTab={handleTabChange} />

      <div className="ml-64 flex-1 p-6">
        <Routes>
          <Route path="/" element={<CampaignOverview />} />
          <Route path="/agents" element={<AgentWorkspace />} />
          <Route path="/analytics" element={<AnalyticsHub />} />
          <Route path="/blueprint" element={<BlueprintIntegration />} />
          <Route path="*" element={<CampaignOverview />} />
        </Routes>
      </div>
    </div>
  );
};

export default Dashboard;
