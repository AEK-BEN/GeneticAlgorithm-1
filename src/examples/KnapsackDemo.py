import math
from GeneticAlgorithm import *
## @page KnapsackPage Solving the Knapsack problem
#  
#  @section KnapsackIntroduction Introduction
#  This page describes how to use the GeneticAlgorithm framework to solve the knapsack problem.
#  The knapsack0-1 problem can be defined as follows:
#   \f{eqnarray*}{
#        \max \limits_{\textbf{s}} z =& \textbf{c}^{\textrm{T}}\textbf{s} \\
#        \textrm{subject to} & \\
#                 & \textbf{v}^{\textrm{T}}\textbf{s} \leq V_{\textrm{max}}\\
#   \f}
#  Where
#  \f$ \textbf{c} \f$ is the cost vector. Element \f$ c_{i} \f$ is the gain from taking object \f$i\f$.
#  \f$ \textbf{v} \f$ is the volume vector. Element \f$ v_{i} \f$ is the volume consumed when taking object \f$i\f$.
#  \f$ \textbf{s} \f$ is the solution. Each decision variable \f$ s_{i}\f$ is binary, and takes the value 1 if the object \f$i\f$ is selected to be part of the solution and 0 otherwise.
#  \f$ V_{\textrm{max}} \f$ is the maximum volume allowed for a solution. Every valid solution must comply with the restriction \f$ V_{\textrm{max}} \leq \textbf{c}^{\textrm{T}}\textbf{s} \f$. The parameter \f$ \lambda \f$ is a penalization factor, used to penalize all the unfeasible individuals.
#
#  The objective function of the problem has been modified according to the lagrangian relaxation technique. Furthermore, to make the \f$ \lambda \f$ selection parameter easier, the penalty term has been implemented in a non-linear way, that penalizes only the non-feasible.   
#
#  @section KnapsackEvaluation Knapsack: Deriving the BaseEvaluationOperator to implement the knapsack objective function
#  
#  The GeneticAlgorithm framework provides a set of GeneticAlgorithm that can be used to easily implement an evaluation function. The GeneticAlgorithm.BaseEvaluationOperator provides the evaluateIndividual method, that can be overloaded to evaluate every individual in the population. All GeneticAlgorithm EvaluationOperators should contain all the non-genotype parameters required to evaluate an individual internally. The __init__ function should be overloaded to receive the problem instance parameters and save them internally. See tha Knapsack class documentation for detailed information on these metods.
#
#  @subsection KnapsackInit The initialization function
#  This snippet of code describes the initialization function. Original commentaries are included, because they describe the class members and relate them to the ecuation shown above.
#  Notice that the initialization function receives and stores all the instance-related constants as object members. This is the expected behavior of any derived Evaluation Operator.
#  @code
#    def __init__(self, maxVolume=0, objectVolumes=[], volumeLambda=0.0, objectCosts=[], **kwargs):
#        super(Knapsack, self).__init__(**kwargs)
#        ## @member maxVolume The maximum volume allowed for feasible solutions \f$ V_{\textrm{max}} \f$
#        self.maxVolume = maxVolume
#        ## @member objectVolumes The vector of object volumes \f$ \textbf{v} \f$
#        self.objectVolumes = objectVolumes
#        ## @member objectCosts The vector of object costs \f$ \textbf{c} \f$
#        self.objectCosts = objectCosts
#        ## @member volumeLambda The penalization factor \f$ \lambda \f$
#        self.volumeLambda = volumeLambda
## @endcode
#
#  @subsection KnapsackEval The evaluateIndividual function
#
#  The main objective of all derived EvaluationOperators is to implement this function. The GeneticAlgorithm Scheduler calls this function for each newly generated individuals, every iteration. The programmer is responsible for filling in the individual.fitness member with the result of its evaluation, as exemplified below:
#
#  @code
#    def evaluateIndividual(self, individual):
#        # Get the vector s
#        segmentsValues = [segment.data for segment in individual.genotype.segments]
#        # Compute the volume used by the solution
#        usedVolume = reduce(lambda x, y: x+y, map(lambda v, s:v*s, self.objectVolumes, segmentsValues))
#        # Compute the solution cost
#        solutionCost = reduce(lambda x, y: x+y, map(lambda v, s:v*s, self.objectCosts, segmentsValues))
#        # The difference between the maximum allowed volume and the solution volume is the residual volume
#        residualVolume = self.maxVolume - usedVolume
#        # If the residual volume is less than 0, the solution is not penalized. The solution is penalized with a cost of lambda*residualVolume otherwise
#        lambdaPenalty = 0 if residualVolume > 0 else self.volumeLambda*residualVolume
#        # The individual fitness is the penalty plus the objective
#        individual.fitness = solutionCost + lambdaPenalty
#  @endcode

 
## @class Knapsack
#  @brief An evaluation operator that computes the relaxed version of the objective function used to solve a knapsack instance.
#
#  This class implements the following evaluation function:
#   \f{eqnarray*}{
#        \max \limits_{\textbf{s}} z =& \textbf{c}^{\textrm{T}}\textbf{s} + f_{\lambda}(\textbf{v}, \textbf{s}) \\
#        f_{\lambda}(\textbf{v}, \textbf{s}) =&
#               \left\{
#                 \begin{array}{rl}
#                   \lambda (V_{\textrm{max}} - \textbf{c}^{\textrm{T}}\textbf{s}) & \textrm{ if }  \textbf{v}^{\textrm{T}}\textbf{s} \leq V_{\textrm{max}}\\
#                   0 &  \textrm{otherwise}
#                 \end{array}
#               \right. \\
#   \f}
#
#  The parameter \f$ \textbf{c} \f$ is the cost vector. Element \f$ c_{i} \f$ is the gain from taking object \f$i\f$.
#  The parameter \f$ \textbf{v} \f$ is the volume vector. Element \f$ v_{i} \f$ is the volume consumed when taking object \f$i\f$.
#  The parameter \f$ \textbf{s} \f$ is the solution. Each decision variable \f$ s_{i}\f$ is binary, and takes the value 1 if the object \f$i\f$ is selected to be part of the solution and 0 otherwise.
#  The parameter \f$ V_{\textrm{max}} \f$ is the maximum volume allowed for a solution. Every valid solution must comply with the restriction \f$ V_{\textrm{max}} \leq \textbf{c}^{\textrm{T}}\textbf{s} \f$. The parameter \f$ \lambda \f$ is a penalization factor, used to penalize all the unfeasible individuals.
class Knapsack(EvaluationOperators.BaseEvaluationOperator):
    ## @fn __init__(self, maxVolume=0, objectVolumes=[], volumeLambda=0.0, objectCosts=[], **kwargs)
    #  @brief Initialize an evaluation operator to implement the evaluation function as described above
    #  @param maxVolume The maximum volume allowed for feasible solutions \f$ V_{\textrm{max}} \f$
    #  @param objectVolumes The vector of object volumes \f$ \textbf{v} \f$
    #  @param objectCosts The vector of object costs \f$ \textbf{c} \f$
    #  @param volumeLambda The penalization factor \f$ \lambda \f$
    def __init__(self, maxVolume=0, objectVolumes=[], volumeLambda=0.0, objectCosts=[], **kwargs):
        super(Knapsack, self).__init__(**kwargs)
        ## @member maxVolume The maximum volume allowed for feasible solutions \f$ V_{\textrm{max}} \f$
        self.maxVolume = maxVolume
        ## @member objectVolumes The vector of object volumes \f$ \textbf{v} \f$
        self.objectVolumes = objectVolumes
        ## @member objectCosts The vector of object costs \f$ \textbf{c} \f$
        self.objectCosts = objectCosts
        ## @member volumeLambda The penalization factor \f$ \lambda \f$
        self.volumeLambda = volumeLambda

    ## @fn evaluateIndividual(self, individual)
    #  @brief Evaluate an individual according to the function described above
    #  @param individual The list [segment.data for segment in individual.genotype.segments] contains the solution vector \f$ \textbf{s} \f$
    def evaluateIndividual(self, individual):
        # Get the vector s
        segmentsValues = [segment.data for segment in individual.genotype.segments]
        # Compute the volume used by the solution
        usedVolume = reduce(lambda x, y: x+y, map(lambda v, s:v*s, self.objectVolumes, segmentsValues))
        # Compute the solution cost
        solutionCost = reduce(lambda x, y: x+y, map(lambda v, s:v*s, self.objectCosts, segmentsValues))
        # The difference between the maximum allowed volume and the solution volume is the residual volume
        residualVolume = self.maxVolume - usedVolume
        # If the residual volume is less than 0, the solution is not penalized. The solution is penalized with a cost of lambda*residualVolume otherwise
        lambdaPenalty = 0 if residualVolume > 0 else self.volumeLambda*residualVolume
        # The individual fitness is the penalty plus the objective
        individual.fitness = solutionCost + lambdaPenalty

