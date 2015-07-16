from FuzzyLogic.Core import TriangularSet, GaussianSet, NDFuzzifier
import numpy as np
import math
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm

low = -4*math.pi
high = 4*math.pi
x = np.linspace(low, high, 101, True)
X, Y = np.meshgrid(x, x)

fuzzifier = NDFuzzifier(TriangularSet(-math.pi, 0, 2*math.pi), GaussianSet(0.5, 3))

f = np.vectorize(fuzzifier.fuzzify)
Z = f(X, Y)



fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.3)
cset = ax.contour(X, Y, Z, zdir='z', offset=-0.5)
cset = ax.contour(X, Y, Z, zdir='x', offset=low)
cset = ax.contour(X, Y, Z, zdir='y', offset=low)

ax.set_xlabel('X')
ax.set_xlim(low, high)
ax.set_ylabel('Y')
ax.set_ylim(low, high)
ax.set_zlabel('Z')
ax.set_zlim(-0.5, 1.5)

plt.show()
