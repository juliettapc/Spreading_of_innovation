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
import random


def main(graph_name):

    min_shift=0
    max_shift=12



    G = nx.read_gml(graph_name)
   

  
   
    list_A=[]
    list_F=[]
    list_s=[]
    list_nodes=[]
    count_A=0
    count_F=0
    for n in G.nodes():
       
        if G.node[n]['type']=="A":
            list_A.append(n)
            list_nodes.append(n)
            G.node[n]['x_position']=count_A
            count_A+=1
        elif G.node[n]["type"]=="F":
            list_F.append(n)
            list_nodes.append(n)
            G.node[n]['x_position']=count_F
            count_F+=1
        elif G.node[n]["type"]=="shift":
            if min_shift<= int(G.node[n]["order"]) and int(G.node[n]["order"])<= max_shift:
                list_s.append(n)               
                list_nodes.append(n)
               
                    
   
     
    SG=nx.subgraph(G, list_nodes)# i take the subgraph that includes only the shifts from [min_shift,max_shift], and all A and F
   
    H=nx.connected_component_subgraphs(SG)[0] # i take the GC to exclude A and F that were not working during those shifts

    



   
   
   # position=nx.graphviz_layout(H,prog='neato',root=hub,args='')  #root= central node
# it is a dictionary: {0: (205.0, 146.0), 1: (168.0, 339.0), 3: (105.0, 372.0), ...}

    position={}

    x_A=len(list_F)
    x_F=len(list_F)

    y_A=len(list_s)*2
    y_F=0
    y_s=len(list_s)
    cont=0
    for n in H.nodes(): 
        print n     
        if H.node[n]["type"]=="A":                              
            x_A=H.node[n]['x_position']           
            position[n]=(x_A,y_A)
            cont+=1

        elif H.node[n]["type"]=="F":  
            x_F=H.node[n]['x_position']           
            position[n]=(x_F,y_F)
            cont+=1

        else:                    
            x_s=len(list_F)+float(H.node[n]["order"])
            position[n]=(x_s,y_s)
            cont+=1



  
   
   
#first draw all the edges:
    nx.draw_networkx_edges(H,position,edgelist=None,alpha=0.5)    


# diff types of doctors=diff colors      
    nx.draw_networkx_nodes(H,position,nodelist=list_s, node_shape = 's', node_color='g', node_size=40) 
    nx.draw_networkx_nodes(H,position,nodelist=list_F, node_shape = 'o', node_color='b', node_size=300)   
    nx.draw_networkx_nodes(H,position,nodelist=list_A, node_shape = 'o', node_color='r', node_size=300)


# possible shapes:  so^>v<dph8
  
 ### i create the legend:
    plot.text(-20,y_A, "Attendings", family='sans-serif', size=14)   # for the hierarchy layout
    plot.text(-20,y_F, "Fellows", family='sans-serif', size=14)
  

    plot.axis('off')  # to not show the axis
    plot.show()

"""
    xy=50.0,0.0
    width,height= 5,10
    p=patches.Ellipse(xy, width, height,facecolor="red",  angle=0.0)
    plot.gca().add_patch(p)    
    plot.draw()

    xy=50.0,-24.0
    width,height= 5,10
    p=patches.Ellipse(xy, width, height,facecolor="blue",  angle=0.0)
    plot.gca().add_patch(p)    
    plot.draw()

    xy=50.0,-45.0
    width,height= 5,10
    p=patches.Ellipse(xy, width, height,facecolor="green",  angle=0.0)
    plot.gca().add_patch(p)    
    plot.draw()
"""
   ####################3



   

######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
   
        main(graph_filename)
    else:
        print "Usage: python script.py path/network.gml"

    
