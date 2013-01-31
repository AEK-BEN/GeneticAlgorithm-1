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

## This code runs only when this script is executed as main
if __name__=='__main__':
#    random.seed(0)
    maximize = False
    ch = Core.Genotype(segments=[GenotypeLibrary.BinaryChromosomeSegment(nBits=i*10) for i in range(1,4)])
    p  = Core.Population(schema=ch, popSize=100, genSize=20, maximize=maximize, mutation_probability=0.01)
    ga = Core.Scheduler(name='Demo',\
                        population=p,\
                        operators=[NumOnes(),\
                                   LoggingOperators.LogGenerations(iterationFrequency=1),\
                                   PlottingOperators.PlotBestLogger(iterationFrequency=1, maximize=maximize),\
                                   SelectionOperators.SUSSelection(),\
                                   SelectionOperators.SelectLethals(),\
                                   Core.Crossover(),\
                                   Core.Mutate()])    
    ga.runGA(100)