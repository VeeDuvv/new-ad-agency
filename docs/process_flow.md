# SPDX-License-Identifier: MIT

# Copyright (c) 2025 Vamsi Duvvuri

# NewCo Ad Agency — AI-Powered Campaign Value Chain

_Last updated: 2025-05-05_

# NewCo Ad Agency – Process Flow

_Last updated: 2025-05-10_

## 1. Overview

This document describes the end-to-end flow of our AI-powered campaign pipeline:

1. **Intake & Onboarding**
2. **Strategy Planning**
3. **Blueprint Generation (L0–L4)**
4. **Micro-Decomposition**
5. **Execution Planning**
6. **API Calling**
7. **Reporting & Insights**

Each step is implemented by an autonomous agent (or pair of agents), with clearly defined inputs, outputs, and hand-offs.

## 2. High-Level Flowchart

````mermaid
flowchart TD
  A[Client Brief] -->|raw text| IntakeAgent
  IntakeAgent -->|campaign_spec| StrategyAgent
  StrategyAgent -->|strategy| FuncArchAgent
  FuncArchAgent -->|L3 tasks| MicroDecompAgent
  MicroDecompAgent -->|subtasks| ExecutionAgent
  ExecutionAgent -->|plan| APICallerAgent
  APICallerAgent -->|real_results| ReportingAgent
  ReportingAgent -->|final_report| ClientDelivery[Client Delivery]


---

### Section 3: Detailed Step Descriptions (Part 1)

```markdown
## 3. Detailed Step Descriptions

### 3.1 IntakeAgent
- **Owner**: Vee (CEO) / Agent key: `intake`
- **Input**:
  - `client_brief`: string
  - `goals`: string
  - `budget`: string or number
  - `KPIs`: array of strings
- **Output**:
  - `campaign_spec` (object) with:
    - `objectives`: string
    - `budget`: float (USD)
    - `KPIs`: string[]
    - `notes`: string
- **Logic**: LLM-prompt → strict JSON

---

### 3.2 StrategyAgent
- **Owner**: Sam (CSO) / Agent key: `strategy`
- **Input**:
  - `campaign_spec`
- **Output**:
  - `strategy` (object) with:
    - `segments`: string[] (2–4 items)
    - `themes`: string[] (2–3 items)
    - `channel_mix`: { [channel: string]: number } (sums to 1)
- **Logic**: LLM-prompt → JSON

---

### 3.3 FuncArchAgent
- **Owner**: Cathy (CTO) / Agent key: `decomp`
- **Input**:
  - `function_name`: string (e.g. “Launch Campaign”)
  - `framework`: “APQC” or “eTOM”
- **Output**:
  - `levels`: {
    - `L0`: [ { … } ]
    - `L1` … `L4`: arrays of same objects with `subitems` nesting
    }
- **Logic**: LLM-prompt → validate JSON schema for L0–L4
### 3.4 MicroDecompAgent
- **Owner**: Cathy / Agent key: `micro_decomp`
- **Input**:
  - Single L3-Task object
- **Output**:
  - `{ subtasks: [ { name, role, tools, deliverable, time_estimate } ] }`
- **Logic**: LLM-prompt → JSON array

---

### 3.5 ExecutionAgent (Planning)
- **Owner**: Amy (COO) / Agent key: `execute`
- **Input**:
  - Single subtask object from MicroDecompAgent
- **Output**:
  - `{ status: "success"|"error", details: { steps_executed: string[] } }`
- **Logic**: LLM-prompt forcing flat JSON

---

### 3.6 APICallerAgent
- **Owner**: Amy / Agent key: `apicaller`
- **Input**:
  - Subtask + `steps_executed` list
- **Output**:
  - `{ status: "...", details: { <API response data> } }`
- **Logic**: HTTP/SDK calls, retries, error-handling

---

### 3.7 ReportingAgent
- **Owner**: Frank (CFO) / Agent key: `report`
- **Input**:
  - `campaign_id` (optional)
  - `executions`: array of execution results
- **Output**:
  - `{ report: { summary: string, KPIs: { total_tasks, successful, failed }, tools_used: string[] } }`
- **Logic**: LLM-prompt → JSON
## 4. Data Contracts & Validation

- **JSON Schema** files for each agent’s input/output (to live in `schemas/`)
- **AuditAgent** will validate payloads against these schemas at runtime
## 5. Change Log

| Date       | Change                                               | By    |
|------------|------------------------------------------------------|-------|
| 2025-05-01 | Initial draft of all seven agents’ flows             | Cathy |
| 2025-05-03 | Added APICallerAgent placeholder                     | Cathy |
| 2025-05-10 | Swapped ExecutionAgent to flat JSON contract         | Cathy |

---

**Next Steps:**
- Commit this file as `docs/process_flow.md` in your repo.
- When agents or flows evolve, update Section 3 and append to the Change Log.
````
