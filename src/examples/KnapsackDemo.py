import math
import random
from GeneticAlgorithm import *

## @class NumOnes
#  @brief An evaluation operator that computes the number of ones in a segment whose data can be converted to binary using the bin() function
class NumOnes(EvaluationOperators.BaseEvaluationOperator):
    ## @fn segmentOnes(self, segment) Compute the number of ones in a binary segment
    #  @brief Compute the number of ones in one genotype segment
    def segmentOnes(self, segment):
        return reduce( lambda x,y: x+y, (bit=='1' for bit in bin(segment.data)[2:]) )
    ## @Fn Call segmentOnes for each segment on the genotype, and add them all together to produce a fitness function.
    def evaluateIndividual(self, individual):
        onesPerSegment = (self.segmentOnes(segment) for segment in individual.genotype.segments)
        individual.fitness = reduce( lambda x,y:x+y, onesPerSegment )

## @class Knapsack
#  @brief An evaluation operator that computes the number of ones in a segment whose data can be converted to binary using the bin() function
class Knapsack(EvaluationOperators.BaseEvaluationOperator):
    def __init__(self, maxVolume=0, objectVolumes=[], volumeLambda=0.0, objectCosts=[], **kwargs):
        super(Knapsack, self).__init__(**kwargs)
        self.maxVolume = maxVolume
        self.objectVolumes = objectVolumes
        self.objectCosts = objectCosts
        self.volumeLambda = volumeLambda
    
    ## @Fn Call segmentOnes for each segment on the genotype, and add them all together to produce a fitness function.
    def evaluateIndividual(self, individual):
        segmentsValues = [segment.data for segment in individual.genotype.segments]
        usedVolume = reduce(lambda x, y: x+y, map(lambda v, s:v*s, self.objectVolumes, segmentsValues))
        solutionCost = reduce(lambda x, y: x+y, map(lambda v, s:v*s, self.objectCosts, segmentsValues))
        
        lambdaPenalty = self.volumeLambda*( self.maxVolume - usedVolume );
        lambdaPenalty = 0 if lambdaPenalty > 0 else lambdaPenalty
        individual.fitness = solutionCost + lambdaPenalty

## This code runs only when this script is executed as main
if __name__=='__main__':
    random.seed(0)
    
    # Kanpsack instance parameters
    nObjects =  132om.randrange(10, 20) for i in xrange(nObjects)]
    maxVolume = reduce(lambda x, y: x+y, objectVolumes) / 2
    volumeLambda = maxVolume*10;
    
    # GA parameters
    maximize = True
    nGenerations = 100
    popSize = nObjects*10
    genSize = int(math.floor( popSize/10 ))
        
    # Genetic algorithm
    ch = Core.Genotype(segments=[GenotypeLibrary.BinaryChromosomeSegment(nBits=1) for i in range(nObjects)])
    p  = Core.Population(schema=ch, popSize=popSize, genSize=genSize, maximize=maximize, mutation_probability=0.01)
    ga = Core.Scheduler(name='Demo',\
                        population=p,\
                        operators=[Knapsack(maxVolume, objectVolumes, volumeLambda, objectCosts),\
                                   LoggingOperators.LogGenerations(iterationFrequency=1),\
                                   PlottingOperators.PlotBestLogger(iterationFrequency=1, maximize=maximize),\
                                   SelectionOperators.KTournament(),\
                                   SelectionOperators.SelectLethals(),\
                                   Core.Crossover(),\
                                   Core.Mutate()])    
    ga.runGA(nGenerations)
    
    print 'Object Volumes', objectVolumes
    print 'Object Costs', objectCosts
    print 'Max Volume', maxVolume
    print 'Volume Lambda', volumeLambda