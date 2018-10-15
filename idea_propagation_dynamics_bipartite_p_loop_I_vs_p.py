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


    prob_min=1.0
    prob_max=1.01
    delta_prob=0.05
    prob_infection=prob_min

    Niter=1000




    dir="../Results/"   
    output_file=dir+"Fraction_infected_vs_p"+str(prob_infection)+"_"+str(Niter)+"iter.dat"   
    file = open(output_file,'wt')    
    file.close()






   
    while prob_infection<= prob_max:

       

        print "p:",prob_infection        

        output_file2=dir+"Average_time_evolution_Infection_p"+str(prob_infection)+"_"+str(Niter)+"iter.dat"
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

            list_I=[]  #list infected doctors
            list_ordering=[]
            list_s=[]
            list_A=[]
            list_F=[]
            for n in G.nodes():
                G.node[n]["status"]="S"  # all nodes are Susceptible
                if G.node[n]['type']=="shift":
                    list_s.append(n)         
                    if G.node[n]['order']==1:
                        seed_shift=n
                        G.node[seed_shift]["status"]="I"  # I infect the fist shift
                   # print "\n\non",G.node[seed_shift]['label'],", the infection starts. Doctors:",
               

                elif G.node[n]['type']=="A":
                    list_A.append(n)
                    
                elif G.node[n]['type']=="F":
                    list_F.append(n)
                


    
            max_shift=len(list_s)+1

   

#pick a random shift to seed the new idea: 
   # seed_shift=random.choice(list_s)
    #G.node[seed_shift]["status"]="I"  # Infected


   

            for doctor in G.neighbors(seed_shift):
                G.node[doctor]["status"]="I"  # all doctor in that shift are also Infected
                list_I.append(G.node[doctor]["label"])
            #print G.node[doctor]["label"],   # ADD ALSO AN INDEPENDENT INFECTION PROB??



      #  print "\nt:",G.node[seed_shift]['order'], "I/N:",float(len(list_I))/(len(list_A)+len(list_F)),"list I:",list_I
        
           


  
# the dynamics starts: 
            list_single_t_evolution=[]
            t=G.node[seed_shift]['order']
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
                                   # print "doctor",G.node[doctor]["label"],"got infected on",G.node[n]['label'] 
       
                           
        
          #  print "\nt:",t, "I/N:",float(len(list_I))/(len(list_A)+len(list_F)),"list I:",list_I
        

                list_single_t_evolution.append(float(len(list_I))/(len(list_A)+len(list_F)))
           
                
                              

                if t==max_shift:
                    list_final_I_values_fixed_p.append(float(len(list_I))/(len(list_A)+len(list_F)))




                t+=1
   
                       
            list_lists_t_evolutions.append(list_single_t_evolution)


      

        file2 = open(output_file2,'at')        
        for s in range(num_shifts):           
            list_fixed_t=[]
            for iter in range (Niter):
                list_fixed_t.append(list_lists_t_evolutions[iter][s])
        # print  "  iter:",iter,"shift:",s, list_lists_t_evolutions[iter][s]
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

    
