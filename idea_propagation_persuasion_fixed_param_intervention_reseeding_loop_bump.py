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
import histograma_bines_gral
import calculate_numeric_integral







def main(graph_name):
 

   G = nx.read_gml(graph_name)   # about the "order" in the shift nodes: not all orders exist, only every 5/2 days. thats why shifts have length (that we ignore for now)
 

   Niter=1000
 
   dir_real_data='../Results/'


   time_window_ahead=7   # number of days in which there will be no Adopters on call

   basic_reeding_start_day=20   # and then plus minus a small random number 

   random_start="NO"

   num_reseeds=1   # per intervention



   min_bump=0.0  # for the doctors that are re-seeded 
   max_bump=0.3
   delta_bump=0.005



# count the number of need re-seeded!!!!!!!!!




   all_team="NO"   # as adopters or not




######################################################################################
#  I read the file of the actual evolution of the idea spreading in the hospital:   ##
######################################################################################



   if all_team=="YES":    
      filename_actual_evol=dir_real_data+"HospitalModel_august1_adoption_counts_all_team_as_adopters_SIMPLER.csv"

   else:
      filename_actual_evol=dir_real_data+"HospitalModel_august1_adoption_counts_SIMPLER.csv"
  
  
   list_actual_evol=[]
   result_actual_file= csv.reader(open(filename_actual_evol, 'rb'), delimiter=',')
   cont=0
   for row in result_actual_file: 
       if cont>0:   # i ignore the first line with the headers
           
           
           num_adopters= row[3]
          
           list_actual_evol.append(float(num_adopters))
          
          

       cont+=1    
  

##################################################################





    # i use the best fit:
   #../Results/network_final_schedule_withTeam3_local/Time_evolutions_Persuasion_alpha0.1_damping0.3_mutual_encourg0.3_threshold0.2_unif_distr_100iter_2012_seed31Oct_finalnetwork.dat




   alpha_F=0.250   # alpha=0: nobody changes their mind     

   alpha_A=0.5*alpha_F  

   damping=0.0     #its harder to go back from YES to NO again. =1 means no effect, =0.5 half the movement from Y->N than the other way around, =0 never go back from Y to N
         
   mutual_encouragement=0.50  # when two Adopters meet, they convince each other even more
        
   threshold=0.50  # larger than, to be an Adopte
  


   
   
   print "\n\nPersuasion process on network, with Niter:",Niter,"\n"
   
  
          
    
   dir="../Results/network_final_schedule_withTeam3_local/" 
 

   
   output_file2="../Results/Final_distance_vs_bump"+str(alpha_F)+"_damping"+str(damping)+"_mutual_encourg"+str(mutual_encouragement)+"_threshold"+str(threshold)+"_unif_distr_"+str(Niter)+"iter_reseeding_start"+str(basic_reeding_start_day)+".dat"        
   file2 = open(output_file2,'wt')    
   file2.close()
   


 
   bump=min_bump
   while bump <= max_bump:
  

    print "bump:", bump


    output_file=dir+"Time_evolutions_Persuasion_alpha"+str(alpha_F)+"_damping"+str(damping)+"_mutual_encourg"+str(mutual_encouragement)+"_threshold"+str(threshold)+"_unif_distr_"+str(Niter)+"iter_reseeding_start"+str(basic_reeding_start_day)+"r_bump"+str(bump)+".dat"        
    file = open(output_file,'wt')    
    file.close()
   



    list_ending_distances=[]
    tot_number_successful_interventions=0
    tot_number_interventions=0

    tot_number_succesfully_reseeded=0

    time_evol_number_adopters_ITER=[]  # list of complete single realizations of the dynamics    
   
    for iter in range(Niter):

       print "   iter:   ",iter



       if   random_start=="YES":

         sign=random.random()
         if sign <0.5:
            sign=-1.
         else:
            sign=1.

         delta_day=random.random()*5.
         start_reseeding=int(basic_reeding_start_day+sign*delta_day)     #   30*10*random.random()   # i let the system evolve freely for a month before i start re-seeding

       else:
         start_reseeding=basic_reeding_start_day
     

