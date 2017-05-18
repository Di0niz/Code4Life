# -*- coding: utf-8 -*-
import unittest
import sys
import StringIO
from app import Sample, Module, World, Strategy
import itertools


class TestStringMethods(unittest.TestCase):

    def test_optimal_availables(self):
        """Поиск оптимального количества рецептов требуемый для формирования выборки"""

        sys.stdin = StringIO.StringIO("""0
        MOLECULES 0 0 0 2 2 2 1 0 0 0 0 0
        MOLECULES 0 0 1 0 0 0 3 0 0 0 0 0
        4 3 4 4 2
        6
        0 0 1 E 1 0 0 1 3 1
        2 0 1 D 1 0 2 1 0 0
        4 0 1 E 1 1 2 1 1 0
        1 1 1 E 1 2 0 2 0 0
        3 1 1 B 1 0 0 0 0 3
        5 1 1 B 1 1 0 0 0 2""")   

        w = World()
        w.update()
        s = Strategy(w)
        s.update()
        av = s.target.find_availables(s.diagnosed)
        self.assertEqual(av[0].sample_id, 2)
        self.assertEqual(av[1].sample_id, 0)
        self.assertEqual(len(av), 2)
        
    def test_potential(self):
        """Проверяем количество потенциальных"""
    
        sys.stdin = StringIO.StringIO("""0
        MOLECULES 0 12 1 1 0 1 3 2 0 0 0 1
        LABORATORY 1 3 3 0 0 3 2 0 1 1 1 0
        1 4 5 1 0
        5
        8 0 2 D 30 0 0 0 6 0
        9 0 2 B 10 0 2 2 3 0
        10 0 2 D 20 3 0 0 0 5
        3 1 1 A 1 3 1 0 0 1
        6 1 1 D 1 2 0 0 2 0""")   

        w = World()
        s = Strategy(w)
        w.update()
        s.update()

        self.assertEqual(len(s.availables), 0)
        self.assertEqual(len(s.potentials), 0)


        command = s.get_action()
        self.assertEqual(command[0], 'DIAGNOSIS')

        sys.stdin = StringIO.StringIO("""0
        MOLECULES 0 0 0 1 0 0 0 0 0 0 0 0
        MOLECULES 0 0 0 0 0 0 1 0 0 0 0 0
        5 4 5 5 4
        6
        0 0 1 E 10 0 4 0 0 0
        2 0 1 A 1 0 2 2 0 1
        4 0 1 A 1 0 1 1 1 1
        1 1 1 B 1 1 0 0 0 2
        3 1 1 A 1 3 1 0 0 1
        5 1 1 C 1 0 0 0 3 0
        """)   

        w = World()
        s = Strategy(w)
        w.update()
        s.update()

        self.assertEqual(len(s.availables), 0)
        self.assertEqual(len(s.potentials), 2)

    def test_min_distance(self):
        """Расчитываем минимальное расстояние между молекулами"""
    
        sys.stdin = StringIO.StringIO("""0
        DIAGNOSIS 0 12 1 1 0 1 3 2 0 0 0 1
        LABORATORY 1 3 3 0 0 3 2 0 1 1 1 0
        1 4 5 1 0
        5
        8 0 2 D 30 0 0 0 6 0
        9 0 2 B 10 0 2 2 3 0
        10 0 2 D 20 3 0 0 0 5
        3 1 1 A 1 3 1 0 0 1
        6 1 1 D 1 2 0 0 2 0
        """)   

        w = World()
        s = Strategy(w)
        w.update()
        s.update()

        self.assertEqual(s.target.find_min_distance(s.diagnosed).sample_id, 8)


    def test_invalid_connect(self):
        """Система расчитывала не верные буквы"""


        sys.stdin = StringIO.StringIO("""0  
        MOLECULES 0 0 0 1 2 2 1 0 0 0 0 0
        MOLECULES 0 0 0 2 0 0 4 0 0 0 0 0
        5 2 3 3 0
        6
        1 0 1 E 1 0 0 2 1 0
        3 0 1 A 1 0 1 2 1 1
        5 0 1 C 1 0 1 0 2 2
        0 1 2 D 10 0 3 0 2 3
        2 1 2 E 20 0 0 0 0 5
        4 1 2 C 10 3 0 2 3 0""")

        w = World()
        s = Strategy(w)
        w.update()
        s.update()
        self.assertEqual(s.calc_letter_molecule(), 'D')
        sys.stdin = StringIO.StringIO("""0  
        MOLECULES 0 46 0 5 0 1 0 2 1 2 3 0
        MOLECULES 0 15 0 0 4 0 0 2 1 1 2 0
        5 0 1 4 5
        6
        12 0 2 B 20 0 2 3 0 3
        16 0 2 B 20 0 5 0 0 0
        18 0 2 D 20 1 4 2 0 0
        15 1 2 E 20 0 0 5 3 0
        17 1 2 C 20 0 5 3 0 0
        19 1 2 E 10 3 2 2 0 0""")
        w = World()
        s = Strategy(w)
        w.update()
        s.update()


        self.assertNotEqual(s.calc_letter_molecule(), 'B')



if __name__ == '__main__':
    unittest.main()
