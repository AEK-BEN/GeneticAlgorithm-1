import Core
import LoggingOperators
import matplotlib.pyplot as plt

class PlotBestLogger(LoggingOperators.BestLogger):
    def __init__(self, **kwargs):
        # Call parent initializer
        super(PlotBestLogger, self).__init__(**kwargs)
        # Configure matplotlib.pyplot to operate interactively
        ## @todo Receive an axes pointer during initialization and plot to that axes upon iteration
        plt.interactive(True)
        
    def plotCallback(self, population):
        super(PlotBestLogger, self).logCallback(population)
        criteria = [getattr(individual, self.criterion) for individual in self.bestLog]
        plt.cla()
        plt.plot(self.numEvaluations, criteria)
        plt.title( 'Best found so far' )
        plt.xlabel( 'number of evaluations' )
        plt.ylabel( self.criterion )
        plt.draw()
        
    iterationCallback  = plotCallback
    evaluationCallback = plotCallback
        
    def finalize(self, population):
        super(PlotBestLogger, self).finalize(population)
        plt.show(block=True)
