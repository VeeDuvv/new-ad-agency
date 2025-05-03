# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri


# agents/factory.py

## fifth grader explanation:
# “This is like a toy factory that makes different kinds of robots.
# When you want a robot, you tell the factory which one you want
# (like a LEGO set). The factory then finds the right robot blueprint
# and builds it for you. This way, you can get any robot you need
# without having to know how to build it yourself!”


import yaml, importlib
from agents.base import Agent

_registry = yaml.safe_load(open("agents/registry.yaml"))

def get_agent(name: str) -> Agent:
    entry = _registry[name]
    module_name, cls_name = entry["impl"].rsplit(".", 1)
    mod = importlib.import_module(module_name)
    cls = getattr(mod, cls_name)
    return cls()  # Must be an Agent subclass
