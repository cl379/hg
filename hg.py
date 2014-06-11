#!/usr/bin/python2

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
        return str(self._x)+','+str(self._y)

class HG():
    def __init__(self, world):
        self._world = world
        self._home = Coordinate (-1,-1)
        self._currentPosition = Coordinate (0,0)
        self._homeRange = 50
        self._population = []
        self._population.append(15)
        self._population.append(15)
        self._mobility = random.random()
        self._biomassNeeded = 100
        
    def __str__(self):
        return str(self._x) + ',' + str(self._y)

    def step(self, step):
        print('HG executing step: ', step)
        self.settle()
        self.doForage()
        self.trackDemography()
        

    def settle(self):
        # if the value is lower than the set mobility attribute (0= never move, 1= always move) the agent moves
        if random.random() < self._mobility:
            self._home = self._world.getRandomDune()
        print 'I am here: ', self._home
        print self._mobility

    def trackDemography(self):
        for i in range(len(self._population)):
            if self._population[i] == -1:
                continue
            newAgent = False
            if i > 1 and self._population[i] >= 15:
                newAgent = self.createAgent(i)
            if newAgent == False:
                self._population[i] = self._population[i]+1
        if random.randint(0, 1) == 1 and self._population[0] != -1 and self._population[1] != -1:
            self._population.append(0)
        print '\tDemography: ', self._population

        if self.getNumberOfIndividuals() > 0:
            return
        self.remove()

    def getNumberOfIndividuals(self):
        individuals = 0
        for i in range(len(self._population)):
            if self._population[i] != -1:
                individuals = individuals + 1
        return individuals

    def createAgent(self, index):
        for agent in self._world._agents:
            mateIndex = agent.getAdultChild()
            if mateIndex != -1:
                newAgent = HG()
                self._world.addAgent(newAgent)
                if random.randint(0,1) == 0:
                    newAgent._home = self._home
                else:
                    newAgent._home - agent._home
                newAgent._population[0] = self._population[index]
                newAgent._population[1] = agent._population[mateIndex]
                self._population[index] = -1
                self._population[mateIndex] = -1
                if random.random() < self.world._mutationRate:
                    newAgent._mobility = random.random()
                else:
                    newAgent._mobility = (self._mobility + agent._mobility)/2.0
                return True
        return False

    def getAdultChild(self):
        for i in range(len(self._population)):
            if i>1 and self._population[i]>=15:
                return i
        return -1


    def doForage(self):
        food = self._world._calories[self._currentPosition._x][self._currentPosition._y]
        while food < self._biomassNeeded:
            for currentHomeRange in range(0, self._homeRange):
                food = food + self._world._calories[self._currentPosition._x][self._currentPosition._y]
            print('food collected: ', self._world._calories)
        else:
            print 'enough food collected'


class World():
    def __init__(self, size):
        self._size = size
        self._ground = [[0 for x in range(size)] for x in range(size)]
        self._groundState = [[0 for x in range(size)] for x in range(size)]
        self._calories = [[100 for x in range(size)] for x in range(size)]
        for i in range(size):
            for j in range(size):
                cellType = random.randint(cellTypes.eDune, cellTypes.eInterdune)
                self._ground[i][j] = cellType
        self._agents = []
        self._mutationRate = 0.1

    def addAgent(self, agent):
        self._agents.append(agent)
        agent._world  = self

    def getRandomDune(self):
        candidates = []
        for i in range (self._size):
            for j in range (self._size):
                if self._ground[i][j] == cellTypes.eDune:
                    candidates.append(Coordinate(i,j))
        index = random.randint(0, len(candidates))
        return candidates[index]

    def checkPosition(self, location):
        if location._x<0 or location._y<0:
            return False
        if location._x>self._size or location._y>self._size:
            return False
        return True

    
def main():
    size = 100
    myWorld = World(size)
    myHG = HG(myWorld)
    timeSteps = 50
    for i in range(timeSteps):
        print('Executing time step: ', i)
        myHG.step(i)

if __name__ == "__main__":
    main()
