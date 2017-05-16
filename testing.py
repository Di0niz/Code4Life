# -*- coding: utf-8 -*-
import unittest
import sys
import StringIO
from app import Sample, Module, World, Strategy


class TestStringMethods(unittest.TestCase):
    def test_potensial(self):
        """Проверяем вычисление потенциальных точек"""

        sys.stdin = StringIO.StringIO('0')

        w = World()

        sys.stdin = StringIO.StringIO("""MOLECULES 1 28 1 0 0 0 3 1 4 0 3 2
        LABORATORY 1 94 2 2 4 0 0 2 1 1 3 1
        3 4 2 6 3
        3
        19 0 2 C 20 0 5 3 0 0
        20 0 2 D 20 1 4 2 0 0
        17 1 3 E 30 3 3 5 3 0
        """)

        w.update()

        s = Strategy(w)

        print s.availables
        print s.potentials

        command = s.get_action()
        print command



        


    pass

if __name__ == '__main__':
    unittest.main()
