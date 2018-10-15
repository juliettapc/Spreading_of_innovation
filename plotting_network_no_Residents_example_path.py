#!/usr/bin/env python

'''
Given a .gml file, i plot the network.

Created by Julia Poncela, on August 2011.

'''

import sys
import os
import networkx as nx
from matplotlib import pyplot
import matplotlib.pyplot as plot
from matplotlib.patches import Wedge, Polygon
import matplotlib.ticker as ticker
from matplotlib import patches as patches


def main(graph_name):

    G = nx.read_gml(graph_name)
    graph_name_plot=graph_name.split(".gml")[0]+".png"

    H=nx.Graph()   # MAKE a COPY of the network so GRAGHVIZ doest freak out.. 
    H.add_edges_from(G.edges())


   


 ##   max=0.0
 ##    hub=None
 ##    for n in G.nodes():
 ##        if len(G.neighbors(n))>max:
   ##          max=G.degree(n)
 ##            hub=n
            
  ##   print hub, max

    for node in G.nodes():
        if G.node[node]['label']=='Wunderink':
            hub=node

           # print hub,G.node[node]['label'], "yayaaaa",len(G.neighbors(node))


    position=nx.graphviz_layout(H,prog='neato',args='')  #root= central node
# it is a dictionary: {0: (205.0, 146.0), 1: (168.0, 339.0), 3: (105.0, 372.0), ...}



 
    list_names_drs_path=["Wunderink"]#Wunderink","Luqman","Mutlu","Marouni","Smith","Cuttica","Schroedl"]   # combination paths1 and 2
    #list_names_drs_path=["Wunderink","Luqman","Mutlu","Marouni"]  #example obtained from Processing code PATH1
#    list_names_drs_path=["Wunderink","Smith","Cuttica","Schroedl"]  #example obtained from Processing code PATH2

    list_A=[]
    list_F=[]
    list_R=[]

    list_A_nodes_path=[]
    list_F_nodes_path=[]

    for n in G.nodes():       

        if n in H.nodes():
            if G.node[n]['type']=="A":
                list_A.append(n)

                if G.node[n]['label'] in list_names_drs_path :
                    list_A_nodes_path.append(n),len(G.neighbors(n))
                    print "\n",n, G.node[n]['label']

            elif G.node[n]["type"]=="F":
                list_F.append(n)

                if G.node[n]['label'] in list_names_drs_path :
                    list_F_nodes_path.append(n)
                    print "\n",n, G.node[n]['label'],len(G.neighbors(n))

            elif G.node[n]["type"]=="R":
                list_R.append(n)               
                for neighbor in G.neighbors(n):
                    H.remove_edge(n, neighbor)
                H.remove_node(n)


    print "# Att:",len(list_A),"# F:",len(list_F),





   # raw_input()

 #   print "  and after:",len(G.nodes())





  
    




# diff types of doctors=diff colors      
   # nx.draw_networkx_nodes(H,position,nodelist=list_R, node_shape = 'o', node_color='g', node_size=100) 
    nx.draw_networkx_nodes(H,position,nodelist=list_F, node_shape = 'o', node_color='b', node_size=250)   
    nx.draw_networkx_nodes(H,position,nodelist=list_A, node_shape = 'o', node_color='r', node_size=250)
#list_nodes_path


## i replot the nodes from the example paht
    nx.draw_networkx_nodes(H,position,nodelist=list_F_nodes_path, node_shape = 'o', node_color='b', node_size=550)   
    nx.draw_networkx_nodes(H,position,nodelist=list_A_nodes_path, node_shape = 'o', node_color='r', node_size=550)
  

#first draw all the edges:
    nx.draw_networkx_edges(H,position,edgelist=None,alpha=0.35)    


 ### i create the legend:
#    plot.text(60,-10, "Attending", family='sans-serif', size=14)
 #   plot.text(60,-29, "Fellow", family='sans-serif', size=14)
  #  plot.text(60,-50, "Resident", family='sans-serif', size=14)


  #  xy=50.0,0.0
   # width,height= 5,10
 
#   p=patches.Ellipse(xy, width, height,facecolor="red",  angle=0.0)
 #   plot.gca().add_patch(p)    
  #  plot.draw()

   # xy=50.0,-24.0
 #   width,height= 5,10
  #  p=patches.Ellipse(xy, width, height,facecolor="blue",  angle=0.0)
   # plot.gca().add_patch(p)    
   # plot.draw()

 #   xy=50.0,-45.0
  #  width,height= 5,10
   # p=patches.Ellipse(xy, width, height,facecolor="green",  angle=0.0)
    #plot.gca().add_patch(p)    
    #plot.draw()
   ####################3



    plot.axis('off')  # to not show the axis
    plot.show()


   

######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
   
        main(graph_filename)

    else:
        print "Usage: python script.py path/network.gml"

    
