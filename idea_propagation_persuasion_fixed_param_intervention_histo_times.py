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
import calculate_envelope_set_curves
import histograma_gral_negv_posit





def main(graph_name):
 

   G = nx.read_gml(graph_name)   # about the "order" in the shift nodes: not all orders exist, only every 5/2 days. thats why shifts have length that we use to weight the interactions accordingly
 
   list_id_weekends_T3=look_for_T3_weekends(G)  # T3 doesnt share fellows in the weekend  (but they are the exception)


   Niter=1000
   dir_real_data='../Results/'


   time_window_ahead=7   # number of days in which there will be no Adopters on call


  


   dict_num_Att_so_far={}      # i get the dict of attendings on call until each day of the study period
   for t in range (0,244):
      dict_num_Att_so_far[t]=find_num_Att_on_call_until_now(G,t)


 
   dict_num_F_so_far={}      # i get the dict of attendings on call until each day of the study period
   for t in range (0,244):     
      dict_num_F_so_far[t]=find_num_Fellows_on_call_until_now(G,t)
     
 
  

   basic_intervention_start_day=20   # and then plus minus a small random number 

   random_start="YES"  # if no, all iter with same initial re-seeding (intervention) day

   num_reseeds=1   # per intervention



   min_bump=0.0  # for the doctors that are re-seeded 
   max_bump=1.0  #same scale as the status, and the adoption threshold
   delta_bump=0.005



   all_team="NO"   # as adopters or not




######################################################################################
#  I read the file of the actual evolution of the idea spreading in the hospital:   ##
######################################################################################



   if all_team=="YES":    
      print "remember that now i use the file of adopters without fellows\n../Results/Actual_evolution_adopters_NO_fellows_only_attendings.dat"
      exit()

   else:
      filename_actual_evol="../Results/Actual_evolution_adopters_NO_fellows_only_attendings.dat"
  


   file1=open(filename_actual_evol,'r')         ## i read the file:  list_dates_and_names_current_adopters.txt  (created with: extract_real_evolution_number_adopters.py)
   list_lines_file=file1.readlines()
            

   list_actual_evol=[]  
   for line in list_lines_file:      # [1:]:   # i exclude the first row   
     
      num_adopters= float(line.split(" ")[1])          
      list_actual_evol.append(num_adopters)


