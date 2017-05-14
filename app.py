# -*- coding: utf-8 -*-
import sys
import random
import math


class ModuleType(object):
    DIAGNOSIS, MOLECULES, LABORATORY = "DIAGNOSIS", "MOLECULES", "LABORATORY"
    
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
        self.storage_a = int(storage_a)
        self.storage_b = int(storage_b)
        self.storage_c = int(storage_c)
        self.storage_d = int(storage_d)
        self.storage_e = int(storage_e)
        self.expertise_a = int(expertise_a)
        self.expertise_b = int(expertise_b)
        self.expertise_c = int(expertise_c)
        self.expertise_d = int(expertise_d)
        self.expertise_e = int(expertise_e)

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
        self.cost_a = int(cost_a)
        self.cost_b = int(cost_b)
        self.cost_c = int(cost_c)
        self.cost_d = int(cost_d)
        self.cost_e = int(cost_e)


class World(object):
    def __init__(self):
        project_count = int(raw_input())
        for i in xrange(project_count):
            a, b, c, d, e = [int(j) for j in raw_input().split()]

    def update(self):
        self.modules = []
        for i in xrange(2):
            module = Module()
            module.update()
            self.modules.append(module)

        available_a, available_b, available_c, available_d, available_e = [int(i) for i in raw_input().split()]

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


class Commands(object):
    DIAGNOSIS = "DIAGNOSIS"
    CONNECT = "CONNECT"
    MOLECULES = "MOLECULES"


class Actions(object):
    DIAGNOSIS = "DIAGNOSIS"
    FIND_SAMPLE = "FIND_SAMPLE"
    GET_SAMPLE = "GET_SAMPLE"
    CONNET_TO_SAMPLE = "CONNET_TO_SAMPLE"
    GET_MOLECULE = "GET_MOLECULE"


class Strategy(object):

    def __init__(self, world):
        self.world = world

        self.sample = None
        if len(self.world.own_samples) > 0:
            self.sample = self.world.own_samples[0]


    def get_action(self):

        command = None
        action = None

        cur_module = self.world.modules[0]

        if cur_module.target == "START_POS":
            command = (Commands.DIAGNOSIS, None)
        elif cur_module.target == ModuleType.DIAGNOSIS:
            action = Actions.GET_SAMPLE
        elif cur_module.target == ModuleType.MOLECULES:
            action = Actions.GET_MOLECULE

        sample = None

        while command is None:

            if action == Actions.FIND_SAMPLE:

                sample = self.world.samples[ int( random.random() * (len(self.world.samples)-1))]

                action = Actions.CONNET_TO_SAMPLE

            elif action == Actions.GET_SAMPLE:

                if self.sample is not None:
                    command = (Commands.MOLECULES, None)
                else:
                    action = Actions.FIND_SAMPLE

            elif action == Actions.CONNET_TO_SAMPLE:
                command = (Commands.CONNECT, sample)

        return command


WORLD = World()

if __name__ == '__main__':
        
    while True:

        WORLD.update()

        STRATEGY = Strategy(WORLD)


        command = STRATEGY.get_action()


        print command