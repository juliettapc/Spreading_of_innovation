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
import csv
import compare_real_evol_vs_simus_to_be_called
import histograma_gral_negv_posit
import histograma_bines_gral
import operator



def main(graph_name):
 


   cutting_day=243  # to separate   training-testing


   Niter_training=1000


   fixed_param=""#FIXED_Pimm0_"    # or ""  # for the Results file that contains the sorted list of best parameters
 

   print_landscape="NO"  # for the whole exploration


   print_training_evol= "YES"#YES"#NO"   # once i know the best fit for the training segment, i run it again to get the curve




   G = nx.read_gml(graph_name)


   list_id_weekends_T3=look_for_T3_weekends(G)  # T3 doesnt share fellows in the weekend  (but they are the exception)


   all_team="NO"   # as adopters or not
   Nbins=20   # for the histogram of sum of distances



   dir_real_data='../Results/'

   dir="../Results/weight_shifts/infection/" 


   delta_end=3.  # >= than + or -  dr difference at the end of the evolution (NO realization ends up closer than this!!!! if 2, i get and empty list!!!)


 


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
#   list_actual_evol_testing=list_actual_evol[(cutting_day-1):]   #i dont use this

  

##################################################################

#../Results/network_final_schedule_withTeam3/infection/Average_time_evolution_Infection_p0.9_Immune0.5_1000iter_2012.dat

   prob_min=0.10
   prob_max=0.101
   delta_prob=0.1
      

   prob_Immune_min=0.1000
   prob_Immune_max=0.101
   delta_prob_Immune=0.1

 


  
   if print_landscape=="YES":
      output_file3="../Results/weight_shifts/Landscape_parameters_infection_train_"+str(Niter_training)+"iter_A_F_inferred_middle_day"+str(cutting_day)+".dat"  
      file3 = open(output_file3,'wt')              
      file3.close()


   
   list_dist_at_ending_point_fixed_parameters=[]
   dict_filenames_tot_distance={}   # i will save the filename as key and the tot distance from that curve to the original one
   dict_filenames_prod_distances={}   
   

   prob_Immune=prob_Immune_min
   while prob_Immune<= prob_Immune_max:
        
      print "prom Immune:",prob_Immune        

      prob_infection=prob_min
      while prob_infection<= prob_max:
                 
        print "  p:",prob_infection        


        output_file2=dir+"Average_time_evolution_Infection_training_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter_training)+"iter_2012_avg_ic_day"+str(cutting_day)+"_A_F_inferred.dat"
     #   file2 = open(output_file2,'wt')                                          I DONT NEED TO WRITE IT, COS I WILL USE THE WHOLE FILE FROM THE WHOLE FIT, WITH THE PARAMETER VALUES THAT THE TESTING-UP-TODAY-125 TELLS ME
      #  file2.close()
        


