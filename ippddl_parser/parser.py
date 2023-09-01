# This file is part of IPPDDL Parser, available at <https://github.com/AndreMoukarzel/ippddl-parser/>.
from fractions import Fraction

from .deterministic_parser import DeterministicParser
from .action import Action


class Parser(DeterministicParser):
    
    SUPPORTED_REQUIREMENTS = DeterministicParser.SUPPORTED_REQUIREMENTS + [
        ':probabilistic-effects', ':conditional-effects', ':rewards', ':imprecise'
    ]


    def parse_domain(self, domain_filename, requirements=SUPPORTED_REQUIREMENTS):
        super().parse_domain(domain_filename, requirements)


    def parse_probabilistic_effect(self, probabilistic_effects, action_name):
        add_effects = []
        del_effects = []
        probabilities = []

        for i in range(0, len(probabilistic_effects), 2):
            prob = Fraction(probabilistic_effects[i]) # Converts string to Fraction
            this_effects = probabilistic_effects[i + 1]
            this_add_effects = []
            this_del_effects = []
            self.split_predicates(this_effects, this_add_effects, this_del_effects, action_name, ' effects')

            add_effects.append(this_add_effects)
            del_effects.append(this_del_effects)
            probabilities.append(prob)
        
        return add_effects, del_effects, probabilities
    

    def parse_imprecise_effect(self, probabilistic_effects, action_name):
        add_effects = []
        del_effects = []
        probabilities = []

        for i in range(0, len(probabilistic_effects), 2):
            prob = [Fraction(val) for val in probabilistic_effects[i]] # Treats the received range of probabilities
            prob.sort()
            this_effects = probabilistic_effects[i + 1]
            this_add_effects = []
            this_del_effects = []
            self.split_predicates(this_effects, this_add_effects, this_del_effects, action_name, ' effects')

            add_effects.append(this_add_effects)
            del_effects.append(this_del_effects)
            probabilities.append(tuple(prob))
        
        return add_effects, del_effects, probabilities


    def parse_action_effects(self, effects: list, action_name: str):
        """Parses the effects of an action.

        The base parser is used in deterministic problems, which are treated as
        a probabilistic problem where all probabilities are 100%.

        Parameters
        ----------
        effects: list
            An action's effects. List with all strings found in an action
            separated by commas.
        action_name: str
            Action's name.
        
        Returns
        -------
        """
        add_effects = []
        del_effects = []
        probabilities = []

        if effects[0] == 'probabilistic':
            prob_effects = effects[1:]
            add_effects, del_effects, probabilities = self.parse_probabilistic_effect(prob_effects, action_name)
        elif effects[0] == 'imprecise':
            prob_effects = effects[1:]
            add_effects, del_effects, probabilities = self.parse_imprecise_effect(prob_effects, action_name)
        else:
            # When the action is deterministic, we hardset its probability of happening to 100%
            self.split_predicates(effects, add_effects, del_effects, action_name, ' effects')
            add_effects = [add_effects]
            del_effects = [del_effects]
            probabilities = [1.0]
        
        return add_effects, del_effects, probabilities
    

    def parse_action(self, group):
        name = group.pop(0)
        if type(name) is not str:
            raise Exception('Action without name definition')
        for act in self.actions:
            if act.name == name:
                raise Exception('Action ' + name + ' redefined')
        parameters = []
        positive_preconditions = []
        negative_preconditions = []
        extensions = []
        add_effects = []
        del_effects = []
        probs = []
        while group:
            t = group.pop(0)
            if t == ':parameters':
                if type(group) is not list:
                    raise Exception('Error with ' + name + ' parameters')
                unparsed_parameters = group.pop(0)
                parameters = self.parse_action_parameters(unparsed_parameters, name)
            elif t == ':precondition':
                self.split_predicates(group.pop(0), positive_preconditions, negative_preconditions, name, ' preconditions')
            elif t == ':effect':
                effects: str = group.pop(0)
                add_effects, del_effects, probs = self.parse_action_effects(effects, name)
            else:
                group.insert(0, t)
                extensions.append(group)
        
        action = Action(name, parameters, positive_preconditions, negative_preconditions, add_effects, del_effects, probs)
        self.parse_action_extended(action, extensions)
        self.actions.append(action)


if __name__ == '__main__':
    import sys, pprint
    domain = sys.argv[1]
    problem = sys.argv[2]
    parser = Parser()
    print('----------------------------')
    pprint.pprint(parser.scan_tokens(domain))
    print('----------------------------')
    pprint.pprint(parser.scan_tokens(problem))
    print('----------------------------')
    parser.parse_domain(domain)
    parser.parse_problem(problem)
    print('Domain name: ' + str(parser.domain_name))
    for act in parser.actions:
        print(act)
    print('----------------------------')
    print('Problem name: ' + str(parser.problem_name))
    print('Objects: ' + str(parser.objects))
    print('State: ' + str([list(i) for i in parser.state]))
    print('Positive goals: ' + str([list(i) for i in parser.positive_goals]))
    print('Negative goals: ' + str([list(i) for i in parser.negative_goals]))
