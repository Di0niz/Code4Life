# -*- coding: utf-8 -*-
import unittest
import sys
import StringIO
from app import Sample, Module, Molecule, World, Strategy
import itertools
import random


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
        av = s.target.find_availables(s.target.diagnosed)
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

        self.assertEqual(len(s.target.availables), 0)
        self.assertEqual(len(s.target.potentials), 0)
        self.assertEqual(len(s.target.unavailables), 3)


        #command = s.get_action()
        #self.assertEqual(command[0], 'DIAGNOSIS')

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

        self.assertEqual(len(s.target.availables), 0)
        self.assertEqual(len(s.target.potentials), 2)

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

        self.assertEqual(s.target.find_min_distance(s.target.diagnosed).sample_id, 8)


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

    def test_compare_samples(self):
        """Операции с рецептами"""
        l = []
        l.append(Molecule(1,2,3,4,5))
        l.append(Molecule(1,3,3,4,5))
        l.append(Molecule(1,3,3,4,2))

        self.assertEqual(Molecule(1,3,3,4,5) in l, True)


    def test_get_reserved(self):
        """Если нам не хватает молекул, тогда расчитываем потребность"""
        sys.stdin = StringIO.StringIO("""0  
        MOLECULES 0 0 1 1 0 3 1 0 0 0 0 0
        MOLECULES 0 0 1 0 1 2 2 0 0 0 0 0
        1 4 4 0 0
        6
        0 0 1 D 1 1 1 1 0 1
        2 0 1 D 1 1 0 0 1 3
        4 0 1 C 1 0 0 0 3 0
        1 1 1 B 1 1 0 1 1 1
        3 1 1 C 1 0 2 0 2 0
        5 1 1 B 1 1 0 0 0 2""")
        
        w = World()
        s = Strategy(w)
        w.update()
        s.update()

        self.assertEqual( s.find_reserve_molecule() in ['B','C','D'], False)


    def test_molecule_cmp(self):
        
        sys.stdin = StringIO.StringIO("""0  
        SAMPLES 0 0 0 0 0 0 0 0 0 0 0 0
        SAMPLES 0 0 0 0 0 0 0 0 0 0 0 0
        5 5 5 5 5
        2
        0 0 1 0 -1 -1 -1 -1 -1 -1
        1 1 1 0 -1 -1 -1 -1 -1 -1""")
        
        w = World()
        s = Strategy(w)
        w.update()
        s.update()

        #print w.match_gain(3, Molecule(7,0,0,0,0),2)

    def test_reserved_result(self):
        """Определяем список молекул которые надо захвтить"""
        sys.stdin = StringIO.StringIO("""0          
        MOLECULES 0 148 2 0 0 0 0 2 3 3 2 7
        MOLECULES 0 159 2 4 1 0 0 4 3 2 3 3
        1 1 4 5 5
        6
        35 0 2 E 10 3 0 3 0 2
        36 0 2 D 10 0 3 0 2 3
        37 0 2 C 20 4 2 0 0 1
        32 1 2 D 20 5 0 0 0 0
        33 1 3 C 40 0 7 0 0 0
        34 1 3 B 40 7 0 0 0 0
        """)

        w = World()
        s = Strategy(w)
        w.update()
        s.update()

        print "ENEMY:"
        print s.enemy.samples
        print s.enemy.availables
        print s.enemy.potentials
        print s.enemy.unavailables


        # расчитываем будующую и текущую экспертизу
        storage, expertise = s.enemy.future(s.enemy.samples)
        need = Molecule(0,0,0,0,0).submodule(storage)

        print need.max(),need.max_letter()
        print need
        print storage, "-" ,expertise

        print s.enemy.potentials


if __name__ == '__main__':
    unittest.main()
