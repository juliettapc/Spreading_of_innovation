
import csv
import sys
from PyGrace.grace import Grace
from PyGrace.colors import ColorBrewerScheme

def main ():



    type_dynamics='pers'  #'inf'  # 'pers' 



    xs=[]
    ys=[]


### for the 95% conf interval :

    if type_dynamics=='inf':
        filename_background="../Results/weight_shifts/Low_high_95.0percent_envelope_Infection_p0.2_Immune0.1_1000iter.dat"

    elif type_dynamics=='pers':
       # filename_background="../Results/weight_shifts/Low_high_95.0percent_envelope_Persuasion_alpha0.3_damping0.0_mutual_encourg0.5_threshold0.9_1000iter.dat"
        filename_background="../Results/weight_shifts/Low_high_95.0percent_envelope_Persuasion_alpha0.1_damping0.0_mutual_encourg0.5_threshold0.5_1000iter_alphaA_eq_alphaF.dat"




    file=open(filename_background,'r')

    lista_lines=file.readlines()   # each element is a line of the file  STRING TYPE!!

    listX0=[]
    listY_low=[]  
    listY_high=[]  

    
    for line in lista_lines:  
        elements=[]
        items=line.strip('\n').split(' ')

        listX0.append(int(items[0]))  
        listY_low.append(float(items[1]))  # number of adopters
        listY_high.append(float(items[2]))  # number of adopters
       


    xs.append(listX0)   
    ys.append(listY_high)

    xs.append(listX0)   
    ys.append(listY_low)





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



#####  Model :
    if type_dynamics=='inf':           
        filename_model="../Results/weight_shifts/Average_time_evolution_Infection_p0.2_Immune0.1_1000iter_2012.dat"

        list_yLegends=["","","Empirical Process","Infection Model"]
        yTitle="Number of Adopters"
        filename="../Results/weight_shifts/figures_pygrace/Fig2C.agr"        
        colors = [7,7,1,2]  # for each series


    elif type_dynamics=='pers':
        filename_model="../Results/weight_shifts/Time_evol_Persuasion_alpha0.1_damping0.0_mutual0.5_threshold0.5_1000iter_alphaA_eq_alphaF.dat"

        list_yLegends=["","","Empirical Process","Persuasion Model"]
        yTitle="Number of Adopters"
        filename="../Results/weight_shifts/figures_pygrace/Fig2F_alphaA_eq_alphaF.agr"                
        colors = [7,7,1,3]  # for each series
        

   

    file_model=open(filename_model,'r')
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
   

    xTitle="Days"
      #  graphTitle="" #empty
       # subtitle="" #empty
         
        
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


 # file order:  high_95_conf_interv, low_95_conf_interv, empirical, model   
   
    cont=0
    for [i,y] in enumerate(ys):
        dataset = graph.add_dataset(zip(xs[i],y),legend=list_yLegends[i])
        dataset.symbol.shape = 0             
        
        dataset.line.linewidth = 3

        if cont==0:

            dataset.fill.type=2   #0: no fill  1: as a poligon   2:to baseline
            dataset.fill.color=7                                              
            dataset.line.color = 7
        elif  cont ==1:          # the fist dataset is just fake data for the background
            dataset.fill.type=2   #0: no fill  1: as a poligon   2:to baseline
            dataset.fill.color=0                                              
            dataset.line.color = 7
        else:
            dataset.line.color = colors[i]

        cont+=1



    graph.legend.char_size = 1.
    graph.legend.loc = (.2,.81)
    graph.legend.box_linestyle=0   # NO legend box
    grace.autoscale()
    grace.write_file(filename)








######################################
if __name__ == '__main__':
    #if len(sys.argv) > 1:
     #   graph_filename = sys.argv[1]
   
        main()
   # else:
     #   print "Usage: python script.py path/network.gml"

    
