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
import csv
import compare_real_evol_vs_simus_to_be_called
import calculate_envelope_set_curves






def main(graph_name):
 

   G = nx.read_gml(graph_name)

   percent_envelope=95.



   Niter=1000


#"../Results/save/Time_evolutions_Persuasion_alpha0.25_damping0.0_mutual_encourg0.5_threshold0.5_unif_distr_1000iter_2012_seed31Oct_finalnetwork.dat"

   alpha_F=0.1  # alpha=0: nobody changes their mind   
   alpha_A=1.*alpha_F

   damping=0.0     #its harder to go back from YES to NO again. =1 means no effect, =0.5 half the movement from Y->N than the other way around, =0 never go back from Y to N        
   mutual_encouragement=0.0  # when two Adopters meet, they convince each other even more      
   threshold=0.5  # larger than, to be an Adopte
  
   
   print "\n\nPersuasion process on network, with Niter:",Niter
   
        
          
    
   dir="../Results/weight_shifts/"  
   output_file=dir+"Time_evolutions_Persuasion_alpha"+str(alpha_F)+"_damping"+str(damping)+"_mutual_encourg"+str(mutual_encouragement)+"_threshold"+str(threshold)+"_unif_distr_"+str(Niter)+"iter_2012_seed31Oct_finalnetwork.dat"        
   file = open(output_file,'wt')    
   file.close()
   


   time_evol_number_adopters_ITER=[]  # list of complete single realizations of the dynamics
  
   
   for iter in range(Niter):

                print "iter:",iter
                list_t=[]
           
                time_evol_number_adopters=[]   # for a single realization of the dynamics


                num_adopters , seed_shift ,max_shift= set_ic(G,threshold)   # i establish who is Adopter and NonAdopter initially, and count how many shifts i have total

                time_evol_number_adopters.append(float(num_adopters))
               # print "initial number of adopters:", num_adopters
                list_t.append(0)




               ########OJO~!!!!!!!!!! COMENTAR ESTO CUANDO ESTOY BARRIENDO TOOOOOOOOOODO EL ESPACIO DE PARAMETROS
              #  file2 = open(output_file.split('.dat')[0]+"_indiv_iter"+str(iter)+".dat",'wt')       
               # file2.close()
              ##########################################



                
               # the dynamics starts:                 
                t=int(seed_shift)+1   # the first time step is just IC.???


                while t<= max_shift:  # loop over shifts, in chronological order  (the order is the day index since seeding_day) 
                         
                    list_t.append(t)
                    for n in G.nodes():
                        if G.node[n]['type']=="shift" and G.node[n]['order']==t:  # i look for the shift corresponding to that time step                    
                            flag_possible_persuasion=0
                            for doctor in G.neighbors(n):                               
                                if G.node[doctor]["status"]=="Adopter":   #first i check if any doctor is an adopter in this shift         
                                    flag_possible_persuasion=1                               
                                    break

                            if flag_possible_persuasion==1:
                                list_doctors=[]
                                for doctor in G.neighbors(n):   # for all drs in that shift
                                    list_doctors.append(doctor)
                                
                                
                                pairs=itertools.combinations(list_doctors,2)    # cos the shift can be 2 but also 3 doctors 
                                for pair in pairs:
                                    doctor1=pair[0]
                                    doctor2=pair[1]
                                                                                        
                                    if G.node[doctor1]['status'] != G.node[doctor2]['status']:  # if they think differently, 
                                                                                              # there will be persuasion
                                        persuasion(G,damping,doctor1,doctor2,alpha_A,alpha_F,threshold)   # i move their values of opinion                  
                                        update_opinions(G,threshold,doctor1,doctor2) #  i update status and make sure the values of the vectors stay between [0,1] 
                                  
                                    else:  # if two Adopters meet, they encourage each other (if two NonAdopters, nothing happens)
                                   
                                       mutual_reinforcement(G,mutual_encouragement,doctor1,doctor2)
                                  
                               
                                    
                    list_Adopters=[]        #count how many i have at this time       
                    for n in G.nodes():              
                        try:
                            if  G.node[n]["status"]=="Adopter":                     
                                if G.node[n]["label"] not in list_Adopters:
                                    list_Adopters.append(G.node[n]["label"])
                        except: pass  # if the node is a shift, it doesnt have a 'status' attribute


        
                   


                    time_evol_number_adopters.append(float(len(list_Adopters)))

                    t+=1
   

                ############## end while loop over t
               

               


             ########OJO~!!!!!!!!!! COMENTAR ESTO CUANDO ESTOY BARRIENDO TOOOOOOOOOODO EL ESPACIO DE PARAMETROS
                #file2 = open(output_file.split('.dat')[0]+"_indiv_iter"+str(iter)+".dat",'at')                
                #for i in range(len(time_evol_number_adopters)):  #ime step by time step                                              
                 #  print >> file2, i,time_evol_number_adopters[i], alpha_F,damping,mutual_encouragement 
                #file.close()
              ########################################################



                time_evol_number_adopters_ITER.append(time_evol_number_adopters)


            #end loop over Niter




   file = open(output_file,'wt')        
   for i in range(len(time_evol_number_adopters)):  #time step by time step
      list_fixed_t=[]
      for iteracion in range (Niter): #loop over all independent iter of the process
         list_fixed_t.append(time_evol_number_adopters_ITER[iteracion][i])  # i collect all values for the same t, different iter  

      print >> file, list_t[i],numpy.mean(list_fixed_t),numpy.std(list_fixed_t), alpha_F,damping,mutual_encouragement   
   file.close()




   calculate_envelope_set_curves.calculate_envelope(time_evol_number_adopters_ITER,percent_envelope,"Persuasion",[alpha_F,damping,mutual_encouragement,threshold])

          



