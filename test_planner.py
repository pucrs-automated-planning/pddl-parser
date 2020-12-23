#!/usr/bin/env python
# Four spaces as indentation [no tabs]

import unittest
from action import Action
from planner import Planner

class Test_Planner(unittest.TestCase):

    #-----------------------------------------------
    # Test solve
    #-----------------------------------------------

    def test_solve_dinner(self):
        planner = Planner()
        self.assertEqual(planner.solve('examples/dinner/dinner.pddl', 'examples/dinner/pb1.pddl'),
            [
                Action('cook', [], [['clean']], [], [['dinner']], []),
                Action('wrap', [], [['quiet']], [], [['present']], []),
                Action('carry', [], [['garbage']], [], [], [['garbage'], ['clean']])
            ]
        )

#-----------------------------------------------
# Main
#-----------------------------------------------
if __name__ == '__main__':
    unittest.main()