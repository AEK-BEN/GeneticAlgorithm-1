import copy
import random


## @class GABaseObject
#  @brief The base object provides the functions repr and str
#
#  The GABaseObject provides a custom behavior for GA objects, which allows for a useful repr() and str() implementation.
#  Because every object on this library is derived from this class, the whole scope of the library can be appreciated in this class' inheritance diagram.
class GABaseObject(object):
    ## @__init__(self, **kwargs)
    #  @brief The default behavior for GA objects 
    # 
    #  The default behavior of GA objects is to accept any kind of named arguments on their constructor, and save them in properties with the same name.
    def __init__(self, **kwargs):
        for param, val in kwargs.items():
            self.__setattr__(param, val)    
    ## @fn __repr__(self)
    #  @brief The string representation of the object
    #
    #  The default behavior of GA objects is return representations as the Python code needed to reproduce the instance self
    def __repr__(self):
        return '%(class)s(%(params)s)' %   \
            { 'class':type(self).__name__, \
              'params':', '.join( [str(prop)+' = '+ repr(value) for prop, value in vars(self).iteritems()] ) }
    ## @fn __str__(self)
    #  @brief The string representation of the object
    #
    #  The default str() representation of GA objects is to return repr()
    def __str__(self):
        return repr(self)

## @class GeneticOperator
#  @brief GeneticOperator is the base class that should be used to implement selection, crossover and mutation
#
#  The class GeneticAlgorithm is a scheduler for that periodically uses objects of this kind to transform the current population. This class can be derived to perform any activity, inclyuding but not limited to:
#  <ul>
#    <li>Logging, computing statistics about populations</li>
#    <li>Interpretation or decoding: Genotype \f$ \rightarrow \f$ Phenotype</li>
#    <li>Evaluation: Phenotype \f$ \rightarrow \f$ fitness</li>
#    <li>Crossover: Genotype \f$\times\f$ Genotype \f$ \rightarrow \f$ Genotype</li>
#    <li>Mutation: Genotype \f$ \rightarrow \f$ Genotype</li>
#  </ul>
#  Every genetic operator may overload any combination of these functions:
#  <ul>
#    <li>initialize</li>
#    <li>iterate</li>
#    <li>finalize</li>
#  </ul>
#  All of these functions receive a population object, which is expected to be modified by the function in order to implement the desired transformation.
#  Please note that a single operator could implement a full genetic algorithm, but modularization is encouraged to allow easy re-use of operators 
class GeneticOperator(GABaseObject):
    ## @fn initialize(population)
    #  @param population The population object to operate upon
    #  @brief This function is called once, during the startup phase of the algorithm
    def initialize(self, population):
        pass
    ## @fn iterate(population)
    #  @param population The population object to operate upon
    #  @brief This function is called once every iteration
    def iterate(self, population):
        pass
    ## @fn finalize(population)
    #  @param population The population object to operate upon
    #  @brief This function is called once at the end of the algorithm run
    def finalize(self, population):
        pass
    
## @class Mutate
#  @brief Mutate an individual
class Mutate(GeneticOperator):
    def mutate(self, population):
        pm = getattr(population, 'mutation_probability', 0.01 )        
        # Evaluate only recently generated items (pointed to by population.lethals)        
        lethals = getattr(population, 'lethals', None )
        #  If population.lethals does not exist, update every individual (and set the lethals list to contain every index)
        if not lethals:
            lethals = range(len(population.individuals))
        # Iterate over recently replaced individuals
        for i in lethals:
            if random.random() < pm:
                population.individuals[i].mutate()
    iterate = mutate

