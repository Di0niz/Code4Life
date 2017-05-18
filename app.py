# -*- coding: utf-8 -*-
import sys
import random
import math
import itertools

DEBUG = False

class Molecule(object):
    def __init__(self, a=0, b=0, c=0, d=0, e=0):
        self.a, self.b, self.c, self.d, self.e = a, b, c, d, e
    
    def add(self, other):
        return Molecule(self.a + other.a, self.b + other.b, self.c + other.c, self.d + other.d, self.e + other.e)
    
    def sub(self, other):
        return Molecule(self.a - other.a, self.b - other.b, self.c - other.c, self.d - other.d, self.e - other.e)

    def submodule(self, other):
        a = max(self.a - other.a, 0)
        b = max(self.b - other.b, 0)
        c = max(self.c - other.c, 0)
        d = max(self.d - other.d, 0)
        e = max(self.e - other.e, 0)
        return Molecule(a, b, c, d, e)

    def min(self):
        return min([self.a,self.b,self.c,self.d,self.e])
        
    def max(self):
        return max([self.a,self.b,self.c,self.d,self.e])
        
    def sum(self):
        return sum([self.a,self.b,self.c,self.d,self.e])

    def diffrent(self):
        return sum([
            1 if self.a != 0 else 0,
            1 if self.b != 0 else 0,
            1 if self.c != 0 else 0,
            1 if self.d != 0 else 0,
            1 if self.e != 0 else 0]
            )
    def abs(self):
        return sum([
            self.a if self.a > 0 else -self.a,
            self.b if self.b > 0 else -self.b,
            self.c if self.c > 0 else -self.c,
            self.d if self.d > 0 else -self.d,
            self.e if self.e > 0 else -self.e]
            )

    def complexity(self):
        diff = max(self.diffrent(),1)
        return self.sum()/diff

    def diagnosed(self):
        return not (self.a == -1 or self.b == -1 or self.c == -1 or self.d == -1 or self.e == -1)
    
    def __repr__(self):
        return "%d %d %d %d %d" % (self.a,self.b,self.c,self.d,self.e)
    
    def letter(self, base=1):
        char = None
        if self.a == base:
            char = 'A'
        elif self.b == base:
            char = 'B'
        elif self.c == base:
            char = 'C'
        elif self.d == base:
            char = 'D'
        elif self.e == base:
            char = 'E'
        return char

    def first_letter(self):
        return self.letter(self.max())
    
    def min_letter(self):
        return self.letter(self.min())

    def max_letter(self):
        return self.letter(self.max())


    @staticmethod
    def parse(char):
        ret = None
        if char == 'A':
            ret = Molecule(1,0,0,0,0)
        elif char == 'B':
            ret = Molecule(0,1,0,0,0)
        elif char == 'C':
            ret = Molecule(0,0,1,0,0)
        elif char == 'D':
            ret = Molecule(0,0,0,1)
        elif char == 'E':
            ret = Molecule(0,0,0,0,1)
        return ret


class ModuleType(object):
    DIAGNOSIS, MOLECULES, LABORATORY, SAMPLES = "DIAGNOSIS", "MOLECULES", "LABORATORY", "SAMPLES"

class Module(object):

    def __init__(self):
        pass

    def update(self):
        raw = raw_input()
        if DEBUG:
            print >> sys.stderr, raw

        target, eta, score, storage_a, storage_b, storage_c, storage_d, storage_e, expertise_a, expertise_b, expertise_c, expertise_d, expertise_e = raw.split()
        self.target = target
        self.eta = int(eta)
        self.score = int(score)

        self.storage = Molecule(int(storage_a), int(storage_b), int(storage_c), int(storage_d), int(storage_e))
        self.expertise = Molecule(int(expertise_a), int(expertise_b), int(expertise_c), int(expertise_d), int(expertise_e))

        self.count_molecules = self.storage.sum()

        self.expected_molecules = self.expertise.sum()


    def find_molecules(self, samples):
        """Определение количества требуемых"""
        storage = self.storage
        results = []
        for sample in samples:
            cost = sample.cost.submodule(self.expertise)
            storage = storage.sub(cost)

        return storage.min_letter()


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


    def find_potentials(self, samples, world):
        """Определение количества требуемых"""

        results = []
        for combination in itertools.permutations(samples):
            expertise = self.expertise
            storage = self.storage.add(world.available)
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

    def find_min_distance(self, samples, limit=0):
        result = None
        min_cost = limit
        for sample in samples:
            cost = sample.cost.submodule(self.storage).submodule(self.expertise)
            cost_sum = cost.sum()

            if cost_sum > min_cost:
                min_cost = cost_sum
                result = sample
        return result



