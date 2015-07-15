import math

# # @class FuzzyLogicBaseObject
#  @brief The base object provides the functions repr and str
#
#  The FuzzyLogicBaseObject provides a custom behavior for FuzzyLogic objects, which allows for a useful repr() and str() implementation.
#  Because every object on this library is derived from this class, the whole scope of the library can be appreciated in this class' inheritance diagram.
class FuzzyLogicBaseObject(object):
    # # @__init__(self, **kwargs)
    #  @brief The default behavior for FuzzyLogic objects 
    # 
    #  The default behavior of FuzzyLogic objects is to accept any kind of named arguments on their constructor, and save them in properties with the same name.
    def __init__(self, **kwargs):
        for param, val in kwargs.items():
            self.__setattr__(param, val)    
    # # @fn __repr__(self)
    #  @brief The string representation of the object
    #
    #  The default behavior of FuzzyLogic objects is return representations as the Python code needed to reproduce the instance self
    def __repr__(self):
        return '%(class)s(%(params)s)' % \
            { 'class':type(self).__name__, \
              'params':', '.join([str(prop) + ' = ' + repr(value) for prop, value in vars(self).iteritems()]) }
    # # @fn __str__(self)
    #  @brief The string representation of the object
    #
    #  The default str() representation of FuzzyLogic objects is to return repr()
    def __str__(self):
        return repr(self)
    
class FuzzySet(FuzzyLogicBaseObject):
    
    # # @fn fuzzify(input)
    #  Return a double value that reflects a membership function
    def fuzzify(self, x):
        return 0.0
    
class TriangularSet(FuzzySet):
    
    def __init__(self, lowerLimit=-1, center=0, upperLimit=1, **kwargs):
        super(TriangularSet, self).__init__(**kwargs)
        self.lowerLimit = lowerLimit
        self.center = center
        self.upperLimit = upperLimit
    
    def fuzzify(self, x):
        output = 0.0
        if x >= self.lowerLimit and x <= self.upperLimit :
            if x < self.center:
                output = (x - self.lowerLimit) / (self.center - self.lowerLimit)
            else:
                output = 1 - ((x - self.center) / (self.upperLimit - self.center))
            
        return output
    
class GaussianSet(FuzzySet):
    def __init__(self, center=0, sigma=1, **kwargs):
        super(GaussianSet, self).__init__(**kwargs)
        self.center = center
        self.sigma = sigma
    
    def fuzzify(self, x):
        num = -math.pow(x - self.center, 2)
        den = 2 * math.pow(self.sigma, 2)
        return math.exp(num / den)

class NDFuzzifier(FuzzySet):
    
    def __init__(self, *sets, **kwargs):
        super(NDFuzzifier, self).__init__(**kwargs)
        self.sets = sets
        
    def fuzzify(self, *x):
        output = 1.0
        for xx, f in zip(x, self.sets):
            output *= f.fuzzify(xx)
        return output