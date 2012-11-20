import copy
import random
from Core import *

## @class BinaryChromosomeSegment
#  @brief This class implements an integer variable encoded by a fixed number of bits
#  @todo: TikZ diagram for this class
# 
#  This class encodes an integer variable using nBits.  
class BinaryChromosomeSegment(BaseChromosomeSegment):
    ## @fn __init__(self, nBits, data)
    #  @param nBits The number of bits for this chromosome segment
    #  @param data The data contained in this chromosome segment
    #  @brief Initialization function for the BinaryChromosomeSegment class
    #
    #  Any named arguments passed to the constructor will be stored on a property with the same name
    def __init__(self, nBits=1, data=None, **kwargs):
        super(BinaryChromosomeSegment, self).__init__(nBits=nBits, data=data, **kwargs)
    
    ## @fn __str__(self)
    #  @brief This function returns the hexadecimal representation of this object
    #  @return A string that contains the hexadecimal representation of this object
    def __str__(self):
        b = bin( self.data )
        return b[:2] + '0' * ( 2+self.nBits-len(b) ) + b[2:]
    
    ## @fn maxValue
    #  @brief Return the maximum value allowed to this chromosome
    #
    #  The max value is determined using this formula: (1<<self.nBits) -1, which is equivalent to the familiar equation \f$ 2^{nBits} -1\f$ 
    def maxValue(self):
        return (1<<self.nBits)-1
    
    ## @fn randomize(acceptFunction = lambda x: True)
    #  @brief Set the chromosome value to a random value
    def randomize(self):
        self.data = random.randint(0, self.maxValue())

    ## @fn __setattr__(self, attr, value)
    #  @brief This function insures that nBits is an integer and that data value never exceeds maxValue(self)   
    def __setattr__(self, attr, value):
        if attr=='nBits':
            v = int(value)
        elif attr=='data':
            v = int(value) & self.maxValue()
        else:
            v = value
        super(BinaryChromosomeSegment, self).__setattr__(attr, value)
    
    ## @fn crossover
    #  @brief Cross two chromosomes choosing a single cross point within the limits of self.    
    #  @return A new BinaryChromosomeSegment object that contains the result of combining self and other
    def crossover(self, other):
        crossPoint = (1<<random.randint(0,self.nBits))-1;
        return BinaryChromosomeSegment(nBits=self.nBits, data=((self.data&crossPoint) | (other.data - (other.data&(~crossPoint)))))
    
    ## @fn mutate(self)
    #  @brief Perform a single bit mutation within the range of self
    def mutate(self):
        self.data = self.data ^ (1<<random.randint(0,self.nBits-1))

