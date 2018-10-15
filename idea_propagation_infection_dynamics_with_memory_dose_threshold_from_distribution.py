#!/usr/bin/env python

'''
Given a .gml network, it simulates a disease-spreading-like process
in the bipartite network (doctors and shifts)
Infection process with memory: cumulative doses that eventually are larger than a threshold (both dose and threshold are drawn from a distribution, they r not fixed)

Created by Julia Poncela, on Dec 2012.

'''


import sys
import os
import networkx as nx
import numpy
import random
import csv
import compare_real_evol_vs_simus_to_be_called
import histograma_bines_gral

def main(graph_name):
 



   G = nx.read_gml(graph_name)


   all_team="NO"   # as adopters or not




   dir_real_data='../Results/'


   delta_end=3  # >= than + or -  dr difference at the end of the evolution (NO realization ends up closer than this!!!! if 2, i get and empty list!!!)

   Niter=1000

   list_id_weekends_T3=look_for_T3_weekends(G)  # T3 doesnt share fellows in the weekend  (but they are the exception)


   output_file3="../Results/weight_shifts/Landscape_parameters_infection_memory_distrib_"+str(Niter)+"iter.dat" 
   file3 = open(output_file3,'wt')        
   file3.close()


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





################################################################################

#../Results/network_final_schedule_withTeam3/infection/Average_time_evolution_Infection_p0.9_Immune0.5_1000iter_2012.dat

   prob_min=0.00
   prob_max=1.01
   delta_prob=0.1
   
   

   prob_Immune_min=0.0
   prob_Immune_max=1.0
   delta_prob_Immune=0.1


  


   dir="../Results/weight_shifts/infection/"    

   dict_filenames_tot_distance={}   # i will save the filename as key and the tot distance from that curve to the original one

   prob_Immune=prob_Immune_min
   while prob_Immune<= prob_Immune_max:
        
      print "prom Immune:",prob_Immune        

      prob_infection=prob_min
      while prob_infection<= prob_max:
                 
               print "  p:",prob_infection       
         

               output_file2=dir+"Average_time_evolution_Infection_memory_distrb_dose_thr_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter)+"iter.dat"
               file2 = open(output_file2,'wt')                                       
               file2.close()
               




        
               num_shifts=0
               for n in G.nodes():
                  G.node[n]["status"]="S" 
                  G.node[n]["infec_value"]=0.   # when this value goes over the infect_threshold, the dr is infected
                  G.node[n]["personal_threshold"]=random.random()  # for a dr to become infected
                  if G.node[n]['type']=="shift":
                     num_shifts+=1


      
               list_lists_t_evolutions=[]     # i create the empty list of list for the Niter temporal evolutions
               
               list_dist_fixed_parameters=[]
               list_abs_dist_at_ending_point_fixed_parameters=[]
               list_final_num_infected=[]

               
               for iter in range(Niter):
            
                  print "     iter:",iter


                  list_I=[]  #list infected doctors
                  list_ordering=[]
                  list_s=[]
                  

            ########### set I.C.

                  max_order=0
                  for n in G.nodes():
                     G.node[n]["status"]="S"  # all nodes are Susceptible
                     if G.node[n]['type']=="shift":
                        list_s.append(n)        
                        if  G.node[n]['order']>max_order:
                           max_order=G.node[n]['order']
                     else:
                        if G.node[n]['label']=="Wunderink"  or G.node[n]["label"]=="Weiss":           
                           G.node[n]["status"]="I"                       
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
                  while t<= max_order:  # loop over shifts, in order           
                     for n in G.nodes():
                        if G.node[n]['type']=="shift" and G.node[n]['order']==t:
                           shift_lenght=int(G.node[n]['shift_lenght'])

                           if shift_lenght==2 and n not in list_id_weekends_T3:
                              shift_lenght=1   # because during weekends, the fellow does rounds one day with Att1 and the other day with Att2.  (weekend shifts for T3 are two day long, with no sharing fellows)
                         #  print "one-day weekend", G.node[n]['label'],G.node[n]['shift_lenght']


                           flag_possible_infection=0
                           for doctor in G.neighbors(n): #first i check if any doctor is infected in this shift
                              if G.node[doctor]["status"]=="I":
                                 flag_possible_infection=1
                                

                           if flag_possible_infection:
                              for doctor in G.neighbors(n): # then the doctors in that shift, gets infected with prob_infection

                                 for i in range(shift_lenght):   # i repeat the infection process several times, to acount for shift lenght
                                    if G.node[doctor]["status"]=="S":
                                       rand=random.random()
                                       if rand<prob_infection:  # with prob p the infection occurres
                                          
                                          G.node[doctor]["infec_value"]+=random.random()  # and bumps the infection_value of that susceptible dr (the dose is random, not fixed)
                                          
                                          if G.node[doctor]["infec_value"]>= G.node[doctor]["personal_threshold"]:  # the threshold for infection is personal
                                          
                                              G.node[doctor]["status"]="I"
                                              if G.node[doctor]["type"]=="A":   # fellows participate in the dynamics, but i only consider the attendings as real adopters
                                                 list_I.append(G.node[doctor]["label"])
                                          

                     list_single_t_evolution.append(float(len(list_I)))

                     t+=1   
                     ######## end t loop




          

                  list_lists_t_evolutions.append(list_single_t_evolution)
             
 
                  list_dist_fixed_parameters.append(compare_real_evol_vs_simus_to_be_called.compare_two_curves( list_actual_evol,list_single_t_evolution))
                  
                  list_abs_dist_at_ending_point_fixed_parameters.append( abs(list_single_t_evolution[-1]-list_actual_evol[-1]) )   # i save the distance at the ending point between the current simu and actual evol

                  list_final_num_infected.append(list_single_t_evolution[-1])

           
                  ######## end loop Niter
      

       


       
       
               list_pair_dist_std_delta_end=[]
               
               list_pair_dist_std_delta_end.append(numpy.mean(list_dist_fixed_parameters) )   # average dist between the curves over Niter
               list_pair_dist_std_delta_end.append(numpy.std(list_dist_fixed_parameters) )
               
               list_pair_dist_std_delta_end.append(numpy.mean(list_abs_dist_at_ending_point_fixed_parameters))
               
               


               file3 = open(output_file3,'at')          # i print out the landscape           
               print >> file3, prob_infection,prob_Immune,numpy.mean(list_abs_dist_at_ending_point_fixed_parameters), numpy.mean(list_dist_fixed_parameters), numpy.mean(list_final_num_infected),numpy.std(list_final_num_infected), numpy.std(list_final_num_infected)/numpy.mean(list_final_num_infected)
               file3.close()

     
               
               if (numpy.mean(list_abs_dist_at_ending_point_fixed_parameters)) <= delta_end:  # i only consider situations close enough at the ending point   
          
                  dict_filenames_tot_distance[output_file2]=list_pair_dist_std_delta_end
 
      



               file2 = open(output_file2,'at')        
               for s in range(len(list_single_t_evolution)):           
                  list_fixed_t=[]
                  for iter in range (Niter):
                     list_fixed_t.append(list_lists_t_evolutions[iter][s])        
                  print >> file2, s,numpy.mean(list_fixed_t)                    
               file2.close()



     

               print list_dist_fixed_parameters

              # histograma_bines_gral.histograma_bins(list_dist_fixed_parameters,50, "../Results/histogr_distances_indiv_infect_memory_simus_to_the_average_curve_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_threshold"+str(infect_threshold)+"_dose"+str(dose)+"_"+str(Niter)+"iter.dat" )  # Nbins=100



               
               prob_infection+= delta_prob
      prob_Immune+= delta_prob_Immune




   compare_real_evol_vs_simus_to_be_called.pick_minimum_same_end(dict_filenames_tot_distance,"Infection_memory_distrib",all_team,Niter,None)

   print "written landscape file:",output_file3

######################################
######################################



def look_for_T3_weekends(G):

   list_ids_T3_weekends=[]
   for n in G.nodes():
      if G.node[n]['type']=='shift':
         if G.node[n]['shift_lenght']==2 and "T3" in G.node[n]['label']:
            list_ids_T3_weekends.append(n)
            

               
   return  list_ids_T3_weekends
   



######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
   
        main(graph_filename)
    else:
        print "Usage: python script.py path/network.gml"

    
