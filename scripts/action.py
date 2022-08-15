#!/usr/bin/env python3

from pddl_parser.action import Action

# -----------------------------------------------
# Main
# -----------------------------------------------
if __name__ == '__main__':
    a = Action('move', [['?ag', 'agent'], ['?from', 'pos'], ['?to', 'pos']],
                       [['at', '?ag', '?from'], ['adjacent', '?from', '?to']],
                       [['at', '?ag', '?to']],
                       [['at', '?ag', '?to']],
                       [['at', '?ag', '?from']])
    print(a)

    objects = {
        'agent': ['ana', 'bob'],
        'pos': ['p1', 'p2']
    }
    types = {'object': ['agent', 'pos']}
    for act in a.groundify(objects, types):
        print(act)
