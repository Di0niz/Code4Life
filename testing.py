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
        av = find_availables(s.target, s.diagnosed)
        self.assertEqual(av[0].sample_id, 2)
        self.assertEqual(av[1].sample_id, 0)
        
    def test_optimal_ways(self):
        """Поиск оптимального количества молекул требуемый для формирования выборки"""
    
        sys.stdin = StringIO.StringIO("""0
        MOLECULES 0 0 0 2 1 1 0 0 0 0 0 0
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

        for combination in itertools.permutations(s.diagnosed):

            storage = s.target.storage
            expetise = s.target.expertise

            priority = None

            for sample in combination:
                cost = sample.cost.sub(expetise)
                storage = storage.sub(cost)
                expetise = expetise.add(sample.gain)
         #       print " ", storage, 

         #    print storage, storage.min(), storage.diffrent(), storage.complexity(), storage.min_letter()

        storage = s.target.storage
        available = w.available
        for sample in w.enemy_samples:
            cost = sample.cost.submodule(expetise)
            available = available.sub(cost)


        expertise = s.target.expertise
        for sample in w.own_samples:
            cost = sample.cost.submodule(expetise)
            storage = storage.sub(cost)
        print storage,  s.target.storage
        find_min_molecule(s)


def find_min_molecule(self):
    print 'a'
        
def find_optimal_order(self, samples):
    pass

def find_availables(self, asamples):
    """Определение количества требуемых в соответствет"""

    results = []
    for combination in itertools.permutations(asamples):
        expertise = self.expertise
        storage = self.storage
        availables = []
        step = 0
        for sample in combination:
            cost = sample.cost.submodule(expertise)
            storage = storage.sub(cost)
            expertise = expertise.add(sample.gain)

            availables.append(sample)
            if storage.min() < 0:
                break

            step = step + 1
            results.append((step, storage.sum(), list(availables)))

    if len(results) > 0:
        all_availables = sorted(results, key=lambda x: (x[0],x[1])).pop()[2]
    else:
        all_availables = []

    return all_availables




        

if __name__ == '__main__':
    unittest.main()
