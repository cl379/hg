



def enum(**enums):
    """ converts a sequence of values to an C++ style enum """
    return type('Enum', (), enums)

cellTypes = enum(eDune=0, eWater=1, eInterdune=2)


class HG(Agent):
    newId = 0

    def __init__(self, ident):
        Agent.__init__(self, ident)
        self._homeRange = 10
        # list of individuals. if value==-1 means that the individual is dead
        # if value != -1 defines the current age of individual
        self._population = []
        self._population.append(15)
        self._population.append(15)
        self._starvationRate = 0
        # shall we give them a surplus for the days in which they are moving?
        self._surplus = 0





    




    def doForage(self):



 class MyWorld(World):

     def createAgent(self):


    """ Same as getRandomDune of the ap model."""
    def establishHome(self):
        candidates = []
        index = Point2DInt(0, 0)       
        for index._x in range(self.getBoundaries().left, self.getBoundaries().right+1):
            for index._y in range(self.getBoundaries().top, self.getBoundaries().bottom+1):
                # TODO preference to vicinity to water body

                if self.getValue('ground', index) == cellTypes.eDune:
                    candidates.append(index.clone())
        index = random.randint(0, len(candidates) - 1)
        return candidates[index]

    def checkMortality(self):


class MyWorldConfig():
    def __init__(self):
        self._size = SizeInt(0,0)
        self._numSteps = 0

        # climate
        self._climateMean = 0
        self._climateSd = 1
        
        # agents
        self._initialPopulation = 0
        self._locationTries = 10
        self._requiredNeedsPercentage = 1.0

        # biomass
        self._biomassKgHa = 0
        self._biomassCaKg = 0
        self._reserve = 1.0




def main():
    parser = argparse.ArgumentParser()
    logging.basicConfig(filename='rain.log', level=logging.INFO)
    parser.add_argument('-x', '--config', default='config.xml', help='config file')
    args = parser.parse_args()
    config = MyWorldConfig()
    config.deserialize(args.config)

    mySimulation = Simulation(config._size, config._numSteps, config._serializeResolution)
    myWorld = MyWorld(mySimulation, config)
    myWorld.initialize()

    myWorld.run()


if __name__ == "__main__":
    main()