## @class Crossover
#  @brief Crossover two individuals from population.matingPool with probability population.crossoverProbability
class Crossover(GeneticOperator):
    def cross(self, population):
        pc = getattr(population, 'crossover_probability', 1.0 )
        # Get the vector of pointers to lethals from population        
        lethals = getattr(population, 'lethals', None)
        # If no vector is available, then all individuals are scheduled for replacement
        if not lethals:
            lethals = xrange(len(population.individuals))
        # Get the number of individuals to replace
        nLethals = len(lethals)
        # Initialize a list of offspring vectors
        offspring = [None] * nLethals        
        # Get the mating pool from the population
        matingPool = getattr(population, 'matingPool', None)
        # If no mating pool is available, raise an error
        if not matingPool:
            raise RuntimeError('No mating pool found on population, a selection operator must come before Crossover')
        # Generate the offspring and insert them in different loops, to conserve the parents unchanged for crossover   
        for i in xrange(nLethals):
            if random.random() < pc:         
                offspring[i] = population.individuals[ matingPool[0] ].crossover( population.individuals[ matingPool[1] ] )
            else:
                offspring[i] = copy.deepcopy(population.individuals[ matingPool[0] ])
            matingPool = matingPool[2:]
        # Insert the offspring in the population
        for i, o in zip(lethals, offspring):
            population.individuals[i] = o    
    iterate = cross;
    
## @class BaseChromosomeSegment
#  @brief This class defines the minimal expression of a chromosome segment.
#
#  This class defines the minimal expresion of a chromosome. This interface contains:
#  <ul>
#    <li>data: The data contained in this segment</li>
#    <li>crossover: Implements the algorithm to combine two chromosome segments</li>
#    <li>mutation: Implements the algorithm to mutate this segment</li>
#    <li>randomize: Assign a valid, random value to self.data</li>
#  </ul> 
class BaseChromosomeSegment(GABaseObject):
    ## @fn __init__(self, data=0, **kwargs)
    #  @brief A constructor that takes data and any number of named arguments, and adds all properties to the object
    #  @param data The data to assign to this segment
    # 
    #  Deriving from this class guarantees the following basic behavior, which is assumed by other GAObject classes:
    # 
    #  <ul>
    #    <li> The data property contains will be used by decode functions to produce a Penotype </li>
    #    <li> The constructor generates a random value for data whenever its not provided </li>
    #    <li> The constructor accepts any number of named arguments, which will be stored in properties of the same name</li>
    # </ul>
    #
    # The methods randomize, crossover and mutate must be re implemented on every specialization of this class. 
    def __init__(self, data=None, **kwargs):
        # Set all named properties first
        super(BaseChromosomeSegment, self).__init__(**kwargs)
        ## @property data This property returns the data used to produce a Genotype
        if data:
            ## @property data
            #  @brief The property that stores the chromosome segment value
            self.data  = data
        else:
            # If no data was provided, randomize the chromosome segment
            self.randomize()
        
    ## @fn randomize(self)
    #  @brief Assign a valid, random value to self.data
    def randomize(self):
        pass
    
    ## @fn crossover(self, other)
    #  @param other Another chromosome segment to be combined with self
    #  @brief This function is the crossover operator interface, and must be implemented for the default crossover functions to work
    #  @note It is recommended that all specializations of this function return a new object, sing the classes Genotype and Individual are containers and handle refereces exclusively. The generation of new chromosome segments is always delegated to this and the constructor functions.
    def crossover(self, other):
        pass
    ## @fn mutate(self)
    #  @brief This function is the mutation operator interface, and must be implemented for the default mutation functions to work 
    def mutate(self, chromo):
        pass

