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


import random


def main(graph_name):
 

    G = nx.read_gml(graph_name)


    threshold=0.75  # larger than, to be an Adopter

    alpha_F_min=0.0
    alpha_F_max=1.01
    delta_alpha_F=0.1
    damping=0.50  #its harder to go back from YES to NO again. =1 means no effect, =0.5 half the movement from Y->N than the other way around, =0 never go back from Y to N


    mutual_encouragement=0.1  # when two Adopters meet, they convince each other even more




   
    tot_num_shifts=0
    for n in G.nodes():           
        if G.node[n]['type']=="shift":               
            tot_num_shifts+=1
            


    alpha_F=alpha_F_min
    while alpha_F<= alpha_F_max:

        alpha_A=0.5*alpha_F

        print "alpha_F:",alpha_F
   
       
        dir="../Results/"   
        output_file2=dir+"Final_number_Adopters_Persuasion_alpha"+str(alpha_F)+"_damping"+str(damping)+"_mutual_encourg"+str(mutual_encouragement)+"_unif_distr_2012.dat"    
        file2 = open(output_file2,'wt')    
        file2.close()


    
        for num_initial_shifts in range(tot_num_shifts):            
                     
            num_initial_shifts+=1


            print num_initial_shifts

            dir="../Results/"   
            output_file=dir+"Time_evolutions_Persuasion_alpha"+str(alpha_F)+"_damping"+str(damping)+"_num_shifts"+str(num_initial_shifts)+"_mutual_encourg"+str(mutual_encouragement)+"_unif_distr_2012.dat"    
            file = open(output_file,'wt')    
            file.close()
            


            list_working_doctors=[] 
            list_s=[]
            list_A=[]
            list_F=[]
            list_seed_shift=[]
            list_order_seed_shift=[]
            for s in range(num_initial_shifts):
                for n in G.nodes():              
                    if G.node[n]['type']=="shift":
                        if n not in list_s:
                            list_s.append(n)                        
                        if G.node[n]['order']==s:                          
                               list_seed_shift.append(n)
                               list_order_seed_shift.append(G.node[n]['order'])
                       

                    elif G.node[n]['type']=="A":
                        if n not in list_A:
                            list_A.append(n)
                            G.node[n]["adoption_vector"]=random.random()*threshold
                            G.node[n]["status"]="NonAdopter"  # initially non-Adopters

                    elif G.node[n]['type']=="F":
                        if n not in list_F:
                            list_F.append(n)
                            G.node[n]["adoption_vector"]=random.random()*threshold
                            G.node[n]["status"]="NonAdopter"  

    
                max_shift=len(list_s)+1

           # print "# doctors:",str(len(list_F)+len(list_A))
           
            list_Adopters=[]                 
            for seed in list_seed_shift: # i can infect initially more than one shift
                for doctor in G.neighbors(seed):
                    G.node[doctor]["status"]="Adopter"  # all doctors in that shift are Infected
                    G.node[doctor]["adoption_vector"]=1.0
                    if G.node[doctor]["label"] not in list_Adopters:
                        list_Adopters.append(G.node[doctor]["label"])

                    if doctor not in list_working_doctors:  # the norm for the fraction of Adopters
                        list_working_doctors.append(G.node[doctor]["label"])

        
           
