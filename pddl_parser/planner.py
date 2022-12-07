#!/usr/bin/env python
# Four spaces as indentation [no tabs]

# This file is part of PDDL Parser, available at <https://github.com/pucrs-automated-planning/pddl-parser>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from .PDDL import PDDL_Parser


class Planner:

    # -----------------------------------------------
    # Solve
    # -----------------------------------------------

    def solve(self, domain, problem):
        # Parser
        parser = PDDL_Parser()
        parser.parse_domain(domain)
        parser.parse_problem(problem)
        # Parsed data
        state = parser.state
        goal_pos = parser.positive_goals
        goal_not = parser.negative_goals
        # Do nothing
        if self.applicable(state, goal_pos, goal_not):
            return []
        # Grounding process
        ground_actions = []
        for action in parser.actions:
            for act in action.groundify(parser.objects, parser.types):
                ground_actions.append(act)
        # Search
        visited = set([state])
        fringe = [state, None]
        while fringe:
            state = fringe.pop(0)
            plan = fringe.pop(0)
            for act in ground_actions:
                if self.applicable(state, act.positive_preconditions, act.negative_preconditions):
                    new_state = self.apply(state, act.add_effects, act.del_effects)
                    if new_state not in visited:
                        if self.applicable(new_state, goal_pos, goal_not):
                            full_plan = [act]
                            while plan:
                                act, plan = plan
                                full_plan.insert(0, act)
                            return full_plan
                        visited.add(new_state)
                        fringe.append(new_state)
                        fringe.append((act, plan))
        return None

    # -----------------------------------------------
    # Applicable
    # -----------------------------------------------

    def applicable(self, state, positive, negative):
        return positive.issubset(state) and negative.isdisjoint(state)

    # -----------------------------------------------
    # Apply
    # -----------------------------------------------

    def apply(self, state, positive, negative):
        return state.difference(negative).union(positive)


# -----------------------------------------------
# Main
# -----------------------------------------------
if __name__ == '__main__':
    import sys, time
    start_time = time.time()
    domain = sys.argv[1]
    problem = sys.argv[2]
    verbose = len(sys.argv) > 3 and sys.argv[3] == '-v'
    planner = Planner()
    plan = planner.solve(domain, problem)
    print('Time: ' + str(time.time() - start_time) + 's')
    if plan is not None:
        print('plan:')
        for act in plan:
            print(act if verbose else act.name + ' ' + ' '.join(act.parameters))
    else:
        sys.exit('No plan was found')
