import Core
import EvaluationOperators
import PlottingOperators

import math
import random
import itertools
import matplotlib.pyplot

## @fn euclideanDistance(u, v)
#  @brief Compute the euclidean distance between two n-dimensional points
def euclideanDistance(u, v):
    return math.sqrt(reduce(lambda x,y: x+y, [ (u[dim]-v[dim])**2 for dim in range(len(u)) ]))

## @class Graph
#  @brief This class 
class Graph(Core.GABaseObject):
    ## @fn __init__(V,E,W,N,**kwargs)
    #  @brief This class models a weighted, directed graph.
    #  @param V A list of of node coordinates, if it is not provided, a random set of coordinates will be produced
    #  @param W A matrix (or list of lists) that contains the edge costs, if not provided, the graph will compute the euclidean distance between nodes
    #  @param N if both V and W are omitted, 
    #  
    #  W must be of size len(V) x len(V) to contain the weights of the graph edge; W[j][i] -> is the cost of going from j to i, nonexisting edges should be represented using the None object; If this parameter is not 
    def __init__(self, V=None, W=[], N=5, **kwargs):
        # Get V from arguments or generate a random set of coordinates
        if V:
            self.V = V;
        else:            
            self.randomizeNodePositions(N)
            
        # Get W from arguments or compute the euclidean distance between node coordinates 
        if W:
            self.W = W
        else:
            self.updateW()
        # Run teh superclass constructor for the rest of the arguments    
        super(Graph, self).__init__(**kwargs)
    
    ## @fn updateW(self)
    #  @brief Update the weight matrix to be consistent with the current node positions
    def updateW(self):
        N = len(self.V)
        # Create a list N of lists of size N
        self.W = [ [0 for i in range(N)] for j in range(N) ]
        # Loop over origin nodes
        for j in range(N):
            # Loop over destinations
            for i in range(j, N):
                # Compute the distance
                d = euclideanDistance(self.V[j], self.V[i])
                # This part assumes that edges are symmetrical, i.e. w[i,j] = w[j,i] 
                self.W[j][i] = d
                self.W[i][j] = d
    
    ## @fn pathLength(self, path)
    #  @brief Compute the length of a path
    #  @param path An iterable that returns the nodes in the desired path
    def pathLength(self, path):
        length  = 0.0
        pivot = path[0]
        for vertex in path[1:]:
            length += self.W[pivot][vertex]
            pivot = vertex
        return length
    
    ## @fn __str__(self)
    #  @brief  A human readable representation of the graph
    #  @return Return a multi-line string representation of the graph
    def __str__(self):
        msg = 'Vertices:\n%s\n' % '\n'.join( '\t(%s)' % ', '.join('%1.3E'%i for i in v) for v in self.V )
        msg += 'Edges:\n%s' % '\n'.join( '\t[%s]' % ', '.join('%1.3E'%i for i in row) for row in self.W )
        return msg
    
    ## @fn __setattr__(self, attribute, value):
    #  @brief Validate that the attributes V and W are consistent
    def __setattr__(self, attribute, value):
        if attribute=='V':
            value = list(value)
        elif attribute=='W':
            n = len(self.V)
            if not all(len(row)==n for row in value):
                raise IndexError('Every row in the weight matrix (W) must have size %d' % n)
            elif not len(value)==n:
                raise IndexError('Weight matrix must be of size %d' % n)
        super(Graph, self).__setattr__(attribute, value)
    
    ## @fn randomize(self, n=None)
    #  @brief Randomize the node positions and modify V
    #  @param n If n is omitted, the number of nodes in the graph remains unchanged, but their positions are changed
    #  @param d This parameter generates nodes in an multi-dimensional universe with d dimensions, the default is a 2-D universe
    def randomizeNodePositions(self, n=None, d=2):
        if n == None:
            n = len(self.V)
        self.V = [ tuple(random.random() for j in range(d)) for i in range(n) ]
        self.updateW()
    
    ## @fn plot(self, edges)
    #  @brief Plot the graph using matplotlib
    #  @param paths A list of tuples. Each tuple contains a path to plot over the graph
    #  @todo Support 3-D plots and path animations     
    def plot(self, paths=None, axes=None):
        if paths==None:
            paths = itertools.combinations(range(len(self.V)), 2)
        if axes==None :
            axes = matplotlib.pyplot
        for p in paths:
            x, y = zip( *[ self.V[vertex] for vertex in p ] )
            axes.plot(x, y)

        vx, vy = zip( *self.V )
        axes.plot(vx, vy, 'ro')

