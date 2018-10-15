
import csv
import sys
from PyGrace.grace import Grace
from PyGrace.colors import ColorBrewerScheme

def main ():


    xs=[]
    ys=[]

    
### Actual evolution :


    filename_actual_evol="../Results/Actual_evolution_adopters_NO_fellows_only_attendings.dat"
    file1=open(filename_actual_evol,'r')


   
    bump=0.4
    window=7


    filename_simu="../Results/weight_shifts/persuasion/Time_evolutions_Persuasion_alpha0.1_damping0.0_mutual_encourg0.5_threshold0.5_num_reseed_per_shift1_1000iter_intervention_start20_window"+str(window)+"_bump"+str(bump)+".dat"
    file2=open(filename_simu,'r')
    
    print filename_simu



    filename_evelope="../Results/weight_shifts/Low_high_95percent_envelope_Persuasion_intervention_alpha0.1_damping0.0_mutual_encourg0.5_threshold0.5_1000iter_window"+str(window)+"_bump"+str(bump)+"_alphaA_eq_alphaF.dat"
    file3=open(filename_evelope,'r')




    filename_original_simu="../Results/weight_shifts/Time_evol_Persuasion_alpha0.1_damping0.0_mutual0.5_threshold0.5_1000iter_alphaA_eq_alphaF.dat"
    file4=open(filename_original_simu,'r')
    



    listX=[]

    listY1=[]
    listY2=[]
    listY3=[]
    listY4=[]
    listY5=[]
    listY6=[]
   




    lista_lines=file3.readlines()   # each element is a line of the file  STRING TYPE!!

   
   
    for line in lista_lines:                   
            items=line.strip('\n').split(' ')

            listX.append(int(items[0]))  # time  
            listY2.append(float(items[1]))  # 95% c.i. (low boundary)
            listY3.append(float(items[2]))  # 95% c.i.  (high boundary)
          

      
    xs.append(listX)   
    ys.append(listY3)
    
    xs.append(listX)   
    ys.append(listY2)




    listX=[]
    lista_lines=file2.readlines()   
   
    for line in lista_lines:                   
            items=line.strip('\n').split(' ')

            listX.append(int(items[0]))  # time  
            listY4.append(float(items[1]))  # num adopters simu
            listY6.append(float(items[7]))  # num Att on call so far.
          

    xs.append(listX)   
    ys.append(listY4)
    
  
   

    listX=[]
    lista_lines=file4.readlines()   
   
    for line in lista_lines:                   
            items=line.strip('\n').split(' ')

            listX.append(int(items[0]))  # time  
            listY5.append(float(items[1]))  # num adopters simu
         

    xs.append(listX)   
    ys.append(listY5)
    
    

    xs.append(listX)   
    ys.append(listY6)
    



    listX=[]
    lista_lines=file1.readlines()   # each element is a line of the file  STRING TYPE!!   
   
    for line in lista_lines:                    
            items=line.strip('\n').split(' ')

            listX.append(int(items[0]))  # time  
            listY1.append(int(items[1]))  # num adopters
          

    xs.append(listX)   
    ys.append(listY1)
    
  
        


    list_yLegends=["","","avg simulation with intervention","avg simulation","# Att on call so far","empirical"]
    xTitle="Days" 
    yTitle="Number of adopters"

    filename="../Results/weight_shifts/figures_pygrace/Fig_intervention_envelope_window"+str(window)+"_bump"+str(bump)+"_and_num_Att_on_call.agr" 
  

    
    colors = [1,3,10,4,3,1]  # for each series
      
        
        
   
        
       
        
    realmultilinegraph(xs,ys,xTitle,yTitle,list_yLegends,filename,colors)
    
    print "\n      printed out:",filename 
    





####################################


def realmultilinegraph(xs,ys,xTitle,yTitle,list_yLegends,filename, colors):
#ys is a list of y-series
    
    

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


 # file order:   high_95_conf_interv, low_95_conf_interv,  empirical, model
   
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
    graph.legend.loc = (.2,.83)
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

    
