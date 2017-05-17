# -*- coding: utf-8 -*-
import unittest
import sys
import StringIO
from app import Sample, Module, World, Strategy
import itertools


class TestStringMethods(unittest.TestCase):
    def test1_potential(self):
        """Проверяем вычисление потенциальных точек"""

        sys.stdin = StringIO.StringIO('0')

        w = World()

        sys.stdin = StringIO.StringIO("""LABORATORY 2 12 2 3 2 1 2 1 0 1 0 1
MOLECULES 2 4 0 0 0 2 0 0 0 1 2 1
3 2 3 2 3
6
8 0 1 A 1 0 1 2 1 1
9 0 1 A 1 0 2 0 0 2
10 0 1 D 10 4 0 0 0 0
6 1 1 E 1 2 2 0 1 0
11 1 1 B 1 1 0 0 0 2
12 1 1 E 1 1 1 1 1 0

        """)

        w.update()

        s = Strategy(w)


        command = s.get_action()

    pass

    def test1_find_order(self):

        sys.stdin = StringIO.StringIO('0')

        w = World()

        # sys.stdin = StringIO.StringIO("""LABORATORY 2 12 2 3 2 1 2 1 0 1 0 1
        # MOLECULES 2 4 0 0 0 2 0 0 0 1 2 1
        # 3 2 3 2 3
        # 4
        # 8 0 1 A 1 0 1 2 1 1
        # 9 0 1 A 1 0 2 0 0 2
        # 10 0 1 D 10 4 0 0 0 0
        # 6 1 1 E 1 2 2 0 1 0
        # 11 1 1 B 1 1 0 0 0 2
        # 12 1 1 E 1 1 1 1 1 0
        # """)
        sys.stdin = StringIO.StringIO("""LABORATORY 0 0 3 1 2 3 0 0 0 0 0 0
        LABORATORY 0 0 2 2 3 2 0 0 0 0 0 0
        0 2 0 0 5
        6
        0 0 1 C 1 0 0 0 3 0
        2 0 1 A 10 0 0 4 0 0
        4 0 1 E 1 2 0 2 0 0
        1 1 1 E 1 0 0 3 0 0
        3 1 1 C 1 2 1 0 0 0
        5 1 1 D 1 0 2 1 0 0""")

        w.update()
        
        s = Strategy(w)

        strong_solution = None
        weak_solution = None

        results = []
        for available in s.availables:

            # перебираем доступные комбинации
            for combination in itertools.permutations([x for x in s.diagnosed if x != available]):

                storage = s.target.storage
                expertise = s.target.expertise

                cost = available.cost.submodule(expertise)
                storage = storage.sub(cost)
                expertise = expertise.add(available.gain)

                step = 0
                results.append((step, storage.sum(), available))

                for sample in combination:

                    cost = sample.cost.submodule(expertise)
                    storage = storage.sub(cost)
                    expertise = expertise.add(sample.gain)


                    if storage.min() < 0:
                        break

                    step = step + 1
                    results.append((step, storage.sum(), available))


        sample = sorted(results, key=lambda x: (x[0],x[1])).pop()
        print sample

        print s.availables
        print s.potentials
        print s.diagnosed


        command = s.get_action()
        print command


    def test_choose_molecule(self):
        sys.stdin = StringIO.StringIO('0')

        w = World()


        sys.stdin = StringIO.StringIO("""MOLECULES 1 24 0 0 1 0 0 3 0 1 1 1
        DIAGNOSIS 2 6 0 1 0 2 0 0 1 1 2 2
        5 4 4 3 5
        6
        13 0 2 B 20 2 0 0 1 4
        14 0 2 A 20 0 0 1 4 2
        15 0 2 A 20 0 0 0 5 0
        6 1 1 E 1 2 2 0 1 0
        16 1 2 0 -1 -1 -1 -1 -1 -1
        17 1 2 0 -1 -1 -1 -1 -1 -1

        """)
        w.update()
        
        s = Strategy(w)

        print s.availables
        print s.potentials
        results = []
        for sample in s.diagnosed:
            cost = sample.cost.submodule(s.target.expertise)
            results.append((cost.sum(), cost.max_letter()))
        print sorted(results, key=lambda x: x[0])[:1]


if __name__ == '__main__':
    unittest.main()
