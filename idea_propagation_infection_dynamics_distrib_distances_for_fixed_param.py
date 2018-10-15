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
import histograma_bines_gral
import calculate_numeric_integral

def main(graph_name):
 



   G = nx.read_gml(graph_name)



   prob_infection=0.9
   prob_Immune=0.5
  
   Niter=100000




   dir_real_data='../Results/'

   all_team="NO"   # as adopters or not



######################################################################################
#  I read the file of the actual evolution of the idea spreading in the hospital:   ##
######################################################################################



   if all_team=="YES":    
      filename_actual_evol=dir_real_data+"HospitalModel_august1_adoption_counts_all_team_as_adopters_SIMPLER.csv"

   else:
      filename_actual_evol=dir_real_data+"HospitalModel_august1_adoption_counts_SIMPLER.csv"
   #ya no necesito CAMBIAR TB EL NOMBRE DEL ARCHIVO EN EL CODIGO PARA COMPARAR CURVAs

  
   list_actual_evol=[]
   result_actual_file= csv.reader(open(filename_actual_evol, 'rb'), delimiter=',')
   cont=0
   for row in result_actual_file: 
       if cont>0:   # i ignore the first line with the headers
           
           
           num_adopters= row[3]
          
           list_actual_evol.append(float(num_adopters))
          
          

       cont+=1    
  

##################################################################










  
# i create the empty list of list for the Niter temporal evolutions
   num_shifts=0
   for n in G.nodes():
      G.node[n]["status"]="S" 
      if G.node[n]['type']=="shift":
         num_shifts+=1
          

      #  list_final_I_values_fixed_p=[]  # i dont care about the final values right now, but about the whole time evol
   list_lists_t_evolutions=[]    

      
   
   for iter in range(Niter):
            
            print "     iter:",iter


            list_I=[]  #list infected doctors
            list_ordering=[]
            list_s=[]
            list_A=[]
            list_F=[]


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
          



                        ######################## WHAT ABOUT SMITH AND SPORN???



                    if G.node[n]['type']=="A":
                        list_A.append(n)
                    
                    if G.node[n]['type']=="F":
                        list_F.append(n)
                

            
           
            list_single_t_evolution=[]
            list_single_t_evolution.append(2.0)  # I always start with TWO infected doctors!!


            for n in G.nodes():   # i make some DOCTORs INMUNE  (anyone except Weiss and Wunderink)
                if (G.node[n]['type']=="A") or ( G.node[n]['type']=="F"):
                    if G.node[n]['label']!="Wunderink"  and G.node[n]["label"]!="Weiss": # these particular two cant be immune
                        rand=random.random()
                        if rand< prob_Immune:
                            G.node[n]["status"]="Immune"



         #   print max_order
  
            ################# the dynamics starts: 
           
            t=1
            while t<= max_order:  # loop over shifts, in order           
                for n in G.nodes():
                    if G.node[n]['type']=="shift" and G.node[n]['order']==t:
                        flag_possible_infection=0
                        for doctor in G.neighbors(n): #first i check if any doctor is infected in this shift
                            if G.node[doctor]["status"]=="I":
                                flag_possible_infection=1
                                

                        if flag_possible_infection:
                            for doctor in G.neighbors(n): # then the doctors in that shift, gets infected with prob_infection
                                if G.node[doctor]["status"]=="S":
                                    rand=random.random()
                                    if rand<prob_infection:
                                        G.node[doctor]["status"]="I"
                                        list_I.append(G.node[doctor]["label"])
                                           

                list_single_t_evolution.append(float(len(list_I)))#/(len(list_A)+len(list_F)))
  

                t+=1
   
                      
            list_lists_t_evolutions.append(list_single_t_evolution)
         

           

    ######## end Niter



   ##############end loop Niter

   average_t_evolution=[]
   for i in range(len(list_single_t_evolution)):  #time step by time step
      list_fixed_t=[]
      for iteracion in range (Niter): #loop over all independent iter of the process
         list_fixed_t.append(list_lists_t_evolutions[iteracion][i])  # i collect all values for the same t, different iter  
         
      average_t_evolution.append(numpy.mean(list_fixed_t))   # i create the mean time evolution      





   list_dist_fixed_parameters=[]
   for lista in list_lists_t_evolutions:
      list_dist_fixed_parameters.append(compare_real_evol_vs_simus_to_be_called.compare_two_curves( lista,average_t_evolution))


               
 


      
   lista_tuplas=histograma_bines_gral.histograma_bins(list_dist_fixed_parameters,75, "../Results/histogr_distances_indiv_infect_simus_to_the_average_curve_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter)+"iter_2012.dat") # Nbins=50

   #print lista_tuplas


   starting_point=compare_real_evol_vs_simus_to_be_called.compare_two_curves( list_actual_evol,average_t_evolution)   # distance between actual curve and the mean curve


   prob=calculate_numeric_integral.integral(lista_tuplas, starting_point)

   print "the probability of having a  distance equal or larger than",starting_point, "between actual-average curve is:", prob, "(it is to say, the prob. of the actual evolution being an individual realization of the Infection Model)"
  
  
   if all_team=="YES":    
      file = open("../Results/distance_actual_to_average_curve_infection_all_team_as_adopters.dat",'wt')  
   else: 
      file = open("../Results/distance_actual_to_average_curve_infection.dat",'wt')  

   print >> file,starting_point, 0.
   print >> file,starting_point+0.1, 1.        
   file.close()






   if all_team=="YES":    
      file2 = open("../Results/Results_distance_actual_to_average_curve_infection_all_team_as_adopters.dat",'wt')       

   else: 
      file2 = open("../Results/Results_distance_actual_to_average_curve_infection.dat",'wt')  


   print >> file2, "the probability of having a  distance equal or larger than",starting_point, "between actual-average curve is:", prob, "(it is to say, the prob. of the actual evolution being an individual realization of the Infection Model)"


   file2.close()


######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
   
        main(graph_filename)
    else:
        print "Usage: python script.py path/network.gml"

    
