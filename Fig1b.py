import csv
import sys
from PyGrace.grace import Grace
from PyGrace.colors import ColorBrewerScheme
def main ():




  #  filename_actual_evol="../Results/HospitalModel_august1_adoption_counts_SIMPLER.csv"
  # result_actual_file= csv.reader(open(filename_actual_evol, 'rb'), delimiter=',')




    filename_actual_evol="../Results/Actual_evolution_adopters_NO_fellows_only_attendings.dat"      #../Results/actual_time_evol_for_gnuplot.dat"
    file=open(filename_actual_evol,'r')

    listX=[]
    listY=[]
  



    lista_lines=file.readlines()   # each element is a line of the file  STRING TYPE!!

   

    
    for line in lista_lines:  
        elements=[]
        items=line.strip('\n').split(' ')

        listX.append(int(items[0]))  #time
        listY.append(int(items[1]))  # number of adopters
       

  #  print listX, listY
  
    
    xTitle="Days"
    yTitle="Number of Adopters"
    title="" #empty
    subtitle="" #empty
    filename="../Results/weight_shifts/figures_pygrace/Fig1b.agr"
    
    
    linegraph(listX,listY,xTitle,yTitle,title,subtitle,filename)

    print "\n      printed out:",filename 
    

#filename="./preba_plot_line_symbols.agr"  # or eps, ps, png, ...
#plottools_pygrace_Laura.linegraphwpts(x,y,xTitle,yTitle,title,subtitle,filename)


#list_yLegends=["whatever1","whatever2"]  # list of legends for the different series
#filename="./preba_plot_multiple_lines.eps"
#plottools_pygrace_Laura.realmultilinegraph(xs,ys,xTitle,yTitle,list_yLegends,title,subtitle,filename)





#filename="./preba_plot_barplot.agr"
#plottools_pygrace_Laura.bargraph(x,y,xTitle,yTitle,title,subtitle,filename)

############################

def linegraph(x,y,xTitle,yTitle,title,subtitle,filename):

    data = zip(x,y)
    
    grace = Grace()
    graph = grace.add_graph()
    
    graph.xaxis.label.text = xTitle
    graph.xaxis.label.char_size =2
    graph.xaxis.ticklabel.format = 'Decimal'
    graph.xaxis.ticklabel.char_size = 2
    graph.xaxis.ticklabel.prec = 0

    
   # graph.world.ymin=0   # i set the x and y range i am plotting
    #graph.world.ymax=20   # i set the x and y range i am plotting
    #graph.yaxis.tick.major_size=2
    
    graph.yaxis.label.text = yTitle
    graph.yaxis.label.char_size = 2 
    graph.yaxis.ticklabel.char_size = 2
    graph.yaxis.ticklabel.format = 'Decimal'
    graph.yaxis.ticklabel.prec = 0

    graph.title.text = title
    graph.title.size = .9 
    graph.subtitle.text = subtitle
    graph.subtitle.size = .7
   
    
    dataset1 = graph.add_dataset(data)
    dataset1.symbol.shape = 0
    dataset1.line.color = 1
    graph.legend.box_linestyle=0   # NO legend box

    grace.autoscale()   #comment this if i wanna set my own xy ranges.
    grace.write_file(filename) 
    

######################################
if __name__ == '__main__':
    #if len(sys.argv) > 1:
     #   graph_filename = sys.argv[1]
   
        main()
   # else:
     #   print "Usage: python script.py path/network.gml"

    
