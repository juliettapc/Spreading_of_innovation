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
 

   dir_simus_data='../Results/network_final_schedule_withTeam3/infection/'
   dir_real_data='../Results/'


   Niter=1000

   output_file3=dir_real_data+"Landscape_parameters_infection"+str(Niter)+"iter.dat" 
   file3 = open(output_file3,'wt')                                       
  


  
   output_file=dir_real_data+"Results_infection_sorted_distance_simulated_to_real_evolutions_all_team_as_adopters"+str(Niter)+"iter.dat"      
 #  output_file=dir_real_data+"Results_infection_sorted_distance_simulated_to_real_evolutions"+str(Niter)+"iter.dat"   


   file = open(output_file,'wt')    # to save the sorted list of path/filenames  and distance_values std_distances
  


######################################################################################
#  I read the file of the actual evolution of the idea spreading in the hospital:   ##
######################################################################################


   filename_actual_evol=dir_real_data+"HospitalModel_august1_adoption_counts_all_team_as_adopters_SIMPLER.csv"
  # filename_actual_evol=dir_real_data+"HospitalModel_august1_adoption_counts_SIMPLER.csv"

 
   list_actual_evol=[]
   result_actual_file= csv.reader(open(filename_actual_evol, 'rb'), delimiter=',')
   cont=0
   for row in result_actual_file: 
       if cont>0:   # i ignore the first line with the headers                         
           num_adopters= row[3]                    
           list_actual_evol.append(float(num_adopters))

       cont+=1    
  





#################################################################################################################
#  I read all the files for the diff. values of the parameters for the simulations of the persuation process : ##
#################################################################################################################


   dict_filenames_tot_distance={}   # i will save the filename as key and the tot distance from that curve to the original one

  


   prob_min=0.0
   prob_max=0.99
   delta_prob=0.01
   
   

   prob_Immune_min=0.0
   prob_Immune_max=0.99
   delta_prob_Immune=0.01
   




   prob_Immune=prob_Immune_min
   while prob_Immune<= prob_Immune_max:
                    
      print "prob_Immune:",prob_Immune

      prob_infection=prob_min
      while prob_infection<= prob_max:
         print "prob:",prob_Immune
          
                
         try:
                   #  Average_time_evolution_Infection_p0.0_Immune0.95_30iter_2012.dat
            filename=dir_simus_data+"Average_time_evolution_Infection_p"+str(prob_infection)+"_Immune"+str(prob_Immune)+"_"+str(Niter)+"iter_2012.dat"

            print filename,

            list_evol_one_simu=[]
            result_att_fellows= csv.reader(open(filename, 'rb'), delimiter=' ')
            for row in result_att_fellows:                    
                num_adopters=row[1]               
                list_evol_one_simu.append(float(num_adopters))

            if  len(list_evol_one_simu)>0:
            
               dict_filenames_tot_distance[filename]=compare_two_curves(list_actual_evol,list_evol_one_simu)
          
          
               print dict_filenames_tot_distance[filename]
            #raw_input()

               print >> file3, prob_infection,prob_Immune,dict_filenames_tot_distance[filename]
          
            else:
               print "THE FILE IS EMPTY"   


         except IOError:  print dir_simus_data+"Average_time_evolution_Infection_p"+str(prob_infection)+"_Immune"+str(prob_Immune)+"_"+str(Niter)+"iter_2012.dat   NOT FOUND"   # if that particular file doesnt exist


         prob_infection += delta_prob     
      prob_Immune += delta_prob_Immune
   




   file3.close()


#########


   minimum_value=1000000.
   for clave in dict_filenames_tot_distance:    
      if float(dict_filenames_tot_distance[clave]) < minimum_value:
           minimum_value= dict_filenames_tot_distance[clave]
           minimum_filename=clave

     # el diccionario dict_filenames_tot_distance   es: clave=path/filename  dict_filenames_tot_distance[clave] =[distancia,std_distancia]




   

   list_sorted_dict_filenames_tot_distance = sorted(dict_filenames_tot_distance.iteritems(), key=operator.itemgetter(1))
   
   for item in list_sorted_dict_filenames_tot_distance:       
       print >> file,item[0],item[1]
       print  item[0],item[1]

   file.close()

# ojo!!!! when i sort the dict, what it get is a LIST of TUPLES, and each tuple (item) is ('/path/filename',[distancia, std_distancia])


# print  "the minimun value",minimum_value, " is for:", minimum_filename 

#####################################################################

def compare_two_curves(list_actual_evol,list_evol_one_simu):
  
   if len(list_evol_one_simu)==0 or len(list_actual_evol) ==0:

      print "empty list for the comparison!!"
      raw_input()
   
   list_dist=[]
   for i in range(len(list_evol_one_simu)):   # i calculate the sum of distances from one curve to another at each same time step
      list_dist.append((list_evol_one_simu[i]-list_actual_evol[i])*(list_evol_one_simu[i]-list_actual_evol[i]))
               # print i, list_evol_one_simu[i][1],list_actual_evol[i][1],list_evol_one_simu[i][1]-list_actual_evol[i][1], dist
      mean_dist=numpy.mean(list_dist)
     
      
   return   mean_dist
         



  
##################################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
    main()
    #else:
     #   print "Usage: python script.py path/network.gml"

    
