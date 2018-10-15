from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.mlab import griddata
from matplotlib.mlab import griddata
import numpy as np
import sys



def main(name,dynamics):


#../Results/weight_shifts/Landscape_parameters_persuasion_1000iter_alphaA_eq_alphaF.dat



    metrics='sum_dist_along_montain'        #sum_dist_along_montain'   #'montain_dist_end'      #'dist_end'  # 'sum_dist_along' 'sum_dist_along_montain' 'SD'  'mean'  'SD_div_mean'


 
    fig = plt.figure()
    ax = Axes3D(fig)   #instead of ax = fig.gca(projection='3d')
    
    data = np.genfromtxt(name)     # data is type  numpy.ndarray
   

    num_levels=20   # for the countour lines

    label_fontsize= 22  # for the labels

    #    Persuasion: 0:alpha,   1:damping,   2:encourg,   3:threshold,   4:dist at end,  5:dist along traject,   6:mean final #,   7, SD final #:   8: SD final # /mean final #
    if dynamics=='persuasion':  # variables that are NOT fixed
        x_index=0
        y_index=1





        x = data[:,x_index]   #columns from the datafile  
        y = data[:,y_index]  # if i use the WRONG COLUMN (one with all constant values), i gives IndexError: invalid index


    #    Infection:    0:Pinfect,   1:Pimmune,   2:dist at end,  3:dist along traject,   4:mean final #,   5: SD final #,   6:: SD final # /mean final #
    elif dynamics=='infection':
        x = data[:,0]  
        y = data[:,1] 


    # Infection memory:    0:Pinfect   1:Pimmune   2:infect Threshold   3: dose   4:dist at end,  5:dist along traject,   6:mean final #,   7, SD final #:   8: SD final # /mean final #
    elif dynamics=='infection_memory':
         x_index=0
         y_index=3

         x = data[:,x_index]  
         y = data[:,y_index]  





    if dynamics=='persuasion'or dynamics=='infection_memory':

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

            z_original = data[:,2]

            maximo=max(z_original)

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


        print min(z_original), max(z_original)
   

    else:
        print 'wrong dynamics!'
        exit()

    xi = np.linspace(min(x), max(x))
    yi = np.linspace(min(y), max(y))

 

   # for label in ax.xaxis.get_ticklabels():   # i set the fontsize of the ticklabels for the axes
    #    label.set_fontsize(30)
      
      #      ax.set_xticks((0,0.2,0.4,0.6,0.8,1))   # otherwise, for some reason it goes 0, 0.2, 0.4 for infection, but 0, 0.1,0.2 for persuasion...

      #  ax.set_xticklabels(('0.2','0.4'))

  #  for label in ax.yaxis.get_ticklabels():   # i set the fontsize of the ticklabels for the axes
   #     label.set_fontsize(30)

    #for label in ax.zaxis.get_ticklabels():   # i set the fontsize of the ticklabels for the axes
     #   label.set_fontsize(30)

   
  

    maximo=max(z_original)   # to set the number of contour lines
    minimo=min(z_original)   # to set the number of contour lines

    print minimo, maximo
    list_levels=[]
    list_levels.append(int(minimo+1))
    
    for i in range (num_levels):
        new_value=list_levels[-1]
        new_value+=int((maximo-minimo)/num_levels)
        list_levels.append(new_value)
       
   # list_levels.append(int(maximo-new_value/10))  
   

    print list_levels


    X, Y = np.meshgrid(xi, yi)
    Z = griddata(x, y, z, xi, yi)
    

     #OJO !! THE XY PLANE PROJECTON FEATURE ONLY WORKS FOR MATPLOTLIB 1.1.1
      #  cset1 = ax.contour(X, Y, Z, zdir='z', levels=list_levels,  cmap=cm.jet,linewidths=3)   #for the countour lines on the landcape
    cset=plt.contour(X,Y,Z,zdir='z',levels=list_levels,offset=0,linewidths=3)  # for the PROJECTION of countour lines  on the xy plane  (offset, is the zvalue for that projection plane)

  
 
#  the argument extend3d=True creates step-like contour lines, instead of just contour lines
       # contour() and contourf() draw contour lines and filled contours, respectively.

 


    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=0.5, cmap=cm.jet, linewidth=0, antialiased=False)  # rstride and cstride are the stepsize (large numbers: i will see large patches)  alpha is opacity: 0=transparent, 1= totally opaque
    
    ax.set_zlim3d(np.min(Z), np.max(Z))
    fig.colorbar(surf,shrink=0.5)  #, aspect=5)   thickness


   


    if dynamics=='infection':
        ax.set_xlabel("P (infection)", fontsize=40)
        ax.set_ylabel("P (immune)", fontsize=40)
        ax.set_zlabel(Zlabel, fontsize=40)                 
                
        plt.show()


#0:alpha,   1:damping,   2:encourg,   3:threshold, 

    elif dynamics=='persuasion':

        if x_index==0:
            ax.set_xlabel('Persuadability', fontsize=40)    
        elif x_index==1:
            ax.set_xlabel('Resistence', fontsize=40)    
        elif x_index==2:
            ax.set_xlabel('Mutual Encouragement', fontsize=40)    
        elif x_index==3:
            ax.set_xlabel('Opinion Threshold', fontsize=40)    


       
        if y_index==0:
            ax.set_ylabel('Persuadability', fontsize=40)    
        elif y_index==1:
            ax.set_ylabel('Resistence', fontsize=40)    
        elif y_index==2:
            ax.set_ylabel('Mutual Encouragement', fontsize=40)    
        elif y_index==3:
            ax.set_ylabel('Opinion Threshold', fontsize=40)    
    
        
        ax.set_zlabel(Zlabel, fontsize=40,rotation=90)

        
       
     
       

#        pp = PdfPages('fig_pers.pdf') #if i want to save the fig to pdf directly
 #       pp.savefig()
  #      pp.close()


        plt.show()

    elif dynamics=='infection_memory':
        ax.set_xlabel("P (infection)", fontsize=40)
        ax.set_ylabel("Infection dose", fontsize=40)
        ax.set_zlabel(Zlabel, fontsize=40)         
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
        print "Usage: python script.py path/datafile  infection_or_persuasion_or_infection_memory"

    