# i create the empty list of list for the Niter temporal evolutions
        num_shifts=0
        num_Drs=0.
        for n in G.nodes():
            G.node[n]["status"]="S" 
            if G.node[n]['type']=="shift":
                num_shifts+=1
            else:
               num_Drs+=1.




      #  list_final_I_values_fixed_p=[]  # i dont care about the final values right now, but about the whole time evol
        list_lists_t_evolutions=[]    

        list_dist_fixed_parameters=[]
        list_dist_abs_at_ending_point_fixed_parameters=[]
        list_final_num_infected=[]
      
       

        for iter in range(Niter_training):
            
        #    print "     iter:",iter

           

   
            list_I=[]  #list infected doctors
            list_ordering=[]            
           


            ########### set I.C.

           
            for n in G.nodes():
                G.node[n]["status"]="S"  # all nodes are Susceptible
                if G.node[n]['type']=="shift":
                    pass
                    
                else:
                    if G.node[n]['label']=="Wunderink"  or G.node[n]["label"]=="Weiss":           
                        G.node[n]["status"]="I"                       
                        list_I.append(G.node[n]['label'])
          

            
           
            list_single_t_evolution=[]
            list_single_t_evolution.append(2.0)  # I always start with TWO infected doctors!!
            old_num_adopters=2


            for n in G.nodes():   # i make some DOCTORs INMUNE  (anyone except Weiss and Wunderink)
                if (G.node[n]['type']=="A") or ( G.node[n]['type']=="F"):
                    if G.node[n]['label']!="Wunderink"  and G.node[n]["label"]!="Weiss": 
                        rand=random.random()
                        if rand< prob_Immune:
                            G.node[n]["status"]="Immune"



         #   print max_order
  
            ################# the dynamics starts: 

            shift_length=5    #i know the first shift (order 0) is of length 5

            t=0
            while t< cutting_day:  # loop over shifts, in order   just until cutting day (training segment)        
              
                for n in G.nodes():
                    if G.node[n]['type']=="shift" and G.node[n]['order']==t:


                        shift_length=int(G.node[n]['shift_length'])
                        effective_shift_length=shift_length
                        if shift_length==2 and n not in list_id_weekends_T3:
                           effective_shift_length=1   # because during weekends, the fellow does rounds one day with Att1 and the other day with Att2.  (weekend shifts for T3 are two day long, with no sharing fellows)
                         #  print "one-day weekend", G.node[n]['label'],G.node[n]['shift_length']


                        flag_possible_infection=0
                        for doctor in G.neighbors(n): #first i check if any doctor is infected in this shift
                            if G.node[doctor]["status"]=="I":
                                flag_possible_infection=1
                                

                        if flag_possible_infection:
                            for doctor in G.neighbors(n): # then the doctors in that shift, gets infected with prob_infection
                                 for i in range(effective_shift_length): 
                                    if G.node[doctor]["status"]=="S":
                                       rand=random.random()
                                       if rand<prob_infection:
                                          G.node[doctor]["status"]="I"
                                          #if G.node[doctor]["type"]=="A":
                                          list_I.append(G.node[doctor]["label"])
                                           
                        
                new_num_adopters=len(list_I)

                if  shift_length==5: # i estimate that adoption happens in the middle of the shift
                       if t+5 < cutting_day:
                          list_single_t_evolution.append(old_num_adopters) 
                       if t+4 < cutting_day:
                          list_single_t_evolution.append(old_num_adopters) 
                       if t+3 < cutting_day:
                          list_single_t_evolution.append(new_num_adopters)
                       if t+2 < cutting_day:
                          list_single_t_evolution.append(new_num_adopters)
                       if t+1 < cutting_day:
                          list_single_t_evolution.append(new_num_adopters)
                       t+=5
                      
        
                elif  shift_length==4:
                        if t+4 < cutting_day:
                           list_single_t_evolution.append(old_num_adopters)                     
                        if t+3 < cutting_day:
                           list_single_t_evolution.append(old_num_adopters) 

                        if t+2 < cutting_day:
                           list_single_t_evolution.append(new_num_adopters)                       
                       
                        if t+1 < cutting_day:
                           list_single_t_evolution.append(new_num_adopters)
                        t+=4
                      
                elif  shift_length==3:
                        if t+3 < cutting_day:
                           list_single_t_evolution.append(old_num_adopters)                     
                       
                        if t+2 < cutting_day:
                           list_single_t_evolution.append(new_num_adopters)
                       
                        if t+1 < cutting_day:
                           list_single_t_evolution.append(new_num_adopters)
                       
                        t+=3
                      


                elif  shift_length==2:
                        if t+2 < cutting_day:
                           list_single_t_evolution.append(old_num_adopters)                     
                       
                        if t+1 < cutting_day:
                           list_single_t_evolution.append(new_num_adopters)
                       
                      
                        t+=2
                      
                elif  shift_length==1:                      
                       if t+1 < cutting_day:
                           list_single_t_evolution.append(new_num_adopters)                       
                       
                       t+=1
               
                old_num_adopters=new_num_adopters


            ######## end t loop
   
           

         


  

            list_lists_t_evolutions.append(list_single_t_evolution)
             
 
            list_dist_fixed_parameters.append(compare_real_evol_vs_simus_to_be_called.compare_two_curves( list_actual_evol_training,list_single_t_evolution))
               
            list_dist_abs_at_ending_point_fixed_parameters.append( abs(list_single_t_evolution[-1]-list_actual_evol_training[-1]) )   # i save the distance at the ending point between the current simu and actual evol

          #  print "actual:",len(list_actual_evol_training),"  simu:",len(list_single_t_evolution)   # 125, 125

            
            list_final_num_infected.append(list_single_t_evolution[-1])

            list_dist_at_ending_point_fixed_parameters.append( list_single_t_evolution[-1]-list_actual_evol_training[-1] )   # i save the distance at the ending point between the current simu and actual evol


        ######## end loop Niter for the training fase
      

    
       
       
        list_pair_dist_std_delta_end=[]
        
        list_pair_dist_std_delta_end.append(numpy.mean(list_dist_fixed_parameters) )   # average dist between the curves over Niter
        list_pair_dist_std_delta_end.append(numpy.std(list_dist_fixed_parameters) )

        list_pair_dist_std_delta_end.append(numpy.mean(list_dist_abs_at_ending_point_fixed_parameters))



        if print_landscape =="YES":
           file3 = open(output_file3,'at')          # i print out the landscape           
           print >> file3, prob_infection,prob_Immune,numpy.mean(list_dist_abs_at_ending_point_fixed_parameters), numpy.mean(list_dist_fixed_parameters), numpy.mean(list_final_num_infected),numpy.std(list_final_num_infected), numpy.std(list_final_num_infected)/numpy.mean(list_final_num_infected)
           file3.close()
     


        if   print_training_evol== "YES":

           file2 = open(output_file2,'wt')        
           for s in range(len(list_single_t_evolution)):           
              list_fixed_t=[]
              for iter in range (Niter_training):
                 list_fixed_t.append(list_lists_t_evolutions[iter][s])        
              print >> file2, s,numpy.mean(list_fixed_t)                    
           file2.close()
           print "written evolution file:", output_file2

    

    



        value=numpy.mean(list_dist_fixed_parameters) *numpy.mean(list_dist_abs_at_ending_point_fixed_parameters) # if SD=0, it is a problem, because then that is the minimun value, but not the optimum i am looking for!!
        
        
        dict_filenames_prod_distances[output_file2]=  value
      

        if (numpy.mean(list_dist_abs_at_ending_point_fixed_parameters)) <= delta_end:  # i only consider situations close enough at the ending point   
          
           dict_filenames_tot_distance[output_file2]=list_pair_dist_std_delta_end
         
      


        prob_infection+= delta_prob
      prob_Immune+= delta_prob_Immune




   if print_training_evol== "NO":  #if i am exploring the whole space

      string_name="infection_training"+fixed_param+str(Niter_training)+"iter_day"+str(cutting_day)+"_A_F_inferred_middle.dat"   # for the "Results" file with the sorted list of files
      list_order_dict=  compare_real_evol_vs_simus_to_be_called.pick_minimum_same_end(dict_filenames_tot_distance,string_name,Niter_training,cutting_day)
      
