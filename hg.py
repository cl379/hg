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
        self._homeRange = 20
        self._population = []
        self._population.append(15)
        self._population.append(15)
        self._mobility = random.random()
        self._caloriesNeeded = 100
        
    def __str__(self):
        return str(self._x) + ',' + str(self._y)

    def step(self, step):
        print 'HG executing step: ', step 
        self.settle()
        food = self.doForage()
        self.computeStarvationRate(food)
        self.trackDemography()
        

    def settle(self):
        # if the value is lower than the set mobility attribute (0= never move, 1= always move) the agent moves
        if random.random() < self._mobility:
            self._home = self.getRandomDune()
        print 'I am here: ', self._home

    def getRandomDune(self):
        candidates = []
        for i in range(self._home._x - self._homeRange, self._home._x + self._homeRange + 1):
            for j in range (self._home._y - self._homeRange, self._home._y + self._homeRange + 1):
                if self._world.checkPosition(Coordinate(i,j)) == True:
                    candidates.append(Coordinate(i, j))
        index = random.randint(0, len(candidates)-1) 
        return candidates[index]


    def trackDemography(self):
        for i in range(len(self._population)):
            if self._population[i] == -1:
                continue
            if self.mortalityCheck(i) == True:
                self._population[i] = -1
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
        print 'I am dead'

    def mortalityCheck(self, i):
        """MortalityCheck =True means the individual at position i dies"""
        if random.random() < self._starvationRate:
            return True
        mortalityProbability = 0.015
        if self._population[i] < 4:
            mortalityProbability = 0.1
        if random.random() < mortalityProbability:
            return True
        return False

    def computeStarvationRate(self, food):
        self._starvationRate = 1.0 - (float(food)/float(self._caloriesNeeded))    
        self._starvationRate = max(0, self._starvationRate)
        print 'starvation is: ', self._starvationRate

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
                newAgent = HG(self._world)
                self._world.addAgent(newAgent)
                if random.randint(0,1) == 0:
                    newAgent._home = self._home
                else:
                    newAgent._home = agent._home
                newAgent._population[0] = self._population[index]
                newAgent._population[1] = agent._population[mateIndex]
                self._population[index] = -1
                agent._population[mateIndex] = -1
                if random.random() < self._world._mutationRate:
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
        food = 0
        candidates = []
        for i in range(self._home._x - self._homeRange, self._home._x + self._homeRange + 1):
            for j in range (self._home._y - self._homeRange, self._home._y + self._homeRange + 1):
                if self._world.checkPosition(Coordinate(i,j)) == True:
                    candidates.append(Coordinate(i, j))
                # TODO random choice of cell to forage in
        for currentPosition in candidates:
            food = food + self._world._calories[currentPosition._x][currentPosition._y]
            self._world._calories[currentPosition._x][currentPosition._y] = 0
            if food > self._caloriesNeeded:
                break
        return food


class World():
    def __init__(self, size):
        self._size = size
        self._ground = [[0 for x in range(size)] for x in range(size)]
        self._groundState = [[0 for x in range(size)] for x in range(size)]
        self._calories = [[10 for x in range(size)] for x in range(size)]
        for i in range(size):
            for j in range(size):
                cellType = random.randint(cellTypes.eDune, cellTypes.eInterdune)
                self._ground[i][j] = cellType
        self._agents = []
        self._mutationRate = 0.1

    def addAgent(self, agent):
        self._agents.append(agent)
        agent._world  = self


    def checkPosition(self, location):
        if location._x<0 or location._y<0:
            return False
        if location._x>=self._size or location._y>=self._size:
            return False
        return True

    
def main():
    size = 100
    numAgents = 10
    myWorld = World(size)
    for i in range(numAgents):
        myHG = HG(myWorld)
        myWorld.addAgent(myHG)
        myHG._home = myHG.getRandomDune()
    timeSteps = 200
    for i in range(timeSteps):
        print 'Executing time step: ', i
        for agent in myWorld._agents:
            agent.step(i)

if __name__ == "__main__":
    main()
