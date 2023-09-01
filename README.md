# IPPDDL Parser [![Actions Status](https://github.com/AndreMoukarzel/ippddl-parser/workflows/build/badge.svg)](https://github.com/AndreMoukarzel/ippddl-parser/actions) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
**Probabilistic Planning with Imprecise Probabilities in Python**

IPPDDL Parser is a simple parser for IPPDDL, an extension of [PPDDL](https://en.wikipedia.org/wiki/Planning_Domain_Definition_Language#PPDDL), described in Python without external dependencies.

It supports the following requirements: ``:strips``, ``:negative-preconditions``, ``:typing``, ``:equality``, ``:probabilistic-effects`` and ``:conditional-effects``.

It contains a non-probabilistic planner only as an example, being compact and readable for educational purposes.

New features are outside the scope of this project, which is intended as a propositional IPPDDL parser to avoid the complexity of grounding and the ambiguity of typing descriptions.

The [PDDL Parser](https://github.com/pucrs-automated-planning/pddl-parser) this project was based off was originally designed and developed by [Mau Magnaguagno](https://github.com/Maumagnaguagno) in 2015 to be used in the classroom, following [HyperTensioN](https://github.com/Maumagnaguagno/HyperTensioN)'s parsing style.

## Source
- [action.py](ippddl_parser/action.py) with an Action class
- [predicate.py](ippddl_parser/predicate.py) with an Predicate class
- [parser.py](ippddl_parser/parser.py) with a basic PDDL parser
- [probabilistic_parser.py](ippddl_parser/probabilistic_parser.py) with an IPPDDL parser, inheriting core functionalities from the base parser above.
- [planner.py](ippddl_parser/planner.py) with a non-probabilistic planner
- [examples](examples/) folder with PDDL, PPDDL and IPPDDL domains:
  - [Dinner](examples/dinner) from Daniel Weld, a propositional domain
  - [Blocks World](examples/blocksworld)
  - [Probabilistic Blocks World](examples/probabilistic_blocksworld)
  - [Travelling Salesman Problem](examples/tsp)
  - [Dock Worker Robot](examples/dwr)

## Installation
The parser and planner can easily be used within other projects once installed.
The examples and tests should work without installation.

```Shell
cd ippddl-parser
pip install -e .
```

## Important Warning

When working with imprecise probability intervals in the IPPDDL language, actions will "settle" the probabilities of
each effect occurring into real probability values contained within the specified intervals.

**It is required to be possible for the sum of those values to be a value of 100% or lower.**

In other words, you may not set imprecise possibilities in a way that more then one effect will take place simultaneously.

Therefore you may not, as an example, create an action with possible effects *e1* and *e2* where their imprecise
probability intervals are defined as being (3/4, 1) for both effects. In this case, the sum of the settled probabilities
would be, at minimun, 3/4 + 3/4 = 6/4 = 150%, which violates the condition determined above.

## Execution
The parsers can be executed without planning, it outputs elements found in the input files and the structures created.

```Shell
cd ippddl-parser
python -B -m ippddl_parser.parser examples/probabilistic_blocksworld/domain.pddl examples/probabilistic_blocksworld/10blocks.pddl
```

If desired, it is possible to use the base deterministic parser for deterministic problems.

```Shell
cd ippddl-parser
python -B -m ippddl_parser.deterministic_parser examples/dinner/dinner.pddl examples/dinner/pb1.pddl
```

<details><summary>Parser output for Dinner example problem</summary>

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
  effects:
        1
          positive effects: [['dinner']]
          negative effects: []

action: wrap
  parameters: []
  positive_preconditions: [['quiet']]
  negative_preconditions: []
  effects:
        1
          positive effects: [['present']]
          negative effects: []

action: carry
  parameters: []
  positive_preconditions: [['garbage']]
  negative_preconditions: []
  effects:
        1
          positive effects: []
          negative effects: [['clean'], ['garbage']]

action: dolly
  parameters: []
  positive_preconditions: [['garbage']]
  negative_preconditions: []
  effects:
        1
          positive effects: []
          negative effects: [['quiet'], ['garbage']]

----------------------------
Problem name: pb1
Objects: {}
State: [['clean'], ['quiet'], ['garbage']]
Positive goals: [['present'], ['dinner']]
Negative goals: [['garbage']]
```
</details>

The planner uses BFS, it outputs the time taken and signatures of the actions in the plan found or failure.
The output of the planner is more verbose with option ``-v``.

```Shell
cd ippddl-parser
python -B -m ippddl_parser.deterministic_planner examples/dinner/dinner.pddl examples/dinner/pb1.pddl -v
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


In the same way, value iteration can also be executed with probabilistic problems. It will output the values of each
state in a problem.

For more fine control over value iteration, such as the stopping conditions and dealing with reward values, using the
API directly is recommended.

```Shell
cd ippddl-parser
python -B -m ippddl_parser.value_iteration examples/blocksworld/blocksworld.pddl examples/blocksworld/pb1.pddl -v
```

<details><summary>Value Iteration output</summary>

```Shell
Time: 0.0009970664978027344s
frozenset({('holding', 'b'), ('equal', 'b', 'b'), ('clear', 'a'), ('equal', 'a', 'a'), ('ontable', 'a')}): 0.125
frozenset({('ontable', 'b'), ('equal', 'b', 'b'), ('clear', 'a'), ('equal', 'a', 'a'), ('clear', 'b'), ('ontable', 'a')}): 0.25
frozenset({('ontable', 'b'), ('equal', 'b', 'b'), ('clear', 'a'), ('on', 'a', 'b'), ('equal', 'a', 'a')}): 1.0
frozenset({('holding', 'a'), ('ontable', 'b'), ('equal', 'b', 'b'), ('equal', 'a', 'a'), ('clear', 'b')}): 0.5
frozenset({('holding', 'a'), ('equal', 'b', 'b'), ('equal', 'a', 'a'), ('holding', 'b')}): 0.25
frozenset({('equal', 'b', 'b'), ('on', 'b', 'a'), ('equal', 'a', 'a'), ('clear', 'b'), ('ontable', 'a')}): 0.0625
```
</details>

## Extensions
New parser features should be added through inheritance using ``super()`` and ``parse_*_extended`` methods.
The Action class may also require modifications to deal with possible extensions.