##################################################################





    # i use the best fit  (over the 250-day curve):
 #  from only Att counted as adopters:  ../Results/weight_shifts/persuasion/alpha0.10_damping0.00/Time_evol_Persuasion_alpha0.1_damping0.0_mutual0.5_threshold0.3_1000iter.dat  THIS IS THE THIRD BEST SOLUTION, BUT ENDS UP CLOSER, SO I PREFER TO USE THIS, TO CHECK THE PERFORMANCE WHEN BUMP=0     


   alpha_F=0.10   # alpha=0: nobody changes their mind     

   alpha_A=alpha_F  

   damping=0.0     #its harder to go back from YES to NO again. =1 means no effect, =0.5 half the movement from Y->N than the other way around, =0 never go back from Y to N
         
   mutual_encouragement=0.50  # when two Adopters meet, they convince each other even more
        
   threshold=0.50  # larger than, to be an Adopte
  


   
   
   print "\n\nPersuasion process on network, with Niter:",Niter,"\n"
   
  
          
    
   dir="../Results/weight_shifts/persuasion/" 
 

   
   output_file2="../Results/weight_shifts/Final_distance_vs_bump_alpha"+str(alpha_F)+"_damping"+str(damping)+"_mutual_encourg"+str(mutual_encouragement)+"_threshold"+str(threshold)+"_num_reseed_per_shift"+str(num_reseeds)+"_"+str(Niter)+"iter_intervention_start"+str(basic_intervention_start_day)+"_window"+str(time_window_ahead)+".dat"        
   file2 = open(output_file2,'wt')    
   file2.close()
   

   output_file5="../Results/weight_shifts/Landscape_intervention_alpha"+str(alpha_F)+"_damping"+str(damping)+"_mutual_encourg"+str(mutual_encouragement)+"_threshold"+str(threshold)+"_num_reseed_per_shift"+str(num_reseeds)+"_"+str(Niter)+"iter_start"+str(basic_intervention_start_day)+"_window"+str(time_window_ahead)+".dat"        
   file5 = open(output_file5,'wt')    
   file5.close()
   



 
 
   bump=min_bump
   while bump <= max_bump:
  
   
    print "bump:", bump


    output_file=dir+"Time_evolutions_Persuasion_alpha"+str(alpha_F)+"_damping"+str(damping)+"_mutual_encourg"+str(mutual_encouragement)+"_threshold"+str(threshold)+"_num_reseed_per_shift"+str(num_reseeds)+"_"+str(Niter)+"iter_intervention_start"+str(basic_intervention_start_day)+"_window"+str(time_window_ahead)+"_bump"+str(bump)+".dat"        
    file = open(output_file,'wt')    
    file.close()
   
    list_intervention_days=[]


    dict_days_list_distances_Att={}
    for i in range(0,244):
       dict_days_list_distances_Att[i]=[]


    list_distances_150day_tot=[]
    list_distances_150day_Att=[]
    list_distances_150day_F=[]

    list_distances_200day_tot=[]
    list_distances_200day_Att=[]
    list_distances_200day_F=[]

    list_distances_at_end_tot=[]
    list_distances_at_end_Att=[]
    list_distances_at_end_F=[]

    tot_number_interventions=0
    tot_number_interventions_Att=0
    tot_number_interventions_F=0

    tot_number_successful_interventions=0        
    tot_number_successful_interventions_Att=0   
    tot_number_successful_interventions_F=0   
    

    
   
    time_evol_number_adopters_tot_ITER=[]  # list of complete single realizations of the dynamics    
    time_evol_number_adopters_Att_ITER=[] 
    time_evol_number_adopters_F_ITER=[]  
   
    for iter in range(Niter):

       print "   iter:   ",iter

        
     
        
       list_t=[]      
       time_evol_number_adopters_Att=[]   # for a single realization of the dynamics ONLY ATTENDING ADOPTERS
       time_evol_number_adopters_F=[]   # for a single realization of the dynamics ONLY fellows ADOPTERS
       time_evol_number_tot_adopters=[]  # Attendings and fellows as adopters
       



      

       if   random_start=="YES":   # i pick the first intervention day
         sign=random.random()
         if sign <0.5:
            sign=-1.
         else:
            sign=1.

         delta_day=random.random()*5.
         start_intervention=int(basic_intervention_start_day+sign*delta_day)     #    i let the system evolve freely for a some time  before i start re-seeding

       else:
         start_intervention=basic_intervention_start_day






       num_adopters , seed_shift ,max_shift= set_ic(G,threshold)   # i establish who is Adopter and NonAdopter initially, and count how many shifts i have total
       
       time_evol_number_adopters_Att.append(float(num_adopters))  # the initial two adopters i know are att
       time_evol_number_adopters_F.append(float(0))
       time_evol_number_tot_adopters.append(float(num_adopters))  # Attendings and fellows as adopters

      
      
       list_t.append(0)
       
       next_intervention_day=start_intervention
       
       
               # the dynamics starts:                 
       t=int(seed_shift)+1  

     
      
      
       while t<= max_shift:  # loop over shifts, in chronological order  (the order is the day index since seeding_day) 
        # print t,  time_evol_number_adopters_Att

         old_num_Att_Adopters=0    
         old_num_F_Adopters=0    
         old_num_Adopters=0     #count number of adopters before an intervention
         for n in G.nodes():
            try:                           
               if G.node[n]["status"]=="Adopter" : 
                  old_num_Adopters+=1.            
                  if G.node[n]["type"]=="A":       
                     old_num_Att_Adopters+=1.            
                  elif G.node[n]["type"]=="F":       
                     old_num_F_Adopters+=1.            
     
            except KeyError : pass  #to ignore the shift-nodes
       


         flag_future=look_ahead(G, time_window_ahead, t)    # i evaluate the next few days, to see if any adopter will be on call: if not, i re-seed some more
         if flag_future =="YES"  and t>= start_intervention  and t==next_intervention_day:
            flag_tot,flag_Att,flag_F=intervention(G,t,bump,threshold,num_reseeds,list_intervention_days)   # num of Att intervened

            next_intervention_day+= time_window_ahead  # i dont reseed everyday of the look_ahead window, just the first day of it

         

            tot_number_interventions+=flag_tot
            tot_number_interventions_Att+=flag_Att
            tot_number_interventions_F+=flag_F




            num_Att_Adopters=0   
            num_F_Adopters=0    
            num_Adopters=0    
            for n in G.nodes():
               try:                           
                  if G.node[n]["status"]=="Adopter": #first i check if any doctor is an adopter in this shift   
                     num_Adopters+=1.    
                     if G.node[n]["type"]=="A":   #first i check if any doctor is an adopter in this shift  
                        num_Att_Adopters+=1.            
                     elif G.node[n]["type"]=="F":   #first i check if any doctor is an adopter in this shift  
                        num_F_Adopters+=1.            

               except KeyError : pass
            

            if  old_num_Adopters < num_Adopters:
               
               tot_number_successful_interventions+=1              
               if num_Adopters-old_num_Adopters >num_reseeds:
                  print "how did i bumped more doctors than",num_reseed,"?? ", t, ": ",num_Adopters-old_num_Adopters
                

            if  old_num_Att_Adopters < num_Att_Adopters:               
               tot_number_successful_interventions_Att+=1  
            
            if  old_num_F_Adopters < num_F_Adopters:               
               tot_number_successful_interventions_F+=1              
              


       
      

         list_t.append(t)
         for n in G.nodes():
            if G.node[n]['type']=="shift" and G.node[n]['order']==t:  # i look for the shift corresponding to that time step   

               shift_lenght=int(G.node[n]['shift_lenght'])
                       
               if shift_lenght==2 and n not in list_id_weekends_T3:
                  shift_lenght=1   # because during weekends, the fellow does rounds one day with Att1 and the other day with Att2.  (weekend shifts for T3 are two day long, with no sharing fellows)

      
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
                           persuasion(G,damping,doctor1,doctor2,alpha_A,alpha_F,threshold,shift_lenght)   # i move their values of opinion                  
                           update_opinions(G,threshold,doctor1,doctor2) #  i update status and make sure the values of the vectors stay between [0,1] 
                                  
                        else:  # if two Adopters meet, they encourage each other (if two NonAdopters, nothing happens)
                                   
                           mutual_reinforcement(G,mutual_encouragement,doctor1,doctor2,shift_lenght)
                                  
         list_Att_Adopters=[]                    
         list_F_Adopters=[]                     
         list_Adopters=[]        #count how many i have at this time       
         for n in G.nodes():              
            try:
               if  G.node[n]["status"]=="Adopter":                                      
                  list_Adopters.append(G.node[n]["label"])
                  if G.node[n]["type"]=="A":
                     list_Att_Adopters.append(G.node[n]["label"])
                  elif G.node[n]["type"]=="F":
                     list_F_Adopters.append(G.node[n]["label"])
            except: pass  # if the node is a shift, it doesnt have a 'status' attribute

                
         
         time_evol_number_adopters_Att.append(float(len(list_Att_Adopters)))
         time_evol_number_adopters_F.append(float(len(list_F_Adopters)))
         time_evol_number_tot_adopters.append(float(len(list_Adopters)))  # Attendings and fellows as adopters

         #print t, "num (att) adopters:",len(list_Att_Adopters),"num (f) adopters:",len(list_F_Adopters),"num (tot) adopters:",len(list_Adopters)


         dict_days_list_distances_Att[t].append(time_evol_number_adopters_Att[t]-list_actual_evol[t])



         t+=1
   

         ############# end while loop over t
               
     

       time_evol_number_adopters_Att_ITER.append(time_evol_number_adopters_Att) 
       time_evol_number_adopters_F_ITER.append(time_evol_number_adopters_F) 
       time_evol_number_adopters_tot_ITER.append(time_evol_number_tot_adopters) 

     
     


       list_distances_150day_Att.append(time_evol_number_adopters_Att[-93]-list_actual_evol[-93])  # because last day is 243      
       list_distances_150day_tot.append(time_evol_number_tot_adopters[-93]-list_actual_evol[-93])

       list_distances_200day_Att.append(time_evol_number_adopters_Att[-43]-list_actual_evol[-43])   
       list_distances_200day_tot.append(time_evol_number_tot_adopters[-43]-list_actual_evol[-43])

       list_distances_at_end_Att.append(time_evol_number_adopters_Att[-1]-list_actual_evol[-1])  
       list_distances_at_end_tot.append(time_evol_number_tot_adopters[-1]-list_actual_evol[-1])




     #  print  "diff. at day 200:",time_evol_number_adopters[-43]-list_actual_evol[-43],time_evol_number_adopters[-43],list_actual_evol[-43],"diff. at the end:",time_evol_number_adopters[-1]-list_actual_evol[-1],time_evol_number_adopters[-1],list_actual_evol[-1] ," if i count tot Att+Fellows at end:",time_evol_number_tot_adopters[-1],"for bump:",bump
                               
  
          
   ##############end loop Niter

    parameters=[alpha_F, damping, mutual_encouragement, threshold,bump,time_window_ahead]
    calculate_envelope_set_curves.calculate_envelope(time_evol_number_adopters_Att_ITER, 95,"Persuasion_intervention",parameters)


   # print time_evol_number_adopters_Att_ITER



    file = open(output_file,'wt')        
    for i in range(len(time_evol_number_adopters_Att)):  #time step by time step
       list_fixed_t_Att=[]     
       list_fixed_t_F=[]     
       list_fixed_t_tot=[]     
      
       for iteracion in range (Niter): #loop over all independent iter of the process

         
         list_fixed_t_Att.append(time_evol_number_adopters_Att_ITER[iteracion][i])  # i collect all values for the same t, different iter  
         list_fixed_t_F.append(time_evol_number_adopters_F_ITER[iteracion][i])  # i collect all values for the same t, different iter  
         list_fixed_t_tot.append(time_evol_number_adopters_tot_ITER[iteracion][i])  # i collect all values for the same t, different iter  
       
        


      
       print >> file, list_t[i],numpy.mean(list_fixed_t_Att),numpy.std(list_fixed_t_Att),numpy.mean(list_fixed_t_F),numpy.std(list_fixed_t_F),numpy.mean(list_fixed_t_tot),numpy.std(list_fixed_t_tot),dict_num_Att_so_far[i],numpy.mean(list_fixed_t_Att)/float(dict_num_Att_so_far[i]),dict_num_F_so_far[i],numpy.mean(list_fixed_t_F)/float(dict_num_F_so_far[i]), alpha_F,damping,mutual_encouragement,threshold       
    file.close()



    print "   written:", output_file

  

    try:
       fraction_success_interv=float(tot_number_successful_interventions)/float(tot_number_interventions)  #averages over Niter
    except ZeroDivisionError:
       fraction_success_interv=0

    try:
       fraction_success_interv_Att=float(tot_number_successful_interventions_Att)/float(tot_number_interventions_Att) #averages over Niter
    except  ZeroDivisionError:
       fraction_success_interv_Att=0

    try:
       fraction_success_interv_F=float(tot_number_successful_interventions_F)/float(tot_number_interventions_F) #averages over Niter
    except  ZeroDivisionError:
       fraction_success_interv_F=0


    file2 = open(output_file2,'at')           
    print >> file2, bump, numpy.mean(list_distances_150day_Att),numpy.std(list_distances_150day_Att), \
        numpy.mean(list_distances_150day_tot),numpy.std(list_distances_150day_tot), \
        numpy.mean(list_distances_200day_Att),numpy.std(list_distances_200day_Att), \
        numpy.mean(list_distances_200day_tot),numpy.std(list_distances_200day_tot),\
        numpy.mean(list_distances_at_end_Att),numpy.std(list_distances_at_end_Att), \
        numpy.mean(list_distances_at_end_tot), numpy.std(list_distances_at_end_tot),\
        float(tot_number_interventions)/float(Niter) , float(tot_number_interventions_Att)/float(Niter) ,float(tot_number_interventions_F)/float(Niter) ,fraction_success_interv, fraction_success_interv_Att, fraction_success_interv_F, bump/float(threshold)
    file2.close()


   
   

            
    print   "fraction successful interventions",fraction_success_interv,"fraction successful interventions on Att",fraction_success_interv_Att,"fraction successful interventions on F",fraction_success_interv_F
   
   

    print "   written:", output_file2
  

    if len(list_intervention_days)>0:
       histogram_filename="../Results/weight_shifts/histogr_interv_days_alpha"+str(alpha_F)+"_damping"+str(damping)+"_mutual_encourg"+str(mutual_encouragement)+"_threshold"+str(threshold)+"_num_reseed_per_shift"+str(num_reseeds)+"_"+str(Niter)+"iter_intervention_start"+str(basic_intervention_start_day)+"_window"+str(time_window_ahead)+"_bump"+str(bump)+".dat"        
       
       
       
