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
    FIND_SAMPLE = "FIND_SAMPLE"
    GET_SAMPLE = "GET_SAMPLE"
    CONNET_TO_SAMPLE = "CONNET_TO_SAMPLE"
    GET_MOLECULE = "GET_MOLECULE"
    LABORATORY = "LABORATORY"
    SAMPLES = "SAMPLES"
    CONNECT_LABORATORY = "CONNECT_LABORATORY"
    CONNECT_SAMPLES = "CONNECT_SAMPLES"


class Strategy(object):

    def __init__(self, world):
        self.world = world

        self.sample = None
        self.undefined = None
    
        for sample in self.world.own_samples:
            if sample.cost_a == -1:
                self.undefined = sample
            else:
                self.sample = self.world.own_samples[0]

        self.target = self.world.modules[0]


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
            action = Actions.GET_SAMPLE
        elif cur_module.target == ModuleType.MOLECULES:
            action = Actions.GET_MOLECULE
        elif cur_module.target == ModuleType.LABORATORY:
            action = Actions.CONNECT_LABORATORY
        elif cur_module.target == ModuleType.SAMPLES:
            action = Actions.CONNECT_SAMPLES

        sample = None

        while command is None:

            if action == Actions.FIND_SAMPLE:
                samples = self.world.own_samples
                if len(samples) > 0:
                    sample = samples[ int( random.random() * (len(samples)-1))]
                    action = Actions.CONNET_TO_SAMPLE
                else:
                    command = (Commands.SAMPLES, None)


            elif action == Actions.GET_SAMPLE:

                if self.sample is not None:

                    if self.undefined is None:
                        command = (Commands.MOLECULES, None)
                    else:
                        command = (Commands.CONNECT, self.undefined.sample_id)
                else:
                    action = Actions.FIND_SAMPLE

            elif action == Actions.CONNET_TO_SAMPLE:
                command = (Commands.CONNECT, sample.sample_id)

            elif action == Actions.CONNECT_LABORATORY:
                if self.sample is None:
                    if self.undefined is None:
                        command = (Commands.SAMPLES, None)
                    else:
                        command = (Commands.DIAGNOSIS, None)
                else:
                    command = (Commands.CONNECT, self.sample.sample_id)

            elif action == Actions.CONNECT_SAMPLES:
                
                if len(self.world.samples) > 0 or len(self.world.own_samples) > 0:
                    command = (Commands.DIAGNOSIS, None)
                else:
                    command = (Commands.CONNECT, 1)

            elif action == Actions.GET_MOLECULE:
                if self.target.storage_a < self.sample.cost_a:
                    command = (Commands.CONNECT, "A")

                elif self.target.storage_b < self.sample.cost_b:
                    command = (Commands.CONNECT, "B")

                elif self.target.storage_c < self.sample.cost_c:
                    command = (Commands.CONNECT, "C")

                elif self.target.storage_d < self.sample.cost_d:
                    command = (Commands.CONNECT, "D")

                elif self.target.storage_e < self.sample.cost_e:
                    command = (Commands.CONNECT, "E")

                else:
                    command = (Commands.LABORATORY, None)

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
