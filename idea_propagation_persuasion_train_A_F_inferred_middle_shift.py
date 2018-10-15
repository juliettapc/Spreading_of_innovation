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
import operator
import histograma_bines_gral
import histograma_gral_negv_posit
 
  


def main(graph_name):
 




   G = nx.read_gml(graph_name)
 
   list_id_weekends_T3=look_for_T3_weekends(G)  # T3 doesnt share fellows in the weekend  (but they are the exception)



   cutting_day=243#125     # to separate   training-testing



   Niter_training=1000


   delta_end=3.  # >= than + or -  dr difference at the end of the evolution



   dir_real_data='../Results/'
   dir="../Results/weight_shifts/persuasion/"  


  
   Nbins=20   # for the histogram of sum of distances


   fixed_param="FIXED_threshold0.5"#_damping0_"    # or ""  # for the Results file that contains the sorted list of best parameters



   print_landscape="NO"  # for the whole exploration

   print_training_evol= "no"   # once i know the best fit for the training segment, i run it again to get the curve






######################################################################################
#  I read the file of the actual evolution of the idea spreading in the hospital:   ##
######################################################################################

   

  
   filename_actual_evol="../Results/Actual_evolution_adopters_from_inference.dat"
  


   file1=open(filename_actual_evol,'r')         ## i read the file:  list_dates_and_names_current_adopters.txt  (created with: extract_real_evolution_number_adopters.py)
   list_lines_file=file1.readlines()
            

   list_actual_evol=[]  
   for line in list_lines_file:      # [1:]:   # i exclude the first row   
     
      num_adopters= float(line.split("\t")[1])          
      list_actual_evol.append(num_adopters)

   list_actual_evol_training=list_actual_evol[:cutting_day]

##################################################################


#../Results/network_final_schedule_withTeam3/Time_evolutions_Persuasion_alpha0.2_damping0.0_mutual_encourg0.7_threshold0.4_unif_distr_50iter_2012_seed31Oct_finalnetwork.dat

 
   alpha_F_min=0.100   #   # alpha=0: nobody changes their mind
   alpha_F_max=0.9001    
   delta_alpha_F=0.10    #AVOID 1.0 OR THE DYNAMICS GETS TOTALLY STUCK AND IT IS NOT ABLE TO PREDICT SHIT!
   

   min_damping=0.0   #0.0     #its harder to go back from YES to NO again. =1 means no effect, =0.5 half the movement from Y->N than the other way around, =0 never go back from Y to N
   max_damping=0.001    #0.451
   delta_damping=0.10  
      

   min_mutual_encouragement=0.000   #  # when two Adopters meet, they convince each other even more
   max_mutual_encouragement=0.95001   
   delta_mutual_encouragement=0.10
   
   
   threshold_min=0.500   #  # larger than, to be an Adopter
   threshold_max=0.501 
   delta_threshold=0.10   # AVOID 1.0 OR THE DYNAMICS GETS TOTALLY STUCK AND IT IS NOT ABLE TO PREDICT SHIT
 
 






   if print_landscape =="YES":
      
      output_file3="../Results/weight_shifts/Landscape_parameters_persuasion_train_"+fixed_param+str(Niter_training)+"iter_A_F_inferred_middle_day"+str(cutting_day)+".dat"   
      file3 = open(output_file3,'wt')        
      file3.close()

 
   
   
   print "\n\nPersuasion process on network, with Niter:",Niter_training
   
   
   dict_filenames_tot_distance={}   # i will save the filename as key and the tot distance from that curve to the original one
   dict_filenames_prod_distances={}   


  

   threshold=threshold_min
   while   threshold<= threshold_max:
      print   "thershold:",threshold

      alpha_F=alpha_F_min
      while alpha_F<= alpha_F_max:            # i explore all the parameter space, and create a file per each set of values
        alpha_A=1.0*alpha_F
        print "  alpha_F:",alpha_F

        mutual_encouragement=min_mutual_encouragement  
        while  mutual_encouragement <= max_mutual_encouragement:
          print "    mutual_encouragement:",mutual_encouragement

          damping=min_damping
          while   damping <= max_damping:
            print "      damping:",damping


         