# the dynamics starts: 
         
            t=int(min(list_order_seed_shift))
            while t<= max_shift:  # loop over shifts, in chronological order   
                         
               
                for n in G.nodes():
                    if G.node[n]['type']=="shift" and G.node[n]['order']==t:
                        flag_possible_persuasion=0
                        for doctor in G.neighbors(n):
                            if doctor not in list_working_doctors:  # the norm for the fraction of Adopters
                                list_working_doctors.append(G.node[doctor]["label"])

                            if G.node[doctor]["status"]=="Adopter":   #first i check if any doctor is an adopter in this shift         
                                flag_possible_persuasion=1                               
                                break

                        if flag_possible_persuasion==1:
                            list_doctors=[]
                            for doctor in G.neighbors(n):
                                list_doctors.append(doctor)
                                
                                
                            pairs=itertools.combinations(list_doctors,2)    # cos the shift can be 2 but also 3 doctors 
                            for pair in pairs:
                                doctor1=pair[0]
                                doctor2=pair[1]
                                                                                        
                                if G.node[doctor1]['status'] != G.node[doctor2]['status']:  # if they think differently, there will be  persuasion:
                                 

                                    #print "  before:",G.node[doctor1]["label"],G.node[doctor1]["adoption_vector"],G.node[doctor1]['status'],",",G.node[doctor2]["label"],G.node[doctor2]["adoption_vector"],G.node[doctor2]['status']

                                    if (G.node[doctor1]['type']=="A") and (G.node[doctor2]['type']=="F"):
                                        delta_AF=G.node[doctor1]["adoption_vector"]-G.node[doctor2]["adoption_vector"]

                                        if float(delta_AF)>=0.0:
                                            G.node[doctor1]["adoption_vector"]=G.node[doctor1]["adoption_vector"]-delta_AF*alpha_A*damping  #from YES to NO
                                            G.node[doctor2]["adoption_vector"]=G.node[doctor2]["adoption_vector"]+delta_AF*alpha_F  #from NO to YES
                                        else:
                                            G.node[doctor1]["adoption_vector"]=G.node[doctor1]["adoption_vector"]-delta_AF*alpha_A
                                            G.node[doctor2]["adoption_vector"]=G.node[doctor2]["adoption_vector"]+delta_AF*alpha_F*damping
                                        
                                    elif (G.node[doctor1]['type']=="F") and (G.node[doctor2]['type']=="A"):
                                        delta_FA=G.node[doctor1]["adoption_vector"]-G.node[doctor2]["adoption_vector"]

                                        if float(delta_FA)>=0.0:
                                            G.node[doctor1]["adoption_vector"]=G.node[doctor1]["adoption_vector"]-delta_FA*alpha_F*damping
                                            G.node[doctor2]["adoption_vector"]=G.node[doctor2]["adoption_vector"]+delta_FA*alpha_A
                                        else:
                                            G.node[doctor1]["adoption_vector"]=G.node[doctor1]["adoption_vector"]-delta_FA*alpha_F
                                            G.node[doctor2]["adoption_vector"]=G.node[doctor2]["adoption_vector"]+delta_FA*alpha_A*damping
                                        
                                        
                                    elif  (G.node[doctor1]['type']=="F") and (G.node[doctor2]['type']=="F"):
                                        delta_FF=G.node[doctor1]["adoption_vector"]-G.node[doctor2]["adoption_vector"]
                                        if float(delta_FF)>=0.0:
                                            G.node[doctor1]["adoption_vector"]=G.node[doctor1]["adoption_vector"]-delta_FF*alpha_F*damping
                                            G.node[doctor2]["adoption_vector"]=G.node[doctor2]["adoption_vector"]+delta_FF*alpha_F
                                        else:
                                            G.node[doctor1]["adoption_vector"]=G.node[doctor1]["adoption_vector"]-delta_FF*alpha_F
                                            G.node[doctor2]["adoption_vector"]=G.node[doctor2]["adoption_vector"]+delta_FF*alpha_F*damping
                                       
                                        
                                    elif  (G.node[doctor1]['type']=="A") and (G.node[doctor2]['type']=="A"):
                                        delta_AA=G.node[doctor1]["adoption_vector"]-G.node[doctor2]["adoption_vector"]
                                        if float(delta_AA)>=0.0:
                                            G.node[doctor1]["adoption_vector"]=G.node[doctor1]["adoption_vector"]-delta_AA*alpha_A*damping
                                            G.node[doctor2]["adoption_vector"]=G.node[doctor2]["adoption_vector"]+delta_AA*alpha_A
                                        else:
                                            G.node[doctor1]["adoption_vector"]=G.node[doctor1]["adoption_vector"]-delta_AA*alpha_A
                                            G.node[doctor2]["adoption_vector"]=G.node[doctor2]["adoption_vector"]+delta_AA*alpha_A*damping
                                        
                                   

