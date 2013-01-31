import Core
import copy

## @class BestLogger
#  @brief This class stores the best individual of the population, if it is better than the last individual found.
class BestLogger(Core.BasePeriodicOperator):
    def __init__(self, **kwargs):
        self.bestLog = []
        self.numEvaluations = []
        self.criterion = 'fitness'
        self.maximize = True
        self.iterationFrequency = 1
        super(BestLogger, self).__init__(**kwargs)
    
    ## @fn logCallback(self, population)
    #  @brief Add a new individual to the log if it is different to the best logged so far
    def logCallback(self, population):        
        currentBest, newBest = self.getBest(population)
        ## @todo Check individual fitness
        if currentBest != newBest:
            self.addToLog(newBest)

            
    iterationCallback  = logCallback
    evaluationCallback = logCallback
    
    ## @fn logBest(self, population)
    #  @brief Append the best individual ever found to the log, and add an evaluation counter
    def addToLog(self, best):        
        self.numEvaluations.append( self.evaluationCounter )
        self.bestLog.append( best )
    
    ## @fn getBest(self, population)
    #  @brief Get the best individual out of the list containing the population and the best individual found so far
    def getBest(self, population): 
        # Get the population size
        n = len(population.individuals)
        # Append the current best to the list of individuals           
        candidates = population.individuals 
        if len(self.bestLog) > 0:
            currentBest = self.bestLog[-1]
            candidates.append(currentBest)
        else:
            currentBest = None
        # Get the comparison criteria from all individuals
        criteria = [getattr(individual, self.criterion) for individual in candidates]
        # Create and zip a lost of pointers 
        indices  = range(n+1)
        sortedFitness = sorted(zip(criteria, indices), key=lambda x: x[0])
        # Select the best individual, according to target
        if self.maximize:
            best = sortedFitness[-1][1]
        else:
            best = sortedFitness[0][1]
        # Return the best candidate
        return (currentBest, candidates[best])
    
    def finalize(self, population):
        for eval, individual in zip( self.numEvaluations, self.bestLog ):
            print ('%4d\t' % eval) + str(individual)

## @class LogGenerations
#  @brief Log the full population of a GA 
class LogGenerations(Core.BasePeriodicOperator):
    def __init__(self, **kwargs):
        self.generationLog  = []
        self.numEvaluations = []
        super(LogGenerations, self).__init__(**kwargs)
        
    def logPopulation(self, population):
            # Append the plain number of evaluations to the evaluation counter
            self.numEvaluations.append(self.evaluationCounter)            
            # Make a deep copy of the population and log it
            self.generationLog.append(copy.deepcopy(population))
    
    iterationCallback  = logPopulation
    evaluationCallback = logPopulation
    
    def finalize(self, population):
        for ev, pop in zip( self.numEvaluations, self.generationLog ):
            print 'Number of evaluations %d' % ev + str(pop) + '\n'