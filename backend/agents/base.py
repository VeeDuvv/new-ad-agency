# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

# agents/base.py
# fifth grader explanation:
# “This is like the blueprint for all our robot helpers. It says that every
# robot helper must take a list of instructions (a dict) and give back
# a list of results (also a dict). But this blueprint is just a plan—
# it doesn’t actually do anything. The real robot helpers will follow
# this plan and do the work!”

from typing import Any, Dict

class Agent:
    """
    All agents take a dict input and return a dict output.
    Concrete subclasses will call out to OpenAI, Nvidia IQ, Google A2A, etc.
    """
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("Must implement run()")
