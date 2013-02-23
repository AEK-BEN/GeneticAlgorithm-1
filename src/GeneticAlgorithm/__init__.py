import copy
import random
import Core
import GenotypeLibrary
import EvaluationOperators
import SelectionOperators
import LoggingOperators
import PlottingOperators
import GraphLibrary

## @mainpage The GeneticAlgorithm documentation
#
#  @copyright <a href="http://www.gnu.org/licenses/gpl.html"> GNU Public License </a> 
#
#  @section MainIntroduction Introduction
#    Hola!
#    
#    This is the documentation page for the GeneticAlgorithm framework. This framework can be freely distributed and used for non-comercial purposes. Any comercial uses are still free, but required to provide this code to comply with the GNU public license and to notify the author (david.said@gmail.com) who can use reference the commercial application for marketing and promotion purposes. Non commercial applications, especially educational are also encouraged to establish contact and provide feedback to the author.   
#    
#    This framework is designed with little external dependencies, but there are some. It has been written with Python 2.7 in mind, however, if enough demand for a python 3 compliant implementation is present, I will gladly make an effort. The only known dependency so far is matplotlib, which is referenced in the install and external dependencies sections below.  
#
#    Please keep in mind that this framework is a work in progress, and better documentation will gradually be produced. In the meantime, do contact me with any questions you may have, I will be happy to answer.
#
#  @section MainDependencies External dependencies and useful links.
#  @subsection MainPython Python 2.7 and tutorials
#    This framework is designed to run on Python 2.7. The links below provide some useful links for Python beginners: 
#    <ul>
#        <li> Introduction: <a href="http://docs.python.org/tutorial/appetite.html">Whetting your appetite.</a></li>
#        <li> Python Download: <a href="http://www.python.org/download/releases/2.7/">python.org</a></li>
#    </ul>
#
#  @subsection MainGit Git tutorials and download
#    You may have noticed that this framework uses GIT version control. I find it very useful and stable, but I'm a beginner myself. Please look at these links to find out how to use it properly and make the most out of it:
#    <ul>
#        <li>Introduction: <a href="http://gitref.org/basic/">GitRef</a></li>
#        <li>Download: <a href="http://git-scm.com/">git-scm.com</a></li>
#    </ul>
#    
#  @subsection MainMatplotlib Matplotlib
#    Some of the framework operators use matplotlib to produce graphics and plots. Please refer to the links below for more information
#    <ul>
#        <li>Documentation: <a href="http://matplotlib.org/contents.html">matplotlib.org</a></li>
#        <li>Download: <a href="http://matplotlib.org/">matplotlib.org</a></li>
#    </ul>
#
#  @section MainInstall Installation instructions
#    
#  <ol>
#    <li>Clone this repository to your system using your favorite method. Refer to the links above if required.</li>
#    <li>Install Python and Matplotlib. Again, refer to the links above if necessary.</li>
#    <li>Add the src/ directory to your PYTHONPATH. Take a look at this <a href="http://www.stereoplex.com/blog/understanding-imports-and-pythonpath">article</a> by Dan Fairs if you need more information.</li>
#    <li>Run the /src/examples/GADemo.py to test your installation. If it works, you're done!</li>
#  </ol>