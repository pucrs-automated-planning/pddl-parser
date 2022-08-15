#!/usr/bin/env python

import sys, pprint
from pddl_parser.PDDL import PDDL_Parser

# -----------------------------------------------
# Main
# -----------------------------------------------
if __name__ == '__main__':
    domain = sys.argv[1]
    problem = sys.argv[2]
    parser = PDDL_Parser()
    print('----------------------------')
    pprint.pprint(parser.scan_tokens(domain))
    print('----------------------------')
    pprint.pprint(parser.scan_tokens(problem))
    print('----------------------------')
    parser.parse_domain(domain)
    parser.parse_problem(problem)
    print('Domain name: ' + parser.domain_name)
    for act in parser.actions:
        print(act)
    print('----------------------------')
    print('Problem name: ' + parser.problem_name)
    print('Objects: ' + str(parser.objects))
    print('State: ' + str([list(i) for i in parser.state]))
    print('Positive goals: ' + str([list(i) for i in parser.positive_goals]))
    print('Negative goals: ' + str([list(i) for i in parser.negative_goals]))