#       print "list interv days:",list_intervention_days
   
       histograma_gral_negv_posit.histograma(list_intervention_days, histogram_filename,True)   # last parameter: whether i want to print out the values Prob=0 or not
    
       print "written histogram interv. days:",histogram_filename



    else:
       print "empty list_intervention_days"
       raw_input()




    file5 = open(output_file5,'at')     
    for t in range (0,244):      
       print >> file5, bump, t, numpy.mean(dict_days_list_distances_Att[t]),numpy.std(dict_days_list_distances_Att[t]), alpha_A,damping, mutual_encouragement,  threshold 
      # print bump, t, numpy.mean(dict_days_list_distances_Att[t]),dict_days_list_distances_Att[t]
    file5.close()
       

 
  


    bump+=delta_bump
    ########################## end loop over bump


   print "\nwritten:", output_file2
   print "   written:", output_file5


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

    
        max_shift=max(list_s) #the last day
       
         
           
        list_Adopters=[]                 
        
        for doctor in G.nodes():    #         (SOLO WUNDERINK & WEISS SON ADOPTERS  SEGUROS AL PRINCIPIO...)
           
           if G.node[doctor]["label"]=="Wunderink"  or G.node[doctor]["label"]=="Weiss":  # for sure, only those two, Sporn and Smith were only told...   
              G.node[doctor]["status"]="Adopter"  
              G.node[doctor]["adoption_vector"]=1.0
              if G.node[doctor]["label"] not in list_Adopters and G.node[doctor]["type"]=="A":
                 list_Adopters.append(G.node[doctor]["label"])

           
       
        return float(len(list_Adopters)),seed_shift,max_shift

