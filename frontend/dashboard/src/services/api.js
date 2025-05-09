// SPDX-License-Identifier: MIT
// Copyright (c) 2025 Vamsi Duvvuri

import axios from "axios";

// Get the API URL from environment variables or use a default
const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5000/api";

// Create an axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000, // 10 seconds
});

// Add a request interceptor for authentication if needed
api.interceptors.request.use(
  (config) => {
    // You can add auth tokens here if needed
    // const token = localStorage.getItem('token');
    // if (token) {
    //   config.headers['Authorization'] = `Bearer ${token}`;
    // }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error:", error);

    // You can add global error handling here
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.error("Response data:", error.response.data);
      console.error("Response status:", error.response.status);
    } else if (error.request) {
      // The request was made but no response was received
      console.error("No response received:", error.request);
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error("Request error:", error.message);
    }

    return Promise.reject(error);
  }
);

// Campaign related API calls
export const campaignService = {
  getAllCampaigns: async () => {
    try {
      const response = await api.get("/campaigns");
      return response.data;
    } catch (error) {
      console.error("Error fetching campaigns:", error);
      throw error;
    }
  },

  getCampaignById: async (campaignId) => {
    try {
      const response = await api.get(`/campaigns/${campaignId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching campaign ${campaignId}:`, error);
      throw error;
    }
  },

  createCampaign: async (campaignData) => {
    try {
      const response = await api.post("/campaigns", campaignData);
      return response.data;
    } catch (error) {
      console.error("Error creating campaign:", error);
      throw error;
    }
  },

  updateCampaign: async (campaignId, campaignData) => {
    try {
      const response = await api.put(`/campaigns/${campaignId}`, campaignData);
      return response.data;
    } catch (error) {
      console.error(`Error updating campaign ${campaignId}:`, error);
      throw error;
    }
  },

  deleteCampaign: async (campaignId) => {
    try {
      const response = await api.delete(`/campaigns/${campaignId}`);
      return response.data;
    } catch (error) {
      console.error(`Error deleting campaign ${campaignId}:`, error);
      throw error;
    }
  },

  getCampaignReport: async (campaignId) => {
    try {
      const response = await api.get(`/campaigns/${campaignId}/report`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching report for campaign ${campaignId}:`, error);
      throw error;
    }
  },
};

// Agent related API calls
export const agentService = {
  getAllAgents: async () => {
    try {
      const response = await api.get("/agents");
      return response.data;
    } catch (error) {
      console.error("Error fetching agents:", error);
      throw error;
    }
  },

  getAgentById: async (agentId) => {
    try {
      const response = await api.get(`/agents/${agentId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching agent ${agentId}:`, error);
      throw error;
    }
  },

  getAgentMetrics: async (agentId) => {
    try {
      const response = await api.get(`/agents/${agentId}/metrics`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching metrics for agent ${agentId}:`, error);
      throw error;
    }
  },

  getAgentLogs: async (agentId) => {
    try {
      const response = await api.get(`/agents/${agentId}/logs`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching logs for agent ${agentId}:`, error);
      throw error;
    }
  },

  restartAgent: async (agentId) => {
    try {
      const response = await api.post(`/agents/${agentId}/restart`);
      return response.data;
    } catch (error) {
      console.error(`Error restarting agent ${agentId}:`, error);
      throw error;
    }
  },

  updateAgentConfig: async (agentId, configData) => {
    try {
      const response = await api.put(`/agents/${agentId}/config`, configData);
      return response.data;
    } catch (error) {
      console.error(`Error updating config for agent ${agentId}:`, error);
      throw error;
    }
  },
};

// Analytics related API calls
export const analyticsService = {
  getOverviewMetrics: async () => {
    try {
      const response = await api.get("/analytics/overview");
      return response.data;
    } catch (error) {
      console.error("Error fetching overview metrics:", error);
      throw error;
    }
  },

  getCampaignPerformance: async (campaignId) => {
    try {
      const response = await api.get(
        `/analytics/campaigns/${campaignId}/performance`
      );
      return response.data;
    } catch (error) {
      console.error(
        `Error fetching performance for campaign ${campaignId}:`,
        error
      );
      throw error;
    }
  },

  getSystemEfficiency: async () => {
    try {
      const response = await api.get("/analytics/system-efficiency");
      return response.data;
    } catch (error) {
      console.error("Error fetching system efficiency metrics:", error);
      throw error;
    }
  },

  getTimeSeriesData: async (metric, period) => {
    try {
      const response = await api.get(
        `/analytics/timeseries/${metric}?period=${period}`
      );
      return response.data;
    } catch (error) {
      console.error(`Error fetching time series data for ${metric}:`, error);
      throw error;
    }
  },
};

// Blueprint maker related API calls
export const blueprintService = {
  getAllBlueprints: async () => {
    try {
      const response = await api.get("/blueprints");
      return response.data;
    } catch (error) {
      console.error("Error fetching blueprints:", error);
      throw error;
    }
  },

  getBlueprintById: async (blueprintId) => {
    try {
      const response = await api.get(`/blueprints/${blueprintId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching blueprint ${blueprintId}:`, error);
      throw error;
    }
  },

  createBlueprint: async (blueprintData) => {
    try {
      const response = await api.post("/blueprints", blueprintData);
      return response.data;
    } catch (error) {
      console.error("Error creating blueprint:", error);
      throw error;
    }
  },

  updateBlueprint: async (blueprintId, blueprintData) => {
    try {
      const response = await api.put(
        `/blueprints/${blueprintId}`,
        blueprintData
      );
      return response.data;
    } catch (error) {
      console.error(`Error updating blueprint ${blueprintId}:`, error);
      throw error;
    }
  },

  deleteBlueprint: async (blueprintId) => {
    try {
      const response = await api.delete(`/blueprints/${blueprintId}`);
      return response.data;
    } catch (error) {
      console.error(`Error deleting blueprint ${blueprintId}:`, error);
      throw error;
    }
  },
};

export default {
  campaignService,
  agentService,
  analyticsService,
  blueprintService,
};
