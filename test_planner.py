# This file is part of IPPDDL Parser, available at <https://github.com/AndreMoukarzel/ippddl-parser/>.

import unittest
from ippddl_parser.action import Action
from ippddl_parser.planner import Planner

class Test_Planner(unittest.TestCase):

    def test_solve_dinner(self):
        planner = Planner()
        self.assertEqual(planner.solve('examples/dinner/dinner.pddl', 'examples/dinner/pb1.pddl'),
            [
                Action('cook', [], [['clean']], [], [(1, [['dinner']])], [(1, [])]),
                Action('wrap', [], [['quiet']], [], [(1, [['present']])], [(1, [])]),
                Action('carry', [], [['garbage']], [], [(1, [])], [(1, [['garbage'], ['clean']])])
            ]
        )


if __name__ == '__main__':
    unittest.main()
