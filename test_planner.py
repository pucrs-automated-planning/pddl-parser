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
from pddl_parser.planner import Planner

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


# -----------------------------------------------
# Main
# -----------------------------------------------
if __name__ == '__main__':
    unittest.main()
