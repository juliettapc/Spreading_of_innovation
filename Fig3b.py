
import csv
import sys
from PyGrace.grace import Grace
from PyGrace.colors import ColorBrewerScheme

def main ():






#####  Models :

    filename_model_I="../Results/weight_shifts/histogr_raw_distances_ending_test_train_infection_memory_distrib_p0.8_Immune0.6_1000iter_day125.dat"
  #  filename_model_P="../Results/weight_shifts/histogr_raw_distances_ending_test_train_persuasion_alpha0.2_damping0.0_mutual_encourg0.5_threshold0.7_1000iter_avg_ic_day125.dat"
    filename_model_P="../Results/weight_shifts/histogr_raw_distances_ending_test_train_persuasion_alpha0.1_damping0.0_mutual_encourg0.5_threshold0.5_1000iter_alphaA_eq_alphaF_day125.dat"

    xs=[]
    ys=[]

    list_files=[filename_model_I,filename_model_P]

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
       



    list_yLegends=["Infection Model","Persuasion Model"]
    
    filename="../Results/weight_shifts/figures_pygrace/Fig3b_alphaA_eq_alphaF.agr"
    
    colors = [2,3]  # for each series
    
    
    yTitle="Probability mass"
    xTitle="Final Diff. in # of adopters"
    
       
         
        
  
    
    
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
    graph.yaxis.tick.minor_size = 0


   
   

    for [i,y] in enumerate(ys):
        dataset = graph.add_dataset(zip(xs[i],y),legend=list_yLegends[i])
        dataset.symbol.shape = 0
     #   dataset.symbol.size = 0.5
      #  dataset.symbol.color = colors[i]
       # dataset.symbol.fill_color = colors[i]
        dataset.line.color = colors[i]

    graph.legend.char_size = 1.
    graph.legend.loc = (.21,.8)
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

    
