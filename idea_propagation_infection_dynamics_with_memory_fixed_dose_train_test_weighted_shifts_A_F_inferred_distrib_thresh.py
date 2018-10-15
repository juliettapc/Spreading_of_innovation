#!/usr/bin/env python

'''
Given a .gml network, it simulates a disease-spreading-like process
in the bipartite network (doctors and shifts)
Infection process with memory: cumulative doses that eventually are larger than a threshold

Created by Julia Poncela, on Dec 2012.

'''


import sys
import os
import networkx as nx
import numpy
import random
import csv
import compare_real_evol_vs_simus_to_be_called
import operator
import histograma_gral_negv_posit
import histograma_bines_gral


def main(graph_name):
 


   cutting_day=175  # to separate   training-testing





   G = nx.read_gml(graph_name)


   all_team="NO"   # as adopters or not

   list_id_weekends_T3=look_for_T3_weekends(G)  # T3 doesnt share fellows in the weekend  (but they are the exception)


   dir_real_data='../Results/'
   Nbins=20   # for the histogram of sum of distances


   delta_end=3.  # >= than + or -  dr difference at the end of the evolution (NO realization ends up closer than this!!!! if 2, i get and empty list!!!)

   Niter=1000
  
   fixed_param=""#FIXED_Pimm0_"    # or ""  # for the Results file that contains the sorted list of best parameters


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
  # list_actual_evol_testing=list_actual_evol[(cutting_day-1):]  # i dont need this one
   
  
##################################################################


   prob_min=0.10
   prob_max=1.01
   delta_prob=0.1
   
   

   prob_Immune_min=0.0    
   prob_Immune_max=1.001
   delta_prob_Immune=0.1

# threshold is not personal, and set randomly to a value (0,1)
 
                   # of a single encounter with an infected  (it cant be zero or it doesnt make sense!)
   dose_min=0.05              #infect_threshold_min
   dose_max=1.001         #######infect_threshold_min/10.
   delta_dose=0.05           ##infect_threshold_min/10.


   dir="../Results/weight_shifts/infection/"       

   dict_filenames_tot_distance={}   # i will save the filename as key and the tot distance from that curve to the original one
   dict_filenames_prod_distances={}   

  

   prob_Immune=prob_Immune_min
   while prob_Immune<= prob_Immune_max:
        
      print "prom Immune:",prob_Immune        

      prob_infection=prob_min
      while prob_infection<= prob_max:
                 
            print "  p:",prob_infection                              
            
            dose=dose_min
            while dose <= dose_max:
               
               print "  dose:",dose





               output_file2=dir+"Average_time_evolution_Infection_memory_training_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_threshold_from_distrib_dose"+str(dose)+"_"+str(Niter)+"iter_day"+str(cutting_day)+"_A_F_inferred.dat"
             #  file2 = open(output_file2,'wt')                                       
              # file2.close()
               



      
               list_lists_t_evolutions=[]     # i create the empty list of list for the Niter temporal evolutions
               
               list_dist_fixed_parameters=[]
               list_dist_at_ending_point_fixed_parameters=[]
               list_dist_abs_at_ending_point_fixed_parameters=[]
              
               
               for iter in range(Niter):
            
              #    print "     iter:",iter


               
                  

            ########### set I.C.


                  list_I=[]  #list infected doctors
                  max_order=0
                  for n in G.nodes():
                     G.node[n]["status"]="S"  # all nodes are Susceptible
                     G.node[n]["infec_value"]=0. 
                     G.node[n]["personal_threshold"]=random.random()  # for a dr to become infected

                     if G.node[n]['type']=="shift":                        
                        if  G.node[n]['order']>max_order:
                           max_order=G.node[n]['order'] # to get the last shift-order for the time loop
                     else:
                        if G.node[n]['label']=="Wunderink"  or G.node[n]["label"]=="Weiss":           
                           G.node[n]["status"]="I"                       
                           G.node[n]["infec_value"]=G.node[n]["personal_threshold"]+ 1.
                           list_I.append(G.node[n]['label'])
          

            
           
                  list_single_t_evolution=[]
                  list_single_t_evolution.append(2.0)  # I always start with TWO infected doctors!!


                  for n in G.nodes():   # i make some DOCTORs INMUNE  (anyone except Weiss and Wunderink)
                     if (G.node[n]['type']=="A") or ( G.node[n]['type']=="F"):
                        if G.node[n]['label']!="Wunderink"  and G.node[n]["label"]!="Weiss": 
                           rand=random.random()
                           if rand< prob_Immune:
                              G.node[n]["status"]="Immune"
                              


        
  
                  ################# the dynamics starts: 
            
                  t=1
                  while t< cutting_day:  # loop over shifts, in order           
                     for n in G.nodes():
                        if G.node[n]['type']=="shift" and G.node[n]['order']==t:
                           shift_length=int(G.node[n]['shift_length'])

                           if shift_length==2 and n not in list_id_weekends_T3:
                              shift_length=1   # because during weekends, the fellow does rounds one day with Att1 and the other day with Att2.  (weekend shifts for T3 are two day long, with no sharing fellows)

                           flag_possible_infection=0
                           for doctor in G.neighbors(n): #first i check if any doctor is infected in this shift
                              if G.node[doctor]["status"]=="I":
                                 flag_possible_infection=1
                                

                           if flag_possible_infection:
                              for doctor in G.neighbors(n): # then the doctors in that shift, gets infected with prob_infection

                                 for i in range(shift_length):   # i repeat the infection process several times, to acount for shift lenght
                                    if G.node[doctor]["status"]=="S":
                                       rand=random.random()
                                       if rand<prob_infection:  # with prob p the infection occurres
                                          
                                          G.node[doctor]["infec_value"]+=dose  # and bumps the infection_value of that susceptible dr
                                          
                                          if G.node[doctor]["infec_value"]>= G.node[doctor]["personal_threshold"]:  # the threshold for infection is personal
                                             
                                             G.node[doctor]["status"]="I"
                                             
                                        
                                                
                                             list_I.append(G.node[doctor]["label"])
                                                

                     list_single_t_evolution.append(float(len(list_I)))

                     t+=1   
                     ######## end t loop





          


                  list_lists_t_evolutions.append(list_single_t_evolution)
             
 
                  #print "actual:",len(list_actual_evol_training),"  simu:",len(list_single_t_evolution)
                  list_dist_fixed_parameters.append(compare_real_evol_vs_simus_to_be_called.compare_two_curves( list_actual_evol_training,list_single_t_evolution))
                  
                  list_dist_abs_at_ending_point_fixed_parameters.append( abs(list_single_t_evolution[-1]-list_actual_evol_training[-1]) )   # i save the distance at the ending point between the current simu and actual evol
                  list_dist_at_ending_point_fixed_parameters.append( list_single_t_evolution[-1]-list_actual_evol_training[-1])    # i save the distance at the ending point between the current simu and actual evol

                           
                  ######## end loop Niter for the training fase
      

       


       
       
               list_pair_dist_std_delta_end=[]
               
               list_pair_dist_std_delta_end.append(numpy.mean(list_dist_fixed_parameters) )   # average dist between the curves over Niter
               list_pair_dist_std_delta_end.append(numpy.std(list_dist_fixed_parameters) )
               
               list_pair_dist_std_delta_end.append(numpy.mean(list_dist_abs_at_ending_point_fixed_parameters))
               

               value=numpy.mean(list_dist_fixed_parameters) *numpy.mean(list_dist_abs_at_ending_point_fixed_parameters)# if SD=0, it is a problem, because then that is the minimun value, but not the optimum i am looking for!!
    
               dict_filenames_prod_distances[output_file2]=  value

               
               if (numpy.mean(list_dist_abs_at_ending_point_fixed_parameters)) <= delta_end:  # i only consider situations close enough at the ending point   
                  
                  dict_filenames_tot_distance[output_file2]=list_pair_dist_std_delta_end
                                                                                          

                  histogram_filename="../Results/weight_shifts/histogr_raw_distances_ending_infection_memory_training_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_threshold_from_distrib_dose"+str(dose)+"_"+str(Niter)+"iter_day"+str(cutting_day)+"_A_F_inferred.dat"
                  histograma_gral_negv_posit.histograma(list_dist_at_ending_point_fixed_parameters,histogram_filename)
                  
                  histogram_filename2="../Results/weight_shifts/histogr_sum_dist_traject_infection_memory_training_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_threshold_from_distrib_dose"+str(dose)+"_"+str(Niter)+"iter_day"+str(cutting_day)+"_A_F_inferred.dat"
                  
                  histograma_bines_gral.histograma_bins(list_dist_fixed_parameters,Nbins,histogram_filename2)
                  
                  
                  print  "written histogram file: ",histogram_filename
                  print  "written histogram file: ",histogram_filename2


               dose+= delta_dose          
            prob_infection+= delta_prob
      prob_Immune+= delta_prob_Immune



 

   string_name="infection_memory_training_"+fixed_param+str(Niter)+"iter_day"+str(cutting_day)+"_A_F_inferred.dat"   # for the "Results" file with the sorted list of files
   
   list_order_dict= compare_real_evol_vs_simus_to_be_called.pick_minimum_same_end(dict_filenames_tot_distance,string_name,Niter,cutting_day)
