#!/usr/bin/env python3

from distutils.core import setup

setup(
    name="pddl_parser",
    version="1.0",
    packages=["pddl_parser"],
    scripts=["scripts/action.py", "scripts/PDDL.py", "scripts/planner.py"]
)
