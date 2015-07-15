from GeneticAlgorithm import *
import math

if __name__=='__main__':
    # Run parameters 
    # random.seed(0)  # Fixed seed for repeatable runs
    nNodes = 16;    # The number of nodes in the graph. Remember, TSP is of exponential difficulty!
    # Control logging operator and population setting with the same flag
    maximize = False
    # Create the graph, randomly
    instanceGraph = GraphLibrary.Graph(N=nNodes)
    # The chromosome schema has n-1 segments, each of length ceil(log(i+1,2)) as required by the ordonez decodification
    ch = Core.Genotype(segments=[GenotypeLibrary.BinaryChromosomeSegment(nBits=int(math.ceil(math.log(i+1,2)))) for i in range(1,nNodes)])
    # Build a population
    #    the TSP is a minimization problem, so maximize is set to false.
    #    mutation probability is greater than the default to prevent premature convergence 
    p  = Core.Population(schema=ch, popSize=10*nNodes, genSize=2*nNodes, maximize=maximize, mutation_probability=0.5)
    # Build the GA scheduler
    #                 Decoding : GraphLibrary.Ordonez
    #               Evaluation : PathLengthFitness
    #     Logging and Plotting : BestPathPlotLogger
    #    Mating pool selection : SUSSelection
    # Elitist lethal selection : SelectLethals
    #                Crossover : Crossover
    #                   Mutate : Mutate
    ga = Core.Scheduler( name='Demo',\
                         population=p,\
                         operators=[ GraphLibrary.Ordonez(),\
                                     GraphLibrary.PathLengthFitness(graph=instanceGraph),\
                                     GraphLibrary.BestPathPlotLogger(maximize=maximize, graph=instanceGraph, iterationFrequency=1),\
                                     #SelectionOperators.SUSSelection(),\
                                     SelectionOperators.KTournament(),\
                                     SelectionOperators.SelectLethals(),\
                                     Core.Crossover(),\
                                     Core.Mutate()])
    # Run the genetic algorithm for 100 generations    
    ga.runGA(30 * nNodes)
    # Print the instance graph at the end
    print '\n' + str(instanceGraph)