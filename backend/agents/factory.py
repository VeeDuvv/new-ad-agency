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
import os
import logging
logger = logging.getLogger("blueprint_maker.factory")

from backend.agents.base import Agent
# Compute the registry path next to this file
_here = os.path.dirname(__file__)
_registry_path = os.path.join(_here, "registry.yaml")

# Load the registry
_registry = yaml.safe_load(open(_registry_path, "r"))
def get_agent(name: str) -> Agent:
    # logger.debug("backend.agents.factory: get_agent(%s)", name)
    entry = _registry[name]
    module_name, cls_name = entry["impl"].rsplit(".", 1)
    mod = importlib.import_module(module_name)
    cls = getattr(mod, cls_name)
    # logger.debug("backend.agents.factory: class(%s)", cls)
    return cls()  # Must be an Agent subclass
