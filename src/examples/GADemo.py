from GeneticAlgorithm import *


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
        # Evaluate only recently generated items (pointed to by population.lethals)        
        lethals = getattr(population, 'lethals', None )
        #  If population.lethals does not exist, update every individual (and set the lethals list to contain every index)
        if not lethals:
            lethals = range(len(population.individuals))
        # The plain number of evaluations counter is initialized in 0 if not found
        self.nE = getattr(self, 'nE', 0) + len(lethals)
        # If this generation should be logged
        if (self.generationCounter % self.saveFrequency) ==0:
            # Initialize the number of evaluations to an empty list if it does not exist
            if not getattr(self, 'numEvaluations', None):
                self.numEvaluations = []
            # Append the plain number of evaluations to the evaluation counter
            self.numEvaluations.append(self.nE)            
            # Make a deep copy of the population and log it
            self.generationLog.append(copy.deepcopy(population))
    
    def finalize(self, population):
        for ev, pop in zip( self.numEvaluations, self.generationLog ):
            print 'Number of evaluations %d' % ev + str(pop) + '\n'

if __name__=='__main__':
    random.seed(0)
    ch = Core.Genotype(segments=[GenotypeLibrary.BinaryChromosomeSegment(nBits=i) for i in range(1,4)])
    p  = Core.Population(schema=ch, popSize=10, genSize=10, maximize=False)#, mutation_probability=0.01, maximize=True)
    ga = Core.Scheduler(name='Demo', population=p, operators=[SumSegments(), LogGenerations(saveFrequency=1), SelectionOperators.SUSSelection(), SelectionOperators.SelectLethals(), Core.Crossover(), Core.Mutate()])    
    ga.runGA(100)
