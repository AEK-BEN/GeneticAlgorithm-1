import copy
import random
from Core import *


class SelectLethals(GeneticOperator):
    def select(self, population):        
        n = len(population.individuals)
        # Get the amount of offspring to produce (2*m = len(mating_pool))
        m = getattr(population, 'genSize', n)        
        fitness = [individual.fitness for individual in population.individuals]
        indices = range(n)
        sortedFitness = sorted(zip(fitness, indices), key=lambda x: x[0])
        if population.maximize:
            L = sortedFitness[:m]
        else:
            L = sortedFitness[-m:]
        population.lethals = [l[1] for l in L]
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
