#!/usr/bin/env python

import csv
import numpy
import networkx as nx
import random
import compare_real_evol_vs_simus_to_be_called


def dynamics( parameters):

   prob_infection=parameters[0]
   prob_Immune=parameters[1]


   graph_name ="../Results/Doctors_shifts_network_withT3.gml"
   G = nx.read_gml(graph_name)

  

   Niter=10000



 # i get the list corresponding to the ACTUAL evolution
   dir_real_data='../Results/'


# filename_actual_evol=dir_real_data+"HospitalModel_august1_adoption_counts_all_team_as_adopters_SIMPLER.csv"
   filename_actual_evol=dir_real_data+"HospitalModel_august1_adoption_counts_SIMPLER.csv"

 
   list_actual_evol=[]
   result_actual_file= csv.reader(open(filename_actual_evol, 'rb'), delimiter=',')
   cont=0
   for row in result_actual_file: 
       if cont>0:   # i ignore the first line with the headers
           
           
           num_adopters= row[3]                        
           list_actual_evol.append(float(num_adopters))

       cont+=1    
    ##################3









   list_dist_fixed_parameters=[]  
   for i in range(Niter):

       
       list_I=[]  #list infected doctors
       list_ordering=[]
       list_s=[]
       list_A=[]
       list_F=[]




            ########### set I.C.

       max_order=0    # 243
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
               if G.node[n]['label']!="Wunderink"  and G.node[n]["label"]!="Weiss": 
                   rand=random.random()
                   if rand< prob_Immune:
                       G.node[n]["status"]="Immune"
                       
    
  
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
   
       ######## end loop time
      
       list_dist_fixed_parameters.append(compare_real_evol_vs_simus_to_be_called.compare_two_curves( list_actual_evol,list_single_t_evolution))


   ######## end Niter

   print  prob_infection, prob_Immune, " --> ",numpy.mean(list_dist_fixed_parameters), numpy.std(list_dist_fixed_parameters)
 
   
                       
   return(numpy.mean(list_dist_fixed_parameters))


###################################################
