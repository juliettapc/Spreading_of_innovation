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
import histograma_gral_negv_posit
import histograma_bines_gral
import calculate_envelope_set_curves


def main(graph_name):
 

   G = nx.read_gml(graph_name)


   list_id_weekends_T3=look_for_T3_weekends(G)  # T3 doesnt share fellows in the weekend  (but they are the exception)

   percent_envelope=95.

   Niter=1001




   cutting_day=175



   min_sum_dist=20   # to compute number of realizations that have a sum of distances smaller than this



   delta_end=3.  # >= than + or -  dr difference at the end of the evolution

   dir_real_data='../Results/'



######################################################################################
#  I read the file of the actual evolution of the idea spreading in the hospital:   ##
######################################################################################




   filename_actual_evol="../Data/Actual_evolution_adopters_NO_fellows_only_attendings_with_list_names.csv"    #   "../Results/Actual_evolution_adopters_from_inference.dat"
  


   file1=open(filename_actual_evol,'r')         ## i read the file:  list_dates_and_names_current_adopters.txt  (created with: extract_real_evolution_number_adopters.py)
   list_lines_file=file1.readlines()
            


   dict_days_list_empirical_att_adopters={}
   list_actual_evol=[]  
   for line in list_lines_file:      # [1:]:   # i exclude the first row            
      day=int(line.split(" ")[0])       
      num_adopters= float(line.split(" ")[1])          
      list_actual_evol.append(num_adopters)

      list_current_att_adopters=[]
      for element in line.split(" ")[2:]:   # i need to ignore the empty columns from the original datafile
         if element:
            if element != '\n':
               list_current_att_adopters.append(element.strip('\n').title())     

      dict_days_list_empirical_att_adopters[day]=list_current_att_adopters
  
   


   list_actual_evol_testing=list_actual_evol[cutting_day:]



##################################################################



 
   alpha_F_min=0.10   
   alpha_F_max=0.101  
   delta_alpha_F=0.10    #AVOID 1.0 OR THE DYNAMICS GETS TOTALLY STUCK AND IT IS NOT ABLE TO PREDICT SHIT!
   

   min_damping=0.00      #its harder to go back from YES to NO again. =1 means no effect, =0.5 half the movement from Y->N than the other way around, =0 never go back from Y to N
   max_damping=0.01  
   delta_damping=0.10  
   
   


   min_mutual_encouragement=0.00     # when two Adopters meet, they convince each other even more
   max_mutual_encouragement=0.01  
   delta_mutual_encouragement=0.10
   
   
   threshold_min=0.50    # larger than, to be an Adopter
   threshold_max=0.501     # KEEP THIS FIXED VALUES FOR NOW
   delta_threshold=0.10   # AVOID 1.0 OR THE DYNAMICS GETS TOTALLY STUCK AND IT IS NOT ABLE TO PREDICT SHIT
    

   
   
   print "\n\nPersuasion process on network, with Niter:",Niter
   
   
   

   threshold=threshold_min
   while   threshold<= threshold_max:
      print   "thershold:",threshold

      alpha_F=alpha_F_min
      while alpha_F<= alpha_F_max:            # i explore all the parameter space, and create a file per each set of valuesllkl
        alpha_A=1.0*alpha_F
        print "  alpha_F:",alpha_F

        mutual_encouragement=min_mutual_encouragement  
        while  mutual_encouragement <= max_mutual_encouragement:
          print "    mutual_encouragement:",mutual_encouragement

          damping=min_damping
          while   damping <= max_damping:
            print "      damping:",damping

                             
            dir="../Results/weight_shifts/persuasion/alpha%.2f_damping%.2f/"  % (alpha_F, damping )

           
         

            ########## i read the list of frequent adopters from simulations, to estimate the ic for fellows                                       
            filename_list_simu_adopt="../Results/weight_shifts/persuasion/List_adopters_fellows_descending_frequency_persuasion_training_alpha"+str(alpha_F)+"_damping"+str(damping)+"_mutual_encourg"+str(mutual_encouragement)+"_threshold"+str(threshold)+"_1000iter_"+str(cutting_day)+"_Att_only_middle.dat"
  
            file_list_simu_adopt=open(filename_list_simu_adopt,'r')  
            list_lines_file=file_list_simu_adopt.readlines()
            
                
            list_sorted_fellow_adopters=[]
            for line in list_lines_file[1:]:   # i exclude the first row            
               adopter=line.split(" ")[0]              
               list_sorted_fellow_adopters.append(adopter)

         #   print  "list sorted fellows:",list_sorted_fellow_adopters 

            num_simu_Fellow_adopters_cutting_day=int( round(float(list_lines_file[0].split("Avg # F adopters ")[1].split(" ")[0])))
          #  print "avg simu number Fellow adopters:",num_simu_Fellow_adopters_cutting_day,int( round(num_simu_Fellow_adopters_cutting_day))

          
           
            list_dist_fixed_parameters_testing_segment=[]
            list_dist_abs_at_ending_point_fixed_parameters=[]
            list_dist_at_ending_point_fixed_parameters=[]
            list_final_num_adopt=[]
            list_abs_dist_point_by_point_indiv_simus_to_actual=[]
            list_dist_point_by_point_indiv_simus_to_actual=[]


            
            list_small_values=[]
            
            
            for iter in range(Niter):

               # print "         ",iter
               
           

                num_realizations_sum_dist_small=0.
                time_evol_number_adopters=[]   # for a single realization of the dynamics


                num_adopters , max_shift= set_ic(G,threshold,cutting_day,dict_days_list_empirical_att_adopters,list_sorted_fellow_adopters,num_simu_Fellow_adopters_cutting_day)

                time_evol_number_adopters.append(float(num_adopters))
                old_num_adopters=num_adopters
                
          

                
               # the dynamics starts:                 
                shift_length=5    #i know the first shift (order 0) is of length 5


                t=cutting_day
                while t<= max_shift:  # loop over shifts, in chronological order  (the order is the day index since seeding_day) 
                   # print 't:',t
                  
                    for n in G.nodes():
                       if G.node[n]['type']=="shift" and G.node[n]['order']==t:  # i look for the shift corresponding to that time step       
                            
                            shift_length=int(G.node[n]['shift_length'])
                          
                            if shift_length==2 and n not in list_id_weekends_T3:
                               shift_length=1   # because during weekends, the fellow does rounds one day with Att1 and the other day with Att2.  (weekend shifts for T3 are two day long, with no sharing fellows)

