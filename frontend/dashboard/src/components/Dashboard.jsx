// SPDX-License-Identifier: MIT
// Copyright (c) 2025 Vamsi Duvvuri

import React, { useState } from "react";
import Sidebar from "./Sidebar";
import CampaignOverview from "./CampaignOverview";
import AgentWorkspace from "./AgentWorkspace";

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState("overview");

  // Placeholder components for remaining tabs
  const AnalyticsHub = () => (
    <div>
      <h2 className="text-2xl font-bold mb-6">Analytics Hub</h2>
      <div className="card">
        <h3 className="text-lg font-medium mb-4">Campaign Performance</h3>
        <p>Your analytics information will appear here.</p>
      </div>
    </div>
  );

  const BlueprintMaker = () => (
    <div>
      <h2 className="text-2xl font-bold mb-6">Blueprint Maker</h2>
      <div className="card">
        <h3 className="text-lg font-medium mb-4">Campaign Blueprint</h3>
        <p>Your blueprint maker will appear here.</p>
      </div>
    </div>
  );

  // Render the active component based on the selected tab
  const renderActiveComponent = () => {
    switch (activeTab) {
      case "overview":
        return <CampaignOverview />;
      case "agents":
        return <AgentWorkspace />;
      case "analytics":
        return <AnalyticsHub />;
      case "blueprint":
        return <BlueprintMaker />;
      default:
        return <CampaignOverview />;
    }
  };

  return (
    <div className="flex">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      <div className="ml-64 flex-1 p-6">{renderActiveComponent()}</div>
    </div>
  );
};

export default Dashboard;