###########################################

def persuasion(G,damping,doctor1,doctor2,alpha_A,alpha_F,threshold,shift_lenght):



    if G.node[doctor1]["adoption_vector"]>=threshold or G.node[doctor2]["adoption_vector"]>=threshold :  # only if at least one doctor is Adopter


        alpha_A=alpha_A*shift_lenght   # to take into account the lenght shift
        alpha_F=alpha_F*shift_lenght 

        
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



def mutual_reinforcement(G,mutual_encouragement,doctor1,doctor2,shift_lenght):

   
    if G.node[doctor1]['status'] =='Adopter'  and G.node[doctor2]['status']=='Adopter':

        mutual_encouragement=mutual_encouragement*shift_lenght
        G.node[doctor1]["adoption_vector"]=G.node[doctor1]["adoption_vector"]+mutual_encouragement
        G.node[doctor2]["adoption_vector"]=G.node[doctor2]["adoption_vector"]+mutual_encouragement

        if  float(G.node[doctor1]["adoption_vector"])>1.0:  
            G.node[doctor1]["adoption_vector"]=1.0  
        if  float(G.node[doctor2]["adoption_vector"])>1.0:     
            G.node[doctor2]["adoption_vector"]=1.0  



##################################################                

def look_ahead(G, time_window_ahead, t):

   flag_reseed="YES"
   for t in range(t, t+time_window_ahead+1):  #for i in range(2,8)=  2,  3, 4, 5, 6, 7 

      for n in G.nodes():
         if G.node[n]['type']=="shift" and G.node[n]['order']==t:  # i look for the shift corresponding to that time step   
            for doctor in G.neighbors(n):                               
               if G.node[doctor]["status"]=="Adopter":   #first i check if any doctor is an adopter in this shift         
                  flag_reseed="NO"                               
                  break
            

   return flag_reseed





