# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

"""
Run this to auto-generate JSON Schema files for every agent:
  python3 backend/utils/generate_schemas.py
They will be emitted to the `schemas/` folder.
"""

import os, json
from backend.schemas.models import (
    IntakeInput, IntakeOutput,
    StrategyInput, StrategyOutput,
    FuncArchInput, FuncArchOutput,
    MicroDecompInput, MicroDecompOutput,
    ExecuteInput, ExecuteOutput,
    APICallerInput, APICallerOutput,
    ReportingInput, ReportingOutput
)

SCHEMAS = {
    "intake_input.json":    IntakeInput,
    "intake_output.json":   IntakeOutput,
    "strategy_input.json":  StrategyInput,
    "strategy_output.json": StrategyOutput,
    "decomp_input.json":    FuncArchInput,
    "decomp_output.json":   FuncArchOutput,
    "micro_decomp_input.json":  MicroDecompInput,
    "micro_decomp_output.json": MicroDecompOutput,
    "execute_input.json":   ExecuteInput,
    "execute_output.json":  ExecuteOutput,
    "apicaller_input.json": APICallerInput,
    "apicaller_output.json":APICallerOutput,
    "report_input.json":    ReportingInput,
    "report_output.json":   ReportingOutput,
}

def main():
    schema_dir = os.path.join(os.getcwd(), "schemas")
    os.makedirs(schema_dir, exist_ok=True)

    for fname, model in SCHEMAS.items():
        schema = model.schema()
        path = os.path.join(schema_dir, fname)
        with open(path, "w") as f:
            json.dump(schema, f, indent=2)
        print(f"Wrote {path}")

if __name__ == "__main__":
    main()
