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
import itertools


import random


def main(graph_name):
 

    G = nx.read_gml(graph_name)


    threshold=0.75

    alpha_F_min=0.2
    alpha_F_max=0.21
    delta_alpha_F=0.05
    damping=0.5   #its harder to go back from YES to NO again.


    Niter=1


    alpha_F=alpha_F_min
    while alpha_F<= alpha_F_max:

        alpha_A=0.5*alpha_F

        print "alpha_F:",alpha_F
   
        dir="../Results/"   
        output_file=dir+"Time_evolutions_Persuasion_alpha"+str(alpha_F)+".dat"    
        file = open(output_file,'wt')    
        file.close()


        output_file2=dir+"Average_time_evolution_Persuasion_alpha"+str(alpha_F)+"_"+str(Niter)+"iter.dat"
        file2 = open(output_file2,'wt')                                       
        file2.close()
        


# i create the empty list of list for the Niter temporal evolutions
        num_shifts=0
        for n in G.nodes():           
            if G.node[n]['type']=="shift":
                num_shifts+=1


    
        list_lists_t_evolutions=[]    
        for iter in range(Niter):            
            print "   iter:",iter

            list_Adopters=[]  #list Adopters
            list_ordering=[]
            list_s=[]
            list_A=[]
            list_F=[]
            for n in G.nodes():              
                if G.node[n]['type']=="shift":
                    list_s.append(n)                        
                    if G.node[n]['order']==1:
                        seed_shift=n                                        

                elif G.node[n]['type']=="A":
                    list_A.append(n)
                    G.node[n]["adoption_vector"]=0.0
                    G.node[n]["status"]="NonAdopter"  # initially non-Adopters
                elif G.node[n]['type']=="F":
                    list_F.append(n)
                    G.node[n]["adoption_vector"]=0.0
                    G.node[n]["status"]="NonAdopter"  

    
            max_shift=len(list_s)+1
                 
            for doctor in G.neighbors(seed_shift):
                G.node[doctor]["status"]="Adopter"  # all doctors in that shift are also Infected
                G.node[doctor]["adoption_vector"]=1.0
                list_Adopters.append(G.node[doctor]["label"])
               
        
            file = open(output_file,'at')                       
            print >> file,G.node[seed_shift]['order'], float(len(list_Adopters))/(len(list_A)+len(list_F)),list_Adopters
            file.close()
        


  
# the dynamics starts: 
            list_single_t_evolution=[]
            t=G.node[seed_shift]['order']
            while t<= max_shift:  # loop over shifts, in chronological order   


               # for node in G.nodes():
                #    if G.node[node]['type']!="shift":
                 #       print  t, G.node[node]['label'],G.node[node]['type'],G.node[node]["adoption_vector"],G.node[node]['status']
                #raw_input()


                for n in G.nodes():
                    if G.node[n]['type']=="shift" and G.node[n]['order']==t:
                        flag_possible_persuasion=0
                        for doctor in G.neighbors(n): #first i check if any doctor is an adopter in this shift
                            if G.node[doctor]["status"]=="Adopter":                                
                                flag_possible_persuasion=1                               
                                break

                        if flag_possible_persuasion==1:
                            list_doctors=[]
                            for doctor in G.neighbors(n):
                                list_doctors.append(doctor)
                                
                                
                            pairs=itertools.combinations(list_doctors,2)     
                            for pair in pairs:
                                doctor1=pair[0]
                                doctor2=pair[1]

