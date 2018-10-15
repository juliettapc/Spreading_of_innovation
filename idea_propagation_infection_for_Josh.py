#!/usr/bin/env python

'''
Given a .gml network, it simulates a disease-spreading-like process
in the bipartite network (doctors and shifts)

Created by Julia Poncela, on August 2011.

'''


import sys
import os
import networkx as nx
import numpy


import random


def main(graph_name):
 



            G = nx.read_gml(graph_name)  # i read the network file and create a network object




            prob_infection=0.21
            prob_Immune=0.14   # i set the value for the two parameters
            
            
            
            print "\n  Idea propagation dynamics ->  Infection.  Probability of infection:", prob_infection, "  Probability Immune:", prob_Immune,"\n"

           
            file_name_indiv_evol="Time_evoulution_idea_propagation_infection_prob_inf"+str(prob_infection)+"prob_Immune"+str(prob_Immune)+".dat"  # i create the (empty for now) output file  
            file3 = open(file_name_indiv_evol,'wt')       
            file3.close()
            ##########################################





            list_I=[]  #list infected doctors            
            list_s=[]
           


            ########### i set Initial Conditions
            max_order=0
            for n in G.nodes():
                G.node[n]["status"]="S"  # all nodes are Susceptible
                if G.node[n]['type']=="shift":
                    list_s.append(n)        
                    if  G.node[n]['order']>max_order:
                        max_order=G.node[n]['order']
                else:
                    if G.node[n]['label']=="Wunderink"  or G.node[n]["label"]=="Weiss":       # two doctors are infected   (i always start with the same TWO infected doctors)
                        G.node[n]["status"]="I"                       
                        list_I.append(G.node[n]['label'])
                                 



            
            list_single_t_evolution=[]  # in this list i will keep the number of infected doctors per each time step
            list_single_t_evolution.append(2.0)  


            for n in G.nodes():   # i make some doctors INMUNE  (anyone except Weiss and Wunderink)
                if (G.node[n]['type']=="A") or ( G.node[n]['type']=="F"):
                    if G.node[n]['label']!="Wunderink"  and G.node[n]["label"]!="Weiss": 
                        rand=random.random()
                        if rand< prob_Immune:
                            G.node[n]["status"]="Immune"



       
  

            ################# the dynamics starts:             
            t=1
            while t<= max_order:  # loop over time steps     
 
                for n in G.nodes():  # i go over all nodes in the network
                    if G.node[n]['type']=="shift" and G.node[n]['order']==t:  # when i find the node corresponding to the current shift (time step):
                        flag_possible_infection=0
                        for doctor in G.neighbors(n): #first i check if any doctor is infected in this shift
                            if G.node[doctor]["status"]=="I":
                                flag_possible_infection=1
                                

                        if flag_possible_infection:  #if the answer is yes, 
                            for doctor in G.neighbors(n): # then the doctors in that shift, get infected with prob_infection
                                if G.node[doctor]["status"]=="S":
                                    rand=random.random()
                                    if rand<prob_infection:
                                        G.node[doctor]["status"]="I"
                                        list_I.append(G.node[doctor]["label"])
                                           

                list_single_t_evolution.append(float(len(list_I)))
                print "t:",t, "  # of infected doctors:",len(list_I)
                t+=1
   



             # i print out the whole time evolution of the system
            file3 = open(file_name_indiv_evol,'at')                
            for i in range(len(list_single_t_evolution)):  #time step by time step                                              
               print >> file3, i,list_single_t_evolution[i], prob_infection, prob_Immune 
            file3.close()
             




######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
   
        main(graph_filename)
    else:
        print "Usage: python script.py path/network.gml"

    
