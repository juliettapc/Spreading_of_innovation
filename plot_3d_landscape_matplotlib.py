from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.mlab import griddata
import numpy as np
import sys
#from matplotlib.backends.backend_pdf import PdfPages  #if i want to save the fig to pdf directly


def main(name,dynamics):
#    name= 'Landscape_parameters_persuasion_threshold0.5_mutual_encoug0.5_100iter_all_landscape.dat'


    metrics='sum_dist_along_montain'   #'montain_dist_end'      #'dist_end'  # 'sum_dist_along' 'sum_dist_along_montain' 'SD'  'mean'  'SD_div_mean'



    fig = plt.figure()
    ax = Axes3D(fig)   #instead of ax = fig.gca(projection='3d')
    
    data = np.genfromtxt(name)     # data is type  numpy.ndarray
   



    label_fontsize= 22  # for the labels

#    Persuasion: 0:alpha,   1:damping,   2:encourg,   3:threshold,   4:dist at end,  5:dist along traject,   6:mean final #,   7, SD final #:   8: SD final # /mean final #

#    Infection: 0:Pinfect,   1:Pimmune,   2:dist at end,  3:dist along traject,   4:mean final #,   5: SD final #,   6:: SD final # /mean final #



    if dynamics=='persuasion':
        x_index=0
        y_index=3



        x = data[:,x_index]   #columns from the datafile  
        y = data[:,y_index]  # if i use the WRONG COLUMN (one with all constant values), i gives IndexError: invalid index

    elif dynamics=='infection':
        x = data[:,0]  
        y = data[:,1] 






    if dynamics=='persuasion':

        if metrics=='montain_dist_end':   # to get the inverse landscape: montain instead of valley
            z_original = data[:,4]

            maximo=max(z_original)
            z=[]
            for item in z_original:
                z.append(maximo-item)

            Zlabel= 'Quality of fit'


        elif metrics=='dist_end':
            z = data[:,4]
            Zlabel= 'Distance at the end'
            
        elif metrics=='sum_dist_along':
            z = data[:,5]
            Zlabel= 'Sum distance along trajectory'
            

        elif metrics=='sum_dist_along_montain':

            z_original = data[:,5]

            maximo=max(z_original)
            z=[]
            for item in z_original:
                z.append(maximo-item)

           
            Zlabel= 'Quality of fit'

        elif metrics=='SD':
            z = data[:,6]
            Zlabel= 'SD final #'
            
        elif metrics=='mean':
            z = data[:,7]
            Zlabel= 'Mean final #'
            
        elif metrics=='SD_div_mean':
            z = data[:,8] 
            Zlabel= 'SD final #/Mean final #'
            
        else: 
            print 'wrong metrics!'
            exit()

    elif dynamics=='infection':

        if metrics=='montain_dist_end':   # to get the inverse landscape: montain instead of valley
            z_original = data[:,2]

            maximo=max(z_original)
            z=[]
            for item in z_original:
                z.append(maximo-item)

            Zlabel= 'Quality of fit'


        elif metrics=='dist_end':
            z = data[:,2]
            Zlabel= 'Distance at the end'
            
        elif metrics=='sum_dist_along':
            z = data[:,3]
            Zlabel= 'Sum distance along trajectory'


        elif metrics=='sum_dist_along_montain':
            z_original = data[:,3]
            maximo=max(z_original)
            z=[]
            for item in z_original:
                z.append(maximo-item)

            Zlabel= 'Quality of fit'



            
        elif metrics=='SD':
            z = data[:,4]
            Zlabel= 'SD final #'
            
        elif metrics=='mean':
            z = data[:,5]
            Zlabel= 'Mean final #'
            
        elif metrics=='SD_div_mean':
            z = data[:,6] 
            Zlabel= 'SD final #/Mean final #'
            
        else: 
            print 'wrong metrics!'
            exit()



    else:
        print 'wrong dynamics!'
        exit()

    xi = np.linspace(min(x), max(x))
    yi = np.linspace(min(y), max(y))





   
      
    X, Y = np.meshgrid(xi, yi)
    Z = griddata(x, y, z, xi, yi)
    
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet, linewidth=0, antialiased=False)  # rstride and cstride are the stepsize (large numbers: i will see large patches)
    
    ax.set_zlim3d(np.min(Z), np.max(Z))
    fig.colorbar(surf)


    

    if dynamics=='infection':
        ax.set_xlabel("P (infection)", fontsize=label_fontsize)
        ax.set_ylabel("P (immune)", fontsize=20)
        ax.set_zlabel(Zlabel, fontsize=20)                 
                
        plt.show()


#0:alpha,   1:damping,   2:encourg,   3:threshold, 

    elif dynamics=='persuasion':

        if x_index==0:
            ax.set_xlabel('Persuadability', fontsize=20)    
        elif x_index==1:
            ax.set_xlabel('Damping', fontsize=20)    
        elif x_index==2:
            ax.set_xlabel('Mutual Encouragement', fontsize=20)    
        elif x_index==3:
            ax.set_xlabel('Opinion Threshold', fontsize=20)    


       
        if y_index==0:
            ax.set_ylabel('Persuadability', fontsize=20)    
        elif y_index==1:
            ax.set_ylabel('Damping', fontsize=20)    
        elif y_index==2:
            ax.set_ylabel('Mutual Encouragement', fontsize=20)    
        elif y_index==3:
            ax.set_ylabel('Opinion Threshold', fontsize=20)    
    
        
        ax.set_zlabel(Zlabel, fontsize=20)

     
        
       
       

#        pp = PdfPages('fig_pers.pdf') #if i want to save the fig to pdf directly
 #       pp.savefig()
  #      pp.close()

        plt.show()
    else:
        print "wrong name for the type of dynamics!"
        
   


  


######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]

        dynamics = sys.argv[2]

      
   
        main(filename,dynamics)
    else:
        print "Usage: python script.py path/datafile  infection_or_persuasion"

    
