## @file GABaseObject-demo.py
#  @brief This file demonstrates the usage model of the GABaseObject function

from GeneticAlgorithm.Core import GABaseObject

# This class exemplifies the advantages of deriving a class from the GABaseObject. 
# Let's have it inherit every function and property from the GABaseObject with no change.
class GeneticExampleClass(GABaseObject):
    pass

# We can make an instance of the class, passing any number of named arguments to the constructor
obj = GeneticExampleClass( name='Example', propertyA=1, propertyB={'key':'value'} )

# We can use the str() or repr() command to print the object
print str(obj) == repr(obj), str(obj)
print obj.name