## @page KnapsackPage Solving the Knapsack problem
#  @section KnapsackGA Running a GeneticAlgorithm using the Knapsack EvaluationOperator
#
#  The knapsack evaluation operator is used in conjunction with the rest of the GeneticAlgorithm framework. This section demonstrates how to implement a script to generate a random knapsack instance and solve it.
#

if __name__=='__main__':
## @page KnapsackPage Solving the Knapsack problem
#  @subsection Generating a random instance
#  This section demonstrates how to generate a random Knapsack instance. The python random package is used for this purpose, as demonstrated below:
#
#  @code 
#    import random
#    random.seed(0)
#    
#    # Kanpsack instance parameters
#    nObjects =  12
#    
#    objectVolumes = [random.randrange(1, 20) for i in xrange(nObjects)]
#    objectCosts = [random.randrange(10, 20) for i in xrange(nObjects)]
#    maxVolume = reduce(lambda x, y: x+y, objectVolumes) / 2
#    volumeLambda = maxVolume*10
#  @endcode    
#
#  The object volumes and costs are generated randomly, while the maxVolume is kept at half the volume of all objects, to make sure that the instance is non-trivial and not every object fits in the optimal solution. The penalty constant volumeLambda is chosen to be proportional to the maximumVolume; This guarantees that non-feasible individuals have lower evaluations than the feasible individuals. 
#
#  @subsection KnapsackConfig Configuring the genetic algoritm
#
#  The Knapsack evaluation function is designed to maximize, so we create a flag that indicates that, and use it to initialize the selection and logging operators.
#  @code 
#    maximize = True
#  @endcode
#
#  The number of generations to run, the populationSize and the generationSize are chosen to be proportional to the size of the problem. These numbers are not guaranteed to produce the best result for a particular instance, but have been found experimentally to produce good results when compared to non-probabilistic search algorithms
# 
#  @code
#    nGenerations = nObjects*5
#    popSize = nObjects*10
#    genSize = int(math.floor( popSize/10 ))
#  @endcode 
#
#  The variable nGenerations will be used to control how many iterations to run using a GAScheduler. The variable popSize will be used during the population construction, and determines how many individuals are contained simultaneously in a population. The variable genSize will be used to initialize the population as well, and controls how many individuals are replaced with each iteration. As a thumbrule, all the parameters that need to be shared between operators, should be a part of the population object. At this point, every required parameter is defined, and we can proceed to initialize GeneticAlgorithm objects.
#
#  First, a prototype chromosome is created. This is used to initialize all the individuals in the population uniformly.
#
#  @code
#    ch = Core.Genotype(segments=[GenotypeLibrary.BinaryChromosomeSegment(nBits=1) for i in range(nObjects)])
#  @endcode
#
#  The main data container on a genetic algorithm is the population object. This contains a list of individuals, and all the parameters that an operator needs to determine how to transform the population, such as mutation probability, crossover probability, the maximization target and how many individuals to replace per iteration (genSize).
#  @code
#    p  = Core.Population(schema=ch, popSize=popSize, genSize=genSize, maximize=maximize, mutation_probability=0.01)
#  @endcode
#
#  The Scheduler object contains a population object, as well as a list of genetic operators that are applied iteratively to the population. Here we instantiate some useful operators:
#  @code
#    ga = Core.Scheduler(name='Demo',\
#                        population=p,\
#                        operators=[Knapsack(maxVolume, objectVolumes, volumeLambda, objectCosts),\
#                                   LoggingOperators.LogGenerations(iterationFrequency=1),\
#                                   PlottingOperators.PlotBestLogger(iterationFrequency=1, maximize=maximize),\
#                                   SelectionOperators.KTournament(),\
#                                   SelectionOperators.SelectLethals(),\
#                                   Core.Crossover(),\
#                                   Core.Mutate()])  
#  @endcode
#
#  The evaluartion operator is the first one, because individuals need to be evaluated before logging, selection, crossover or mutation can occur. The first GeneticOperator object in the list is an instance of our Knapsack class; Note that every variable that characterizes an instance is passed to the initialization function of the object, so that it can reference them whenever it is required.
#  The logging operators come next. The LogGenerations operator simply stores a copy of a population and all its individuals every time that an iterationFrequency iterations have elapsed. This example stores every generation of the run.
#  The PlotBestLogger operator is instantiated next. This operator can be instantiated multiple times, and used to keep track of several properties of an individual. This is the reason why the maximization flag has to be passed to this operator. This class samples the fitness member by default every time that an iterationFrequency iterations have elapsed.
#  The traditional genetic operators are instantiated next. The KTournament operator implements a 2-tournament selection scheme by default; It sets the matingPool member of the population object to contain a list of indices, which identify the parent individuals used to produce the iteration offspring. The SelectLethals operator selects the worse genSize individuals and marks them for removal with every iteration. The crossover operator generates new individuals by combining the genotypes of the parents in the mating pool, using a one-point crossover algorithm. Finally, the mutation operator may select a random bit from the new offspring and flip its value, to introduce variability to the population.
#
#  @code
#    ga.runGA(nGenerations)
#  @endcode
#
#  The last block calls the runGA function of the newly created scheduler. This causes the GeneticAlgorithm to run for nGenerations. Every GeneticOperator is an object that supports the basic initialize(), iterate() and finalize() functions. As their name suggests, the Scheduler calls the initialization function of every operator once at the beginning of the run. The iterate function is called nGenerations times, using the genetic operators in a round-robin order. The finalize function of every object is called once after the last iteration, this step is usually implemented by logging operators to print the ga run logged variables to a file or screen.
    import random
    random.seed(0)
    
    # Kanpsack instance parameters
    nObjects =  12
    
    objectVolumes = [random.randrange(1, 20) for i in xrange(nObjects)]
    objectCosts = [random.randrange(10, 20) for i in xrange(nObjects)]
    maxVolume = reduce(lambda x, y: x+y, objectVolumes) / 2
    volumeLambda = maxVolume*10
    
    # GA parameters
    maximize = True
    nGenerations = nObjects*5
    popSize = nObjects*10
    genSize = int(math.floor( popSize/10 ))
        
    # Genetic algorithm
    ch = Core.Genotype(segments=[GenotypeLibrary.BinaryChromosomeSegment(nBits=1) for i in range(nObjects)])
    print ch
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
#    ga.runGA(nGenerations)
    
    print 'Object Volumes', objectVolumes
    print 'Object Costs', objectCosts
    print 'Max Volume', maxVolume
    print 'Volume Lambda', volumeLambda