####################################
                                    if float(G.node[doctor1]["adoption_vector"])>=threshold: 
                                        G.node[doctor1]['status']="Adopter"               
                                        if  float(G.node[doctor1]["adoption_vector"])>1.0:   # i make sure the values of the vectors stay between [0,1]                                          
                                            G.node[doctor1]["adoption_vector"]=1.0  
                                    else:                                       

                                        G.node[doctor1]['status']="NonAdopter"                                   
                                        if float(G.node[doctor1]["adoption_vector"])<0.0:    # i make sure the values of the vectors stay between [0,1]                                         
                                            G.node[doctor1]["adoption_vector"]=0.0
                                            



                                    if float(G.node[doctor2]["adoption_vector"])>=threshold:
                                        G.node[doctor2]['status']="Adopter"                                                                                                             
                                        if  float(G.node[doctor2]["adoption_vector"])>1.0:                                            
                                            G.node[doctor2]["adoption_vector"]=1.0
                                            
                                    else:                                       
                                        G.node[doctor2]['status']="NonAdopter"
                                        if float(G.node[doctor2]["adoption_vector"])<0.0:                                          
                                            G.node[doctor2]["adoption_vector"]=0.0


                                    #print "   after:",G.node[doctor1]["label"],G.node[doctor1]["adoption_vector"],G.node[doctor1]['status'],",",G.node[doctor2]["label"],G.node[doctor2]["adoption_vector"],G.node[doctor2]['status']
                                else:  # if two Adopters meet, they encourage each other
                                    #print "  before:",G.node[doctor1]["label"],G.node[doctor1]["adoption_vector"],G.node[doctor1]['status'],",",G.node[doctor2]["label"],G.node[doctor2]["adoption_vector"],G.node[doctor2]['status']
                                    if G.node[doctor1]['status'] =='Adopter'  and G.node[doctor2]['status']=='Adopter':
                                        G.node[doctor1]["adoption_vector"]=G.node[doctor1]["adoption_vector"]+mutual_encouragement
                                        G.node[doctor2]["adoption_vector"]=G.node[doctor2]["adoption_vector"]+mutual_encouragement
                                        if  float(G.node[doctor1]["adoption_vector"])>1.0:                                             
                                            G.node[doctor1]["adoption_vector"]=1.0  
                                        if  float(G.node[doctor2]["adoption_vector"])>1.0:                                             
                                            G.node[doctor2]["adoption_vector"]=1.0  

                                    #print "   after:",G.node[doctor1]["label"],G.node[doctor1]["adoption_vector"],G.node[doctor1]['status'],",",G.node[doctor2]["label"],G.node[doctor2]["adoption_vector"],G.node[doctor2]['status']
                               
                                   

                                    
                list_Adopters=[]               
                for n in G.nodes():              
                    try:
                        if  G.node[n]["status"]=="Adopter":                     
                            if G.node[n]["label"] not in list_Adopters:
                                list_Adopters.append(G.node[n]["label"])
                    except: pass
               
        
                file = open(output_file,'at')                       
                print >> file,t, float(len(list_Adopters)),len(list_working_doctors)
                file.close()
    
               
               # print  "# adopters at t",t, len(list_Adopters),list_Adopters
               
                t+=1
   
            file2 = open(output_file2,'at')
            print >> file2,num_initial_shifts,float(len(list_Adopters)),len(list_working_doctors),alpha_F,mutual_encouragement,damping,threshold
            file2.close()



        file2 = open(output_file2,'at')
        print >> file2,"\n"
        file2.close()

        alpha_F += delta_alpha_F
    


######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
   
        main(graph_filename)
    else:
        print "Usage: python script.py path/network.gml"

    
