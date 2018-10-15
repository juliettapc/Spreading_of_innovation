
import csv
import sys
from PyGrace.grace import Grace
from PyGrace.colors import ColorBrewerScheme

def main ():


    xs=[]
    ys=[]

    
### Actual evolution :


    window=10  # or 1, 5, 7,10



    filename1="../Results/weight_shifts/Final_distance_vs_bump_alpha0.1_damping0.0_mutual_encourg0.0_threshold0.5_num_reseed_per_shift1_10000iter_intervention_start20_window1_comparison_to_simu_without_interv.dat"
    file1=open(filename1,'r')


     
    
    filename2="../Results/weight_shifts/Final_distance_vs_bump_alpha0.1_damping0.0_mutual_encourg0.0_threshold0.5_num_reseed_per_shift1_10000iter_intervention_start20_window3_comparison_to_simu_without_interv.dat"
    file2=open(filename2,'r')  
    


 
    filename3="../Results/weight_shifts/Final_distance_vs_bump_alpha0.1_damping0.0_mutual_encourg0.0_threshold0.5_num_reseed_per_shift1_10000iter_intervention_start20_window5_comparison_to_simu_without_interv.dat"

    file3=open(filename3,'r') 
    



    filename4="../Results/weight_shifts/Final_distance_vs_bump_alpha0.1_damping0.0_mutual_encourg0.0_threshold0.5_num_reseed_per_shift1_10000iter_intervention_start20_window7_comparison_to_simu_without_interv.dat"

    file4=open(filename4,'r')  


    listX=[]

    listY1=[]
    listY2=[]
    listY3=[]
    listY4=[]
   

   



    listX=[]
    lista_lines=file1.readlines()   
   
    for line in lista_lines:                   
            items=line.strip('\n').split(' ')

            listX.append(float(items[1]))  # bump/threshold
            listY1.append(float(items[10]))  # num interventions per iter
          

    xs.append(listX)   
    ys.append(listY1)
    
  #----



    listX=[]
    lista_lines=file2.readlines()   
   
    for line in lista_lines:                   
            items=line.strip('\n').split(' ')

            listX.append(float(items[1]))  # bump/threshold
            listY2.append(float(items[10]))  # num interventions per iter
          

    xs.append(listX)   
    ys.append(listY2)
    
  #----



    listX=[]
    lista_lines=file3.readlines()   
   
    for line in lista_lines:                   
            items=line.strip('\n').split(' ')

            listX.append(float(items[1]))  # bump/threshold
            listY3.append(float(items[10]))  # num interventions per iter
          

    xs.append(listX)   
    ys.append(listY3)
    
  #----

   
   
    listX=[]
    lista_lines=file4.readlines()   
   
    for line in lista_lines:                   
            items=line.strip('\n').split(' ')

            listX.append(float(items[1]))  # bump/threshold
            listY4.append(float(items[10]))  # num interventions per iter
          

    xs.append(listX)   
    ys.append(listY4)
    
  #----
     


    list_yLegends=["window=1","window=3","window=5","window=7"]
    xTitle="Prompt size" 
    yTitle="Number of interventions"

    filename="../Results/intervention/Fig_intervention_number_interventions_vs_bump_diff_w.agr" 
  

    colors = [1,2,3,4]  # for each series
       
        
        
   
        
       
        
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

    
