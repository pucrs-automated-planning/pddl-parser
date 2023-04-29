from .action import Action
from .parser import Parser


class ProbabilisticParser(Parser):
    
    SUPPORTED_REQUIREMENTS = Parser.SUPPORTED_REQUIREMENTS + [
        ':probabilistic-effects', ':conditional-effects', ':rewards'
    ]


    def parse_domain(self, domain_filename, requirements=SUPPORTED_REQUIREMENTS):
        super().parse_domain(domain_filename, requirements)


    def parse_probabilistic_effect(self, probabilistic_effects, action_name):
        add_effects = []
        del_effects = []

        for i in range(0, len(probabilistic_effects), 2):
            prob = probabilistic_effects[i]
            this_effects = probabilistic_effects[i + 1]
            this_add_effects = []
            this_del_effects = []
            self.split_predicates(this_effects, this_add_effects, this_del_effects, action_name, ' effects')

            add_effects.append((prob, this_add_effects))
            del_effects.append((prob, this_del_effects))
        
        return add_effects, del_effects


    def parse_action_effects(self, effects, action_name):
        """Parses the effects of an action.

        The base parser is used in deterministic problems, and therefore all
        actions are assumed to have only one possible outcome with add and del
        effects
        """
        add_effects = []
        del_effects = []

        if effects[0] == 'probabilistic':
            prob_effects = effects[1:]
            add_effects, del_effects = self.parse_probabilistic_effect(prob_effects, action_name)
            """
            for i in range(0, len(prob_effects), 2):
                prob = prob_effects[i]
                this_effects = prob_effects[i + 1]
                this_add_effects = []
                this_del_effects = []
                self.split_predicates(this_effects, this_add_effects, this_del_effects, action_name, ' effects')

                add_effects.append((prob, this_add_effects))
                del_effects.append((prob, this_del_effects))
            """
        else:
            # When the action is deterministic, we hardset its probability of happening to 100%
            self.split_predicates(effects, add_effects, del_effects, action_name, ' effects')
            add_effects = [(1, add_effects)]
            del_effects = [(1, del_effects)]
        
        return add_effects, del_effects


if __name__ == '__main__':
    import sys, pprint
    domain = sys.argv[1]
    problem = sys.argv[2]
    parser = ProbabilisticParser()
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
