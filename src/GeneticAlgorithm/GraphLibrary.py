import Core
import random
import math

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
            self.V = [ (random.random(), random.random()) for i in range(N) ]
        # Get W from arguments or compute the euclidean distance between node coordinates 
        if W:
            self.W = W;
        else:
            N = len(self.V)
            # Create a list N of lists of size N
            self.W = [ [0 for i in range(N)] for j in range(N) ]
            distance = lambda u, v : math.sqrt(reduce(lambda x,y: x+y, [ (u[dim]-v[dim])**2 for dim in range(len(u)) ]))
            for j in range(N):
                for i in range(j, N):
                    d = distance(self.V[j], self.V[i]) 
                    self.W[j][i] = d
                    self.W[i][j] = d
        # Run teh superclass constructor for the rest of the arguments    
        super(Graph, self).__init__(**kwargs)
    
    def __str__(self):
        msg = 'Vertices:\n%s\n' % '\n'.join( '\t(%s)' % ', '.join('%1.3E'%i for i in v) for v in self.V )
        msg += 'Edges:\n%s' % '\n'.join( '\t[%s]' % ', '.join('%1.3E'%i for i in row) for row in self.W )
        return msg
        
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
    
    def randomize(self, n):
        self.V = range(1, n+1)
        
    def plot(self, edges=None):
        import itertools
        import matplotlib.pyplot as plt
        if edges==None:
            edges = itertools.combinations(range(len(self.V)), 2)
        for e in edges:
            x, y = zip( *[ self.V[vertex] for vertex in e ] )
            plt.plot(x, y, 'k-')
        vx, vy = zip( *self.V )
        plt.plot(vx, vy, 'ro')


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
    import matplotlib.pyplot as plt
    import time
    plt.interactive(True)
    for i in range(60):
        g = Graph()
        plt.cla()
        g.plot()
        plt.draw()
        time.sleep(1/60.0)
    plt.show()