class Sample(object):

    def __init__(self):
        pass

    def update(self):
        raw = raw_input()
        if DEBUG:
            print >> sys.stderr, raw
        sample_id, carried_by, rank, expertise_gain, health, cost_a, cost_b, cost_c, cost_d, cost_e = raw.split()
        self.sample_id = int(sample_id)
        self.carried_by = int(carried_by)
        self.rank = int(rank)
        self.health = int(health)
        self.cost = Molecule(int(cost_a),int(cost_b),int(cost_c),int(cost_d),int(cost_e))
        self.gain = Molecule.parse(expertise_gain)

        self.diagnosed = self.cost.diagnosed()

        if self.diagnosed:
            self.complexity = self.cost.complexity()
        else: 
            self.complexity = 999

    def __repr__(self):
        return "%2d-%d: %s" % (self.sample_id,self.rank, self.cost)

class World(object):
    def __init__(self):
        project_count = int(raw_input())
        self.projects = []
        for i in xrange(project_count):
            raw = raw_input()
            if DEBUG:
                print >> sys.stderr, raw

            self.projects.append([int(j) for j in raw.split()])

    def update(self):
        self.modules = []
        for i in xrange(2):
            module = Module()
            module.update()
            self.modules.append(module)
        raw = raw_input()
        if DEBUG:
            print >> sys.stderr, raw
        a,b,c,d,e = [int(i) for i in raw.split()]
        self.available = Molecule(a,b,c,d,e)


        self.own_samples = []
        self.samples = []
        self.enemy_samples = []
        self.clound_samples = []
        sample_count = int(raw_input())
        for i in xrange(sample_count):
            sample = Sample()
            sample.update()
            if sample.carried_by == 1:
                self.enemy_samples.append(sample)
                
            elif sample.carried_by == 0:
                self.own_samples.append(sample)
            
            elif sample.carried_by == -1:
                self.clound_samples.append(sample)
            
            self.samples.append(sample)

class Commands(object):
    DIAGNOSIS = "DIAGNOSIS"
    WAIT = "WAIT"
    CONNECT = "CONNECT"
    MOLECULES = "MOLECULES"
    LABORATORY = "LABORATORY"
    SAMPLES = "SAMPLES"

def print_command(comm):

    ret = "WAIT"
    command, param, comment = comm
    if command == Commands.DIAGNOSIS:
        ret = "GOTO DIAGNOSIS"
    elif command == Commands.CONNECT and param is not None: 
        ret = "CONNECT %s" % param
    elif command == Commands.MOLECULES:
        ret = "GOTO MOLECULES"
    elif command == Commands.LABORATORY:
        ret = "GOTO LABORATORY"
    elif command == Commands.SAMPLES:
        ret = "GOTO SAMPLES"

    if comment is None:
        print ret
    else:
        print ret + ' ' + comment


