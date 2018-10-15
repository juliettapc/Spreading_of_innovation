from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.mlab import griddata

from matplotlib.mlab import griddata

import numpy as np
import sys
#from matplotlib.backends.backend_pdf import PdfPages  #if i want to save the fig to pdf directly


def main(name,dynamics):


   
#../Results/weight_shifts/Landscape_intervention_alpha0.1_damping0.0_mutual_encourg0.5_threshold0.5_num_reseed_per_shift1_1000iter_start20_window7.dat

    fig = plt.figure()
    ax = Axes3D(fig)   #instead of ax = fig.gca(projection='3d')
    
    data = np.genfromtxt(name)     # data is type  numpy.ndarray
   
 

    label_fontsize= 22  # for the labels



   
    x = data[:,0]  
    y = data[:,1] 
    z = data[:,2]   #  if there are any nan, the lanscape with come out all in one color




 

    Zlabel= 'Number extra adopters' 
    xi = np.linspace(min(x), max(x))
    yi = np.linspace(min(y), max(y))

    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] ):#+ ax.get_xticklabels() + ax.get_yticklabels() + ax.get_zticklabels()):
        item.set_fontsize(30)   # to set the tick font size (and label font size)



    X, Y = np.meshgrid(xi, yi)
    Z = griddata(x, y, z, xi, yi)
    

   
      #  cset1 = ax.contour(X, Y, Z, zdir='z', levels=list_levels,  cmap=cm.jet,linewidths=3)   #for the countour lines on the landcape
    cset=plt.contour(X,Y,Z,zdir='z',offset=0,linewidths=1)  # for the PROJECTION of countour lines  on the xy plane  (offset, is the zvalue for that projection plane)

  #  the argument extend3d=True creates step-like contour lines, instead of just contour lines
       # contour() and contourf() draw contour lines and filled contours, respectively.

 
   


    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=0.5, cmap=cm.jet, linewidth=0, antialiased=False)  # rstride and cstride are the stepsize (large numbers: i will see large patches)  alpha is opacity: 0=transparent, 1= totally opaque
    
    ax.set_zlim3d(np.min(Z), np.max(Z))
    fig.colorbar(surf)


  
 #   ax.set_xlim3d(0, 1)
  #  ax.set_ylim3d(0, 1)
   # ax.set_zlim3d(0, 16000)
   

       
    ax.set_xlabel('Opinion bump', fontsize=30)                
    ax.set_ylabel('Days', fontsize=30)          
    ax.set_zlabel('Number extra adopters', fontsize=30)
    
        
       
     
       

#        pp = PdfPages('fig_pers.pdf') #if i want to save the fig to pdf directly
 #       pp.savefig()
  #      pp.close()

    plt.show()
   
   


  


######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]

        dynamics = sys.argv[2]

      
   
        main(filename,dynamics)
    else:
        print "Usage: python script.py path/datafile  infection_or_persuasion"

    
