# -*- coding: utf-8 -*-
import sys
import random
import math


class ModuleType(object):
    DIAGNOSIS, MOLECULES, LABORATORY, SAMPLES = "DIAGNOSIS", "MOLECULES", "LABORATORY", "SAMPLES"

class Module(object):

    def __init__(self):
        pass

    def update(self):
        raw = raw_input()
        print >> sys.stderr, raw

        target, eta, score, storage_a, storage_b, storage_c, storage_d, storage_e, expertise_a, expertise_b, expertise_c, expertise_d, expertise_e = raw.split()
        self.target = target
        self.eta = int(eta)
        self.score = int(score)
        self.storage = {}
        self.storage['a'] = int(storage_a)
        self.storage['b'] = int(storage_b)
        self.storage['c'] = int(storage_c)
        self.storage['d'] = int(storage_d)
        self.storage['e'] = int(storage_e)
        self.expertise = {}
        self.expertise['a'] = int(expertise_a)
        self.expertise['b'] = int(expertise_b)
        self.expertise['c'] = int(expertise_c)
        self.expertise['d'] = int(expertise_d)
        self.expertise['e'] = int(expertise_e)

        self.molecules = int(storage_a) + int(storage_b) + int(storage_c) + int(storage_d) + int(storage_e)

    def find_molecules(self, samples):
        """Определение количества требуемых"""
        molecules = {'a':0,'b':0,'c':0,'d':0,'e':0}
        # sum molecules
        for sample in samples:
            if sample.diagnosed:
                for key in sample.cost:
                    molecules[key] = molecules[key] + sample.cost[key]

        # div 
        for key in self.storage:
            molecules[key] = molecules[key] - self.storage[key]
            # вычитаем очки опыта
            molecules[key] = molecules[key] - self.expertise[key]

        res = {}
        for key in molecules:
            if molecules[key] > 0:
                res[key] = molecules[key]

        return res


    def find_availables(self, samples):
        """Определение количества требуемых"""

        availables = []

        molecules = {'a':0,'b':0,'c':0,'d':0,'e':0}
        for key in self.storage:
            molecules[key] = molecules[key] + self.storage[key] + self.expertise[key]

        # sum molecules
        for sample in samples:
            if sample.diagnosed:
                av_sample = True
                for key in sample.cost:
                    if molecules[key] - sample.cost[key] < 0:
                        av_sample = False

                if av_sample:

                    availables.append(sample)

                    for key in sample.cost:
                        molecules[key] = molecules[key] - sample.cost[key]

        return availables

class Sample(object):

    def __init__(self):
        pass

    def update(self):
        raw = raw_input()
        print >> sys.stderr, raw
        sample_id, carried_by, rank, expertise_gain, health, cost_a, cost_b, cost_c, cost_d, cost_e = raw.split()
        self.sample_id = int(sample_id)
        self.carried_by = int(carried_by)
        self.rank = int(rank)
        self.health = int(health)
        self.cost = {}
        self.cost['a'] = int(cost_a)
        self.cost['b'] = int(cost_b)
        self.cost['c'] = int(cost_c)
        self.cost['d'] = int(cost_d)
        self.cost['e'] = int(cost_e)

        self.diagnosed = (int(cost_a) != -1)


class World(object):
    def __init__(self):
        project_count = int(raw_input())
        for i in xrange(project_count):
            raw = raw_input()
            print >> sys.stderr, raw

            a, b, c, d, e = [int(j) for j in raw.split()]

    def update(self):
        self.modules = []
        for i in xrange(2):
            module = Module()
            module.update()
            self.modules.append(module)
        raw = raw_input()
        
        print >> sys.stderr, raw
        available_a, available_b, available_c, available_d, available_e = [int(i) for i in raw.split()]
        self.available ={}
        self.available['a'] = available_a
        self.available['b'] = available_b
        self.available['c'] = available_c
        self.available['d'] = available_d
        self.available['e'] = available_e


        self.own_samples = []
        self.samples = []
        self.enemy_samples = []
        sample_count = int(raw_input())
        for i in xrange(sample_count):
            sample = Sample()
            sample.update()
            if sample.carried_by == 1:
                self.enemy_samples.append(sample)
            elif sample.carried_by == 0:
                self.own_samples.append(sample)
            else:
                self.samples.append(sample)

    def check_available(self, molecules):
        available = True
        for key in molecules:
            if self.available[key] < molecules[key]:
                available = False

        return available


class Commands(object):
    DIAGNOSIS = "DIAGNOSIS"
    WAIT = "WAIT"
    CONNECT = "CONNECT"
    MOLECULES = "MOLECULES"
    LABORATORY = "LABORATORY"
    SAMPLES = "SAMPLES"

def print_command(comm):

    ret = "WAIT"
    command, param = comm
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
    print ret

