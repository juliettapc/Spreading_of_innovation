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



   cutting_day=125  # i use this only for the filenames




   for_testing_fixed_set="YES"   # when YES, fixed values param, to get all statistics on final distances etc
# change the range for the parameters accordingly

   envelopes="YES"

   Niter=1000   # 100 iter seems to be enough (no big diff. with respect to 1000it)

   percent_envelope=95.
   
   list_id_weekends_T3=look_for_T3_weekends(G)  # T3 doesnt share fellows in the weekend  (but they are the exception)
   Nbins=200   # for the histogram of sum of distances


   all_team="NO"   # as adopters or not

   dir_real_data='../Results/'
   dir="../Results/weight_shifts/infection/" 

   delta_end=3.  # >= than + or -  dr difference at the end of the evolution (NO realization ends up closer than this!!!! if 2, i get and empty list!!!)


   if for_testing_fixed_set=="NO":
      output_file3="../Results/weight_shifts/Landscape_parameters_infection_"+str(Niter)+"iter_A_F_inferred.dat" 
      file3 = open(output_file3,'wt')        
      
      file3.close()



######################################################################################
#  I read the file of the actual evolution of the idea spreading in the hospital:   ##
######################################################################################



   if all_team=="YES":    
      print "remember that now i use the file of adopters without fellows\n../Results/Actual_evolution_adopters_NO_fellows_only_attendings.dat"
      exit()

   else:
      filename_actual_evol="../Results/Actual_evolution_adopters_from_inference.dat"
  


   file1=open(filename_actual_evol,'r')         ## i read the file:  list_dates_and_names_current_adopters.txt  (created with: extract_real_evolution_number_adopters.py)
   list_lines_file=file1.readlines()
            

   list_actual_evol=[]  
   for line in list_lines_file:      # [1:]:   # i exclude the first row   
     
      num_adopters= float(line.split("\t")[1])          
      list_actual_evol.append(num_adopters)



##################################################################




