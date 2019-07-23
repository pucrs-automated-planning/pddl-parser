# PDDL Parser [![Build Status](https://travis-ci.org/pucrs-automated-planning/pddl-parser.svg?branch=master)](https://travis-ci.org/pucrs-automated-planning/pddl-parser) [![DOI](https://zenodo.org/badge/42985356.svg)](https://zenodo.org/badge/latestdoi/42985356)
**planning in Python**

## Source
- [action.py](action.py) with an Action structure.
- [PDDL.py](PDDL.py) with a PDDL parser.
- [planner.py](planner.py) with a planner.
- [dinner](dinner) folder with a PDDL example from Daniel Weld, the Dinner domain.

## Parser execution
```Shell
# Parser can be used separately
cd pddl-parser
python -B PDDL.py dinner/dinner.pddl dinner/pb1.pddl
# Output
----------------------------
['define',
 ['domain', 'dinner'],
 [':requirements', ':strips'],
 [':predicates', ['clean'], ['dinner'], ['quiet'], ['present'], ['garbage']],
 [':action',
  'cook',
  ':parameters',
  [],
  ':precondition',
  ['and', ['clean']],
  ':effect',
  ['and', ['dinner']]],
 [':action',
  'wrap',
  ':parameters',
  [],
  ':precondition',
  ['and', ['quiet']],
  ':effect',
  ['and', ['present']]],
 [':action',
  'carry',
  ':parameters',
  [],
  ':precondition',
  ['and', ['garbage']],
  ':effect',
  ['and', ['not', ['garbage']], ['not', ['clean']]]],
 [':action',
  'dolly',
  ':parameters',
  [],
  ':precondition',
  ['and', ['garbage']],
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
```Shell
# Planning using BFS
cd pddl-parser
python -B planner.py dinner/dinner.pddl dinner/pb1.pddl
# Output
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