class Actions(object):
    DIAGNOSIS = "DIAGNOSIS"
    DIAGNOSIS_CONNECT = "DIAGNOSIS_CONNECT"
    DIAGNOSIS_TO_MOLECULES = "DIAGNOSIS_TO_MOLECULES"

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


class Strategy(object):

    def __init__(self, world):
        self.world = world

        self.diagnosed = []
        self.undiagnosed = []
        self.availables = []

        # Определяем примеры которые необходимо проверить
        for sample in self.world.own_samples:
            if sample.diagnosed:
                self.diagnosed.append(sample)
            else:
                self.undiagnosed.append(sample)

        self.target = self.world.modules[0]

        self.availables = self.target.find_availables(self.diagnosed)

    def greed_molecule(self):
        molecule = None

        order_keys = sorted(self.world.available,key=self.world.available.get)

        for key in order_keys:
            if self.world.available[key] > 0 and self.world.available[key] < self.target.molecules:
                molecule = key
                break

        return molecule

    def get_action(self):

        command = None
        action = None

        cur_module = self.world.modules[0]

        if cur_module.target == "START_POS":
            if len(self.world.samples) > 0:
                command = (Commands.DIAGNOSIS, None)
            else:
                command = (Commands.SAMPLES, None)
        elif cur_module.target == ModuleType.DIAGNOSIS:
            action = Actions.DIAGNOSIS
        elif cur_module.target == ModuleType.MOLECULES:
            action = Actions.MOLECULES
        elif cur_module.target == ModuleType.LABORATORY:
            action = Actions.LABORATORY
        elif cur_module.target == ModuleType.SAMPLES:
            action = Actions.SAMPLES

        print >>sys.stderr, "START: ", action


        while command is None:

            if action == Actions.SAMPLES:
                if len(self.undiagnosed) < 3:
                    action = Actions.SAMPLES_CONNECT
                else:
                    action = Actions.SAMPLES_TO_DIAGNOSIS

            elif action == Actions.SAMPLES_CONNECT:
                command = (Commands.CONNECT, 1)

            elif action == Actions.SAMPLES_TO_DIAGNOSIS:
                command = (Commands.DIAGNOSIS, None)

            elif action == Actions.DIAGNOSIS:
                if len(self.undiagnosed):
                    action = Actions.DIAGNOSIS_CONNECT
                else:
                    action = Actions.DIAGNOSIS_TO_MOLECULES

            elif action == Actions.DIAGNOSIS_CONNECT:
                command = (Commands.CONNECT, self.undiagnosed.pop().sample_id)

            elif action == Actions.DIAGNOSIS_TO_MOLECULES:
                command = (Commands.MOLECULES, None)

            elif action == Actions.MOLECULES:
                molecules = self.target.find_molecules(self.diagnosed)

                if len(molecules.keys()) > 0:
                    action = Actions.MOLECULES_CONNECT
                #elif self.target.molecules < 10:
                #    action = Actions.MOLECULES_GREED
                else:
                    action = Actions.MOLECULES_TO_LABORATORY
            elif action == Actions.MOLECULES_CONNECT:
                molecules = self.target.find_molecules(self.diagnosed)

                if self.target.molecules < 10 and self.world.check_available(molecules):
                    command = (Commands.CONNECT, molecules.popitem()[0])
                else:
                    action = Actions.MOLECULES_TO_LABORATORY

            elif action == Actions.MOLECULES_GREED:
                free_molecules = self.greed_molecule()

                if free_molecules is not None:
                    command = (Commands.CONNECT, free_molecules)
                else:
                    action = Actions.MOLECULES_TO_LABORATORY

            elif action == Actions.MOLECULES_TO_LABORATORY:
                command = (Commands.LABORATORY, None)

            elif action == Actions.LABORATORY:
                if len(self.availables) > 0:
                    action = Actions.LABORATORY_CONNECT
                elif len(self.diagnosed) > 0:
                    action = Actions.LABORATORY_TO_MOLECULES
                elif len(self.undiagnosed) > 0:
                    action = Actions.LABORATORY_TO_DIAGNOSIS
                else:
                    action = Actions.LABORATORY_TO_SAMPLES

            elif action == Actions.LABORATORY_TO_DIAGNOSIS:
                command = (Commands.DIAGNOSIS, None)
            elif action == Actions.LABORATORY_TO_MOLECULES:
                command = (Commands.MOLECULES, None)
            elif action == Actions.LABORATORY_TO_SAMPLES:
                command = (Commands.SAMPLES, None)
            elif action == Actions.LABORATORY_CONNECT:
                command = (Commands.CONNECT, self.availables.pop().sample_id)

            else:
                # Дорабатываем систему
                Command = (Commands.WAIT, None)

            print >>sys.stderr, "DESITION: ", action, command

        return command


WORLD = World()

if __name__ == '__main__':
        
    while True:

        WORLD.update()

        STRATEGY = Strategy(WORLD)


        command = STRATEGY.get_action()


        print_command(command)
