#!/usr/bin/env python

'''
Given a .gml network, it simulates a disease-spreading-like process
in the bipartite network (doctors and shifts)

Created by Julia Poncela, on August 2011.

'''

import csv
import sys
import os
import networkx as nx
import numpy
import histograma_gral
import histograma_gral_negv_posit_return_list_freq
import random
import scipy
from  scipy import stats


def main(graph_name):
 



   G = nx.read_gml(graph_name)

   maximo=7   # for the distribution of deltaYs of a 5day time window
   minimo=-2

 
######################################################################################
#  I read the file of the actual evolution of the idea spreading in the hospital:   ##
######################################################################################


   dir_real_data='../Results/'


# filename_actual_evol=dir_real_data+"HospitalModel_august1_adoption_counts_all_team_as_adopters_SIMPLER.csv"
   filename_actual_evol=dir_real_data+"HospitalModel_august1_adoption_counts_SIMPLER.csv"

 
  
  
   list_actual_evol=[]
   result_actual_file= csv.reader(open(filename_actual_evol, 'rb'), delimiter=',')
   cont=0
   for row in result_actual_file: 
       if cont>0:   # i ignore the first line with the headers
           
           list_time_step_actual_evol=[]
           time=row[0]       
           num_adopters= row[3]
           list_time_step_actual_evol.append(int(time))
           list_time_step_actual_evol.append(float(num_adopters))
          
           list_actual_evol.append(list_time_step_actual_evol)

       cont+=1    
  



   delta_days=5   # for the histogram of Ydelta over that period of time
   list_actual_5day_Ydeltas=[]
   for i in range(len(list_actual_evol)):      
      try:  # because at the end of the time evol i cant calculate 5day interv.
         list_actual_5day_Ydeltas.append(list_actual_evol[i+delta_days][1]-list_actual_evol[i][1])
      except IndexError: pass

   
  

  

  

    ###########################




   Niter=10000

#../Results/network_final_schedule_withTeam3/infection/Average_time_evolution_Infection_p1.0_Immune0.5_1000iter_2012.dat

   prob_min=1.0
   prob_max=1.0
   delta_prob=0.01
   
   

   prob_Immune_min=0.5
   prob_Immune_max=0.51
   delta_prob_Immune=0.01
   





   dir="../Results/network_final_schedule_withTeam3_local/infection/"   


        

   prob_Immune=prob_Immune_min
   while prob_Immune<= prob_Immune_max:
        
      print "prom Immune:",prob_Immune        

      prob_infection=prob_min
      while prob_infection<= prob_max:
                 
        print "  p:",prob_infection        


        output_file2=dir+"Average_time_evolution_Infection_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter)+"iter_2012.dat"
        file2 = open(output_file2,'wt')                                       
        file2.close()
        



      #  list_final_I_values_fixed_p=[]  # i dont care about the final values right now, but about the whole time evol
        list_lists_t_evolutions=[]    
        list_simus_5day_Ydeltas=[]
        
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
   



                       
            list_lists_t_evolutions.append(list_single_t_evolution)
          
      
            for i in range(len(list_single_t_evolution)):
               try:  # because at the end of the time evol i cant calculate 5day interv.
                  list_simus_5day_Ydeltas.append(list_single_t_evolution[i+delta_days]-list_single_t_evolution[i])
               except: pass



        #################################end loop over Niter
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


        list_simu_freq, maximo, minimo=histograma_gral_negv_posit_return_list_freq.histograma(list_simus_5day_Ydeltas,dir_real_data+"Histogr_5day_deltaY_simus_infection_prob_infect_"+str(prob_infection)+"_Immune"+str(prob_Immune)+".dat",1,None, None)   # last parameter is a flag: =1, returns normalized values, =0, non normalized (just frequencies)

       

        list_actual_freq, maximo, minimo=histograma_gral_negv_posit_return_list_freq.histograma(list_actual_5day_Ydeltas,dir_real_data+"Histogr_5day_deltaY_actual_evol.dat",0, maximo, minimo)  # last parameters are a flag: =1, returns normalized values, =0, non normalized (just frequencies), maximo, minimo

        sum_actual_freq=sum(list_actual_freq)
        print list_actual_freq ,sum_actual_freq





        sum_simu_freq=sum(list_simu_freq)
       # print list_simu_freq ,sum_simu_freq

       

        for i in range(len(list_simu_freq)):
          # print list_simu_freq[i],
           list_simu_freq[i]=list_simu_freq[i]*sum_actual_freq
           #print list_simu_freq[i]

        print list_actual_freq
        print list_simu_freq


     
        flag_last=1   # i need to remove comon null final/initial entries among the two lists
        flag_first=1
        while flag_last==1 or flag_first==1:

           if (list_actual_freq[-1]==0 and list_simu_freq[-1]==0 ):
              list_actual_freq.pop(-1) # i remove the null entries at the end of both lists  (otherwise the chi test gives nan)
              list_simu_freq.pop(-1) 
           else :
              flag_last=0
              
           if (list_actual_freq[0]==0 and list_simu_freq[0]==0 ):
              list_actual_freq.pop(0) # i remove the null entries at the beginning of both lists  (otherwise the chi test gives nan)
              list_simu_freq.pop(0) 
           else :
              flag_first=0




                 # print list_simu_freq,list_actual_freq
           
        print list_simu_freq,sum(list_simu_freq),list_actual_freq,sum(list_actual_freq)
           








        print list_actual_freq
        print list_simu_freq
       
        print  "results chi-squre, p-value comparing actual vs infection:",stats.chisquare(scipy.array(list_actual_freq),scipy.array(list_simu_freq)), "  for:",Niter, "iterations"  # for this test, the length of the two list of frequencies MUST be the same





        prob_infection+= delta_prob
      prob_Immune+= delta_prob_Immune


######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
   
        main(graph_filename)
    else:
        print "Usage: python script.py path/network.gml"

    