#add the case of two Adopters that become even more convinced.
###################                                                                                               
                                if G.node[doctor1]['status'] != G.node[doctor2]['status']:  # if they think differently, there will be  persuasion:
                                    print "possible persuasion:", G.node[doctor1]['label'],G.node[doctor1]["adoption_vector"], G.node[doctor1]['status'],"--",G.node[doctor2]['label'],G.node[doctor2]["adoption_vector"], G.node[doctor2]['status'],
                                   
                                    if (G.node[doctor1]['type']=="A") and (G.node[doctor2]['type']=="F"):
                                        delta_AF=G.node[doctor1]["adoption_vector"]-G.node[doctor2]["adoption_vector"]
                                        G.node[doctor1]["adoption_vector"]=G.node[doctor1]["adoption_vector"]-delta_AF*alpha_A
                                        G.node[doctor2]["adoption_vector"]=G.node[doctor2]["adoption_vector"]+delta_AF*alpha_F
                                       
                                        
                                    elif (G.node[doctor1]['type']=="F") and (G.node[doctor2]['type']=="A"):
                                        delta_AF=G.node[doctor2]["adoption_vector"]-G.node[doctor1]["adoption_vector"]
                                        G.node[doctor1]["adoption_vector"]=G.node[doctor1]["adoption_vector"]+delta_AF*alpha_F
                                        G.node[doctor2]["adoption_vector"]=G.node[doctor2]["adoption_vector"]-delta_AF*alpha_A
                                        
                                        
                                    elif  (G.node[doctor1]['type']=="F") and (G.node[doctor2]['type']=="F"):
                                        delta_FF=G.node[doctor1]["adoption_vector"]-G.node[doctor2]["adoption_vector"]
                                        G.node[doctor1]["adoption_vector"]=G.node[doctor1]["adoption_vector"]-delta_FF*alpha_F
                                        G.node[doctor2]["adoption_vector"]=G.node[doctor2]["adoption_vector"]+delta_FF*alpha_F
                                       
                                        
                                    elif  (G.node[doctor1]['type']=="A") and (G.node[doctor2]['type']=="A"):
                                        delta_AA=G.node[doctor1]["adoption_vector"]-G.node[doctor2]["adoption_vector"]
                                        G.node[doctor1]["adoption_vector"]=G.node[doctor1]["adoption_vector"]-delta_AA*alpha_A
                                        G.node[doctor2]["adoption_vector"]=G.node[doctor2]["adoption_vector"]+delta_AA*alpha_A
                                        
                                   

####################################
                                    if float(G.node[doctor1]["adoption_vector"])>=threshold: 
                                        G.node[doctor1]['status']="Adopter"
                                        list_Adopters.append(G.node[doctor1]["label"])      
                                        print "  ",doctor1,G.node[doctor1]['status'],G.node[doctor1]["adoption_vector"]

                                        if  float(G.node[doctor1]["adoption_vector"])>1.0:   # i make sure the values of the vectors stay between [0,1]
                                            print "re-adjusting to 1.0!",G.node[doctor1]["adoption_vector"]
                                            G.node[doctor1]["adoption_vector"]=1.0  
                                    else:
                                        try:
                                            list_Adopters.append(G.node[doctor1]["label"])
                                            print   G.node[doctor1]["label"], "goes back to NonAdopter"
                                        except: pass

                                        G.node[doctor1]['status']="NonAdopter"                                   
                                        if float(G.node[doctor1]["adoption_vector"])<0.0:    # i make sure the values of the vectors stay between [0,1]
                                            print "re-adjusting!",G.node[doctor1]["adoption_vector"]
                                            G.node[doctor1]["adoption_vector"]=0.0
                                            



                                    if float(G.node[doctor2]["adoption_vector"])>=threshold:
                                        G.node[doctor2]['status']="Adopter"
                                        list_Adopters.append(G.node[doctor2]["label"])                                                                              
                                        if  float(G.node[doctor2]["adoption_vector"])>1.0:
                                            #print "re-adjusting!",G.node[doctor2]["adoption_vector"]
                                            G.node[doctor2]["adoption_vector"]=1.0
                                            
                                    else:
                                        try:
                                            list_Adopters.append(G.node[doctor2]["label"])  
                                           # print   G.node[doctor2]["label"], "goes back to NonAdopter"
                                        except: pass
                                        G.node[doctor2]['status']="NonAdopter"
                                        if float(G.node[doctor2]["adoption_vector"])<0.0:
                                          #  print "re-adjusting!",G.node[doctor2]["adoption_vector"]
                                            G.node[doctor2]["adoption_vector"]=0.0

         

                                    print "after:",G.node[doctor1]["label"],G.node[doctor1]["adoption_vector"],G.node[doctor1]['status'],G.node[doctor2]["label"],G.node[doctor2]["adoption_vector"],G.node[doctor2]['status']
                                    raw_input()

                                    print  "# adopters", len(list_Adopters)

                list_single_t_evolution.append(float(len(list_Adopters))/(len(list_A)+len(list_F)))
           
                
                file = open(output_file,'at')                       
                print >> file,t, float(len(list_Adopters))/(len(list_A)+len(list_F)),list_Adopters
                file.close()
                





                t+=1
   
            file = open(output_file,'at')
            print >> file,"\n"
            file.close()


            list_lists_t_evolutions.append(list_single_t_evolution)


      

        file2 = open(output_file2,'at')        
        for s in range(num_shifts):           
            list_fixed_t=[]
            for iter in range (Niter):
                list_fixed_t.append(list_lists_t_evolutions[iter][s])      
            print >> file2, s,numpy.mean(list_fixed_t)                    
        file2.close()



        alpha_F += delta_alpha_F
    


######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
   
        main(graph_filename)
    else:
        print "Usage: python script.py path/network.gml"

    