##################################################                

def  intervention(G, t,bump,threshold,num_reseeds,list_intervention_days):

   flag_Att=0
   flag_F=0
   flag_tot=0

   cont_reseeds=0
   for n in G.nodes():     

      if G.node[n]['type']=="shift" :

         lenght=int(G.node[n]['shift_lenght'])
         if (G.node[n]['order']>=t  and G.node[n]['order']<t+lenght) and cont_reseeds<= num_reseeds:  # i look for the shift corresponding to that time step       (remember that not all t's from the dynamics have an asociated shift, because shifts have lenght 2 and 5)   
         
            flag_option_bump=0  # i check whether there are NonAdopters i can give a bump to
            list_drs=G.neighbors(n)

            list_NonAdopters=[]
            for dr in list_drs:
               if  G.node[dr]["status"]=="NonAdopter":
                  flag_option_bump=1
                  list_NonAdopters.append(dr)

            if flag_option_bump ==1:
               doctor= random.choice(list_NonAdopters)
             
               flag_tot+=1  

               if  G.node[doctor]['type']=="A":
                  flag_Att+=1
               elif  G.node[doctor]['type']=="F":
                  flag_F+=1
                  
             
              

               G.node[doctor]["adoption_vector"]+=bump  # i give a bump to a doctors in the intervention shift
               cont_reseeds+=1

               list_intervention_days.append(t)


               if float(G.node[doctor]["adoption_vector"])>=threshold:
                  G.node[doctor]['status']="Adopter"          
                #  if  G.node[doctor]['type']=="A":
                                    
                 #    print "i just bumped an Attending!"                 

         
                  if  float(G.node[doctor]["adoption_vector"])>1.0:                                            
                     G.node[doctor]["adoption_vector"]=1.0
              


               
               if cont_reseeds== num_reseeds:
                     #print "i exactly what was necessary on shift", t
                  break

               elif cont_reseeds> num_reseeds:
                     print "i bumpped more than necessary on shift", t
                     #raw_input()
                     break



   return flag_tot,flag_Att,flag_F   # i return the number intervented Attendings



