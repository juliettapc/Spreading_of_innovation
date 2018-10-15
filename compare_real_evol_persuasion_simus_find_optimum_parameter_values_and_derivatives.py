#!/usr/bin/env python

'''
Given a bunch of files corresponding to different values of the parameters of the persuation simulation model (Hospital project), compare them all with the actual evolution of the number of adopters, to fit the better values of the parameters.

Created by Julia Poncela, on August 2012.

'''

import csv
import sys
import os
import operator
import numpy

def main():
 

   dir_simus_data='../Results/network_final_schedule_withTeam3/'
   dir_real_data='../Results/'





   #output_file=dir_real_data+"Results_persuation_sorted_distance_simulated_to_real_evolutions.dat"   
   output_file=dir_real_data+"Results_persuation_sorted_distance_simulated_to_real_evolutions_all_team_as_adopters.dat"   
   file = open(output_file,'wt')    # to save the sorted list of path/filenames  and distance_values std_distances
  



   #output_file2=dir_real_data+"Results_persuation_sorted_distance_derivatives_simulated_to_real_evolutions.dat"   
   output_file2=dir_real_data+"Results_persuation_sorted_distance_derivatives_simulated_to_real_evolutions_all_team_as_adopters.dat"   
   file2 = open(output_file2,'wt')    # to save the sorted list of path/filenames  and distance_values std_distances
  




######################################################################################
#  I read the file of the actual evolution of the idea spreading in the hospital:   ##
######################################################################################



  # filename_actual_evol=dir_real_data+"HospitalModel_august1_adoption_counts_SIMPLER.csv"
   filename_actual_evol=dir_real_data+"HospitalModel_august1_adoption_counts_all_team_as_adopters_SIMPLER.csv"

 
   list_actual_evol=[]
   list_actual_evol_derivatives=[]  
   result_actual_file= csv.reader(open(filename_actual_evol, 'rb'), delimiter=',')
   cont=0
   for row in result_actual_file: 
       if cont>0:   # i ignore the first line with the headers
           
           list_time_step_actual_evol_derivatives=[]
           list_time_step_actual_evol=[]

           time=int(row[0])       
           num_adopters= float(row[3])
           list_time_step_actual_evol.append(time)
           list_time_step_actual_evol.append(num_adopters)

           if cont>1:  # the first point doesnt have a derivative
              list_time_step_actual_evol_derivatives.append(time)
              list_time_step_actual_evol_derivatives.append(num_adopters-old_value)   # each time step is =1, so i dont need to divided by time2-time1

           old_value=num_adopters

           list_actual_evol.append(list_time_step_actual_evol)
           list_actual_evol_derivatives.append(list_time_step_actual_evol_derivatives)

       cont+=1    
  





