import time
import Core
import LoggingOperators
import matplotlib.pyplot

## @class PlotBestLogger
#  @brief A BestLogger specialization that plots the historic progression of the best criterion with each tick
class PlotBestLogger(LoggingOperators.BestLogger):
    #  @fn __init__(self, criterionAxis=None, figure=None, **kwargs)
    #  @brief The genetic operator constructor
    #  @pram criterionAxis A matplotlib axes object, used to plot the best found evaluation so far
    #  @param figure The figure that contains both the criterion and graph axis
    #
    #  Any parameter can be omitted, in that a new object of the required type will be created to initialize properties    
    def __init__(self, criterionAxis=None, figure=None, **kwargs):
        # Call parent initializer
        super(PlotBestLogger, self).__init__(**kwargs)
        # Configure matplotlib.pyplot to operate interactively
        matplotlib.pyplot.interactive(True)
        if criterionAxis==None:
            figure, criterionAxis = matplotlib.pyplot.subplots()
        # Store the target axes
        self.criterionAxis = criterionAxis
        self.figure=figure
        self.figure.show()
    
    ## @fn plotCallback(self, population)
    #  @brief Logs the best found so far using it's parent callback, and then plots the historic progression of the evaluation criteria
    #  @param population The population used to look for the best found so far
    def plotCallback(self, population):
        super(PlotBestLogger, self).logCallback(population)
        if not (self.criterionAxis==None):
            criteria = [getattr(individual, self.criterion) for individual in self.bestLog]
            self.criterionAxis.cla()
            self.criterionAxis.plot(self.numEvaluations, criteria)
            self.criterionAxis.set_title( 'Best found so far' )
            self.criterionAxis.set_xlabel( 'number of evaluations' )
            self.criterionAxis.set_ylabel( self.criterion )
            matplotlib.pyplot.draw()
            matplotlib.pyplot.pause(0.0001)
            
        
    iterationCallback  = plotCallback
    evaluationCallback = plotCallback
    
    ## @fn finalize(self, population)
    #  @brief This function shows the plot one more time, and then blocks to allow the user to choose when the plot window is terminated.
    def finalize(self, population):
        super(PlotBestLogger, self).finalize(population)
        matplotlib.pyplot.show(block=True)
