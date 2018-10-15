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


def main(graph_name):
 



   G = nx.read_gml(graph_name)




   Niter=10000



   prob_min=0.21
   prob_max=0.22
   delta_prob=0.1
   
   

   prob_Immune_min=0.14
   prob_Immune_max=0.15
   delta_prob_Immune=0.1
   





   dir="../Results/network_final_schedule_withTeam3/infection/"   



   prob_Immune=prob_Immune_min
   while prob_Immune<= prob_Immune_max:
        
      print "prom Immune:",prob_Immune        

      prob_infection=prob_min
      while prob_infection<= prob_max:
                 
        print "  p:",prob_infection        


        output_file2=dir+"Average_time_evolution_Infection_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter)+"iter_2012.dat"
        file2 = open(output_file2,'wt')                                       
        file2.close()
        


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


            #######OJO~!!!!!!!!!! COMENTAR ESTO CUANDO ESTOY BARRIENDO TOOOOOOOOOODO EL ESPACIO DE PARAMETROS
          #  file_name_indiv_evol=output_file2.strip("Average_").split('.dat')[0]+"_indiv_iter"+str(iter)+".dat"
           
          #  file3 = open(file_name_indiv_evol,'wt')       
          #  file3.close()
              ##########################################





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
                    if G.node[n]['label']!="Wunderink"  and G.node[n]["label"]!="Weiss": 
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
   



 ########OJO~!!!!!!!!!! COMENTAR ESTO CUANDO ESTOY BARRIENDO TOOOOOOOOOODO EL ESPACIO DE PARAMETROS
           # file3 = open(file_name_indiv_evol,'at')                
          #  for i in range(len(list_single_t_evolution)):  #ime step by time step                                              
             #  print >> file3, i,list_single_t_evolution[i], prob_infection, prob_Immune 
           # file3.close()
              ########################################################



                       
            list_lists_t_evolutions.append(list_single_t_evolution)
           # print "len(list_single_t_evolution)",len(list_single_t_evolution)

      

        file2 = open(output_file2,'at')        
        for s in range(len(list_single_t_evolution)):           
            list_fixed_t=[]
            for iter in range (Niter):
                list_fixed_t.append(list_lists_t_evolutions[iter][s])        
            print >> file2, s,numpy.mean(list_fixed_t)                    
        file2.close()



       # file = open(output_file,'at')   
        #print >> file,  prob_infection, numpy.mean(list_final_I_values_fixed_p)
        #file.close()




        prob_infection+= delta_prob
      prob_Immune+= delta_prob_Immune


######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
   
        main(graph_filename)
    else:
        print "Usage: python script.py path/network.gml"

    