#    print "one-day weekend", G.node[n]['label'],G.node[n]['shift_length']




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
                                        persuasion(G,damping,doctor1,doctor2,alpha_A,alpha_F,threshold,shift_length)   # i move their values of opinion                  
                                        update_opinions(G,threshold,doctor1,doctor2) #  i update status and make sure the values of the vectors stay between [0,1] 
                                  
                                    else:  # if two Adopters meet, they encourage each other (if two NonAdopters, nothing happens)
                                   
                                       mutual_reinforcement(G,mutual_encouragement,doctor1,doctor2,shift_length)
                           # else:
                            #   print "  no persuasion possible during shift (no adopters present)!"   
                               
                    list_Adopters=[]        
                    for n in G.nodes():              
                       try:
                          if  G.node[n]["status"]=="Adopter":                                                    
                             if G.node[n]["label"] not in list_Adopters and G.node[n]["type"]=="A":
                                list_Adopters.append(G.node[n]["label"])
                       except: pass  # if the node is a shift, it doesnt have a 'status' attribute                   
                    new_num_adopters=len(list_Adopters)


                    if  shift_length==5: # i estimate that adoption happens in the middle of the shift
                       if t+5 < max_shift:
                          time_evol_number_adopters.append(old_num_adopters) 
                       if t+4 < max_shift:
                          time_evol_number_adopters.append(old_num_adopters) 
                       if t+3 < max_shift:
                          time_evol_number_adopters.append(new_num_adopters)
                       if t+2 < max_shift:
                          time_evol_number_adopters.append(new_num_adopters) 
                       if t+1 < max_shift:
                              time_evol_number_adopters.append(new_num_adopters) 
                       t+=5
                      
        
                    elif  shift_length==4:
                        if t+4 < max_shift:
                           time_evol_number_adopters.append(old_num_adopters)                     
                        if t+3 < max_shift:
                           time_evol_number_adopters.append(old_num_adopters) 

                        if t+2 < max_shift:
                           time_evol_number_adopters.append(new_num_adopters)                       
                       
                        if t+1 < max_shift:
                           time_evol_number_adopters.append(new_num_adopters) 
                        t+=4
                      
                    elif  shift_length==3:
                        if t+3 < max_shift:
                           time_evol_number_adopters.append(old_num_adopters)                     
                       
                        if t+2 < max_shift:
                           time_evol_number_adopters.append(new_num_adopters)
                       
                        if t+1 < max_shift:
                           time_evol_number_adopters.append(new_num_adopters)
                       
                        t+=3
                      


                    elif  shift_length==2:
                        if t+2 < max_shift:
                           time_evol_number_adopters.append(old_num_adopters)                     
                       
                        if t+1 < max_shift:
                           time_evol_number_adopters.append(new_num_adopters)
                       
                      
                        t+=2
                      
                    elif  shift_length==1:                      
                        if t+1 < max_shift:
                           time_evol_number_adopters.append(new_num_adopters)                       
                       
                        t+=1
                      

                    old_num_adopters=new_num_adopters             
                   
   

                ############## end while loop over t
               
                dist=compare_real_evol_vs_simus_to_be_called.compare_two_curves( list_actual_evol_testing,time_evol_number_adopters)             
                if dist < min_sum_dist:                  
                   list_small_values.append(dist)
              
               
                

            #######################end loop over Niter
          
         

            print "fraction realizations with sum distances smaller than", min_sum_dist,"is  ",float(len(list_small_values))/float(Niter),"namelly:",list_small_values
          
                



            
          
            damping += delta_damping
          mutual_encouragement += delta_mutual_encouragement
        alpha_F += delta_alpha_F
      threshold  += delta_threshold
    
  

  