###############################################


def set_ic(G,threshold):

        list_s=[]
        list_A=[]
        list_F=[]
      
        num_shifts=0
        for n in G.nodes():              
            if G.node[n]['type']=="shift":
                num_shifts+=1
                if  G.node[n]['order'] not in list_s:
                    list_s.append(G.node[n]['order'])                        
                if "2011/10/31" in G.node[n]['label']: # actual seeding date                                             
                    seed_shift=G.node[n]['order']
                    seed=n   

            elif G.node[n]['type']=="A":
                if n not in list_A:
                    list_A.append(n)
                    G.node[n]["adoption_vector"]=random.random()*threshold  #values from [0,threshold)
                    G.node[n]["status"]="NonAdopter"  # initially non-Adopters

            elif G.node[n]['type']=="F":
                if n not in list_F:
                    list_F.append(n)
                    G.node[n]["adoption_vector"]=random.random()*threshold
                    G.node[n]["status"]="NonAdopter"  

    
        max_shift=max(list_s)
       
         
           
        list_Adopters=[]                 
        
        for doctor in G.nodes():    #         (SOLO WUNDERINK & WEISS SON ADOPTERS  SEGUROS AL PRINCIPIO...)
           
           if G.node[doctor]["label"]=="Wunderink"  or G.node[doctor]["label"]=="Weiss":  # for sure, only those two, then Sporn and Smith were told...   or G.node[doctor]["label"]=="Sporn"    or G.node[doctor]["label"]=="Smith"
              G.node[doctor]["status"]="Adopter"  
              G.node[doctor]["adoption_vector"]=1.0
              if G.node[doctor]["label"] not in list_Adopters:
                 list_Adopters.append(G.node[doctor]["label"])

           
       
        return float(len(list_Adopters)),seed_shift,max_shift

###########################################

def persuasion(G,damping,doctor1,doctor2,alpha_A,alpha_F,threshold):

    if G.node[doctor1]["adoption_vector"]>=threshold or G.node[doctor2]["adoption_vector"]>=threshold :  # only if at least one doctor is Adopter

        
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
                

            

#####################################



def update_opinions(G,threshold,doctor1,doctor2):

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
            

########################################################



def mutual_reinforcement(G,mutual_encouragement,doctor1,doctor2):


    if G.node[doctor1]['status'] =='Adopter'  and G.node[doctor2]['status']=='Adopter':
        G.node[doctor1]["adoption_vector"]=G.node[doctor1]["adoption_vector"]+mutual_encouragement
        G.node[doctor2]["adoption_vector"]=G.node[doctor2]["adoption_vector"]+mutual_encouragement

        if  float(G.node[doctor1]["adoption_vector"])>1.0:                                             
            G.node[doctor1]["adoption_vector"]=1.0  
        if  float(G.node[doctor2]["adoption_vector"])>1.0:                                             
            G.node[doctor2]["adoption_vector"]=1.0  
                




##################################################
######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
   
        main(graph_filename)
    else:
        print "Usage: python script.py path/network.gml"

    
