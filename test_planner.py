# This file is part of IPPDDL Parser, available at <https://github.com/AndreMoukarzel/ippddl-parser/>.

import unittest
from ippddl_parser.action import Action
from ippddl_parser.deterministic_planner import DeterministicPlanner

class TestPlanner(unittest.TestCase):

    def test_solve_dinner(self):
        planner = DeterministicPlanner()
        self.assertEqual(planner.solve('examples/dinner/dinner.pddl', 'examples/dinner/pb1.pddl'),
            [
                Action('cook', [], [['clean']], [], [[['dinner']]], [[]], [1]),
                Action('wrap', [], [['quiet']], [], [[['present']]], [[]], [1]),
                Action('carry', [], [['garbage']], [], [[]], [[['garbage'], ['clean']]], [1])
            ]
        )


if __name__ == '__main__':
    unittest.main()