## @class Genotype
#  @brief The base Genotype class from which all chromosomes must derived
#
#  The Genotype class is primarily a container that supports the minimum GA interface:
#  <ul>
#      <li>randomize(self)</li>
#      <li>mutate(self)</li>
#      <li>crossover(self, other)</li>
#  </ul>
class Genotype(GABaseObject):
    ## @fn init(segments=[])
    #  @brief Initialize the genotype
    #  @param segments A list of BaseChromosomeSegment or derived objects 
    def __init__(self, segments=[]):
        self.segments = segments
    ## @fn __setattr__(self, attribute, value)
    #  @brief This function allows typechecking to occur for segments, without the need for accessors
    def __setattr__(self, attribute, value):
        if attribute == 'segments':
            super(Genotype, self).__setattr__(attribute, [])
            for seg in value:
                self.addSegment(seg)
        else:
            super(Genotype, self).__setattr__(attribute, value)
    ## @fn randomie(self)
    #  @brief Assign a random value to every segment
    def randomize(self):
        for s in self.segments:
            s.randomize()
    ## @fn addSegment(self, segment)
    #  @brief Add a segment to the genotype.        
    def addSegment(self, segment):
        if isinstance(segment, BaseChromosomeSegment):
            self.segments.append(segment)
    ## @fn crossover(self, other)
    #  @brief Perform a one-point crossover between self an and other Genotype
    #  @return A Genotype object that contains the new genotype
    #  @warning Segments are references to objects. It is recommended that 
    def crossover(self, other):
        crossPoint = random.randrange( len(self.segments) )
        return Genotype( self.segments[:crossPoint] + \
                           [ self.segments[crossPoint].crossover(other.segments[crossPoint]) ] + \
                           other.segments[crossPoint+1:] )
    ## @fn mutate(self)
    #  @brief Select one segment randomly and call mutate() on it
    def mutate(self):
        mutant = random.randrange( len(self.segments) )
        self.segments[mutant].mutate()
    ## @fn __str__(self)
    #        
    def __str__(self):
        return '[%s]' % ', '.join([str(s) for s in self.segments])
    
##  @example GABaseObject-demo.py
#   This example shows the usage model for the GABaseObject class
## @class Individual
#  @brief This class is a container intended to store all information relevant to an individual.
#
#  This class is a container, intended to store all information relevant to an individual, including but not limited to:
#  <ul>
#    <li>Genotype</li>
#    <li>Phenotype</li>
#    <li>Evaluation</li>
#    <li>Non-generational information, such as:</li>
#      <ul>
#        <li>Age</li>
#        <li>Fitness moving average</li>
#        <li>Fitness variance</li>
#      </ul>
#  </ul>             
class Individual(GABaseObject):
    ## @fn __init__(self, genotype=[], **kwargs)
    #  @brief The individual constructor
    #
    #  The minimum expression of an individual is to have a genotype and fitness value. Any other imaginable property can be added at this stage by passing a named parameter 
    def __init__(self, genotype=Genotype(), fitness=0.0, **kwargs):
        super(Individual, self).__init__(genotype=genotype, fitness=fitness, **kwargs)        
            
    ## @fn randomize(self)
    #  @brief Call self.genotype.randomize()
    def randomize(self):
        self.genotype.randomize()
        
    ## @fn valuesToStr(self)
    #  @brief Return the string representation of the values of all properties
    #  @param separator The string that separates property values
    #  @return The string representation of the values of all properties separated by the optional separator string      
    def valuesToStr(self, separator='\t'):        
        return separator.join( [str(value) for value in vars(self).itervalues()] )
    
    ## @fn propertiesToStr(self)
    #  @brief Return the names of all properties in the order that valuesToStr prints them
    #  @param separator The string that separates property names
    #  @return The names properties separated by the optional separator string          
    def propertiesToStr(self, separator='\t'):
        return separator.join( [str(prop) for prop in vars(self).iterkeys()] )
    
    ## @fn __str__(self)
    #  @brief Return a string representation of self, accordin to the function toStr
    # 
    #  The behavior of this function can be easily changed with the following technique:
    #  @code
    #  Individual.__str__ = lambda(self) : self.toStr(propertyList=['property1', 'property2', ...])
    #  @endcode
    #  Where the propertyList is a list of strings containing the names of the properties to display
    def __str__(self):
        return self.valuesToStr()

    ## @fn crossover(self, other)
    #  @brief Crossover self and another genotype
    #  @return an Individual object containing the crossover of self and other
    def crossover(self, other):
        offspring = copy.deepcopy(self)
        offspring.genotype = offspring.genotype.crossover( other.genotype )
        return offspring
    
    ## @fn mutate
    #  @brief call mutate() on self's chromosome
    def mutate(self):
        self.genotype.mutate()
    
