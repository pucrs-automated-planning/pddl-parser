# This file is part of IPPDDL Parser, available at <https://github.com/AndreMoukarzel/ippddl-parser/>.

import unittest
from ippddl_parser.action import Action
from ippddl_parser.parser import Parser


class TestParser(unittest.TestCase):

    def test_scan_tokens_domain(self):
        parser = Parser()
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
        parser = Parser()
        self.assertEqual(parser.scan_tokens('examples/dinner/pb1.pddl'),
            ['define', ['problem', 'pb1'],
            [':domain', 'dinner'],
            [':init', ['garbage'], ['clean'], ['quiet']],
            [':goal', ['and', ['dinner'], ['present'], ['not', ['garbage']]]]]
        )


    def test_parse_domain(self):
        parser = Parser()
        parser.parse_domain('examples/dinner/dinner.pddl')
        self.assertEqual(parser.domain_name, 'dinner')
        self.assertEqual(parser.requirements, [':strips'])
        self.assertEqual([pred.name for pred in parser.predicates], ['clean', 'dinner', 'quiet', 'present', 'garbage'])
        self.assertEqual(parser.types, {})
        self.assertEqual(parser.actions,
            [
                Action('cook', [], [['clean']], [], [[['dinner']]], [[]]),
                Action('wrap', [], [['quiet']], [], [[['present']]], [[]]),
                Action('carry', [], [['garbage']], [], [[]], [[['garbage'], ['clean']]]),
                Action('dolly', [], [['garbage']], [], [[]], [[['garbage'], ['quiet']]])
            ]
        )


    def test_parse_domain_with_custom_requirements(self):
        parser = Parser()
        parser.parse_domain('examples/dinner/dinner.pddl', [':strips', ':custom'])
        parser = Parser()
        self.assertRaises(Exception, parser.parse_domain, 'examples/dinner/dinner.pddl', [])


    def test_parse_problem(self):
        def frozenset_of_tuples(data):
            return frozenset([tuple(t) for t in data])
        parser = Parser()
        parser.parse_domain('examples/dinner/dinner.pddl')
        parser.parse_problem('examples/dinner/pb1.pddl')
        self.assertEqual(parser.problem_name, 'pb1')
        self.assertEqual(parser.objects, {})
        self.assertEqual(parser.state, frozenset_of_tuples([['garbage'], ['clean'], ['quiet']]))
        self.assertEqual(parser.positive_goals, frozenset_of_tuples([['dinner'], ['present']]))
        self.assertEqual(parser.negative_goals, frozenset_of_tuples([['garbage']]))


    def test_parse_undefined_types(self):
        parser = Parser()
        parser.types = {}
        parser.parse_types(['location', 'pile', 'robot', 'crane', 'container'])
        self.assertEqual(parser.types, {'object': ['location', 'pile', 'robot', 'crane', 'container']})

    def test_parse_defined_types(self):
        parser = Parser()
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


    def test_parse_objects(self):
        parser = Parser()
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


    def test_split_predicates(self):
        pos_pre = ['pre', 'a']
        neg_pre = ['not', ['pre', 'b']]
        conjunction = ['and', pos_pre, neg_pre]
        pos = []
        neg = []
        parser = Parser()
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



if __name__ == '__main__':
    unittest.main()