#################################################################################################################
#  I read all the files for the diff. values of the parameters for the simulations of the persuation process : ##
#################################################################################################################


   dict_filenames_tot_distance={}   # i will save the filename as key and the tot distance from that curve to the original one
   dict_filenames_tot_distance_derivatives={}   

   Niter=30
   

   threshold_min=0.0  # larger than, to be an Adopter
   threshold_max=1.0 
   delta_threshold=0.1

   alpha_F_min=0.00   # alpha=0: nobody changes their mind
   alpha_F_max=1.01
   delta_alpha_F=0.1
   
   min_damping=0.0     #its harder to go back from YES to NO again. =1 means no diff, =0.5 half the movement from Y->N than the other way around, =0 never go back from Y to N
   max_damping=1.0
   delta_damping=0.1  
   
   
   min_mutual_encouragement=0.0  # when two Adopters meet, they convince each other even more
   max_mutual_encouragement=1.0  
   delta_mutual_encouragement=0.1
   

   threshold=threshold_min
   while   threshold<= threshold_max:


     alpha_F=alpha_F_min
     while alpha_F<= alpha_F_max:           
        alpha_A=0.5*alpha_F     

        mutual_encouragement=min_mutual_encouragement  
        while  mutual_encouragement <= max_mutual_encouragement:
 
          damping=min_damping
          while   damping <= max_damping:
 
         
              
            filename=dir_simus_data+"Time_evolutions_Persuasion_alpha"+str(alpha_F)+"_damping"+str(damping)+"_mutual_encourg"+str(mutual_encouragement)+"_threshold"+str(threshold)+"_unif_distr_"+str(Niter)+"iter_2012_seed31Oct_finalnetwork.dat"
          

            list_evol_one_simu=[]
            list_evol_one_simu_derivatives=[]
            result_att_fellows= csv.reader(open(filename, 'rb'), delimiter=' ')
            cont=0
            for row in result_att_fellows: 
                list_time_step_simu=[]
                list_time_step_simu_derivatives=[]

                time=int(row[0])       
                num_adopters=float(row[1])

                list_time_step_simu.append(time)
                list_time_step_simu.append(num_adopters)

                if cont>0:  # the first point doesnt have a derivative
                   list_time_step_simu_derivatives.append(time)
                   list_time_step_simu_derivatives.append(num_adopters-old_value)

                old_value=num_adopters

                list_evol_one_simu.append(list_time_step_simu)
                list_evol_one_simu_derivatives.append(list_time_step_simu_derivatives)

                cont+=1



            list_dist=[]
            list_dist_derivatives=[]
            for i in range(len(list_evol_one_simu)):   # i calculate the sum of distances from one curve to another at each same time step
                list_dist.append((list_evol_one_simu[i][1]-list_actual_evol[i][1])*(list_evol_one_simu[i][1]-list_actual_evol[i][1]))

                try:  # because the list of derivatives is one unit shorter

                   list_dist_derivatives.append((list_evol_one_simu[i][1]-list_actual_evol[i][1])*(list_evol_one_simu[i][1]-list_actual_evol[i][1]) +  (list_evol_one_simu_derivatives[i][1]-list_actual_evol_derivatives[i][1])*(list_evol_one_simu_derivatives[i][1]-list_actual_evol_derivatives[i][1]))

                  # list_dist_derivatives.append((list_evol_one_simu_derivatives[i][1]-list_actual_evol_derivatives[i][1])*(list_evol_one_simu_derivatives[i][1]-list_actual_evol_derivatives[i][1]))  #THIS VERSION GIVES AS OPTIMUM AN EVOLUTION THAT IS ALMOST FLAT, NEAR ZERO

                
                 
                except: pass

            mean_dist=numpy.mean(list_dist)
            std_dist=numpy.std(list_dist)

            mean_dist_derivatives=numpy.mean(list_dist_derivatives)
            std_dist_derivatives=numpy.std(list_dist_derivatives)



           

          #  print mean_dist, mean_dist_derivatives

            list_mean_std_dist=[]   # for the pair dist-std_dist
            list_mean_std_dist.append(mean_dist)
            list_mean_std_dist.append(std_dist)

            list_mean_std_dist_derivatives=[] 
            list_mean_std_dist_derivatives.append(mean_dist_derivatives)
            list_mean_std_dist_derivatives.append(std_dist_derivatives)



            dict_filenames_tot_distance[filename]=list_mean_std_dist
            dict_filenames_tot_distance_derivatives[filename]=list_mean_std_dist_derivatives
          

            damping += delta_damping
          mutual_encouragement += delta_mutual_encouragement
        alpha_F += delta_alpha_F
     threshold  += delta_threshold
 

   minimum_value=1000000.
   for clave in dict_filenames_tot_distance:       # acording to distance
      if float(dict_filenames_tot_distance[clave][0]) < minimum_value:
           minimum_value= dict_filenames_tot_distance[clave][0]
           minimum_filename=clave



   minimum_value_derivatives=1000000.
   for clave in dict_filenames_tot_distance_derivatives:       # acording to distance for the derivatives    
      
      if float(dict_filenames_tot_distance_derivatives[clave][0]) < minimum_value_derivatives:
           minimum_value_derivatives= dict_filenames_tot_distance_derivatives[clave][0]
           minimum_filename_derivatives=clave



  


     # el diccionario dict_filenames_tot_distance   es: clave=path/filename  dict_filenames_tot_distance[clave] =[distancia,std_distancia]




   

# ojo!!!! when i sort the dict, what it get is a LIST of TUPLES, and each tuple (item) is ('/path/filename',[distancia, std_distancia])


   list_sorted_dict_filenames_tot_distance = sorted(dict_filenames_tot_distance.iteritems(), key=operator.itemgetter(1))

   list_sorted_dict_filenames_tot_distance_derivatives = sorted(dict_filenames_tot_distance_derivatives.iteritems(), key=operator.itemgetter(1))

  


 
   for item in list_sorted_dict_filenames_tot_distance:       
       print >> file,item[0],item[1][0],item[1][1]
       print  item[0],item[1][0],item[1][1]

   file.close()




   for item in list_sorted_dict_filenames_tot_distance_derivatives:       
       print >> file2,item[0],item[1][0],item[1][1]
       print  item[0],item[1][0],item[1][1]

   file2.close()






 #  print  "\n\nthe minimun value",minimum_value, " is for:", minimum_filename 
  # print  "the minimun value for derivatives ",minimum_value_derivatives, " is for:", minimum_filename_derivatives 


##################################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
    main()
    #else:
     #   print "Usage: python script.py path/network.gml"

    
