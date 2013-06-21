import Core

## @class BaseEvaluationOperator
#  @brief This class provides an easy way of developing evaluation operators that only evaluate recently replaced individuals
class BaseEvaluationOperator(Core.GeneticOperator):
    ## @fn evaluateIndividual(self, individual)
    #  @brief This function evaluates one individual; Overload this function on all derived operators
    def evaluateIndividual(self, individual):
        individual.fitness = 0.0
    ## @fn evaluate(self, population)
    #  @brief This function applies the evaluateIndividual function to every recently replaced individual in the population
    def evaluate(self, population):
        # Evaluate only recently generated items (pointed to by population.lethals)        
        lethals = getattr(population, 'lethals', None )
        #  If population.lethals does not exist, update every individual (and set the lethals list to contain every index)
        if not lethals:
            lethals = range(len(population.individuals))        
        # Iterate over recently replaced individuals
        for i in lethals:
            self.evaluateIndividual(population.individuals[i])
            
    initialize = evaluate
    iterate    = evaluate
    finalize   = evaluate
