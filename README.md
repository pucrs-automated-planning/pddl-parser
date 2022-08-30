# PDDL Parser [![Actions Status](https://github.com/pucrs-automated-planning/pddl-parser/workflows/build/badge.svg)](https://github.com/pucrs-automated-planning/pddl-parser/actions) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4391071.svg)](https://doi.org/10.5281/zenodo.4391071) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
**Classical Planning in Python**

PDDL Parser is a simple parser for [PDDL](https://en.wikipedia.org/wiki/Planning_Domain_Definition_Language), described in Python without external dependencies.
It supports ``:strips``, ``:negative-preconditions`` and ``:typing`` requirements.
It contains a planner only as an example, being compact and readable for educational purposes.
New features are outside the scope of this project, which was originally intended as a propositional PDDL parser to avoid the complexity of grounding and the ambiguity of typing descriptions.

PDDL Parser was originally designed and developed by [Mau Magnaguagno](https://github.com/Maumagnaguagno) in 2015 to be used in the classroom, following [HyperTensioN](https://github.com/Maumagnaguagno/HyperTensioN)'s parsing style.

## Source
- [action.py](pddl_parser/action.py) with an Action class
- [PDDL.py](pddl_parser/PDDL.py) with a PDDL parser
- [planner.py](pddl_parser/planner.py) with a planner
- [examples](examples/) folder with PDDL domains:
  - [Dinner](examples/dinner) from Daniel Weld, a propositional domain
  - [Blocks World](examples/blocksworld)
  - [Travelling Salesman Problem](examples/tsp)
  - [Dock Worker Robot](examples/dwr)

## Installation
The parser and planner can easily be used within other projects once installed.
The examples and tests should work without installation.

```Shell
cd pddl-parser
python setup.py install
```

## Execution
The parser can be executed without planning, it outputs elements found in the input files and the structures created.

```Shell
cd pddl-parser
python -B -m pddl_parser.PDDL examples/dinner/dinner.pddl examples/dinner/pb1.pddl
```

<details><summary>Parser output</summary>

```Shell
----------------------------
['define',
 ['domain', 'dinner'],
 [':requirements', ':strips'],
 [':predicates', ['clean'], ['dinner'], ['quiet'], ['present'], ['garbage']],
 [':action', 'cook', ':precondition', ['clean'], ':effect', ['dinner']],
 [':action', 'wrap', ':precondition', ['quiet'], ':effect', ['present']],
 [':action',
  'carry',
  ':precondition',
  ['garbage'],
  ':effect',
  ['and', ['not', ['garbage']], ['not', ['clean']]]],
 [':action',
  'dolly',
  ':precondition',
  ['garbage'],
  ':effect',
  ['and', ['not', ['garbage']], ['not', ['quiet']]]]]
----------------------------
['define',
 ['problem', 'pb1'],
 [':domain', 'dinner'],
 [':init', ['garbage'], ['clean'], ['quiet']],
 [':goal', ['and', ['dinner'], ['present'], ['not', ['garbage']]]]]
----------------------------
Domain name: dinner
action: cook
  parameters: []
  positive_preconditions: [['clean']]
  negative_preconditions: []
  add_effects: [['dinner']]
  del_effects: []

action: wrap
  parameters: []
  positive_preconditions: [['quiet']]
  negative_preconditions: []
  add_effects: [['present']]
  del_effects: []

action: carry
  parameters: []
  positive_preconditions: [['garbage']]
  negative_preconditions: []
  add_effects: []
  del_effects: [['garbage'], ['clean']]

action: dolly
  parameters: []
  positive_preconditions: [['garbage']]
  negative_preconditions: []
  add_effects: []
  del_effects: [['garbage'], ['quiet']]

----------------------------
Problem name: pb1
Objects: {}
State: [['garbage'], ['clean'], ['quiet']]
Positive goals: [['dinner'], ['present']]
Negative goals: [['garbage']]
```
</details>

The planner uses BFS, it outputs the time taken and signatures of the actions in the plan found or failure.
The output of the planner is more verbose with option ``-v``.

```Shell
cd pddl-parser
python -B -m pddl_parser.planner examples/dinner/dinner.pddl examples/dinner/pb1.pddl -v
```

<details><summary>Planner output</summary>

```Shell
Time: 0.00200009346008s
plan:
action: cook
  parameters: []
  positive_preconditions: [['clean']]
  negative_preconditions: []
  add_effects: [['dinner']]
  del_effects: []

action: wrap
  parameters: []
  positive_preconditions: [['quiet']]
  negative_preconditions: []
  add_effects: [['present']]
  del_effects: []

action: carry
  parameters: []
  positive_preconditions: [['garbage']]
  negative_preconditions: []
  add_effects: []
  del_effects: [['garbage'], ['clean']]
```
</details>

## API

### Action
```Python
class Action:
    def __init__(self, name, parameters, positive_preconditions, negative_preconditions, add_effects, del_effects)
    def __str__(self)
    def __eq__(self, other)
    def groundify(self, objects, types)
    def replace(self, group, variables, assignment)
```

### Parser
```Python
class PDDL_Parser:
    def scan_tokens(self, filename)
    def parse_domain(self, domain_filename, requirements=SUPPORTED_REQUIREMENTS)
    def parse_domain_extended(self, t, group)
    def parse_hierarchy(self, group, structure, name, redefine)
    def parse_objects(self, group, name)
    def parse_types(self, types)
    def parse_predicates(self, group)
    def parse_action(self, group)
    def parse_action_extended(self, action, group)
    def parse_problem(self, problem_filename)
    def parse_problem_extended(self, t, group)
    def split_predicates(self, group, positive, negative, name, part)
```

### Planner
```Python
class PDDL_Planner:
    def solve(self, domain, problem)
    def applicable(self, state, positive, negative)
    def apply(self, state, positive, negative)
```

## Extensions
New parser features should be added through inheritance using ``super`` and ``parse_*_extended`` methods.
The Action class may also require modifications to deal with possible extensions.