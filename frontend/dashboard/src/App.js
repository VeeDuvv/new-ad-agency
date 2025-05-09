// SPDX-License-Identifier: MIT
// Copyright (c) 2025 Vamsi Duvvuri

import React from "react";
import { Routes, Route } from "react-router-dom";
import Dashboard from "./components/Dashboard";
import "./index.css";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/*" element={<Dashboard />} />
      </Routes>
    </div>
  );
}

export default App;