#../Results/weight_shifts/infection/Average_time_evolution_Infection_training_p0.8_Immune0.3_1000iter_2012_avg_ic_day125.dat ESTOS VALORES SON EL OPTIMUM FIT THE 152-DIAS
   prob_min=0.4
   prob_max=0.401
   delta_prob=0.1
   
   

   prob_Immune_min=0.50
   prob_Immune_max=0.51
   delta_prob_Immune=0.1
   




     

   dict_filenames_tot_distance={}   # i will save the filename as key and the tot distance from that curve to the original one

   prob_Immune=prob_Immune_min
   while prob_Immune<= prob_Immune_max:
        
      print "prom Immune:",prob_Immune        

      prob_infection=prob_min
      while prob_infection<= prob_max:
                 
        print "  p:",prob_infection        


        if for_testing_fixed_set=="YES":
           output_file2=dir+"Average_time_evolution_Infection_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter)+"iter_A_F_inferred.dat"

        else:
           output_file2=dir+"Average_time_evolution_Infection_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter)+"iter_A_F_inferred.dat"


        file2 = open(output_file2,'wt')                                       
        file2.close()
        



      #  list_final_I_values_fixed_p=[]  # i dont care about the final values right now, but about the whole time evol
        list_lists_t_evolutions=[]    

        list_dist_fixed_parameters=[]
        list_dist_fixed_parameters_testing_segment=[]
        list_abs_dist_at_ending_point_fixed_parameters=[]
        list_dist_at_ending_point_fixed_parameters=[]
        list_final_num_infected=[]
        list_abs_dist_point_by_point_indiv_simus_to_actual=[]
        list_dist_point_by_point_indiv_simus_to_actual=[]

     #   list_abs_dist_at_cutting_day=[]

        for iter in range(Niter):
            
            print "     iter:",iter


            #######OJO~!!!!!!!!!! COMENTAR ESTO CUANDO ESTOY BARRIENDO TOOOOOOOOOODO EL ESPACIO DE PARAMETROS
        #    file_name_indiv_evol=output_file2.strip("Average_").split('.dat')[0]+"_indiv_iter"+str(iter)+".dat"
           
         #   file4 = open(file_name_indiv_evol,'wt')       
          #  file4.close()
              ##########################################




            ########### set I.C.

            list_I=[]  #list infected doctors                
            max_order=0
            for n in G.nodes():
                G.node[n]["status"]="S"  # all nodes are Susceptible
                if G.node[n]['type']=="shift":                      
                    if  G.node[n]['order']>max_order:
                        max_order=G.node[n]['order']   # to get the last shift-order for the time loop
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
                                     if rand<prob_infection:
                                        G.node[doctor]["status"]="I"
                                        
                                       # if G.node[doctor]["type"]=="A":   # fellows participate in the dynamics, but i only consider the attendings as real adopters
                                        list_I.append(G.node[doctor]["label"])
                                        
              #  if for_testing_fixed_set=="YES":
               #    if t==cutting_day:
                #      list_abs_dist_at_cutting_day.append(abs(float(list_actual_evol[-1])-float(len(list_I))))
                 #     print abs(float(list_actual_evol[-1])-float(len(list_I))), float(list_actual_evol[t]),float(len(list_I))
                     

                list_single_t_evolution.append(float(len(list_I)))

                t+=1
   


                ######## end t loop




            ########OJO~!!!!!!!!!! COMENTAR ESTO CUANDO ESTOY BARRIENDO TOOOOOOOOOODO EL ESPACIO DE PARAMETROS
           # file4 = open(file_name_indiv_evol,'at')                
            #for i in range(len(list_single_t_evolution)):  #time step by time step                            
             #  print >> file4, i,list_single_t_evolution[i], prob_infection, prob_Immune 
            #file4.close()
            ########################################################



          

            list_lists_t_evolutions.append(list_single_t_evolution)
             
 
            list_dist_fixed_parameters.append(compare_real_evol_vs_simus_to_be_called.compare_two_curves( list_actual_evol,list_single_t_evolution))
            list_dist_fixed_parameters_testing_segment.append(compare_real_evol_vs_simus_to_be_called.compare_two_curves_testing_segment( list_actual_evol,list_single_t_evolution, cutting_day))
                 
            list_abs_dist_at_ending_point_fixed_parameters.append( abs(list_single_t_evolution[-1]-list_actual_evol[-1]) )   # i save the distance at the ending point between the current simu and actual evol
            list_dist_at_ending_point_fixed_parameters.append( list_single_t_evolution[-1]-list_actual_evol[-1])    # i save the distance at the ending point between the current simu and actual evol
            list_final_num_infected.append(list_single_t_evolution[-1])


            for  index in range(len(list_single_t_evolution)):
               
               list_abs_dist_point_by_point_indiv_simus_to_actual.append(abs(list_single_t_evolution[index]-list_actual_evol[index]))
               list_dist_point_by_point_indiv_simus_to_actual.append(list_single_t_evolution[index]-list_actual_evol[index])


           
        ######## end loop Niter
      



       
       
        list_pair_dist_std_delta_end=[]
        
        list_pair_dist_std_delta_end.append(numpy.mean(list_dist_fixed_parameters) )   # average dist between the curves over Niter
        list_pair_dist_std_delta_end.append(numpy.std(list_dist_fixed_parameters) )

        list_pair_dist_std_delta_end.append(numpy.mean(list_abs_dist_at_ending_point_fixed_parameters))


        if for_testing_fixed_set=="NO":   
           file3 = open(output_file3,'at')          # i print out the landscape           
           print >> file3, prob_infection,prob_Immune,numpy.mean(list_abs_dist_at_ending_point_fixed_parameters), numpy.mean(list_dist_fixed_parameters), numpy.mean(list_final_num_infected),numpy.std(list_final_num_infected)
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

        print "printed out: ", output_file2
       # raw_input()

        if  envelopes=="YES":
           calculate_envelope_set_curves.calculate_envelope(list_lists_t_evolutions,percent_envelope,"Infection",[prob_infection,prob_Immune])






        if for_testing_fixed_set=="YES":

           num_valid_endings=0.
           for item in list_abs_dist_at_ending_point_fixed_parameters:
              if item <= delta_end:  # i count how many realizations i get close enough at the ending point         
                 num_valid_endings+=1.
     

           print "average distance of the optimum in the testing segment:",numpy.mean(list_dist_fixed_parameters),numpy.std(list_dist_fixed_parameters),list_dist_fixed_parameters,"\n"
           print "fraction of realizations that end within delta_doctor:",num_valid_endings/Niter,"mean ending dist:",numpy.mean(list_dist_at_ending_point_fixed_parameters), "SD final dist",numpy.std(list_dist_at_ending_point_fixed_parameters) ,list_dist_at_ending_point_fixed_parameters,"\n"
        
        

           histogram_filename="../Results/weight_shifts/histogr_raw_distances_ending_infection_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter)+"iter_day"+str(cutting_day)+"_A_F_inferred.dat"
           histograma_gral_negv_posit.histograma(list_dist_at_ending_point_fixed_parameters,histogram_filename)



           histogram_filename2="../Results/weight_shifts/histogr_sum_dist_traject_infection_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter)+"iter_day"+str(cutting_day)+"_A_F_inferred.dat"
          
           histograma_bines_gral.histograma_bins(list_dist_fixed_parameters,Nbins,histogram_filename2)



           histogram_filename3="../Results/weight_shifts/histogr_sum_dist_testing_segment_infection_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter)+"iter_day"+str(cutting_day)+"_A_F_inferred.dat"
                 
           histograma_bines_gral.histograma_bins_zero(list_dist_fixed_parameters_testing_segment,Nbins,histogram_filename3)



           histogram_filename4="../Results/weight_shifts/histogr_abs_dist_point_by_point_infection_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter)+"iter_day"+str(cutting_day)+"_A_F_inferred.dat"
           histograma_gral_negv_posit.histograma(list_abs_dist_point_by_point_indiv_simus_to_actual,histogram_filename4)



           histogram_filename5="../Results/weight_shifts/histogr_dist_point_by_point_infection_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter)+"iter_day"+str(cutting_day)+"_A_F_inferred.dat"
           histograma_gral_negv_posit.histograma(list_dist_point_by_point_indiv_simus_to_actual,histogram_filename5)




           output_file10="../Results/weight_shifts/Summary_results_infection_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter)+"iter_day"+str(cutting_day)+"_A_F_inferred.dat"          
           file10 = open(output_file10,'wt')    
           
           print >> file10, "Summary results from best fit infection with",Niter, "iter, and with values for the parameters:  prob_inf ",prob_infection," prob immune: ",prob_Immune,"\n"
           
           print >> file10, "average distance of the optimum in the testing segment:",numpy.mean(list_dist_fixed_parameters),numpy.std(list_dist_fixed_parameters),list_dist_fixed_parameters,"\n"
           print >> file10,  "fraction of realizations that end within delta_doctor:",num_valid_endings/Niter,"mean ending dist:",numpy.mean(list_dist_at_ending_point_fixed_parameters), "SD final dist",numpy.std(list_dist_at_ending_point_fixed_parameters) ,list_dist_at_ending_point_fixed_parameters,"\n"
           
           
           print >> file10,  "written optimum best fit evolution file:",output_file2
           print  >> file10,"written histogram file: ",histogram_filename
           
           file10.close()


        
           print  "written Summary file: ",output_file10
        




        prob_infection+= delta_prob
      prob_Immune+= delta_prob_Immune

   if for_testing_fixed_set=="NO":   # only if i am exploring the whole landscape, i need to call this function, otherwise, i already know the optimum
      compare_real_evol_vs_simus_to_be_called.pick_minimum_same_end(dict_filenames_tot_distance,"Infection_weight",all_team,Niter,None)  # last argument doesnt apply (cutting day)




   if for_testing_fixed_set=="NO":
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

    
