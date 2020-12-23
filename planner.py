#!/usr/bin/env python
# Four spaces as indentation [no tabs]

from PDDL import PDDLParser


class Planner:
    # -----------------------------------------------
    # Solve
    # -----------------------------------------------
    def __init__(self):
        pass

    def solve(self, domain, problem):
        # Parser
        parser = PDDLParser()
        parser.parse_domain(domain)
        parser.parse_problem(problem)
        # Parsed data
        state = parser.state
        goal_pos = frozenset(parser.positive_goals)
        goal_not = frozenset(parser.negative_goals)
        # Do nothing
        if self.applicable(state, goal_pos, goal_not):
            return []
        # Grounding process
        ground_actions = []
        for action in parser.actions:
            for act in action.groundify(parser.objects, parser.types):
                ground_actions.append(act)
        # Search
        visited = set(state)
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
        return frozenset(state) - negative | positive


# ==========================================
# Main
# ==========================================
if __name__ == '__main__':
    import sys
    import time
    start_time = time.time()
    domain = sys.argv[1]
    problem = sys.argv[2]
    planner = Planner()
    plan = planner.solve(domain, problem)
    print('Time: ' + str(time.time() - start_time) + 's')
    if plan:
        print('Plan -')
        for act in plan:
            print(act)
    else:
        print('No plan was found')
