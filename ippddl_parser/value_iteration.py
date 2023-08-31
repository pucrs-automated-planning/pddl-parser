# This file is part of IPPDDL Parser, available at <https://github.com/AndreMoukarzel/ippddl-parser/>.
from typing import Dict, List

from .parser import Parser


class ValueIterator:
    """Object that executes value iteration on a probabilistic planning problem
    that can be represented as an MDP.
    """
    GAMMA: float = 0.5

    def solve(self, domain, problem, max_diff: float=0.05, iter_limit: int = 1000):
        # Parser
        parser = Parser()
        parser.parse_domain(domain)
        parser.parse_problem(problem)
        # Parsed data
        init_state = parser.state
        goal_pos = parser.positive_goals
        goal_neg = parser.negative_goals
        # Grounding process
        ground_actions = []
        for action in parser.actions:
            for act in action.groundify(parser.objects, parser.types):
                ground_actions.append(act)
        # Discover all states
        all_states = self.get_all_states(init_state, ground_actions)
        # Value Iteration
        max_iter_diff: float = 999.0 # Max difference between updated values in this iteration
        state_vals: Dict[str, float] = {} # Value dict of states
        for state in all_states:
            # Initialize all states with value zero (could be a random value too!)
            state_vals[state] = 0.0

        iter_num: int = 0
        while max_iter_diff > max_diff and iter_num < iter_limit:
            max_iter_diff = 0.0

            for state, state_val in state_vals.items():
                # Don't look at future states if current state is already a goal
                if self.state_reward(state, goal_pos, goal_neg):
                    new_state_val = self.state_reward(state, goal_pos, goal_neg)
                    max_iter_diff = max(max_iter_diff, abs(new_state_val - state_vals[state]))
                    state_vals[state] = new_state_val
                    continue

                q_values: List[float] = []
                for act in ground_actions:
                    if act.is_applicable(state):
                        # "Future" states are the s', the states reached by applying the action to current state s 
                        future_states, probabilities = act.get_possible_resulting_states(state)
                        future_state_vals: List[float] = []
                        for i, fut_state in enumerate(future_states):
                            fut_state_val = state_vals[fut_state] * probabilities[i]
                            future_state_vals.append(fut_state_val) #+ self.state_reward(fut_state, goal_pos, goal_neg))
                        q_val = sum(future_state_vals)
                        q_values.append(q_val)
                
                if len(q_values) > 0:
                    new_state_val = self.state_reward(state, goal_pos, goal_neg) + self.GAMMA * max(q_values)
                    max_iter_diff = max(max_iter_diff, abs(new_state_val - state_val))
                    state_vals[state] = new_state_val
            iter_num += 1
        
        return state_vals


    def applicable(self, state, positive, negative):
        return positive.issubset(state) and negative.isdisjoint(state)
    

    def state_reward(self, state, goal_pos, goal_neg) -> float:
        if self.applicable(state, goal_pos, goal_neg):
            # Is a goal state
            return 1.0
        return 0.0
    

    def get_all_states(self, init_state, ground_actions):
        """Uses breadth-first search (BFS) to reach all states of the problem
        and then returns them
        """
        visited = set([init_state])
        fringe = [init_state]
        while fringe:
            state = fringe.pop(0)
            for act in ground_actions:
                if act.is_applicable(state):
                    possible_new_states, _ = act.get_possible_resulting_states(state)
                    for new_state in possible_new_states:
                        if new_state not in visited:
                            visited.add(new_state)
                            fringe.append(new_state)
        return visited


if __name__ == '__main__':
    import sys, time
    start_time = time.time()
    domain = sys.argv[1]
    problem = sys.argv[2]
    iterator = ValueIterator()
    state_vals = iterator.solve(domain, problem)
    print('Time: ' + str(time.time() - start_time) + 's')
    for state, val in state_vals.items():
        print(f"{state}: {val}")