## @class Population
#  @brief This class is a container, intended to store references to individuals and all their     
class Population(GABaseObject):
    ## @fn __init__(self, individuals=[], individualSchema=Genotype(), **kwargs)
    #  @brief The Population constructor
    #  @param individuals A list of Individual objects
    #  @param schema A Genotype that will be used as template to produce the genotypes of the population
    #  @parap popSize If popSize is provided, self.populate(popSize) and self.randomize() are called after initialization, note that this overrides the value passed to individuals
    def __init__(self, name='', individuals=[], schema=Genotype(), popSize=None, maximize=True, **kwargs):
        super(Population, self).__init__(name=name, individuals=individuals, schema=schema, maximize=maximize, **kwargs)
        if popSize:
            self.populate(popSize)
            self.randomize()
        
    ## @fn __str__(self)
    #  @brief The string representation of the population
    #
    #  This function prints all variables associated with self. Note that any user-defined property will be printed as well
    def __str__(self):
        msg = [ self.name ]
        for prop, value in vars(self).iteritems():
            if prop == 'name' or prop == 'schema' or prop == 'individuals' :
                continue
            else:
                msg+=[ str(prop) + ': ' + str(value) ]
        msg+= [ 'schema: ' + repr(self.schema) ]
        msg+= [ 'Individuals: (' + self.individuals[0].propertiesToStr(',') + ')' ] + [str(i) + '\t' + str(ind) for i, ind in enumerate(self.individuals) ]    
        return '\n'.join(msg)
    
    ## @fn populate(n=100)
    #  @brief Generate the list of individuals by copying the schema n times
    #  @param n The number of individuals to contain in the population
    def populate(self, n=100):
        self.individuals = [ Individual(genotype=copy.deepcopy(self.schema)) for i in xrange(n) ]
    
    ## @fn randomize(self)
    #  @brief Randomize the population by calling randomize on each individual
    def randomize(self):
        for individual in self.individuals:
            individual.randomize()

## @class Scheduler
#  @brief A class that encapsulates a Population and a list of GeneticOperator
#
#  The class GAShceduler encapsulates a list of GeneticOperator objects and a population.
#  This class is designed to be the highest level of abstraction of a GA. The scheduler applies the genetic operators in order, and provides the following interface:
#
#  <ul>
#    <li>initialize</li>
#    <li>iterate</li>
#    <li>initialize</li>
#  <ul>
class Scheduler(GABaseObject):
    ## @fn __init__(self, name='Untitled', operators=[], population=Population()):
    #  @brief GAScheduler
    def __init__(self, name='Untitled', operators=[], population=Population(), **kwargs):
        super(Scheduler, self).__init__(name=name, operators=operators, population=population, **kwargs)
    ## @fn __str__(self)
    #  @brief Return the string representation of the scheduler
    def __str__(self):
        msg = ['name: ' + str(self.name)]
        msg+= ['\n'.join(['operators:'] + [str(o) for o in self.operators])]
        msg+= ['population: ' + str(self.population)]
        return '\n'.join(msg)

    ## @fn initialize(self)
    #  @brief This function is called at the begining of the runGA method
    #
    #  This function calls the initialize function of every operator on population once. Genetic operators are expected to initialize any variables 
    def initialize(self):
        for o in self.operators:
            o.initialize(self.population)

    ## @fn iterate(self)
    #  @brief This function is called every iteration of the runGA method
    # 
    #  Every operator iterate method over self.population
    def iterate(self):
        for o in self.operators:
            o.iterate(self.population)
    
    ## @fn finalize(self)
    #  @brief This function is called once at the end of the runGA method
    #
    #  Callthe finalize method of every operator at the end of runGA
    def finalize(self):
        for o in self.operators:
            o.finalize(self.population)
    
    ## @fn runGA
    #  @brief Initialize, run n iterations and finalize the GA run
    #  @param n The number of iterations to run
    def runGA(self, n):
        self.initialize()
        for i in xrange(n):
            self.iterate()
        self.finalize()
