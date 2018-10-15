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
import calculate_envelope_set_curves


def main(graph_name):
 



   G = nx.read_gml(graph_name)



   cutting_day=175     # i use this only for the filenames




   for_testing_fixed_set="YES"   # when YES, fixed values param, to get all statistics on final distances etc
# change the range for the parameters accordingly

   envelopes="YES"

   Niter=1000   # 100 iter seems to be enough (no big diff. with respect to 1000it)




   percent_envelope=95.
   
   list_id_weekends_T3=look_for_T3_weekends(G)  # T3 doesnt share fellows in the weekend  (but they are the exception)
   Nbins=1000   # for the histogram of sum of distances


   all_team="NO"   # as adopters or not

   dir_real_data='../Results/'
   dir="../Results/weight_shifts/infection/" 

   delta_end=3.  # >= than + or -  dr difference at the end of the evolution (NO realization ends up closer than this!!!! if 2, i get and empty list!!!)




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




#../Results/weight_shifts/infection/Average_time_evolution_Infection_training_p0.8_Immune0.3_1000iter_2012_avg_ic_day125.dat ESTOS VALORES SON EL OPTIMUM FIT THE 152-DIAS
   prob_min=1.00
   prob_max=1.001
   delta_prob=0.1
   
   

   prob_Immune_min=0.700
   prob_Immune_max=0.7001
   delta_prob_Immune=0.1
   



   prob_Immune=prob_Immune_min
   while prob_Immune<= prob_Immune_max:
        
      print "prom Immune:",prob_Immune        

      prob_infection=prob_min
      while prob_infection<= prob_max:
                 
        print "  p:",prob_infection        


        
        output_file2=dir+"Average_time_evolution_Infection_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter)+"iter_day"+str(cutting_day)+"_Att_only_middle_real_ic.dat"     


        file2 = open(output_file2,'wt')                                       
        file2.close()
        

  
          ########## i read the list of frequent adopters from simulations, to estimate the ic for fellows

       
        filename_list_simu_adopt="../Results/weight_shifts/infection/List_adopters_fellows_descending_frequency_Infection_training_p"+str(prob_infection)+"_Immune"+str(prob_Immune)+"_1000iter_2012_avg_ic_day"+str(cutting_day)+"_Att_only_middle.dat"
        
       # print filename_list_simu_adopt
        file_list_simu_adopt=open(filename_list_simu_adopt,'r')        
        list_lines_file=file_list_simu_adopt.readlines()
        
        
        list_sorted_fellow_adopters=[]
        for line in list_lines_file[1:]:   # i exclude the first row            
           adopter=line.split(" ")[0]              
           list_sorted_fellow_adopters.append(adopter)
           
       # print  "list sorted fellows:",list_sorted_fellow_adopters 

        num_simu_Fellow_adopters_cutting_day=int( round(float(list_lines_file[0].split("Avg # F adopters ")[1].split(" ")[0])))
        #print "avg simu number Fellow adopters:",num_simu_Fellow_adopters_cutting_day,int( round(num_simu_Fellow_adopters_cutting_day))
          ################



        
        list_lists_t_evolutions=[]    

      
        list_dist_fixed_parameters_testing_segment=[]
        list_abs_dist_at_ending_point_fixed_parameters=[]
        list_dist_at_ending_point_fixed_parameters=[]
        list_final_num_infected=[]
        list_abs_dist_point_by_point_indiv_simus_to_actual=[]
        list_dist_point_by_point_indiv_simus_to_actual=[]

    

        for iter in range(Niter):
            
         #   print "     iter:",iter


    
            ########### set I.C.  according to the empirical data
            dict_name_node={}
            list_I=[]                  
            max_order=0
            
            for n in G.nodes():
                G.node[n]["status"]="S"  # all nodes are Susceptible
                if G.node[n]['type']=="shift":                      
                    if  G.node[n]['order']>max_order:
                        max_order=G.node[n]['order']   # to get the last shift-order for the time loop
                else:
                   dict_name_node[G.node[n]["label"]]=n                  
                   if G.node[n]['label'] in dict_days_list_empirical_att_adopters[cutting_day]:           
                        G.node[n]["status"]="I"                       
                        list_I.append(G.node[n]['label'])
                       
           
            list_fellows=[]
            for i in range(num_simu_Fellow_adopters_cutting_day):  
               fellow_adopter=  list_sorted_fellow_adopters[i]   # this list is sorted from more to less frequent adopter   
               node=dict_name_node[fellow_adopter]
               G.node[node]["status"]="I"
               list_fellows.append(fellow_adopter)

      
            list_single_t_evolution=[]          
            old_num_adopters=len(list_I)
            list_single_t_evolution.append(old_num_adopters)  # I always start with TWO infected doctors!!

            for n in G.nodes():   # i make some DOCTORs INMUNE  (anyone except Weiss and Wunderink)
                if (G.node[n]['type']=="A") or ( G.node[n]['type']=="F"):
                    if (G.node[n]['label'] not in dict_days_list_empirical_att_adopters[cutting_day]) and (G.node[n]['label'] not in list_fellows):
                        rand=random.random()
                        if rand< prob_Immune:
                            G.node[n]["status"]="Immune"




       
  
            ################# the dynamics starts: 
            
            
            shift_length=5    #i know the first shift (order 0) is of length 5

            t=cutting_day
            while t<= max_order:  # loop over shifts, in order  
                
                for n in G.nodes():
                    if G.node[n]['type']=="shift" and G.node[n]['order']==t:
                      

                        shift_length=int(G.node[n]['shift_length'])

                        if shift_length==2 and n not in list_id_weekends_T3:
                           shift_length=1   # because during weekends, the fellow does rounds one day with Att1 and the other day with Att2.  (weekend shifts for T3 are two day long, with no sharing fellows)
                         #  print "one-day weekend", G.node[n]['label'],G.node[n]['shift_length']

                        flag_possible_infection=0
                        for doctor in G.neighbors(n): #first i check if any doctor is infected in this shift
                            if G.node[doctor]["status"]=="I":
                                flag_possible_infection=1
                                
                       
                        if flag_possible_infection:
                           
                           for doctor in G.neighbors(n): # then the doctors in that shift, gets infected with prob_infection
                               for i in range(shift_length):   # i repeat the infection process several times, to acount for shift length
                                  if G.node[doctor]["status"]=="S":
                                     rand=random.random()
                                     if rand<prob_infection:
                                        G.node[doctor]["status"]="I"
                                        
                                        if G.node[doctor]["type"]=="A":   # fellows participate in the dynamics, but i only consider the attendings as real adopters
                                           list_I.append(G.node[doctor]["label"])
                                        
          

                new_num_adopters=len(list_I)
               

                if  shift_length==5: # i estimate that adoption happens in the middle of the shift
                       if t+5 < max_order:
                          list_single_t_evolution.append(old_num_adopters) 
                       if t+4 < max_order:
                          list_single_t_evolution.append(old_num_adopters) 
                       if t+3 < max_order:
                          list_single_t_evolution.append(new_num_adopters)
                       if t+2 < max_order:
                          list_single_t_evolution.append(new_num_adopters)
                       if t+1 < max_order:
                          list_single_t_evolution.append(new_num_adopters)
                       t+=5
                      
        
                elif  shift_length==4:
                        if t+4 < max_order:
                           list_single_t_evolution.append(old_num_adopters)                     
                        if t+3 < max_order:
                           list_single_t_evolution.append(old_num_adopters) 

                        if t+2 < max_order:
                           list_single_t_evolution.append(new_num_adopters)                       
                       
                        if t+1 < max_order:
                           list_single_t_evolution.append(new_num_adopters)
                        t+=4
                      
                elif  shift_length==3:
                        if t+3 < max_order:
                           list_single_t_evolution.append(old_num_adopters)                     
                       
                        if t+2 < max_order:
                           list_single_t_evolution.append(new_num_adopters)
                       
                        if t+1 < max_order:
                           list_single_t_evolution.append(new_num_adopters)
                       
                        t+=3
                      


                elif  shift_length==2:
                        if t+2 < max_order:
                           list_single_t_evolution.append(old_num_adopters)                     
                       
                        if t+1 < max_order:
                           list_single_t_evolution.append(new_num_adopters)
                       
                      
                        t+=2
                      
                elif  shift_length==1:                      
                       if t+1 < max_order:
                           list_single_t_evolution.append(new_num_adopters)                       
                       
                       t+=1
               
                old_num_adopters=new_num_adopters
              


                ######## end t loop

         

            list_lists_t_evolutions.append(list_single_t_evolution)
             
             # now i only run the testing segment!
            list_dist_fixed_parameters_testing_segment.append(compare_real_evol_vs_simus_to_be_called.compare_two_curves( list_actual_evol_testing,list_single_t_evolution))
           
                 
            list_abs_dist_at_ending_point_fixed_parameters.append( abs(list_single_t_evolution[-1]-list_actual_evol_testing[-1]) )   # i save the distance at the ending point between the current simu and actual evol
            list_dist_at_ending_point_fixed_parameters.append( list_single_t_evolution[-1]-list_actual_evol_testing[-1])    # i save the distance at the ending point between the current simu and actual evol
            list_final_num_infected.append(list_single_t_evolution[-1])


            for  index in range(len(list_single_t_evolution)):
               
               list_abs_dist_point_by_point_indiv_simus_to_actual.append(abs(list_single_t_evolution[index]-list_actual_evol_testing[index]))
               list_dist_point_by_point_indiv_simus_to_actual.append(list_single_t_evolution[index]-list_actual_evol_testing[index])


           
        ######## end loop Niter
      



      
        



        file2 = open(output_file2,'at')        
        for s in range(len(list_single_t_evolution)):           
            list_fixed_t=[]
            for iter in range (Niter):
                list_fixed_t.append(list_lists_t_evolutions[iter][s])        
            print >> file2, s+cutting_day,numpy.mean(list_fixed_t)                    
        file2.close()

        print "printed out: ", output_file2
    

        if  envelopes=="YES":
           calculate_envelope_set_curves.calculate_envelope(list_lists_t_evolutions,percent_envelope,"Infection",[prob_infection,prob_Immune])




        num_valid_endings=0.
        for item in list_abs_dist_at_ending_point_fixed_parameters:
              if item <= delta_end:  # i count how many realizations i get close enough at the ending point         
                 num_valid_endings+=1.
     

        print "average distance of the optimum in the testing segment:",numpy.mean(list_dist_fixed_parameters_testing_segment),numpy.std(list_dist_fixed_parameters_testing_segment),list_dist_fixed_parameters_testing_segment,"\n"
        print "fraction of realizations that end within delta_doctor:",num_valid_endings/Niter,"mean ending dist:",numpy.mean(list_dist_at_ending_point_fixed_parameters), "SD final dist",numpy.std(list_dist_at_ending_point_fixed_parameters) ,list_dist_at_ending_point_fixed_parameters,"\n"
        
        
        
        histogram_filename="../Results/weight_shifts/histogr_raw_distances_ending_infection_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter)+"iter_day"+str(cutting_day)+"_Att_only_middle_real_ic.dat"     
        histograma_gral_negv_posit.histograma(list_dist_at_ending_point_fixed_parameters,histogram_filename)
        

        histogram_filename3="../Results/weight_shifts/histogr_sum_dist_testing_segment_infection_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter)+"iter_day"+str(cutting_day)+"_Att_only_middle_real_ic.dat"     
        
        
        histograma_bines_gral.histograma_bins_zero(list_dist_fixed_parameters_testing_segment,Nbins,histogram_filename3)
        
        print min(list_dist_fixed_parameters_testing_segment),max(list_dist_fixed_parameters_testing_segment)
        
        
        histogram_filename4="../Results/weight_shifts/histogr_abs_dist_point_by_point_infection_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter)+"iter_day"+str(cutting_day)+"_Att_only_middle_real_ic.dat"     
        histograma_gral_negv_posit.histograma(list_abs_dist_point_by_point_indiv_simus_to_actual,histogram_filename4)



        histogram_filename5="../Results/weight_shifts/histogr_dist_point_by_point_infection_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter)+"iter_day"+str(cutting_day)+"_Att_only_middle_real_ic.dat"     
        histograma_gral_negv_posit.histograma(list_dist_point_by_point_indiv_simus_to_actual,histogram_filename5)
        
        
        
        
        output_file10="../Results/weight_shifts/Summary_results_infection_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter)+"iter_day"+str(cutting_day)+"_Att_only_middle_real_ic.dat"               
        file10 = open(output_file10,'wt')    
        
        print >> file10, "Summary results from best fit infection with",Niter, "iter, and with values for the parameters:  prob_inf ",prob_infection," prob immune: ",prob_Immune,"\n"
        
        print >> file10, "average distance of the optimum in the testing segment:",numpy.mean(list_dist_fixed_parameters_testing_segment),numpy.std(list_dist_fixed_parameters_testing_segment),list_dist_fixed_parameters_testing_segment,"\n"
        print >> file10,  "fraction of realizations that end within delta_doctor:",num_valid_endings/Niter,"mean ending dist:",numpy.mean(list_dist_at_ending_point_fixed_parameters), "SD final dist",numpy.std(list_dist_at_ending_point_fixed_parameters) ,list_dist_at_ending_point_fixed_parameters,"\n"
        
           
        print >> file10,  "written optimum best fit evolution file:",output_file2
        print  >> file10,"written histogram file: ",histogram_filename
           
        file10.close()


        
        print  "written Summary file: ",output_file10
        


        prob_infection+= delta_prob
      prob_Immune+= delta_prob_Immune

 



######################################
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

    
