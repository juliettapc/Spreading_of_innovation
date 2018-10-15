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

    G = nx.read_gml(graph_name)
    graph_name_plot=graph_name.split(".gml")[0]+".png"

    H=nx.Graph()   # MAKE a COPY of the network so GRAGHVIZ doest freak out.. 
    H.add_edges_from(G.edges())




    max=0.0
    hub=None
    for n in G.nodes():
        if len(G.neighbors(n))>max:
            max=G.degree(n)
            hub=n

        if G.node[n]["type_doctor"]=="A":
            for k in G.neighbors(n):   
                if   G.node[n]["type_doctor"]==G.node[k]["type_doctor"] :
                    print G.node[n]["type_doctor"],"--",G.node[k]["type_doctor"]
            
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




    list_A=[]
    list_F=[]
    list_R=[]
    for n in G.nodes():
        if n in H.nodes():
            if G.node[n]['type_doctor']=="A":
                list_A.append(n)
            elif G.node[n]["type_doctor"]=="F":
                list_F.append(n)
            elif G.node[n]["type_doctor"]=="R":
                list_R.append(n)
   
    print "# Att:",len(list_A),"# F:",len(list_F),"# R:",len(list_R),









   # position=nx.graphviz_layout(H,prog='neato',root=hub,args='')  #root= central node
# it is a dictionary: {0: (205.0, 146.0), 1: (168.0, 339.0), 3: (105.0, 372.0), ...}

    position_modified={}

    x_A=0.0
    x_F=0.0
    x_R=-250.0
    for n in H.nodes():
        if G.node[n]["type_doctor"]=="A":                     
           
            x_A=x_A+500.0/float(len(list_A))

            if (G.node[n]["label"]=="Prickett") or (G.node[n]["label"]=="Gates"):
                position_modified[n]=(x_A,300.0-20)

            else:                               
                position_modified[n]=(x_A,300.0)
           
        if G.node[n]["type_doctor"]=="F":                   
           
            x_F=x_F+500.0/float(len(list_F))
            position_modified[n]=(x_F,200.0)

        if G.node[n]["type_doctor"]=="R":           
           
            x_R=x_R+1000.0/float(len(list_R))
            position_modified[n]=(x_R,100.0)
        

#first draw all the edges:
    nx.draw_networkx_edges(H,position_modified,edgelist=None,alpha=0.35)    


# diff types of doctors=diff colors      
    nx.draw_networkx_nodes(H,position_modified,nodelist=list_R, node_shape = 'o', node_color='g', node_size=50) 
    nx.draw_networkx_nodes(H,position_modified,nodelist=list_F, node_shape = 'o', node_color='b', node_size=200)   
    nx.draw_networkx_nodes(H,position_modified,nodelist=list_A, node_shape = 'o', node_color='r', node_size=200)


  
  
 ### i create the legend:
    plot.text(-200,300, "Attendings", family='sans-serif', size=14)   # for the hierarchy layout
    plot.text(-200,200, "Fellows", family='sans-serif', size=14)
    plot.text(-300,80, "Residents", family='sans-serif', size=14)

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

    
