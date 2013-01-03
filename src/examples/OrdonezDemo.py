from GeneticAlgorithm import *
import math

if __name__=='__main__':
#    random.seed(0)
    nNodes = 5;
    ch = Core.Genotype(segments=[GenotypeLibrary.BinaryChromosomeSegment(nBits=int(math.ceil(math.log(i+1,2)))) for i in range(1,nNodes)])    
    p  = Core.Population(schema=ch, popSize=10, genSize=10, maximize=False)#, mutation_probability=0.01, maximize=True)
    ga = Core.Scheduler(name='Demo', population=p, operators=[GraphLibrary.Ordonez()] )#;, operators=[SumSegments(), LogGenerations(saveFrequency=1), SelectionOperators.SUSSelection(), SelectionOperators.SelectLethals(), Core.Crossover(), Core.Mutate()])    
    ga.runGA(1)
    
    print ga