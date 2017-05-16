# -*- coding: utf-8 -*-
import unittest
import sys
import StringIO
from app import Sample, Module, World, Strategy


class TestStringMethods(unittest.TestCase):
    def test_potential(self):
        """Проверяем вычисление потенциальных точек"""

        sys.stdin = StringIO.StringIO('0')

        w = World()

        sys.stdin = StringIO.StringIO("""DIAGNOSIS 0 0 0 0 0 0 0 0 0 0 0 0
        MOLECULES 0 0 0 1 0 0 0 0 0 0 0 0
        6 5 6 6 6
        4
        1 0 2 D 30 0 0 0 6 0
        2 0 2 E 20 0 0 5 3 0
        3 0 2 D 10 0 3 0 2 3
        0 1 2 E 20 0 1 4 2 0
        """)

        w.update()

        s = Strategy(w)

        print s.availables
        print s.potentials
        print s.diagnosed

        command = s.get_action()
        print command

    pass

if __name__ == '__main__':
    unittest.main()