## @class Ordonez(Core.GeneticOperator)
#  @brief A GeneticAlgorithm::Core::GeneticOperator derivate that decodes a binary genotype as a permutation of the numbers 0:n, where n is the number of segments in the genotype 
class Ordonez(EvaluationOperators.BaseEvaluationOperator):    
    ## @fn evaluateIndividual(self, population)
    #  @brief Decode the binary genotype on each individual, and replace the phenotype with the resulting permutation
    # 
    #  Algorithm:
    #    <ol>
    #        <li>Start permutation with edge 0</li>
    #        <li>For each segment j in the genotype: 
    #            <ol>
    #            <li>Compute the integer residue of dividing the jth value by j+1</li>
    #            <li>Insert the j+1 thn node in the position computed above</li>
    #            </ol> </li>
    #
    #  This algorithm guarantees valid hamiltonian cycles over a completely-connected graph. 
    def evaluateIndividual(self, individual):
        # All permutations start with 0         
        perm = [0];
        geno = [segment.data for segment in individual.genotype.segments]
        for j in range(len(geno)):                
            position = geno[j] % (j+2)
            perm.insert(position, j+1)
            
        individual.phenotype = perm;

## @class PathLengthFitness(Core.GeneticOperator)
#  @brief A GeneticAlgorithm::Core::GeneticOperator derivate that uses  
class PathLengthFitness(EvaluationOperators.BaseEvaluationOperator):
    def __init__(self, graph=None, **kwargs):
        super(PathLengthFitness, self).__init__(**kwargs)
        if graph==None:
            graph = Graph()
        self.graph = graph
    
    # @fn evaluateIndividual(self, individual)
    # @brief Use the graph's weight matrix to compute the length of the path contained in the individual's phenotype
    def evaluateIndividual(self, individual):
        path = individual.phenotype + individual.phenotype[0:1]
        individual.fitness = self.graph.pathLength(path)

## @todo Make a node matching decoding, evaluation and logger/plotter
## @todo Make an edge/node covering decoding, evaluation and logger/plotter


## @class BestPathPlotLogger
#  @brief This class extends the PlottingOperators::PlotBestLogger to display the best tour found so far.
class BestPathPlotLogger(PlottingOperators.PlotBestLogger):
    ## @fn __init__(self, graph=None, criterionAxis=None, graphAxis=None, figure=None, **kwargs):
    #  @brief The genetic operator constructor
    #  @param graph The graph used to plot paths
    #  @pram criterionAxis A matplotlib axes object, used to plot the best found evaluation so far
    #  @param graphAxis The matplotlib axes object used to display the best found tour so far
    #  @param figure The figure that contains both the criterion and graph axis
    #
    #  Any parameter can be omitted, in that a new object of the required type will be created to initialize properties
    def __init__(self, graph=None, criterionAxis=None, graphAxis=None, figure=None, maximize=False, **kwargs):
        if graph==None:
            graph = Graph()
        if (criterionAxis == None) and (graphAxis==None):
            figure, (criterionAxis, graphAxis) = matplotlib.pyplot.subplots(1, 2)
        super(BestPathPlotLogger, self).__init__(criterionAxis, figure, **kwargs)
        self.graph = graph;
        self.graphAxis = graphAxis
        self.maximize = maximize        
    
    ## @plotGraphCallback(self, population):
    #  @brief This function is invoked periodically and displays the best found so far tour, and the historic evaluations plot
    #  @param population The current population where a new best is searched for 
    def plotGraphCallback(self, population):
        if len(self.bestLog) >= 1:
            path = (self.bestLog[-1].phenotype[i] for i in range(len(self.graph.V)) + [0] )
            self.graphAxis.cla()
            self.graph.plot(axes=self.graphAxis, paths=[path])
        super(BestPathPlotLogger, self).plotCallback(population)        
        
    iterationCallback  = plotGraphCallback
    evaluationCallback = plotGraphCallback
        
if __name__=='__main__':
    import time
    import matplotlib.pyplot
    matplotlib.pyplot.interactive(True)
    g = Graph()
    for i in range(10):
        g.randomizeNodePositions()
        matplotlib.pyplot.cla()
        g.plot()
        matplotlib.pyplot.draw()
        time.sleep(1/10.0)
    matplotlib.pyplot.show()