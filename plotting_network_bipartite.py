#!/usr/bin/env python

'''
Given a .gml file, i plot the network.

Created by Julia Poncela, on August 2011.

'''

import sys
import os
import networkx as nx
import matplotlib.pyplot as plot
from matplotlib.patches import Wedge, Polygon
import matplotlib.ticker as ticker
from matplotlib import patches as patches
import random


def main(graph_name):



    G = nx.read_gml(graph_name)
    graph_name_plot=graph_name.split(".gml")[0]+"__.png"

    H=nx.Graph()   # MAKE a COPY of the network so GRAGHVIZ doest freak out.. 
    H.add_edges_from(G.edges())



    size_A=200
    size_F=200
    size_s=100

    max=0.0
    hub=None
    for n in G.nodes():
        if len(G.neighbors(n))>max:
            max=G.degree(n)
            hub=n
       
            
    print hub, max




   
#this works just fine:   
    #layout=nx.graphviz_layout(H,prog='twopi',root=None,args='')  #root= central node
    #nx.draw(H,layout,alpha=0.85,node_color='r',with_labels=False)  # alpha=opacity
    #plot.show()


   
#prog= one of: twopi, gvcolor, wc, ccomps, tred, sccmap, fdp, circo, neato, acyclic, nop, gvpr, dot

            #dot for directed hierarchical networks
            #neato uses a spring-algorithm
            #twopi creates kinda fan-arrangement






#this two siple ones work just fine
    #layout = nx.random_layout(H)      
    #layout=nx.spring_layout(H)   
    #nx.draw(H,layout,alpha=0.85,node_color='r',with_labels=False)  # alpha=opacity
    #plot.show()



    max_order=0
    list_orderings=[]
    list_A=[]
    list_F=[]
    list_s=[]
    for n in G.nodes():
        if n in H.nodes():
            if G.node[n]['type']=="A":
                list_A.append(n)
            elif G.node[n]["type"]=="F":
                list_F.append(n)
            else:
              
                list_s.append(n)
                list_orderings.append(G.node[n]["order"])
                if G.node[n]["order"]>max_order:
                    max_order=G.node[n]["order"]
                    
   
    print "# Att:",len(list_A),"# F:",len(list_F),"# shifts:",len(list_s),max_order


    #print sorted(list_orderings),len(sorted(list_orderings))



   # position=nx.graphviz_layout(H,prog='neato',root=hub,args='')  #root= central node
# it is a dictionary: {0: (205.0, 146.0), 1: (168.0, 339.0), 3: (105.0, 372.0), ...}

    position_modified={}

    x_A=len(list_F)+25
    x_F=len(list_F)+25
   

    y_A=len(list_s)*1.5
    y_F=0
    y_s=len(list_s)*.75
    cont=0 #
    for n in H.nodes():
        if G.node[n]["type"]=="A":                     
           
            x_A=x_A+1.6*float(len(list_s))/len(list_A) 
            position_modified[n]=(x_A,y_A)
           
        elif G.node[n]["type"]=="F":                   
           
            x_F=x_F+1.6*float(len(list_s))/len(list_F)
            position_modified[n]=(x_F,y_F)

        else:                    
            x_s= len(list_F)+ cont          # this kinda works: x_s=len(list_F)+float(G.node[n]["order"])
            position_modified[n]=(x_s,y_s)
            cont+=2

#first draw all the edges:
    nx.draw_networkx_edges(H,position_modified,edgelist=None,alpha=0.2)    


# diff types of doctors=diff colors      
    nx.draw_networkx_nodes(H,position_modified,nodelist=list_s, node_shape = 's', node_color='g', node_size=size_s) 
    nx.draw_networkx_nodes(H,position_modified,nodelist=list_F, node_shape = 'o', node_color='b', node_size=size_F)   
    nx.draw_networkx_nodes(H,position_modified,nodelist=list_A, node_shape = 'o', node_color='r', node_size=size_A)


# possible shapes:  so^>v<dph8
  
 ### i create the legend:
##    plot.text(-20,y_A, "Attendings", family='sans-serif', size=14)   # for the hierarchy layout
##    plot.text(-20,y_F, "Fellows", family='sans-serif', size=14)
  

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

    