# it returns a list of tuples like this :  ('../Results/network_final_schedule_withTeam3_local/infection/Average_time_evolution_Infection_training_p0.7_Immune0.0_2iter_2012.dat', [2540.0, 208.0, 1.0])  the best set of parameters  being the fist one of the elements in that list.



   
   
   
   list_order_dict2= compare_real_evol_vs_simus_to_be_called.pick_minimum_prod_distances(dict_filenames_prod_distances,string_name,Niter,cutting_day)


   

   prob_infection=float(list_order_dict[0][0].split("_p")[1].split("_")[0])
   prob_Immune=float(list_order_dict[0][0].split("_Immune")[1].split("_")[0]) 
   dose=float(list_order_dict[0][0].split("_dose")[1].split("_")[0])
 
  
   
  
   print "\nOptimum parameters (old method) at day",cutting_day," are: p=",prob_infection," Pimmune=",prob_Immune," infection threshold from distribution, and dose=",dose
   


  # optimum_filename=list_order_dict2[0][0]

   prob_infection=float(list_order_dict2[0][0].split("_p")[1].split("_")[0])
   prob_Immune=float(list_order_dict2[0][0].split("_Immune")[1].split("_")[0])  
   dose=float(list_order_dict2[0][0].split("_dose")[1].split("_")[0])
 
  
 
   print "Optimum parameters (product of distances and SDs) at day",cutting_day," are: p=",prob_infection," Pimmune=",prob_Immune," infection threshold from distribution, and dose=",dose

   


######################################



def look_for_T3_weekends(G):

   list_ids_T3_weekends=[]
   for n in G.nodes():
      if G.node[n]['type']=='shift':
         if G.node[n]['shift_length']==2 and "T3" in G.node[n]['label']:
            list_ids_T3_weekends.append(n)
            

               
   return  list_ids_T3_weekends
   






######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
   
        main(graph_filename)
    else:
        print "Usage: python script.py path/network.gml"

    