class Actions(object):
    DIAGNOSIS = "DIAGNOSIS"
    DIAGNOSIS_CONNECT = "DIAGNOSIS_CONNECT"
    DIAGNOSIS_TO_MOLECULES = "DIAGNOSIS_TO_MOLECULES"
    DIAGNOSIS_TO_CLOUD = "DIAGNOSIS_TO_CLOUD"
    DIAGNOSIS_FROM_CLOUD = "DIAGNOSIS_FROM_CLOUD"
    DIAGNOSIS_TO_SAMPLE = "DIAGNOSIS_TO_SAMPLE"

    SAMPLES = "SAMPLES"
    SAMPLES_CONNECT = "SAMPLES_CONNECT"
    SAMPLES_TO_DIAGNOSIS = "SAMPLES_TO_DIAGNOSIS"


    LABORATORY = "LABORATORY"
    LABORATORY_CONNECT = "LABORATORY_CONNECT"
    LABORATORY_TO_DIAGNOSIS = "LABORATORY_TO_DIAGNOSIS"
    LABORATORY_TO_SAMPLES = "LABORATORY_TO_SAMPLES"
    LABORATORY_TO_MOLECULES = "LABORATORY_TO_MOLECULES"

    MOLECULES = "MOLECULES"
    MOLECULES_CONNECT = "MOLECULES_CONNECT"
    MOLECULES_GREED = "MOLECULES_GREED"
    MOLECULES_TO_LABORATORY = "MOLECULES_TO_LABORATORY"
    MOLECULES_TO_DIAGNOSIS = "MOLECULES_TO_DIAGNOSIS"


