# SPDX-License-Identifier: MIT

# Copyright (c) 2025 Vamsi Duvvuri

# NewCo Ad Agency — AI-Powered Campaign Value Chain

_Last updated: 2025-05-05_

## Overview

This document captures the end-to-end process flow for our AI-driven ad agency, mapping each stage to its responsible agent and human role. We update this file whenever the pipeline or responsibilities shift.

---

## 1. Client Intake & Onboarding

**Owner:** Vee (CEO) / `IntakeAgent`

- **Input:** Raw client brief (goals, budget, KPIs, notes)
- **Output:** `campaign_spec` JSON with fields:
  - `objectives`
  - `budget`
  - `KPIs`
  - `notes`

---

## 2. Strategy Planning

**Owner:** Sam (CSO) / `StrategyAgent`

- **Input:** `campaign_spec`
- **Output:** `strategy` JSON:
  - `segments`: List of audience segments
  - `themes`: Creative themes
  - `channel_mix`: Channel budget proportions

---

## 3. Campaign Blueprint (L0–L4)

**Owner:** Cathy (CTO) / `FuncArchAgent`

- **Input:** `strategy` + `function_name` + `framework`
- **Output:** `blueprint` JSON with five levels:
  - **L0**: Function
  - **L1**: Processes
  - **L2**: Activities
  - **L3**: Tasks
  - **L4**: Subtasks

---

## 4. Micro-Decomposition

**Owner:** Cathy (CTO) / `MicroDecompAgent`

- **Input:** Each L3 task object
- **Output:** `subtasks` array (3–6 subtasks per task)

---

## 5. Execution Planning

**Owner:** Amy (COO) / `ExecutionAgent`

- **Input:** Single subtask object
- **Output:**
  ```json
  {
    "status":"success"|"error",
    "details":{ "steps_executed":[<tool names>] }
  }
  ```
