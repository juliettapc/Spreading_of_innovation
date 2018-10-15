from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.mlab import griddata
import numpy as np
import sys

def main(name):
    fig = plt.figure()
    ax = Axes3D(fig)   #instead of ax = fig.gca(projection='3d')
    
    data = np.genfromtxt(name) #'Landscape_parameters_persuasion_threshold0.5_mutual_encoug0.5_100iter_all_landscape.dat')  
    
    x = data[:,0]   #columns from the datafile
    y = data[:,1]
    z = data[:,4]
    
    xi = np.linspace(min(x), max(x))
    yi = np.linspace(min(y), max(y))
    
    X, Y = np.meshgrid(xi, yi)
    Z = griddata(x, y, z, xi, yi)
    
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet,
                           linewidth=0, antialiased=False)  # rstride and cstride are the stepsize (large numbers: i will see large patches)
    
    ax.set_zlim3d(np.min(Z), np.max(Z))
    fig.colorbar(surf)
    

    ax.set_xlabel("Xlabel")
    ax.set_ylabel("Ylabel")
    ax.set_zlabel("Zlabel")
    
    plt.show()


######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        main(filename)
    else:
        print "Usage: python script.py path/datafile  "

    

