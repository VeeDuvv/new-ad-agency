// SPDX-License-Identifier: MIT
// Copyright (c) 2025 Vamsi Duvvuri

import React from "react";

const BlueprintIntegration = () => {
  const openBlueprintMaker = () => {
    window.open("/blueprint", "_blank");
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold mb-6">Blueprint Maker</h2>

      <div className="card">
        <h3 className="text-lg font-medium mb-4">Launch Blueprint Maker</h3>
        <p className="mb-6">
          The Blueprint Maker is a tool for decomposing functions into
          hierarchical tasks. It allows you to visualize the breakdown of
          complex advertising functions into manageable components.
        </p>
        <button onClick={openBlueprintMaker} className="btn-primary">
          Open Blueprint Maker
        </button>
      </div>

      <div className="card">
        <h3 className="text-lg font-medium mb-4">Recent Blueprints</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Function Name
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Framework
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Created
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
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Creative Development
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  APQC
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  May 8, 2025
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <button className="text-primary-600 hover:text-primary-900 mr-3">
                    View
                  </button>
                  <button className="text-secondary-600 hover:text-secondary-900">
                    Edit
                  </button>
                </td>
              </tr>
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Media Planning
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  APQC
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  May 5, 2025
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <button className="text-primary-600 hover:text-primary-900 mr-3">
                    View
                  </button>
                  <button className="text-secondary-600 hover:text-secondary-900">
                    Edit
                  </button>
                </td>
              </tr>
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Campaign Analysis
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  eTOM
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  May 3, 2025
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <button className="text-primary-600 hover:text-primary-900 mr-3">
                    View
                  </button>
                  <button className="text-secondary-600 hover:text-secondary-900">
                    Edit
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default BlueprintIntegration;
