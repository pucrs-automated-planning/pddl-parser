#!/usr/bin/env python
# Four spaces as indentation [no tabs]

import itertools


class Action:
    def __init__(self, name, parameters, positive_preconditions, negative_preconditions, add_effects, del_effects):
        self.name = name
        self.parameters = tuple(parameters)
        self.positive_preconditions = frozenset((tuple(expr) for expr in positive_preconditions))
        self.negative_preconditions = frozenset((tuple(expr) for expr in negative_preconditions))
        self.add_effects = frozenset((tuple(expr) for expr in add_effects))
        self.del_effects = frozenset((tuple(expr) for expr in del_effects))

    def __repr__(self):
        return 'action: ' + self.name + \
               '\n  parameters: ' + str(list(self.parameters)) + \
               '\n  positive_preconditions: ' + str(list(self.positive_preconditions)) + \
               '\n  negative_preconditions: ' + str(list(self.negative_preconditions)) + \
               '\n  add_effects: ' + str(list(self.add_effects)) + \
               '\n  del_effects: ' + str(list(self.del_effects)) + '\n'

    def __str__(self):
        out = f'{self.name}('
        params = list(self.parameters)
        for p in params[:-1]:
            out += f'{p}, '
        if params:
            out += f'{params[-1]})'
        else:
            out += ')'
        return out

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def groundify(self, objects, types):
        if not self.parameters:
            yield self
            return
        type_map = []
        variables = []
        for var, typ in self.parameters:
            type_stack = [typ]
            items = []
            while type_stack:
                t = type_stack.pop()
                if objects.get(t):
                    items.extend(objects[t])
                elif types.get(t):
                    type_stack.extend(types[t])
                else:
                   raise Exception(f'Unrecognized type {t}')
            type_map.append(items)
            variables.append(var)
        for assignment in itertools.product(*type_map):
            positive_preconditions = self.replace(self.positive_preconditions, variables, assignment)
            negative_preconditions = self.replace(self.negative_preconditions, variables, assignment)
            add_effects = self.replace(self.add_effects, variables, assignment)
            del_effects = self.replace(self.del_effects, variables, assignment)
            yield Action(self.name, assignment, positive_preconditions, negative_preconditions, add_effects, del_effects)

    def replace(self, group, variables, assignment):
        g = []
        for pred in group:
            pred = list(pred)
            iv = 0
            for v in variables:
                while v in pred:
                    pred[pred.index(v)] = assignment[iv]
                iv += 1
            g.append(pred)
        return g


if __name__ == '__main__':
    a = Action('move', [['?ag', 'agent'], ['?from', 'pos'], ['?to', 'pos']],
        [['at', '?ag', '?from'], ['adjacent', '?from', '?to']],
        [['at', '?ag', '?to']],
        [['at', '?ag', '?to']],
        [['at', '?ag', '?from']]
    )
    print(a)

    objects = {
        'agent': ['ana', 'bob'],
        'pos': ['p1', 'p2']
    }
    types = {}
    for act in a.groundify(objects, types):
        print(act)
