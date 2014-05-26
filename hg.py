#!/usr/bin/python2.7

import random

def enum(**enums):
    """ converts a sequence of values to an C++ style enum """
    return type('Enum', (), enums)

cellTypes = enum(eDune=0, eWater=1, eInterdune=2)


class Coordinate():
    def __init__(self, x, y):
        self._x = x
        self._y = y
    def __str__(self):
        return str(self._x)+','+str(sel._y)

class HG():
    def __init__(self, world):
        self._world = world
        self._home = Coordinate (-1,-1)
        self._homeRange = 10

    def step(self, step):
        print('HG executing step: ', step)
        self.settle()
        self.doForage()

    def settle(self):
        print('\tSettle')
        self._home = self._world.getRandomDune()
        print('I am here: ', self._home)

    def doForage(self):
        print('\tResources collected')

    def trackDemography(self):
        print('\tDemography')


class World():
    def __init__(self, size):
        self._size = size
        self._ground = [[0 for x in range(size)] for x in range(size)]
        for i in range(size):
            for j in range(size):
                cellType = random.randint(cellTypes.eDune, cellTypes.eInterdune)
                self._ground[i][j] = cellType


    def getRandomDune(self):
        candidates = []
        for i in range (self._size):
            for j in range (self._size):
                if self._ground[i][j] == cellTypes.eDune:
                    candidates.append(Coordinate(i,j))
        index = random.randint(0, len(candidates))
        return candidates[index]

def main():
    size = 100
    myWorld = World(size)
    myHG = HG(myWorld)
    timeSteps = 10
    for i in range(timeSteps):
        print('Executig time step: ', i)
        myHG.step(i)

if __name__ == "__main__":
    main()
