# PDDL Parser [![Build Status](https://travis-ci.org/pucrs-automated-planning/pddl-parser.svg?branch=master)](https://travis-ci.org/pucrs-automated-planning/pddl-parser) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4391071.svg)](https://doi.org/10.5281/zenodo.4391071)
**Classical Planning in Python**

## Source
- [action.py](action.py) with an Action class
- [PDDL.py](PDDL.py) with a PDDL parser
- [planner.py](planner.py) with a planner
- [examples](examples/) folder with PDDL domains:
  - [Airport](examples/airport) from AIPS2000 Planning Competition
  - [Dinner](examples/dinner) from Daniel Weld, a propositional domain
  - [Blocks World](examples/blocksworld)
  - [Dock Worker Robot](examples/dwr)
  - [Travelling Salesman Problem](examples/tsp)

## Parser execution
```Shell
# Parser can be used separately
cd pddl-parser
python -B PDDL.py examples/dinner/dinner.pddl examples/dinner/pb1.pddl
# Output
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

## Planner execution
The output of the planner is more verbose with option ``-v``.

```Shell
# Planning using BFS
cd pddl-parser
python -B planner.py examples/dinner/dinner.pddl examples/dinner/pb1.pddl -v
# Output
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

## API

### Action
```Python
class Action:
    def __init__(self, name, parameters, positive_preconditions, negative_preconditions, add_effects, del_effects, extensions = None)
    def __str__(self)
    def __eq__(self, other)
    def groundify(self, objects, types)
    def replace(self, group, variables, assignment)
```

### Parser
```Python
class PDDL_Parser:
    def scan_tokens(self, filename)
    def parse_domain(self, domain_filename)
    def parse_domain_extended(self, t, group)
    def parse_hierarchy(self, group, structure, name, redefine)
    def parse_objects(self, group, name)
    def parse_types(self, types)
    def parse_predicates(self, group)
    def parse_action(self, group)
    def parse_action_extended(self, t, group)
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

## Notes
New Parser features should be added through inheritance using ``super`` and ``parse_*_extended`` methods.
The Action class must be replaced to deal with possible extensions.
The planner is only an example, being compact for educational purposes.
New features are outside the scope of this project, which was originally intended as a propositional PDDL parser to avoid the complexity of grounding and the ambiguity of typing descriptions.