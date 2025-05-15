// SPDX-License-Identifier: MIT
// Copyright (c) 2025 Vamsi Duvvuri

import React from "react";

const Sidebar = ({ activeTab, setActiveTab }) => {
  // Navigation items
  const navItems = [
    { id: "overview", label: "Campaign Overview" },
    { id: "agents", label: "Agent Workspace" },
    { id: "analytics", label: "Analytics Hub" },
    { id: "blueprint", label: "Blueprint Maker" },
  ];

  return (
    <div className="bg-primary-800 text-white w-64 h-screen fixed left-0 top-0 flex flex-col">
      <div className="p-6">
        <h2 className="text-2xl font-bold">AI-Native Ad Agency</h2>
      </div>

      <nav className="mt-6">
        <ul>
          {navItems.map((item) => (
            <li key={item.id} className="px-2 py-1">
              <button
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center px-4 py-2 w-full text-left rounded-lg ${
                  activeTab === item.id
                    ? "bg-primary-700 text-white"
                    : "text-primary-100 hover:bg-primary-700"
                }`}
              >
                {item.label}
              </button>
            </li>
          ))}
        </ul>
      </nav>

      <div className="absolute bottom-0 w-64 p-6">
        <div className="flex items-center">
          <div className="h-8 w-8 rounded-full bg-primary-500 flex items-center justify-center">
            <span className="font-bold">C</span>
          </div>
          <div className="ml-3">
            <p className="font-medium">Claude (CTO)</p>
            <p className="text-xs text-primary-300">Online</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
