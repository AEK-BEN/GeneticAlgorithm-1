import copy
import random
import Core
import GenotypeLibrary
import SelectionOperators

## @class SumSegments
#  @brief This class implements a Genetic operator that simply sums the genotype value of every individual and sets it as the fitness
class SumSegments(Core.GeneticOperator):
    ## @fn sumSegments(self, population)
    #  @brief Selectively update individuals in the population
    #
    #  If the population contains a field called lethals, iterate over those indices and update the individual's fitness. If the population does not contain the lethals property, update every individual
    def sumSegments(self, population):
        # Evaluate only recently generated items (pointed to by population.lethals)        
        lethals = getattr(population, 'lethals', None )
        #  If population.lethals does not exist, update every individual (and set the lethals list to contain every index)
        if not lethals:
            lethals = range(len(population.individuals))
        # Iterate over recently replaced individuals
        for i in lethals:
            population.individuals[i].fitness = float(reduce( lambda x,y: x+y, [segment.data for segment in population.individuals[i].genotype.segments]))
        population.lethals = lethals
    
    ## Set the initialize, iterate and finalize methods to point to sumSegments
    initialize = sumSegments;
    iterate    = sumSegments;
    finalize   = sumSegments;   

class LogGenerations(Core.GeneticOperator):
    def __init__(self, **kwargs):
        super(LogGenerations, self).__init__(**kwargs)
        self.generationLog = []
        self.numEvaluations = []
        self.generationCounter = 0
        self.saveFrequency = getattr(self, 'saveFrequency', 1)
        
    def iterate(self, population):
        self.generationCounter = self.generationCounter + 1        
        if (self.generationCounter % self.saveFrequency) ==0:
            # Evaluate only recently generated items (pointed to by population.lethals)        
            lethals = getattr(population, 'lethals', None )
            #  If population.lethals does not exist, update every individual (and set the lethals list to contain every index)
            if not lethals:
                lethals = range(len(population.individuals))
            if not getattr(self, 'numEvaluations', None):
                nE = 0
                self.numEvaluations = []
            else:
                nE = self.numEvaluations[-1]
            self.numEvaluations.append(nE + len(lethals))
            self.generationLog.append(copy.deepcopy(population))
    
    def finalize(self, population):
        for ev, pop in zip( self.numEvaluations, self.generationLog ):
            print 'Number of evaluations %d' % ev + str(pop) + '\n'

if __name__=='__main__':
    random.seed(2)
    ch = Core.Genotype(segments=[GenotypeLibrary.BinaryChromosomeSegment(nBits=i) for i in range(1,4)])
    p  = Core.Population(schema=ch, popSize=50, maximize=True)
    ga = Core.Scheduler(name='Demo', population=p, operators=[SumSegments(), SelectionOperators.SUSSelection(), SelectionOperators.SelectLethals(), Core.Crossover(), Core.Mutate(), LogGenerations(saveFrequency=10)])    
    ga.runGA(100)