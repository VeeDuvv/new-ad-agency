# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

"""
File: backend/utils/test_decompositions.py

Need for this file (5th-grader explanation):
Imagine you have many different toy sets, like 'Client Acquisition & Onboarding'
or 'Reporting & Insights'. This tester lets you pick any toy set name—like
'Client Acquisition & Onboarding'—and asks our Blueprint Maker to list all the
little steps it needs under APQC (or eTOM, if you choose). That way, you can
quickly see breakdowns for lots of functions in one place.
"""

import sys
import json
from backend.agents.openai.func_decomp_agent import FuncArchAgent

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_decompositions.py \"Function Name\" [framework]")
        print("  framework: APQC (default) or eTOM")
        sys.exit(1)

    fn = sys.argv[1]
    framework = sys.argv[2] if len(sys.argv) > 2 else "APQC"

    agent = FuncArchAgent()
    print(f"\n--- Decomposition for: {fn}  (framework: {framework}) ---\n")
    result = agent.decompose(fn, framework)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
