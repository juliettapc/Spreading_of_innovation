import csv
import sys
from PyGrace.grace import Grace
from PyGrace.colors import ColorBrewerScheme
def main ():




  #  filename_actual_evol="../Results/HospitalModel_august1_adoption_counts_SIMPLER.csv"
  # result_actual_file= csv.reader(open(filename_actual_evol, 'rb'), delimiter=',')




    filename_actual_evol="../Results/Actual_evolution_adopters_NO_fellows_only_attendings.dat"      #../Results/actual_time_evol_for_gnuplot.dat"
    file=open(filename_actual_evol,'r')

    xs=[]
    ys=[]

    listX=[]
    listY=[]
    listZ=[]
  



    lista_lines=file.readlines()   # each element is a line of the file  STRING TYPE!!

   

    
    for line in lista_lines:  
        elements=[]
        items=line.strip('\n').split(' ')

        listX.append(int(items[0]))  #time
        listY.append(int(items[1]))  # number of adopters
        listZ.append(int(items[2]))  # number of ATT on call so far
       

  #  print listX, listY
  
    

 
    
    xs.append(listX)     # Att on call so far
    ys.append(listZ)

    xs.append(listX)   # adopters
    ys.append(listY)

    xTitle="Days"
    yTitle=""
    title="" #empty
    subtitle="" #empty
    filename="../Results/weight_shifts/figures_pygrace/Fig1b_with_Att_on_call.agr"
    list_yLegends=["Number doctors on call so far","Number of Adopters"]
    colors = [4,1]  # for each series
    
    realmultilinegraph(xs,ys,xTitle,yTitle,list_yLegends,filename,colors)

    print "\n      printed out:",filename 
    


############################


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


    for [i,y] in enumerate(ys):
        dataset = graph.add_dataset(zip(xs[i],y),legend=list_yLegends[i])

        dataset.symbol.shape = 0
        dataset.line.color = colors[i]
        dataset.line.linewidth = 2.5

    graph.legend.char_size = 1.5
    graph.legend.loc = (.3,.5)
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

    

######################################
if __name__ == '__main__':
    #if len(sys.argv) > 1:
     #   graph_filename = sys.argv[1]
   
        main()
   # else:
     #   print "Usage: python script.py path/network.gml"

    
