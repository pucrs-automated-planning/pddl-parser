# This file is part of PDDL Parser, available at <https://github.com/pucrs-automated-planning/pddl-parser>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import itertools


class Action:

    def __init__(self, name, parameters, positive_preconditions, negative_preconditions, prob_add_effects, prob_del_effects):
        def frozenset_of_tuples(data):
            return frozenset([tuple(t) for t in data])
        self.name = name
        self.parameters = tuple(parameters)  # Make parameters a tuple so we can hash this if need be
        self.positive_preconditions = frozenset_of_tuples(positive_preconditions)
        self.negative_preconditions = frozenset_of_tuples(negative_preconditions)

        self.effect_probabilities = []
        self.add_effects = []
        self.del_effects = []
        for i in range(len(prob_add_effects)):
            prob = prob_add_effects[i][0]
            this_add_effects = frozenset_of_tuples(prob_add_effects[i][1])
            this_del_effects = frozenset_of_tuples(prob_del_effects[i][1])
            self.effect_probabilities.append(prob)
            self.add_effects.append(this_add_effects)
            self.del_effects.append(this_del_effects)


    def __str__(self):
        return_str = 'action: ' + self.name + \
            '\n  parameters: ' + str(list(self.parameters)) + \
            '\n  positive_preconditions: ' + str([list(i) for i in self.positive_preconditions]) + \
            '\n  negative_preconditions: ' + str([list(i) for i in self.negative_preconditions]) + \
            '\n  effects:'
        for i, prob in enumerate(self.effect_probabilities):
            return_str += f'\n\t{prob}' + \
                f'\n\t  {str([list(eff) for eff in self.add_effects[i]])}' + \
                f'\n\t  {str([list(eff) for eff in self.del_effects[i]])}'
        return return_str + '\n'


    def __eq__(self, other):
        return self.__dict__ == other.__dict__


    def groundify(self, objects, types):
        if not self.parameters:
            yield self
            return
        type_map = []
        variables = []
        for var, type in self.parameters:
            type_stack = [type]
            items = []
            while type_stack:
                t = type_stack.pop()
                if t in objects:
                    items += objects[t]
                if t in types:
                    type_stack += types[t]
            type_map.append(items)
            variables.append(var)
        for assignment in itertools.product(*type_map):
            positive_preconditions = self.replace(self.positive_preconditions, variables, assignment)
            negative_preconditions = self.replace(self.negative_preconditions, variables, assignment)
            add_effects = self.replace_effects(self.add_effects, variables, assignment)
            del_effects = self.replace_effects(self.del_effects, variables, assignment)
            yield Action(self.name, assignment, positive_preconditions, negative_preconditions, add_effects, del_effects)


    def replace(self, group, variables, assignment):
        new_group = []
        for pred in group:
            pred = list(pred)
            for i, p in enumerate(pred):
                if p in variables:
                    pred[i] = assignment[variables.index(p)]
            new_group.append(pred)
        return new_group


    def replace_effects(self, effects, variables, assignment):
        new_effects = []
        for i, eff in enumerate(effects):
            prob = self.effect_probabilities[i]
            replaced_eff = self.replace(eff, variables, assignment)
            # Removes repetitions from replaced effects
            new_effects.append((prob, replaced_eff))
        return new_effects
    

    def get_related_predicates(self) -> set:
        all_predicates = []
        for pred in self.positive_preconditions:
            all_predicates.append(pred[0])
        for pred in self.negative_preconditions:
            all_predicates.append(pred[0])
        for prop_effect in self.add_effects:
            for pred in prop_effect:
                all_predicates.append(pred[0])
        for prop_effect in self.del_effects:
            for pred in prop_effect:
                all_predicates.append(pred[0])
        return set(all_predicates)



if __name__ == '__main__':
    a = Action('move', [['?ag', 'agent'], ['?from', 'pos'], ['?to', 'pos']],
                       [['at', '?ag', '?from'], ['adjacent', '?from', '?to']],
                       [['at', '?ag', '?to']],
                       [(1, [['at', '?ag', '?to']])],
                       [(1, [['at', '?ag', '?from']])])
    print(a)

    objects = {
        'agent': ['ana', 'bob'],
        'pos': ['p1', 'p2']
    }
    types = {'object': ['agent', 'pos']}
    for act in a.groundify(objects, types):
        print(act)
