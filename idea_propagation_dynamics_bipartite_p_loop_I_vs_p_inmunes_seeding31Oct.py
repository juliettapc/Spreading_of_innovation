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
 



    G = nx.read_gml(graph_name)


    prob_min=0.0
    prob_max=1.01
    delta_prob=0.05
    prob_infection=prob_min

    Niter=500


    prob_Inmune=0.70


    dir="../Results/"   
    output_file=dir+"Fraction_infected_vs_p"+str(prob_infection)+"_"+"Inmune"+str(prob_Inmune)+"_"+str(Niter)+"iter_seed31Oct_2012.dat"   
    file = open(output_file,'wt')    
    file.close()






   
    while prob_infection<= prob_max:

       

        print "p:",prob_infection        

        output_file2=dir+"Average_time_evolution_Infection_p"+str(prob_infection)+"_"+"Inmune"+str(prob_Inmune)+"_"+str(Niter)+"iter_seed31Oct_2012.dat"
        file2 = open(output_file2,'wt')                                       
        file2.close()
        


# i create the empty list of list for the Niter temporal evolutions
        num_shifts=0
        for n in G.nodes():
            G.node[n]["status"]="S" 
            if G.node[n]['type']=="shift":
                num_shifts+=1


        list_final_I_values_fixed_p=[]
        list_lists_t_evolutions=[]    
        for iter in range(Niter):
            
            print "   iter:",iter

            list_seed_shifts=[]
            order_first_shift_seeded=100000                       
            list_I=[]  #list infected doctors
            list_ordering=[]
            list_s=[]
            list_A=[]
            list_F=[]

            first_node_seeded=None
            for n in G.nodes():
                G.node[n]["status"]="S"  # all nodes are Susceptible
                if G.node[n]['type']=="shift":
                    list_s.append(n)   
                   
                    if "10/31/11" in G.node[n]['label']: 
                        G.node[n]["status"]="I"  # I infect the fist shift
                        list_seed_shifts.append(n)
                        if G.node[n]['order']<order_first_shift_seeded:
                            first_node_seeded=n
                            order_first_shift_seeded=G.node[n]['order']

           
                elif G.node[n]['type']=="A":
                    list_A.append(n)
                    
                elif G.node[n]['type']=="F":
                    list_F.append(n)
                


           
                                  

            max_shift=len(list_s)+1

   
            for seed_shift in list_seed_shifts:   # seeding particular doctors
                for doctor in G.neighbors(seed_shift):
                    if G.node[doctor]["label"]=="Wunderink" or G.node[doctor]["label"]=="Sporn" or G.node[doctor]["label"]=="Smith":  # one entire team and one doctor in the other team
                        G.node[doctor]["status"]="I"
                        list_I.append(G.node[doctor]["label"])
                    




            for n in G.nodes():   # i make some DOCTORs INMUNE
                if (G.node[n]['type']=="A") or ( G.node[n]['type']=="F"):
                    rand=random.random()
                    if rand< prob_Inmune:
                        G.node[n]["status"]="Inmune"


  
# the dynamics starts: 
            list_single_t_evolution=[]
            t=G.node[first_node_seeded]['order']
           
            while t<= max_shift:  # loop over shifts, in order           
                for n in G.nodes():
                    if G.node[n]['type']=="shift" and G.node[n]['order']==t:
                        flag_possible_infection=0
                        for doctor in G.neighbors(n): #first i check if any doctor is infected in this shift
                            if G.node[doctor]["status"]=="I":
                                flag_possible_infection=1
                                break

                        if flag_possible_infection:
                            for doctor in G.neighbors(n): # then the doctors in that shift get infected with prob_infection
                                if G.node[doctor]["status"]=="S":
                                    rand=random.random()
                                    if rand<prob_infection:
                                        G.node[doctor]["status"]="I"
                                        list_I.append(G.node[doctor]["label"])
                                           

                list_single_t_evolution.append(float(len(list_I))/(len(list_A)+len(list_F)))
           
                
                              

                if t==max_shift:
                    list_final_I_values_fixed_p.append(float(len(list_I))/(len(list_A)+len(list_F)))




                t+=1
   
                       
            list_lists_t_evolutions.append(list_single_t_evolution)


      

        file2 = open(output_file2,'at')        
        for s in range(len(list_single_t_evolution)):           
            list_fixed_t=[]
            for iter in range (Niter):
                list_fixed_t.append(list_lists_t_evolutions[iter][s])        
            print >> file2, s,numpy.mean(list_fixed_t)                    
        file2.close()



        file = open(output_file,'at')   
        print >> file,  prob_infection, numpy.mean(list_final_I_values_fixed_p)
        file.close()




        prob_infection+= delta_prob


######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
   
        main(graph_filename)
    else:
        print "Usage: python script.py path/network.gml"

    
