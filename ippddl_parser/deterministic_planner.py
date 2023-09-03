# This file is part of IPPDDL Parser, available at <https://github.com/AndreMoukarzel/ippddl-parser/>.

from .deterministic_parser import DeterministicParser


class DeterministicPlanner:
    """ Planner that uses breadth-first search (BFS) to reach the goal states of
    a deterministic problem.
    """

    def solve(self, domain, problem):
        # Parser
        parser = DeterministicParser()
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
                if act.is_applicable(state):
                    new_state = act.apply(state)
                    if new_state not in visited:
                        if self.applicable(new_state, goal_pos, goal_not):
                            print("found goal")
                            full_plan = [act]
                            while plan:
                                act, plan = plan
                                full_plan.insert(0, act)
                            return full_plan
                        visited.add(new_state)
                        fringe.append(new_state)
                        fringe.append((act, plan))
        return None


    def applicable(self, state, positive, negative):
        return positive.issubset(state) and negative.isdisjoint(state)



if __name__ == '__main__':
    import sys, time
    start_time = time.time()
    domain = sys.argv[1]
    problem = sys.argv[2]
    verbose = len(sys.argv) > 3 and sys.argv[3] == '-v'
    planner = DeterministicPlanner()
    plan = planner.solve(domain, problem)
    print('Time: ' + str(time.time() - start_time) + 's')
    if plan is not None:
        print('plan:')
        for act in plan:
            print(act if verbose else f"\t{act.name} {' '.join(act.parameters)}")
    else:
        sys.exit('No plan was found')
