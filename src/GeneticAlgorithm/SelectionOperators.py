import copy
import random
from Core import *

## @class SelectLethals
#  @brief Select the individuals to replace based on the population.maximize flag and the population.genSize property
#
#  Select as many individuals as indicated by population.genSize to be replaced during the next crossover operation
class SelectLethals(GeneticOperator):
    ## @fn select(self, population)
    #  @brief Select the individuals to replace based on the population.maximize flag and the population.genSize property
    def select(self, population):        
        # Get the population size
        n = len(population.individuals)
        # Get the amount of offspring to produce (2*m = len(mating_pool))
        m = getattr(population, 'genSize', n)
        #  Get a fitness vector out of the individual vector        
        fitness = [individual.fitness for individual in population.individuals]
        indices = range(n)
        sortedFitness = sorted(zip(fitness, indices), key=lambda x: x[0])
        # Select the m worse individuals in the generation to be replaced
        if population.maximize:
            L = sortedFitness[:m]
        else:
            L = sortedFitness[-m:]
        # Update the lethals vector
        population.lethals = [l[1] for l in L]
    # Select individuals for replacement only during the iterate phase of runGA    
    iterate     = select

## @class KTournament
#  @brief A selection operator that implements the k-tournament algorithm
class KTournament(GeneticOperator):
    ## @fn __init__(self, k=2, **kwargs)
    #  @brief The genetic operator constructor
    #  @param k The number of individuals that will participate in every tournament 
    def __init__(self, k=2, **kwargs):
        super(KTournament, self).__init__(**kwargs)
        self.k = k

    ## @fn selectBest(self, candidates, population)
    #  @brief Given a list of candidates and a population, decide which cantidae is the best
    #  @param candidates A list of indexes that point to the tournament candiadates
    #  @param population A Core.Population object that contains the contender individuals
    #  @return The index of the best individual among the candidates
    def selectBest(self, contenders, population):
        sortedContenders = sorted([(population.individuals[i].fitness,i) for i in contenders], key=lambda x: x[0])
        if population.maximize:
            return sortedContenders[-1][1]
        else:
            return sortedContenders[0][1]
    
    ## @fn select(self, population)
    #  @brief Perform the k-tournament selection
    # 
    #  The k-tournament selection algorithm consists on creating tournaments in which k random individuals participate. The best individual is selected for each tournament, and is selected to belong to the mating pool.
    #  M torunaments are performed, where M is equal to population.genSize (or n if this property is not found)
    def select(self, population):
        # Number of individuals
        n = len(population.individuals)
        # Get the amount of offspring to produce (2*m = len(mating_pool))
        m = getattr(population, 'genSize', n)
        # Compute the contenders for each torunament
        tournaments = [ [random.randrange(n) for contender in xrange(self.k) ] for tournament in xrange(2*m) ]
        # Put the tournament winners on the mating pool
        population.matingPool = [self.selectBest(contenders, population) for contenders in tournaments ]
    # Make iterate function call select instead
    iterate = select
                
## @class SUSSelection
#  @brief This operator performs stochastic uniform selection over the population, updating the field matingPool
#
#  This class performs SUS for both maximization or minimization, the mating pool is simply a list of indices that point to the parents. If minimization is desired, the population.maximize flag must be set to False.
#  If population.genSize exists, the mating pool will be twice that number (to produce the same number of offspring); If this parameter does not exist, the mating pool will have twice the length of population.individuals
class SUSSelection(GeneticOperator):
    def select(self, population):
        # Number of individuals
        n = len(population.individuals)
        # Fitness vector
        fit = [ind.fitness for ind in population.individuals]
        # Adjust the pdf for minimization
        if not population.maximize:
            pdf = [0.0]*n
            M = max(fit) + (1.0)
            for i in xrange(n):
                pdf[i] = M - fit[i]
        else:
            pdf = fit        
        # Normalization factor
        F = reduce(lambda x, y: x+y, pdf)
        # Cumulative distribution function
        cdf = [pdf[0]/F] *n
        # Probability distribution function
        for i in xrange(1, n):
            cdf[i] = cdf[i-1] + pdf[i]/F            
        # Get the amount of offspring to produce (2*m = len(mating_pool))
        m = getattr(population, 'genSize', n)
        # Distance between ticks in SUS -> 1/2*m := 0.5/m
        delta = 0.5/m
        # Initialize the mating pool
        matingPool = [ 0 ] * (2*m)
        # SUS implements a roulette with 2*m equidistant ticks, this variable stores the position of the current tick (as a probability)
        currentTick = delta * random.random()
        # Generate 2*m parent pointers 
        for i in xrange(2*m):
            # Find the first entry on the cdf that is greater than or equal to the current tick
            for slicePointer in xrange(n):
                if cdf[slicePointer] > currentTick:
                    break
            # The ith element on the maitingPool is slice pointer
            matingPool[i] = slicePointer
            currentTick += delta
            while currentTick > 1.0:
                currentTick -= 1.0
        random.shuffle(matingPool)
        population.matingPool = matingPool
    iterate = select    
