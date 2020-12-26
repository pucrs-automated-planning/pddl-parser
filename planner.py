#!/usr/bin/env python
# Four spaces as indentation [no tabs]

from PDDL import PDDL_Parser

class Planner:
    def __init__(self, plan_format):
        self.plan_format = plan_format
        
    #-----------------------------------------------
    # Solve
    #-----------------------------------------------

    def solve(self, domain, problem):
        # Parser
        parser = PDDL_Parser(self.plan_format)
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

    #-----------------------------------------------
    # Applicable
    #-----------------------------------------------

    def applicable(self, state, positive, negative):
        return positive.issubset(state) and negative.isdisjoint(state)

    #-----------------------------------------------
    # Apply
    #-----------------------------------------------

    def apply(self, state, positive, negative):
        return state.difference(negative).union(positive)


def display_help():
    print('usage: python -B planner.py [option] domain_file problem_file')
    print('Options and arguments:')
    print('-h:           print this help message and exit (also --help)')
    print('-f=OPT:       format for printing plan actions (also --format)')
    print('              OPT is NORMAL or VERBOSE; default is NORMAL.')
    print('domain_file:  Planning Domain Definition Language (PDDL) domain file')
    print('problem_file: Planning Domain Definition Language (PDDL) problem file')
    print()


#-----------------------------------------------
# Main
#-----------------------------------------------
if __name__ == '__main__':
    import sys, time
    start_time = time.time()
    narg = len(sys.argv)
    if narg != 3 and narg != 4:
        display_help()
        sys.exit(0)
    arg1 = sys.argv[1].strip()
    domain = None
    problem = None
    format = 'normal'
    if arg1 == '--help' or arg1 == '-h':
        display_help()
        sys.exit(0)
    elif arg1.startswith('-f=') or arg1.startswith('--format='):
        _, format = arg1.split('=')
        format = format.lower()
        domain = sys.argv[2]
        problem = sys.argv[3]
    else:
        domain = sys.argv[1]
        problem = sys.argv[2]
    planner = Planner(format)
    plan = planner.solve(domain, problem)
    print('Time: ' + str(time.time() - start_time) + 's')
    if plan:
        print('plan:')
        for act in plan:
            print(act)
    else:
        print('No plan was found')