# it returns a list of tuples like this :  ('../Results/network_final_schedule_withTeam3_local/infection/Average_time_evolution_Infection_training_p0.7_Immune0.0_2iter_2012.dat', [2540.0, 208.0, 1.0])  the best set of parameters  being the fist one of the elements in the list.



 
   
      list_order_dict2= compare_real_evol_vs_simus_to_be_called.pick_minimum_prod_distances(dict_filenames_prod_distances,string_name,Niter_training,cutting_day)



 
   #  i already know the optimum, now i run the dynamics with those values, starting from the average state on the cutting point, and test: 




        
      optimum_filename=list_order_dict2[0][0]
      prob_infection=float(list_order_dict2[0][0].split("_p")[1].split("_")[0])
      prob_Immune=float(list_order_dict2[0][0].split("_Immune")[1].split("_")[0])
      
      
  
      print "Optimum parameters (product of distances along_traject and at the end) at day",cutting_day," are: p=",prob_infection," and Pimmune=",prob_Immune
      


      print "Run that simulation with the optimum parameter set:",optimum_filename
  






      output_file10="../Results/weight_shifts/Summary_results_training_segment_infection_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter_training)+"iter_avg_ic_day"+str(cutting_day)+"_A_F_inferred_middle.dat"          
      file10 = open(output_file10,'wt')    
      
      print >> file10, "Summary results from train-testing persuasion with",Niter_training, "iter , using all the individual cutting points as IC, and with values for the parameters:  prob_inf ",prob_infection," prob immune: ",prob_Immune,"\n"
      
      print >> file10,  "Look for the file (or run that simulation) with the optimum parameter set:",optimum_filename
      file10.close()

   if print_landscape=="YES":
      print "printed out landscape file:",output_file3


######################################



def look_for_T3_weekends(G):

   list_ids_T3_weekends=[]
   for n in G.nodes():
      if G.node[n]['type']=='shift':
         if G.node[n]['shift_length']==2 and "T3" in G.node[n]['label']:
            list_ids_T3_weekends.append(n)
            

               
   return  list_ids_T3_weekends
   







######################################
###############################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
   
        main(graph_filename)
    else:
        print "Usage: python script.py path/network.gml"

    
