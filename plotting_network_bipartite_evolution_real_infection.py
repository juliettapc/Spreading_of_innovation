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
from datetime import *

def main(graph_name,datafile):


    G = nx.read_gml(graph_name)
   
    list_doctors_network=[]
    for node in G.nodes():
        if G.node[node]["label"] not in list_doctors_network and G.node[node]["type"] != "shift":
            list_doctors_network.append(G.node[node]["label"])

   

    for item in list_doctors_network:
        print item

   
    last_order=88 # i just plot the shift up to today's date, aprox
        
        
    file=open(datafile,'r')         ## i read the file:  list_dates_and_names_current_adopters.txt  (created with: extract_real_evolution_number_adopters.py)
    list_lines_file=file.readlines()
          
    max_number_doctors=35    
    list_list_adopters=[] 
    cont=0
    for line in list_lines_file [1:]:   # i exclude the first row                    
        
        parts=line.split(" ")       # example of a line:  2011-11-09 00:00:00 Wunderink Lam Ngan Dematte 
        list=[]

        if cont==0:  # the first line with adopters

            for i in range(2,max_number_doctors):   # to account for the diff. lengh of every line, and exclude the second colum that is just 00:00:00             
                try:                   
                    doctor=parts[i]                
                    if doctor != "\n" and doctor in list_doctors_network:                        
                        list.append(doctor)

                except: 
                    break
        else:  # in the rest of the lines, i check if there are any NEW additions 


            try:  
                doctor=parts[i]
                if (parts[-1] in list_doctors_network) and (parts[-1] not in list_doctors_network):   #i check if the last element of the new line is dif. from the last element from the previous one
                    list.append(doctor)
                    print  parts[-1], list_list_adopters[(cont-1)][-1]
            except: pass
            



        list_list_adopters.append(list)
        cont=+1

    #print list_list_adopters
    raw_input()




    for index in range(len(list_list_adopters)):   # i plot one network per evolution step (one new infected at a time)

       
        H=nx.Graph()   # MAKE a COPY of the network so GRAGHVIZ doest freak out.. 
        H.add_edges_from(G.edges())

        graph_name_plot=graph_name.split(".gml")[0]+str(index)+".png"

               

        
        list_adopters=list_list_adopters[index]
        list_adopters_node_number=[]
        position_adopters={}       
       

      
       
        list_A=[]
        list_F=[]
        list_s=[]
        list_s_up_to_today=[]
        for n in G.nodes():
            if n in H.nodes():
                if G.node[n]['type']=="A":
                    list_A.append(n)
                elif G.node[n]["type"]=="F":
                    list_F.append(n)
                else:
                    list_s.append(n)                   
                    if G.node[n]["order"]<=last_order:   # i only plot the first part of the network (up to today's date)
                        list_s_up_to_today.append(n)
                        
                          
   
       
        position_modified={}       
        x_A=len(list_F)
        x_F=len(list_F)
        
        y_A=len(list_s)*2
        y_F=0
        y_s=len(list_s)
        for n in H.nodes():
            if G.node[n]["type"]=="A":                     
           
                x_A=x_A+float(len(list_s))/len(list_A) 
                position_modified[n]=(x_A,y_A)               

                for doctor in list_adopters:   # i check if the current node is in the list of adopter doctors
                    if G.node[n]["label"]==doctor: 
                           position_adopters[n]=(x_A,y_A)
                           list_adopters_node_number.append(n)                                                     
                           break

           
            elif G.node[n]["type"]=="F":                   
           
                x_F=x_F+float(len(list_s))/len(list_F)
                position_modified[n]=(x_F,y_F)                

            else:                    
                x_s=float(G.node[n]["order"])*2.5#x_s=len(list_F)+float(G.node[n]["order"])
                position_modified[n]=(x_s,y_s)
               

      #  print list_s_up_to_today,len(list_s),len(list_s_up_to_today)
       

       # i remove the shifts yet to come, so i will not plot them
        for nodo in H.nodes():
            if (G.node[nodo]["type"]== "shift") and (nodo not in list_s_up_to_today):                               
                H.remove_node(nodo)
               
           

        #first draw all the edges:
        nx.draw_networkx_edges(H,position_modified,edgelist=None,alpha=0.5)    


       # diff types of doctors=diff colors      
        nx.draw_networkx_nodes(H,position_modified,nodelist=list_s_up_to_today, node_shape = 's', node_color='g', node_size=100) 
        nx.draw_networkx_nodes(H,position_modified,nodelist=list_F, node_shape = 'o', node_color='b', node_size=300)   
        nx.draw_networkx_nodes(H,position_modified,nodelist=list_A, node_shape = 'o', node_color='r', node_size=300)

        nx.draw_networkx_nodes(H,position_adopters,nodelist=list_adopters_node_number, node_shape = 'o', node_color='y', node_size=300)
        

    # possible shapes:  so^>v<dph8


  
 ### i create the legend:
        plot.text(-20,y_A, "Attendings", family='sans-serif', size=14)   # for the hierarchy layout
        plot.text(-20,y_F, "Fellows", family='sans-serif', size=14)
        

        plot.axis('off')  # to not show the axis
        plot.show()
        raw_input()  # so it can plot each figure for each value of the loop, and allow me to save them one by one.

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
    if len(sys.argv) > 2:
        graph_filename = sys.argv[1]
        datafile = sys.argv[2]
   
        main(graph_filename,datafile)
    else:
        print "Usage: python script.py path/network.gml  path/datafile_evolution"

    
