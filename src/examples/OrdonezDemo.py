from GeneticAlgorithm import *
import math

class Ordonez(Core.GeneticOperator):
    def decode(self, population):
        # Evaluate only recently generated items (pointed to by population.lethals)        
        lethals = getattr(population, 'lethals', None )
        #  If population.lethals does not exist, update every individual (and set the lethals list to contain every index)
        if not lethals:
            lethals = range(len(population.individuals))
        # Iterate over recently replaced individuals
        for i in lethals:            
            perm = [0];
            geno = [segment.data for segment in population.individuals[i].genotype.segments]
            for j in range(len(geno)):                
                position = geno[j] % (j+2)
                perm.insert(position, j+1)
                
            population.individuals[i].phenotype = perm;
    ## Set the initialize, iterate and finalize methods to point to sumSegments
    initialize = decode;
    iterate    = decode;
    finalize   = decode;             

if __name__=='__main__':
#    random.seed(0)
    nNodes = 5;
    ch = Core.Genotype(segments=[GenotypeLibrary.BinaryChromosomeSegment(nBits=int(math.ceil(math.log(i+1,2)))) for i in range(1,nNodes)])
    
    p  = Core.Population(schema=ch, popSize=10, genSize=10, maximize=False)#, mutation_probability=0.01, maximize=True)
    ga = Core.Scheduler(name='Demo', population=p, operators=[Ordonez()] )#;, operators=[SumSegments(), LogGenerations(saveFrequency=1), SelectionOperators.SUSSelection(), SelectionOperators.SelectLethals(), Core.Crossover(), Core.Mutate()])    
    ga.runGA(1)
    
    print ga