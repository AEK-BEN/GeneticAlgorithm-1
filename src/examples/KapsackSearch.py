from GeneticAlgorithm.Core import GABaseObject as BaseObject
import random

class SearchNode(BaseObject):
    # Create a new node, and compute its cost
    def __init__(self, solution=[], objectCosts=[], objectVolumes=[]):
        self.solution = solution
        if solution != []:
            self.cost = self.solutionCost(objectCosts)
            self.volume = self.solutionVolume(objectVolumes)
        else:
            self.cost = 0
            self.volume = 0
    
    # Return adjacent solutions
    def neighbors(self, objectCosts, objectVolumes, maxVolume):
        if len(self.solution) == len(objectVolumes):
            return []
        else:
            neighbors = [SearchNode( solution=self.solution + [b], objectCosts=objectCosts, objectVolumes=objectVolumes )\
                         for b in range(2)]
            return [n for n in neighbors if not n.exceedsVolume(maxVolume)]
    
    # Returns true if the current node exceeds the maximum volume
    def exceedsVolume(self, maxVolume):
        return (self.volume > maxVolume)
    
    # Returns the current node solution cost
    def solutionCost(self, objectCosts):
        return reduce(lambda x,y:x+y, [self.solution[i]*objectCosts[i] for i in range(len(self.solution))])

    def solutionVolume(self, objectVolumes):
        return reduce(lambda x,y:x+y, [self.solution[i]*objectVolumes[i] for i in range(len(self.solution))])

    # Determines if two nodes are equal
    def __eq__(self, other):
        return self.solution == other.solution

class SearchManager(BaseObject):
    # Create a new search
    def __init__(self, objectVolumes, maxVolume, objectCosts):
        # Store the parameters
        self.objectVolumes = objectVolumes
        self.objectCosts = objectCosts
        self.maxVolume = maxVolume
        
        self.nExpansions = 0;
        
        initialNode = SearchNode(solution=[], objectCosts=self.objectCosts, objectVolumes=self.objectVolumes)
        self.openNodes = [initialNode]
        self.closedNodes = []
        self.bestFound = initialNode
    
    # Expand one node
    def expand(self):
        # Choose the node with the highest cost
        i, node = max( enumerate(self.openNodes), key=lambda t: t[1].cost )
        # Remove the node from the list of open nodes and append it to the list of closed nodes
        self.closedNodes.append( self.openNodes.pop(i) )
        print 'Expanding ', str(node)
        self.nExpansions += 1
        # Get the node's neighbors
        neighbors = node.neighbors(objectCosts=self.objectCosts, objectVolumes=self.objectVolumes, maxVolume=self.maxVolume)
        # Examine every neighbor
        for n in neighbors:
            # If the neighbor is either the open or closed node lists
            #  or the cumulative cost is already greater than the best found and the cost is smaller at the same time
            #  discard the neighbor, otherwise, append it to the list of the open nodes
            if (n not in self.openNodes) and\
               (n not in self.closedNodes) and\
               not (n.volume >= self.bestFound.volume and n.cost < self.bestFound.cost):
                # Append the node to the list of open nodes
                self.openNodes.append(n)
                # If the node has a better cost than the 
                if n.cost > self.bestFound.cost:
                    self.bestFound = n
                    print 'New best found:', str(n)
            else:
                'Discarding ', str(n)
    
    # Expand all nodes in the open list until it's exhausted
    def run(self):
        while len(self.openNodes) > 0:
            self.expand()
        print 'Best found', self.bestFound
        return self.bestFound
                    
                    
        
if __name__ == '__main__':
    random.seed(0)

    # Kanpsack instance parameters
    nObjects =  12
    
    objectVolumes = [random.randrange(1, 20) for i in xrange(nObjects)]
    objectCosts = [random.randrange(10, 20) for i in xrange(nObjects)]
    maxVolume = reduce(lambda x, y: x+y, objectVolumes) / 2
    volumeLambda = maxVolume*10;
    
    search = SearchManager(objectVolumes, maxVolume, objectCosts)
    search.run()
    print 'Number of expansions', search.nExpansions
    print 'Object Volumes', objectVolumes
    print 'Object Costs', objectCosts
    print 'Max Volume', maxVolume
    print 'Volume Lambda', volumeLambda
            
    
    
    