######################################



def look_for_T3_weekends(G):

   list_ids_T3_weekends=[]
   for n in G.nodes():
      if G.node[n]['type']=='shift':
         if G.node[n]['shift_lenght']==2 and "T3" in G.node[n]['label']:
            list_ids_T3_weekends.append(n)
            

               
   return  list_ids_T3_weekends
 ##################################################
######################################


def  find_num_Att_on_call_until_now(G,t):

   
   list_names_so_far=[]
   for node in G.nodes():
      if G.node[node]['type']=="shift" and G.node[node]['order']<=t :                 
         for doctor in G.neighbors(node):                       
               if  G.node[doctor]['type']=="A" :
                  if G.node[doctor]['label'] not in list_names_so_far:
                     list_names_so_far.append(G.node[doctor]['label'])
                  
                 
                
   return len(list_names_so_far)
 ##################################################
######################################


def  find_num_Fellows_on_call_until_now(G,t):

   
   list_names_so_far=[]
   for node in G.nodes():
      if G.node[node]['type']=="shift" and G.node[node]['order']<=t :                 
         for doctor in G.neighbors(node):                       
               if  G.node[doctor]['type']=="F" :
                  if G.node[doctor]['label'] not in list_names_so_far:
                     list_names_so_far.append(G.node[doctor]['label'])
                  
                 
                
   return len(list_names_so_far)
##################################################
######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
   
        main(graph_filename)
    else:
        print "Usage: python script.py path/network.gml"

    
