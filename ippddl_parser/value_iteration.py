# This file is part of IPPDDL Parser, available at <https://github.com/AndreMoukarzel/ippddl-parser/>.
from typing import Dict
from fractions import Fraction

from .parser import Parser


class ValueIterator:
    """Object that executes value iteration on a probabilistic planning problem
    that can be represented as an MDP.
    """
    GAMMA: float = 0.1

    def solve(self, domain, problem, max_diff: float=0.05, iter_limit: int = 500):
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
                for act in ground_actions:
                    if self.applicable(state, act.positive_preconditions, act.negative_preconditions):
                        if self.applicable(state, goal_pos, goal_neg):
                            # If state is a goal/terminal state, doesn't look for future states in value iteration
                            state_vals[state] = self.state_reward(state, goal_pos, goal_neg)
                            continue

                        # "Future" states are the s', the states reached by applying the action to current state s 
                        future_states = self.apply(state, act.add_effects, act.del_effects)
                        future_state_vals = []
                        for i, fut_state in enumerate(future_states):
                            state_prob = Fraction(act.probabilities[i])
                            fut_state_val = state_vals[fut_state] * state_prob
                            future_state_vals.append(fut_state_val)
                        new_state_val = self.state_reward(state, goal_pos, goal_neg) + self.GAMMA * max(future_state_vals)

                        max_iter_diff = max(max_iter_diff, abs(new_state_val - state_val))
                        state_vals[state] = new_state_val
            iter_num += 1
        
        return state_vals



    def applicable(self, state, positive, negative):
        return positive.issubset(state) and negative.isdisjoint(state)


    def apply(self, state, positive, negative) -> list:
        """Applies all the possible positive and negative effects to a state,
        returning a list of the possible resulting states and their probabilities.
        """
        resulting_states = []
        for i in range(len(positive)):
            pos_effects = positive[i]
            neg_effects = negative[i]
            new_state = state.difference(neg_effects).union(pos_effects)
            resulting_states.append(new_state)
        return resulting_states
    

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
                if self.applicable(state, act.positive_preconditions, act.negative_preconditions):
                    possible_new_states = self.apply(state, act.add_effects, act.del_effects)
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
    verbose = len(sys.argv) > 3 and sys.argv[3] == '-v'
    interator = ValueIterator()
    state_vals = interator.solve(domain, problem)
    print('Time: ' + str(time.time() - start_time) + 's')
    print(state_vals)