###############################################


def set_ic(G,threshold,cutting_day,dict_days_list_empirical_att_adopters,list_sorted_fellow_adopters,num_simu_Fellow_adopters_cutting_day):

        list_s=[]
        list_A=[]
        list_F=[]
      
        list_empirical_att_adopters=dict_days_list_empirical_att_adopters[cutting_day]
       # print len(list_empirical_adopters)," initial adopters @ day", cutting_day, "  :", list_empirical_adopters

        dict_name_node={}
        num_shifts=0
        for n in G.nodes():              
            if G.node[n]['type']=="shift":
                num_shifts+=1
                if  G.node[n]['order'] not in list_s:
                    list_s.append(G.node[n]['order'])                        
               
            elif G.node[n]['type']=="A":
                if n not in list_A:
                    list_A.append(n)
                    G.node[n]["adoption_vector"]=random.random()*threshold  #values from [0,threshold)
                    G.node[n]["status"]="NonAdopter"  # initially non-Adopters

                dict_name_node[G.node[n]["label"]]=n

            elif G.node[n]['type']=="F":
                if n not in list_F:
                    list_F.append(n)
                    G.node[n]["adoption_vector"]=random.random()*threshold
                    G.node[n]["status"]="NonAdopter"  
                dict_name_node[G.node[n]["label"]]=n
    
        max_shift=max(list_s)
        
       
         
      
        list_Adopters=[]    
        for doctor in G.nodes():              
           if G.node[doctor]["label"] in list_empirical_att_adopters:   # i set ic for the testing segment according to the empirical data
              G.node[doctor]["status"]="Adopter"  
              G.node[doctor]["adoption_vector"]=1.0
              list_Adopters.append(G.node[doctor]["label"])

        for i in range(num_simu_Fellow_adopters_cutting_day):  
           fellow_adopter=  list_sorted_fellow_adopters[i]   # this list is sorted from more to less frequent adopter          
           node=dict_name_node[fellow_adopter]
           G.node[node]["status"]="Adopter"  
           G.node[node]["adoption_vector"]=1.0

           
       
            
      


        return float(len(list_Adopters)),max_shift

###########################################

def persuasion(G,damping,doctor1,doctor2,alpha_A,alpha_F,threshold,shift_length):

    if G.node[doctor1]["adoption_vector"]>=threshold or G.node[doctor2]["adoption_vector"]>=threshold :  # only if at least one doctor is Adopter
        
        alpha_A=alpha_A*shift_length   # to take into account the length shift
        alpha_F=alpha_F*shift_length 
      
        
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



def mutual_reinforcement(G,mutual_encouragement,doctor1,doctor2,shift_length):

    mutual_encouragement=mutual_encouragement*shift_length
    if G.node[doctor1]['status'] =='Adopter'  and G.node[doctor2]['status']=='Adopter':
        G.node[doctor1]["adoption_vector"]=G.node[doctor1]["adoption_vector"]+mutual_encouragement
        G.node[doctor2]["adoption_vector"]=G.node[doctor2]["adoption_vector"]+mutual_encouragement

        if  float(G.node[doctor1]["adoption_vector"])>1.0:                                             
            G.node[doctor1]["adoption_vector"]=1.0  
        if  float(G.node[doctor2]["adoption_vector"])>1.0:                                             
            G.node[doctor2]["adoption_vector"]=1.0  
                


######################################



def look_for_T3_weekends(G):

   list_ids_T3_weekends=[]
   for n in G.nodes():
      if G.node[n]['type']=='shift':
         if G.node[n]['shift_length']==2 and "T3" in G.node[n]['label']:
            list_ids_T3_weekends.append(n)
            

               
   return  list_ids_T3_weekends
   



##################################################
######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
   
        main(graph_filename)
    else:
        print "Usage: python script.py path/network.gml"

    