class Strategy(object):

    def __init__(self, world):
        self.world = world

        # признак определяет, что необходимо сбросить дорогие молекулы
        self.flush_high_cost = False

    def update(self):
        self.diagnosed = []
        self.undiagnosed = []
        self.availables = []
        self.potentials = []

        # Определяем примеры которые необходимо проверить
        for sample in self.world.own_samples:
            if sample.diagnosed:
                self.diagnosed.append(sample)
            else:
                self.undiagnosed.append(sample)

        self.target = self.world.modules[0]
        self.enemy = self.world.modules[1]

        all_potentials = self.target.find_potentials(self.diagnosed, self.world)
        self.availables = self.target.find_availables(self.diagnosed)

        self.potentials = [x for x in all_potentials if x not in self.availables]

    def greed_molecule(self):
        molecule = None

        order_keys = sorted(self.world.available,key=self.world.available.get)

        for key in order_keys:
            if self.world.available[key] > 0 and self.world.available[key] < self.target.molecules:
                molecule = key
                break

        return molecule

    def next_sample(self):
        results = []
        for available in self.availables:

            # перебираем доступные комбинации
            for combination in itertools.permutations([x for x in self.diagnosed if x != available]):

                storage = self.target.storage
                expertise = self.target.expertise

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

        return sample[2]
        

    def get_action(self):

        command = None
        action = None

        cur_module = self.world.modules[0]

        if cur_module.target == "START_POS":
            if len(self.world.samples) > 0:
                command = (Commands.DIAGNOSIS, None, action)
            else:
                command = (Commands.SAMPLES, None, action)
        elif cur_module.target == ModuleType.DIAGNOSIS:
            action = Actions.DIAGNOSIS
        elif cur_module.target == ModuleType.MOLECULES:
            action = Actions.MOLECULES
        elif cur_module.target == ModuleType.LABORATORY:
            action = Actions.LABORATORY
        elif cur_module.target == ModuleType.SAMPLES:
            action = Actions.SAMPLES

        while command is None:
            #
            # SAMPLES
            #
            if action == Actions.SAMPLES:
                if len(self.world.own_samples) < 3:
                    action = Actions.SAMPLES_CONNECT
                else:
                    action = Actions.SAMPLES_TO_DIAGNOSIS
                    
            elif action == Actions.SAMPLES_CONNECT:
                # здесь необходимо делать выборку в соответствии с рангом

                if self.target.expertise.complexity() > 2:
                    command = (Commands.CONNECT, 3, action)
                elif self.target.expertise.max() > 2:
                    command = (Commands.CONNECT, 2, action)
                else:
                    command = (Commands.CONNECT, 1, action)

            elif action == Actions.SAMPLES_TO_DIAGNOSIS:
                command = (Commands.DIAGNOSIS, None, action)

            #
            # DIAGNOSIS
            #
            elif action == Actions.DIAGNOSIS:
                if len(self.undiagnosed):
                    action = Actions.DIAGNOSIS_CONNECT
                elif self.flush_high_cost == True:
                    action = Actions.DIAGNOSIS_TO_CLOUD
                elif len(self.potentials) == 0 and len(self.availables) == 0 and len(self.diagnosed) == 3:
                    self.flush_high_cost = True
                elif len(self.world.own_samples) < 2:
                    action = Actions.DIAGNOSIS_TO_SAMPLE
                else:
                    action = Actions.DIAGNOSIS_TO_MOLECULES

            elif action == Actions.DIAGNOSIS_CONNECT:
                command = (Commands.CONNECT, self.undiagnosed.pop().sample_id, action)

            elif action == Actions.DIAGNOSIS_TO_MOLECULES:
                command = (Commands.MOLECULES, None, action)
            elif action == Actions.DIAGNOSIS_TO_CLOUD:
                
                max_sample = self.target.find_min_distance(self.diagnosed, 2)
                if max_sample is not None:
                    command = (Commands.CONNECT, max_sample.sample_id, action)
                else:
                    self.flush_high_cost = False
                    action = Actions.DIAGNOSIS
            elif action == Actions.DIAGNOSIS_FROM_CLOUD:
                
                pass
                #command = (Commands.MOLECULES, None, action)
            elif action == Actions.DIAGNOSIS_TO_SAMPLE:
                command = (Commands.SAMPLES, None, action)

            #
            # MOLECULES
            #
            elif action == Actions.MOLECULES:
                if self.target.count_molecules < 10 and len(self.potentials) > 0:
                    action = Actions.MOLECULES_CONNECT
                #elif self.target.molecules < 10:
                #    action = Actions.MOLECULES_GREED
                elif len(self.potentials) == 0 and len(self.availables) == 0 and len(self.diagnosed) > 0:
                    action = Actions.MOLECULES_TO_DIAGNOSIS
                else:
                    action = Actions.MOLECULES_TO_LABORATORY
            elif action == Actions.MOLECULES_CONNECT:
                molecules = self.target.find_molecules(self.potentials)

                if self.target.count_molecules < 10 and molecules is not None:
                    command = (Commands.CONNECT, molecules, action)
                #elif self.target.molecules < 10:
                #    action = Actions.MOLECULES_GREED
                else:
                    action = Actions.MOLECULES_TO_LABORATORY

            elif action == Actions.MOLECULES_GREED:
                free_molecules = self.greed_molecule()

                if free_molecules is not None:
                    command = (Commands.CONNECT, free_molecules, action)
                else:
                    action = Actions.MOLECULES_TO_LABORATORY

            elif action == Actions.MOLECULES_TO_LABORATORY:
                command = (Commands.LABORATORY, None, action)

            elif action == Actions.MOLECULES_TO_DIAGNOSIS:
                command = (Commands.DIAGNOSIS, None, action)

            #
            # LABORATORY
            #
            elif action == Actions.LABORATORY:
                if len(self.availables) > 0:
                    action = Actions.LABORATORY_CONNECT
                elif len(self.potentials) > 0:
                    action = Actions.LABORATORY_TO_MOLECULES
                elif len(self.undiagnosed) > 0:
                    action = Actions.LABORATORY_TO_DIAGNOSIS
                else:
                    action = Actions.LABORATORY_TO_SAMPLES

            elif action == Actions.LABORATORY_TO_DIAGNOSIS:
                command = (Commands.DIAGNOSIS, None, action)
            elif action == Actions.LABORATORY_TO_MOLECULES:
                command = (Commands.MOLECULES, None, action)
            elif action == Actions.LABORATORY_TO_SAMPLES:
                command = (Commands.SAMPLES, None, action)
            elif action == Actions.LABORATORY_CONNECT:
                command = (Commands.CONNECT, self.next_sample().sample_id, action)

            else:
                # Дорабатываем систему
                Command = (Commands.WAIT, None, action)
            if DEBUG:
                print >>sys.stderr, "DISITION: ", action, command

        return command



if __name__ == '__main__':

    DEBUG = True
    WORLD = World()

    STRATEGY = Strategy(WORLD)

    while True:

        WORLD.update()
        STRATEGY.update()


        command = STRATEGY.get_action()

        print_command(command)
