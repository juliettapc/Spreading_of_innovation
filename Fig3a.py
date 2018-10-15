
import csv
import sys
from PyGrace.grace import Grace
from PyGrace.colors import ColorBrewerScheme

def main ():


    xs=[]
    ys=[]


### for the background :
    filename_background="../Results/save/background_train_test.dat"

    file=open(filename_background,'r')

    lista_lines=file.readlines()   # each element is a line of the file  STRING TYPE!!

    listX0=[]
    listY0=[]  
    
    for line in lista_lines:  
        elements=[]
        items=line.strip('\n').split(' ')

        listX0.append(int(items[0]))  
        listY0.append(int(items[1]))  # number of adopters
       



    xs.append(listX0)   
    ys.append(listY0)




    
### Actual evolution :
    filename_actual_evol="../Results/Actual_evolution_adopters_NO_fellows_only_attendings.dat"

    file=open(filename_actual_evol,'r')

    lista_lines=file.readlines()   # each element is a line of the file  STRING TYPE!!

   
    listX1=[]
    listY1=[]  
    
    for line in lista_lines:  
        elements=[]
        items=line.strip('\n').split(' ')

        listX1.append(int(items[0]))  #time
        listY1.append(int(items[1]))  # number of adopters
       



    xs.append(listX1)   
    ys.append(listY1)
  
        

#####  Models :

  


#    filename_model_P_train_test="../Results/weight_shifts/Time_evol_Persuasion_train_alpha0.2_damping0.0_mutual0.5_threshold0.7_1000iter.dat"

    filename_model_P_train_test="../Results/weight_shifts/Time_evol_Persuasion_train_alpha0.1_damping0.0_mutual0.5_threshold0.5_1000iter_alphaA_eq_alphaF.dat"


    filename_model_I_train_test="../Results/weight_shifts/Average_time_evolution_Infection_train_test_p0.8_Immune0.6_1000iter_2012.dat"




    list_files=[filename_model_P_train_test,filename_model_I_train_test]

    for filename in list_files:

       

        file_model=open(filename,'r')
        lista_lines_model=file_model.readlines()   # each element is a line of the file  STRING TYPE!!
        
        
        listX2=[]
        listY2=[]  
        
        for line in lista_lines_model:  
            elements=[]
            items=line.strip('\n').split(' ')
       
            try:
                listX2.append(int(items[0]))  #time
                listY2.append(float(items[1]))  # number of adopters
            except ValueError: pass  # for the last empty line of the file




        xs.append(listX2)   
        ys.append(listY2)

       
        

    list_yLegends=["","Experimental","Persuasion Model","Infection Model"]
    yTitle="Number of Adopters"
    filename="../Results/weight_shifts/figures_pygrace/Fig3a_alphaA_alphaF.agr"

    colors = [0,1,3,2]  # for each series
    xTitle="Days"
     
         
        
        
   
        
       
        
    realmultilinegraph(xs,ys,xTitle,yTitle,list_yLegends,filename,colors)
    
    print "\n      printed out:",filename 
    





####################################


def realmultilinegraph(xs,ys,xTitle,yTitle,list_yLegends,filename, colors):
#ys is a list of y-series
#xs is a list of x-series
    
   

#1:black
#2:red
#3: light green
#4:dark blue
#5:yellow
#6:light brown
#7:grey
#8:purple
#9:cyan
#10:pink
#11:orange
#12: purple2
#13:maroon
#14:cyan2
#15:dark green

    grace = Grace()
    graph = grace.add_graph()
  #  obj1 = grace.add_drawing_object(DrawText)
    



   # graph.title.text = graphTitle 
    graph.title.size = 1.2
    #graph.subtitle.text = subtitle
    graph.subtitle.size = .6
    
    graph.xaxis.label.text = xTitle
    graph.xaxis.label.char_size =  2
    graph.xaxis.ticklabel.format = 'Decimal'
    graph.xaxis.ticklabel.char_size = 2
    graph.xaxis.ticklabel.prec = 2
    
    graph.yaxis.label.text = yTitle
    graph.yaxis.label.char_size = 2
    graph.yaxis.ticklabel.char_size = 2
    graph.yaxis.ticklabel.format = 'Decimal'
    graph.yaxis.ticklabel.prec = 2


# filename order:  background,  empirical, filename_model_I_train,filename_model_I_test,filename_model_P_train,filename_model_P_test
   
    cont=0
    for [i,y] in enumerate(ys):   # enumerate([j,u,l,i,a]) returs a list of tuples: [(0,j),(1,u),(2,l),(3,i),(4,a)]
 # zip([a,b,c],[1,2,3]) returns  [(a,1),(b,2),(c,3)]

        
        dataset = graph.add_dataset(zip(xs[i],y),legend=list_yLegends[i])

        dataset.symbol.shape = 0

        if cont==0:          # the fist dataset is just fake data for the background
            dataset.fill.type=2   #0: no fill  1: as a poligon   2:to baseline
            dataset.fill.color=7                                              
            dataset.line.color = 7
            
        else:
                                
            dataset.line.color = colors[i]
            dataset.line.linewidth = 3
            if cont==3 or cont==5:
                dataset.line.linestyle = 4
            

       
        cont+=1



    graph.legend.char_size = 1.
    graph.legend.loc = (.2,.81)
    graph.legend.box_linestyle=0   # 0 meanis NO legend box
    graph.legend.box_fill_color=7   # 0 means NO legend box

  #  obj1.drawtext.text="YAY!"   # 0 means NO legend box




    grace.autoscale()
    grace.write_file(filename)








######################################
if __name__ == '__main__':
    #if len(sys.argv) > 1:
     #   graph_filename = sys.argv[1]
   
        main()
   # else:
     #   print "Usage: python script.py path/network.gml"

    