#       print start_reseeding 
    



   
     
       list_t=[]     
       time_evol_number_adopters=[]   # for a single realization of the dynamics
      
      
       num_adopters , seed_shift ,max_shift= set_ic(G,threshold)   # i establish who is Adopter and NonAdopter initially, and count how many shifts i have total
       
       time_evol_number_adopters.append(float(num_adopters))       
       list_t.append(0)
       
       
       
       
       next_reseeding_day=start_reseeding
       
       
       ############## the dynamics starts:    
             
       t=int(seed_shift)+1   # the first time step is just IC.???
      
      
       while t<= max_shift:  # loop over shifts, in chronological order  (the order is the day index since seeding_day) 
                     
         old_num_Adopters=0    
         for n in G.nodes():
            try:                           
               if G.node[n]["status"]=="Adopter":   #first i check if any doctor is an adopter in this shift         
                  old_num_Adopters+=1.            
            except KeyError : pass
       


         flag_future=look_ahead(G, time_window_ahead, t)    # i evaluate the next few days, to see if any adopter will be on call: if not, i re-seed some more
         if flag_future =="YES"  and t>= start_reseeding  and t==next_reseeding_day:
            reseeding(G,t,bump,threshold,num_reseeds)

            next_reseeding_day+= time_window_ahead  # i dont reseed everyday of the look_ahead window, just the first day of it

            print "     reseeding on day", t

            tot_number_interventions+=1

            num_Adopters=0    
            for n in G.nodes():
               try:                           
                  if G.node[n]["status"]=="Adopter":   #first i check if any doctor is an adopter in this shift         
                     num_Adopters+=1.            
               except KeyError : pass
            print "       # adopters before the bump",old_num_Adopters
            
            print "          # adopters after the bump",num_Adopters

            if  old_num_Adopters < num_Adopters:
               print "            successful bump!"
               tot_number_successful_interventions+=1
               tot_number_succesfully_reseeded+=(num_Adopters-old_num_Adopters)





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
   

         ############# end while loop over t
               
     
       time_evol_number_adopters_ITER.append(time_evol_number_adopters)
       list_ending_distances.append(time_evol_number_adopters[-1]-list_actual_evol[-1])
                               
  
          
   ##############end loop Niter

    file = open(output_file,'wt')        
    for i in range(len(time_evol_number_adopters)):  #time step by time step
       list_fixed_t=[]
       for iteracion in range (Niter): #loop over all independent iter of the process
         list_fixed_t.append(time_evol_number_adopters_ITER[iteracion][i])  # i collect all values for the same t, different iter  

       print >> file, list_t[i],numpy.mean(list_fixed_t),numpy.std(list_fixed_t), alpha_F,damping,mutual_encouragement       
    file.close()





    file2 = open(output_file2,'at')           
    print >> file2, bump, numpy.mean(list_ending_distances),numpy.std(list_ending_distances), float(tot_number_interventions)/float(Niter) ,float(tot_number_successful_interventions)/float(Niter),float(tot_number_succesfully_reseeded)/float(Niter), bump/float(threshold)
    file2.close()





            
    print   "   tot # interventions",float(tot_number_interventions)/float(Niter),"tot # successful interventions",float(tot_number_successful_interventions)/float(Niter),"tot # successfully reseeded drs:",float(tot_number_succesfully_reseeded)/float(Niter)
   

    print "   written:", output_file







    bump+=delta_bump
    ########################## end loop over bump


   print "\nwritten:", output_file2


########################################################
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

def look_ahead(G, time_window_ahead, t):

   flag_reseed="YES"
   for t in range(t, t+time_window_ahead+1):  #for i in range(2,8):  2  3 4  5 6 7 

      for n in G.nodes():
         if G.node[n]['type']=="shift" and G.node[n]['order']==t:  # i look for the shift corresponding to that time step               
            for doctor in G.neighbors(n):                               
               if G.node[doctor]["status"]=="Adopter":   #first i check if any doctor is an adopter in this shift         
                  flag_reseed="NO"                               
                  break
            

   return flag_reseed





##################################################                

def  reseeding(G, t,bump,threshold,num_reseeds):

  
  
   cont_reseeds=0
   for n in G.nodes():     

      if G.node[n]['type']=="shift" and (G.node[n]['order']>=t  and G.node[n]['order']<=t+7) and cont_reseeds<= num_reseeds:  # i look for the shift corresponding to that time step          
         
         for doctor in G.neighbors(n):    # for now, i give a bump to all doctors in the reseeding shift

           

            if G.node[doctor]["status"]=="NonAdopter": 
               
               
               G.node[doctor]["adoption_vector"]+=bump

              

              
               if float(G.node[doctor]["adoption_vector"])>=threshold:
                  G.node[doctor]['status']="Adopter"          
                  cont_reseeds+=1
                  
                  if  float(G.node[doctor]["adoption_vector"])>1.0:                                            
                     G.node[doctor]["adoption_vector"]=1.0
              



   
  

##################################################
######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
   
        main(graph_filename)
    else:
        print "Usage: python script.py path/network.gml"

    
