#!/usr/bin/env python
# Four spaces as indentation [no tabs]

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

import unittest
from pddl_parser.action import Action
from pddl_parser.PDDL import PDDL_Parser


class Test_PDDL(unittest.TestCase):

    # -----------------------------------------------
    # Test scan_tokens
    # -----------------------------------------------

    def test_scan_tokens_domain(self):
        parser = PDDL_Parser()
        self.assertEqual(parser.scan_tokens('examples/dinner/dinner.pddl'),
            ['define', ['domain', 'dinner'],
            [':requirements', ':strips'],
            [':predicates', ['clean'], ['dinner'], ['quiet'], ['present'], ['garbage']],
            [':action', 'cook',
              ':precondition', ['clean'],
              ':effect', ['dinner']],
            [':action', 'wrap',
              ':precondition', ['quiet'],
              ':effect', ['present']],
            [':action', 'carry',
              ':precondition', ['garbage'],
              ':effect', ['and', ['not', ['garbage']], ['not', ['clean']]]],
            [':action', 'dolly',
              ':precondition', ['garbage'],
              ':effect', ['and', ['not', ['garbage']], ['not', ['quiet']]]]]
        )

    def test_scan_tokens_problem(self):
        parser = PDDL_Parser()
        self.assertEqual(parser.scan_tokens('examples/dinner/pb1.pddl'),
            ['define', ['problem', 'pb1'],
            [':domain', 'dinner'],
            [':init', ['garbage'], ['clean'], ['quiet']],
            [':goal', ['and', ['dinner'], ['present'], ['not', ['garbage']]]]]
        )

    # -----------------------------------------------
    # Test parse domain
    # -----------------------------------------------

    def test_parse_domain(self):
        parser = PDDL_Parser()
        parser.parse_domain('examples/dinner/dinner.pddl')
        self.assertEqual(parser.domain_name, 'dinner')
        self.assertEqual(parser.requirements, [':strips'])
        self.assertEqual(parser.predicates, {'clean': {}, 'dinner': {}, 'quiet': {}, 'present': {}, 'garbage': {}})
        self.assertEqual(parser.types, {})
        self.assertEqual(parser.actions,
            [
                Action('cook', [], [['clean']], [], [['dinner']], []),
                Action('wrap', [], [['quiet']], [], [['present']], []),
                Action('carry', [], [['garbage']], [], [], [['garbage'], ['clean']]),
                Action('dolly', [], [['garbage']], [], [], [['garbage'], ['quiet']])
            ]
        )

    def test_parse_domain_with_custom_requirements(self):
        parser = PDDL_Parser()
        parser.parse_domain('examples/dinner/dinner.pddl', [':strips', ':custom'])
        parser = PDDL_Parser()
        self.assertRaises(Exception, parser.parse_domain, 'examples/dinner/dinner.pddl', [])

    # -----------------------------------------------
    # Test parse problem
    # -----------------------------------------------

    def test_parse_problem(self):
        def frozenset_of_tuples(data):
            return frozenset([tuple(t) for t in data])
        parser = PDDL_Parser()
        parser.parse_domain('examples/dinner/dinner.pddl')
        parser.parse_problem('examples/dinner/pb1.pddl')
        self.assertEqual(parser.problem_name, 'pb1')
        self.assertEqual(parser.objects, {})
        self.assertEqual(parser.state, frozenset_of_tuples([['garbage'], ['clean'], ['quiet']]))
        self.assertEqual(parser.positive_goals, frozenset_of_tuples([['dinner'], ['present']]))
        self.assertEqual(parser.negative_goals, frozenset_of_tuples([['garbage']]))

    # -----------------------------------------------
    # Test parse predicates
    # -----------------------------------------------

    def test_parse_predicates(self):
        parser = PDDL_Parser()
        parser.predicates = {}
        parser.parse_predicates([
            ['untyped_pred', '?v1', '?v2', '?v3'],
            ['typed_pred', '?v1', '-', 'type1', '?v2', '-', 'type1', '?v3', '-', 'object'],
            ['shared_type_pred', '?v1', '?v2', '-', 'type1', '?v3']
        ])
        self.assertEqual(parser.predicates, {
            'untyped_pred': {'?v1': 'object', '?v2': 'object', '?v3': 'object'},
            'typed_pred': {'?v1': 'type1', '?v2': 'type1', '?v3': 'object'},
            'shared_type_pred': {'?v1': 'type1', '?v2': 'type1', '?v3': 'object'}
        })

    #-----------------------------------------------
    # Test parse types
    #-----------------------------------------------

    def test_parse_undefined_types(self):
        parser = PDDL_Parser()
        parser.types = {}
        parser.parse_types(['location', 'pile', 'robot', 'crane', 'container'])
        self.assertEqual(parser.types, {'object': ['location', 'pile', 'robot', 'crane', 'container']})

    def test_parse_defined_types(self):
        parser = PDDL_Parser()
        parser.types = {}
        parser.parse_types([
            'place', 'locatable', 'level', '-', 'object',
            'depot', 'market', '-', 'place',
            'truck', 'goods', '-', 'locatable'
        ])
        self.assertEqual(parser.types, {
            'object': ['place', 'locatable', 'level'],
            'place': ['depot', 'market'],
            'locatable': ['truck', 'goods']
        })

    #-----------------------------------------------
    # Test objects
    #-----------------------------------------------

    def test_parse_objects(self):
        parser = PDDL_Parser()
        parser.types = {}
        parser.objects = {}
        parser.parse_types(['airplane', 'segment', 'direction', 'airplanetype', 'a'])
        parser.parse_objects([
            'b', '-', 'a',
            'a', '-', 'a',
            'north', 'south', '-', 'direction',
            'light', 'medium', 'heavy', '-', 'airplanetype',
            'element1', '-', 'object',
            'seg_pp_0_60', 'seg_ppdoor_0_40', '-', 'segment',
            'airplane_CFBEG', '-', 'airplane',
            'element2'
        ], 'test')
        self.assertEqual(parser.objects, {
            'a': ['b', 'a'],
            'object': ['element1', 'element2'],
            'direction': ['north', 'south'],
            'airplanetype': ['light', 'medium', 'heavy'],
            'segment': ['seg_pp_0_60', 'seg_ppdoor_0_40'],
            'airplane': ['airplane_CFBEG']
        })

    # -----------------------------------------------
    # Test split predicates
    # -----------------------------------------------

    def test_split_predicates(self):
        pos_pre = ['pre', 'a']
        neg_pre = ['not', ['pre', 'b']]
        conjunction = ['and', pos_pre, neg_pre]
        pos = []
        neg = []
        parser = PDDL_Parser()
        self.assertRaises(Exception, parser.split_predicates, 'a', pos, neg, 'test', 'error')
        parser.split_predicates([], pos, neg, 'test', 'empty')
        self.assertEqual(pos, [])
        self.assertEqual(neg, [])
        parser.split_predicates(pos_pre, pos, neg, 'test', 'positve atomic')
        self.assertEqual(pos, [pos_pre])
        self.assertEqual(neg, [])
        pos = []
        parser.split_predicates(neg_pre, pos, neg, 'test', 'negative atomic')
        self.assertEqual(pos, [])
        self.assertEqual(neg, [neg_pre[-1]])
        pos = []
        neg = []
        parser.split_predicates(conjunction, pos, neg, 'test', 'conjunction')
        self.assertEqual(pos, [pos_pre])
        self.assertEqual(neg, [neg_pre[-1]])


# -----------------------------------------------
# Main
# -----------------------------------------------
if __name__ == '__main__':
    unittest.main()