#            dir="../Results/weight_shifts/persuasion/alpha%.2f_damping%.2f/"  % (alpha_F, damping )
           
            output_file=dir+"Time_evolutions_Persuasion_training_alpha"+str(alpha_F)+"_damping"+str(damping)+"_mutual_encourg"+str(mutual_encouragement)+"_threshold"+str(threshold)+"_unif_distr_"+str(Niter_training)+"iter_alphaA_eq_alphaF"+"_"+str(cutting_day)+"_A_F_inferred_middle.dat"         


         

            time_evol_number_adopters_ITER=[]  # list of complete single realizations of the dynamics
            list_dist_fixed_parameters=[]
            list_dist_at_ending_point_fixed_parameters=[]
            list_dist_abs_at_ending_point_fixed_parameters=[]

           
            list_networks_at_cutting_day=[]

            list_final_num_adopt=[]


            for iter in range(Niter_training):

               # print "         ",iter
              
           
                time_evol_number_adopters=[]   # for a single realization of the dynamics

               


                num_adopters , seed_shift ,max_shift= set_ic(G,threshold)   # i establish who is Adopter and NonAdopter initially, and count how many shifts i have total

                time_evol_number_adopters.append(float(num_adopters))               
               

                old_num_adopters=num_adopters

                
               ########### the dynamics starts:                 
             
                shift_length=5    #i know the first shift (order 0) is of length 5

                t=0   
                while t< cutting_day:  # loop over shifts, in chronological order  (the order is the day index since seeding_day) 
                                             
                    for n in G.nodes():
                        if G.node[n]['type']=="shift" and G.node[n]['order']==t:  # i look for the shift corresponding to that time step                      (not all t's exists as 'orders' in the network!! just the days corresponding to the beginning of each shift)

                            shift_length=int(G.node[n]['shift_length'])
                            effective_shift_length=shift_length

                            if shift_length==2 and n not in list_id_weekends_T3:
                               effective_shift_length=1   # because during weekends, the fellow does rounds one day with Att1 and the other day with Att2.  (weekend shifts for T3 are two day long, with no sharing fellows)



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
                                        persuasion(G,damping,doctor1,doctor2,alpha_A,alpha_F,threshold,effective_shift_length)   # i move their values of opinion 
                                        update_opinions(G,threshold,doctor1,doctor2) #  i update status and make sure the values of the vectors stay between [0,1] 
                                  
                                    else:  # if two Adopters meet, they encourage each other (if two NonAdopters, nothing happens)
                                   
                                       mutual_reinforcement(G,mutual_encouragement,doctor1,doctor2,shift_length)
                                                                 

                    list_Adopters=[]        
                    for n in G.nodes():              
                       try:
                          if  G.node[n]["status"]=="Adopter":                                                    
                             if G.node[n]["label"] not in list_Adopters :#and G.node[n]["type"]=="A":
                                list_Adopters.append(G.node[n]["label"])
                       except: pass  # if the node is a shift, it doesnt have a 'status' attribute                   
                    new_num_adopters=len(list_Adopters)

                    if  shift_length==5: # i estimate that adoption happens in the middle of the shift
                       if t+5 < cutting_day:
                          time_evol_number_adopters.append(old_num_adopters) 
                       if t+4 < cutting_day:
                          time_evol_number_adopters.append(old_num_adopters) 
                       if t+3 < cutting_day:
                          time_evol_number_adopters.append(new_num_adopters)
                       if t+2 < cutting_day:
                          time_evol_number_adopters.append(new_num_adopters)
                       if t+1 < cutting_day:
                          time_evol_number_adopters.append(new_num_adopters)
                       t+=5
                      
        
                    elif  shift_length==4:
                        if t+4 < cutting_day:
                           time_evol_number_adopters.append(old_num_adopters)                     
                        if t+3 < cutting_day:
                           time_evol_number_adopters.append(old_num_adopters) 

                        if t+2 < cutting_day:
                           time_evol_number_adopters.append(new_num_adopters)                       
                       
                        if t+1 < cutting_day:
                           time_evol_number_adopters.append(new_num_adopters)
                        t+=4
                      
                    elif  shift_length==3:
                        if t+3 < cutting_day:
                           time_evol_number_adopters.append(old_num_adopters)                     
                       
                        if t+2 < cutting_day:
                           time_evol_number_adopters.append(new_num_adopters)
                       
                        if t+1 < cutting_day:
                           time_evol_number_adopters.append(new_num_adopters)
                       
                        t+=3
                      


                    elif  shift_length==2:
                        if t+2 < cutting_day:
                           time_evol_number_adopters.append(old_num_adopters)                     
                       
                        if t+1 < cutting_day:
                           time_evol_number_adopters.append(new_num_adopters)
                       
                      
                        t+=2
                      
                    elif  shift_length==1:                      
                        if t+1 < cutting_day:
                           time_evol_number_adopters.append(new_num_adopters)                       
                       
                        t+=1
                      

                    old_num_adopters=new_num_adopters

                ############## end while loop over t
               

               
               
                time_evol_number_adopters_ITER.append(time_evol_number_adopters)


                list_final_num_adopt.append(time_evol_number_adopters[-1])

               
                list_dist_fixed_parameters.append(compare_real_evol_vs_simus_to_be_called.compare_two_curves( list_actual_evol_training,time_evol_number_adopters))
               
                list_dist_abs_at_ending_point_fixed_parameters.append( abs(time_evol_number_adopters[-1]-list_actual_evol_training[-1]) )

                list_dist_at_ending_point_fixed_parameters.append( time_evol_number_adopters[-1]-list_actual_evol_training[-1]) 



               
              
             

            #######################   end loop Niter for the training fase


            list_pair_dist_std_delta_end=[]
        
            list_pair_dist_std_delta_end.append(numpy.mean(list_dist_fixed_parameters) )   # average dist between the curves over Niter
            list_pair_dist_std_delta_end.append(numpy.std(list_dist_fixed_parameters) )

            list_pair_dist_std_delta_end.append(numpy.mean(list_dist_abs_at_ending_point_fixed_parameters))

         

                     
            value=numpy.mean(list_dist_fixed_parameters) *numpy.mean(list_dist_abs_at_ending_point_fixed_parameters) # if SD=0, it is a problem, because then that is the minimun value, but not the optimum i am looking for!!
        
            dict_filenames_prod_distances[output_file]=  value                  


            if (numpy.mean(list_dist_abs_at_ending_point_fixed_parameters)) <= delta_end:  # i only consider situations close enough at the ending point   
               dict_filenames_tot_distance[output_file]=list_pair_dist_std_delta_end 
  
          
            if print_landscape =="YES":
               file3 = open(output_file3,'at')          # i print out the landscape           
               print >> file3, alpha_F, damping, mutual_encouragement, threshold,numpy.mean(list_dist_abs_at_ending_point_fixed_parameters), numpy.mean(list_dist_fixed_parameters),  numpy.mean(list_final_num_adopt),numpy.std(list_final_num_adopt),  numpy.std(list_final_num_adopt)/numpy.mean(list_final_num_adopt)
               file3.close()




            #histogram_filename="../Results/weight_shifts/histogr_raw_distances_ending_test_train_alpha"+str(alpha_F)+"_damping"+str(damping)+"_mutual_encourg"+str(mutual_encouragement)+"_threshold"+str(threshold)+"_unif_distr_"+str(Niter_training)+"iter_alphaA_eq_alphaF"+"_"+str(cutting_day)+"_A_F_inferred.dat"     
            #histograma_gral_negv_posit.histograma(list_dist_at_ending_point_fixed_parameters,histogram_filename)
            
            #histogram_filename2="../Results/weight_shifts/histogr_sum_dist_traject_infection_training_alpha"+str(alpha_F)+"_damping"+str(damping)+"_mutual_encourg"+str(mutual_encouragement)+"_threshold"+str(threshold)+"_unif_distr_"+str(Niter_training)+"iter_alphaA_eq_alphaF"+"_"+str(cutting_day)+"_A_F_inferred.dat"     
            
            #histograma_bines_gral.histograma_bins(list_dist_fixed_parameters,Nbins,histogram_filename2)


            if print_training_evol=="YES":
               file = open(output_file,'wt')        
               for i in range(len(time_evol_number_adopters)):  #time step by time step
                  list_fixed_t=[]
                  for iteracion in range (Niter_training): #loop over all independent iter of the process
                     list_fixed_t.append(time_evol_number_adopters_ITER[iteracion][i])  # i collect all values for the same t, different iter  

                  print >> file, i,numpy.mean(list_fixed_t),numpy.std(list_fixed_t), alpha_F,damping,mutual_encouragement       
               file.close()
               print "written evolution file:", output_file
           

             
          
            damping += delta_damping
          mutual_encouragement += delta_mutual_encouragement
        alpha_F += delta_alpha_F
      threshold  += delta_threshold
    


   string_name="persuasion_training_"+fixed_param+str(Niter_training)+"iter_"+str(cutting_day)+"_A_F_inferred_middle.dat"            # for the "Results" file with the sorted list of files
   list_order_dict=  compare_real_evol_vs_simus_to_be_called.pick_minimum_same_end(dict_filenames_tot_distance,string_name,Niter_training,cutting_day)


  
   
   list_order_dict2= compare_real_evol_vs_simus_to_be_called.pick_minimum_prod_distances(dict_filenames_prod_distances,string_name,Niter_training,cutting_day)

  



  
   if print_landscape =="YES":
      print "printed out landscape file:",output_file3


   print "\n\n"


###############################################
#####################################################

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
              if G.node[doctor]["label"] not in list_Adopters :#and G.node[doctor]["type"]=="A":
                 list_Adopters.append(G.node[doctor]["label"])

           
       
        return float(len(list_Adopters)),seed_shift,max_shift

           
       
      

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

    
