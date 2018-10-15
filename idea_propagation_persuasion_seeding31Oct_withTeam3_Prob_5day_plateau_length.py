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
import itertools
import random
import histograma_gral
import histograma_gral_negv_posit_return_list_freq
import scipy
from  scipy import stats
import histograma_bines_gral


 ########OJO~!!!!!!!!!! COMENTAR LA ESCRITURA DE ARCHIVOS INDIVIDUALES (LINEA 149...)  ESTO CUANDO ESTOY BARRIENDO TOOOOOOOOOODO EL ESPACIO DE PARAMETROS





def main(graph_name):
 
   
   Niter=1000
   

   G = nx.read_gml(graph_name)

   maximo=100    # for the distribution of deltaYs of a 5day time window and plateau lengths
   minimo=-5
 
 
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
   list_actual_plateau_lengths=[]


   length=1
   for i in range(len(list_actual_evol)):
      
      try:  # because at the end of the time evol i cant calculate 5day interv.
         list_actual_5day_Ydeltas.append(list_actual_evol[i+delta_days][1]-list_actual_evol[i][1])
      except IndexError: pass
     
      if i>0:  # for the first enty, i dont have anything to compare to
         if previous_value==list_actual_evol[i][1]:
            length+=1
         else:
            list_actual_plateau_lengths.append(length)
            length=1


      previous_value=list_actual_evol[i][1]
  
  
#   ../Results/network_final_schedule_withTeam3/Time_evolutions_Persuasion_alpha0.2_damping0.0_mutual_encourg0.7_threshold0.4_unif_distr_50iter_2012_seed31Oct_finalnetwork.dat

  

   alpha_F_min=0.1   # alpha=0: nobody changes their mind
   alpha_F_max=0.11
   delta_alpha_F=0.1
   

   min_damping=0.30     #its harder to go back from YES to NO again. =1 means no effect, =0.5 half the movement from Y->N than the other way around, =0 never go back from Y to N
   max_damping=0.31
   delta_damping=0.1  
   
   
   min_mutual_encouragement=0.3  # when two Adopters meet, they convince each other even more
   max_mutual_encouragement=0.31
   delta_mutual_encouragement=0.1
   
   
   threshold_min=0.2  # larger than, to be an Adopte
   threshold_max=0.21
   delta_threshold=0.1


   
   print "\n\nPersuasion process on network, with Niter:",Niter
   
   
   

   threshold=threshold_min
   while   threshold<= threshold_max:
      print   "thershold:",threshold

      alpha_F=alpha_F_min
      while alpha_F<= alpha_F_max:            # i explore all the parameter space, and create a file per each set of values
        alpha_A=0.5*alpha_F
        print "  alpha_F:",alpha_F

        mutual_encouragement=min_mutual_encouragement  
        while  mutual_encouragement <= max_mutual_encouragement:
          print "    mutual_encouragement:",mutual_encouragement

          damping=min_damping
          while   damping <= max_damping:
            print "      damping:",damping


          
    
            dir="../Results/network_final_schedule_withTeam3_local/"  
            output_file=dir+"Time_evolutions_Persuasion_alpha"+str(alpha_F)+"_damping"+str(damping)+"_mutual_encourg"+str(mutual_encouragement)+"_threshold"+str(threshold)+"_unif_distr_"+str(Niter)+"iter_2012_seed31Oct_finalnetwork.dat"        
            file = open(output_file,'wt')    
            file.close()
            


            time_evol_number_adopters_ITER=[]  # list of complete single realizations of the dynamics
            list_simus_5day_Ydeltas=[]
            list_simus_plateau_lengths=[]


            for iter in range(Niter):
                print "         ",iter
                list_t=[]
           
                time_evol_number_adopters=[]   # for a single realization of the dynamics


                num_adopters , seed_shift ,max_shift= set_ic(G,threshold)   # i establish who is Adopter and NonAdopter initially, and count how many shifts i have total

                time_evol_number_adopters.append(float(num_adopters))
#                print "initial number of adopters:", num_adopters
                list_t.append(0)




               ########OJO~!!!!!!!!!! COMENTAR ESTO CUANDO ESTOY BARRIENDO TOOOOOOOOOODO EL ESPACIO DE PARAMETROS
               # file2 = open(output_file.split('.dat')[0]+"_indiv_iter"+str(iter)+".dat",'wt')       
                #file2.close()
              ##########################################



                
               # the dynamics starts:                 
                t=int(seed_shift)+1   # the first time step is just IC.???


                while t<= max_shift:  # loop over shifts, in chronological order  (the order is the day index since seeding_day) 
                         
                    list_t.append(t)
                    for n in G.nodes():
                        if G.node[n]['type']=="shift" and G.node[n]['order']==t:  # i look for the shift corresponding to that time step                    
                            flag_possible_persuasion=0
                            for doctor in G.neighbors(n):                               
                                if G.node[doctor]["status"]=="Adopter":   #first i check if any doctor is an adopter in this shift         
                                    flag_possible_persuasion=1                               
                                    break

                            if flag_possible_persuasion==1:
                                list_doctors=[]
                                for doctor in G.neighbors(n):   # for all drs in that shift
                                    list_doctors.append(doctor)
                                
                                
                                pairs=itertools.combinations(list_doctors,2)    # cos the shift can be 2 but also 3 doctors 
                                for pair in pairs:
                                    doctor1=pair[0]
                                    doctor2=pair[1]
                                                                                        
                                    if G.node[doctor1]['status'] != G.node[doctor2]['status']:  # if they think differently, 
                                                                                              # there will be persuasion
                                        persuasion(G,damping,doctor1,doctor2,alpha_A,alpha_F,threshold)   # i move their values of opinion                  
                                        update_opinions(G,threshold,doctor1,doctor2) #  i update status and make sure the values of the vectors stay between [0,1] 
                                  
                                    else:  # if two Adopters meet, they encourage each other (if two NonAdopters, nothing happens)
                                   
                                       mutual_reinforcement(G,mutual_encouragement,doctor1,doctor2)
                                  
                               
                                    
                    list_Adopters=[]        #count how many i have at this time       
                    for n in G.nodes():              
                        try:
                            if  G.node[n]["status"]=="Adopter":                     
                                if G.node[n]["label"] not in list_Adopters:
                                    list_Adopters.append(G.node[n]["label"])
                        except: pass  # if the node is a shift, it doesnt have a 'status' attribute


        
                   


                    time_evol_number_adopters.append(float(len(list_Adopters)))

               






                    t+=1
   

                ###################### end while loop over t
               

               


                ########OJO~!!!!!!!!!! COMENTAR ESTO CUANDO ESTOY BARRIENDO TOOOOOOOOOODO EL ESPACIO DE PARAMETROS
                #file2 = open(output_file.split('.dat')[0]+"_indiv_iter"+str(iter)+".dat",'at')                
                #for i in range(len(time_evol_number_adopters)):  #ime step by time step                                              
                #print >> file2, i,time_evol_number_adopters[i], alpha_F,damping,mutual_encouragement 
                #file.close()
                ########################################################




               

                time_evol_number_adopters_ITER.append(time_evol_number_adopters)

                length=1
                for i in range(len(time_evol_number_adopters)):
                   try:  # because at the end of the time evol i cant calculate 5day interv.
                      list_simus_5day_Ydeltas.append(time_evol_number_adopters[i+delta_days]-time_evol_number_adopters[i])
                   except: pass

                   if i>0:  # for the first enty, i dont have anything to compare to
                      if previous_value==time_evol_number_adopters[i]:
                         length+=1
                      else:
                         list_simus_plateau_lengths.append(length)
                         length=1

                   previous_value=time_evol_number_adopters[i]
  







            #################################end loop over Niter
            file = open(output_file,'wt')        
            for i in range(len(time_evol_number_adopters)):  #time step by time step
                list_fixed_t=[]
                for iteracion in range (Niter): #loop over all independent iter of the process
                    list_fixed_t.append(time_evol_number_adopters_ITER[iteracion][i])  # i collect all values for the same t, different iter  

                print >> file, list_t[i],numpy.mean(list_fixed_t),numpy.std(list_fixed_t), alpha_F,damping,mutual_encouragement       
            file.close()


      

          
         
         ### i calculate histograms for deltaY in a 5day window:  (actual and simus) ##

            list_simu_freq_5day, maximo, minimo=histograma_gral_negv_posit_return_list_freq.histograma(list_simus_5day_Ydeltas,dir_real_data+"Histogr_5day_deltaY_simus_persuasion_alpha"+str(alpha_F)+"_damping"+str(damping)+"_mutual_encourg"+str(mutual_encouragement)+"_threshold"+str(threshold)+".dat",1,None,None)#maximo, minimo)  # last parameter is a flag: =1, returns normalized values, =0, non normalized (just frequencies)

            list_actual_freq_5day, maximo, minimo=histograma_gral_negv_posit_return_list_freq.histograma(list_actual_5day_Ydeltas,dir_real_data+"Histogr_5day_deltaY_actual_evol.dat",1, maximo, minimo)  # last parameters are a flag: =1, returns normalized values, =0, non normalized (just frequencies), maximo, minimo




            sum_actual_freq_5day=sum(list_actual_freq_5day)
           # print list_actual_freq ,sum_actual_freq


            sum_simu_freq_5day=sum(list_simu_freq_5day)
       # print list_simu_freq ,sum_simu_freq

       

            for i in range(len(list_simu_freq_5day)):         
               list_simu_freq_5day[i]=list_simu_freq_5day[i]*sum_actual_freq_5day
          



            flag_last=1   # i need to remove comon null final/initial entries among the two lists
            flag_first=1
            while flag_last==1 or flag_first==1:

               if (list_actual_freq_5day[-1]==0 and list_simu_freq_5day[-1]==0 ):
                  list_actual_freq_5day.pop(-1) # i remove the null entries at the end of both lists  (otherwise the chi test gives nan)
                  list_simu_freq_5day.pop(-1) 
               else :
                  flag_last=0

               if (list_actual_freq_5day[0]==0 and list_simu_freq_5day[0]==0 ):
                  list_actual_freq_5day.pop(0) # i remove the null entries at the beginning of both lists  (otherwise the chi test gives nan)
                  list_simu_freq_5day.pop(0) 
               else :
                  flag_first=0




                 # print list_simu_freq,list_actual_freq
           
         #   print "done!",list_simu_freq_5day,sum(list_simu_freq_5day),list_actual_freq_5day,sum(list_actual_freq_5day)
           
           

            print list_actual_freq_5day
            print list_simu_freq_5day

            print  "results chi-squre, p-value comparing deltaY-5day windows actual vs persuasion:",stats.chisquare(scipy.array(list_actual_freq_5day),scipy.array(list_simu_freq_5day)), "  for:",Niter, "iterations \n\n\n"


            ###################################    


            maximo=200    # for the distribution of deltaYs of a 5day time window and plateau lengths
            minimo=-5
   


           ### i calculate histograms for plateau lengths:  (actual and simus) ##       
     
        

            list_simu_freq, maximo, minimo=histograma_gral_negv_posit_return_list_freq.histograma(list_simus_plateau_lengths,dir_real_data+"Histogr_plateau_length_simus_persuasion_alpha"+str(alpha_F)+"_damping"+str(damping)+"_mutual_encourg"+str(mutual_encouragement)+"_threshold"+str(threshold)+".dat",1,None,None)#maximo, minimo)  # last parameter is a flag: =1, returns normalized values, =0, non normalized (just frequencies)


            maximo=200    # for the distribution of deltaYs of a 5day time window and plateau lengths
            minimo=-5
   

       
            list_simu_freq = histograma_bines_gral.histograma_bins_return_only_freq(list_simus_plateau_lengths,15,dir_real_data+"Histogr_plateau_length_simus_persuasion_alpha"+str(alpha_F)+"_damping"+str(damping)+"_mutual_encourg"+str(mutual_encouragement)+"_threshold"+str(threshold)+"_bins.dat")
            
            maximo=200
            minimo=-5


            list_actual_freq = histograma_bines_gral.histograma_bins_return_only_freq(list_actual_plateau_lengths,15,dir_real_data+"Histogr_plateau_length_actual_evol_bins.dat")





# KS test for the cumulative distributions of plateau lengths

       
            aux,list_simu_freq_cumulat=histograma_bines_gral.histograma_bins_return_prob_and_cumul(list_simus_plateau_lengths,15,dir_real_data+"Histogr_plateau_length_simus_persuasion_alpha"+str(alpha_F)+"_damping"+str(damping)+"_mutual_encourg"+str(mutual_encouragement)+"_threshold"+str(threshold)+"_cumulat_bins.dat")

            list_cumulat_prob_simu=[]
            for item in list_simu_freq_cumulat:
                list_cumulat_prob_simu.append(item[1])


            aux,list_actual_freq_cumulat=histograma_bines_gral.histograma_bins_return_prob_and_cumul(list_actual_plateau_lengths,15,dir_real_data+"Histogr_plateau_length_actual_cumulat_bins.dat")



            list_cumulat_prob_actual=[]
            for item in list_actual_freq_cumulat:
                list_cumulat_prob_actual.append(item[1])





            sum_actual_freq=sum(list_actual_freq)
           # print list_actual_freq ,sum_actual_freq


            sum_simu_freq=sum(list_simu_freq)
       # print list_simu_freq ,sum_simu_freq

       

            for i in range(len(list_simu_freq)):         
               list_simu_freq[i]=list_simu_freq[i]*sum_actual_freq
        



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
           
          #  print "done!",list_simu_freq,sum(list_simu_freq),list_actual_freq,sum(list_actual_freq)
           

            print  list_simu_freq, len(list_simu_freq)
            print list_actual_freq, len(list_actual_freq)

            for i in range(len(list_simu_freq)):
               if list_simu_freq[i]==0 and list_actual_freq[i]==0:
                  print "element", i, "of both lists is null!!"
                 #raw_input()
       

          #  print  "results chi-squre, p-value comparing  plateau-lengths actual vs persuasion:",stats.chisquare(scipy.array(list_actual_freq),scipy.array(list_simu_freq)), "  for:",Niter, "iterations"

         


            print "KS test actual vs persuasion", scipy.stats.ks_2samp(list_actual_plateau_lengths,list_simus_plateau_lengths)


            print list_cumulat_prob_actual
            print list_cumulat_prob_simu
            print "KS test actual vs persuasion  (for cumulative distrib)", scipy.stats.ks_2samp(list_cumulat_prob_actual,list_cumulat_prob_simu)



   ###################################          






          
            damping += delta_damping
          mutual_encouragement += delta_mutual_encouragement
        alpha_F += delta_alpha_F
      threshold  += delta_threshold
    






###############################################
#############################################################3

def set_ic(G,threshold):

        list_s=[]
        list_A=[]
        list_F=[]
      
        num_shifts=0
        for n in G.nodes():              
            if G.node[n]['type']=="shift":
                num_shifts+=1
                if  G.node[n]['order'] not in list_s:
                    list_s.append(G.node[n]['order'])                        
                if "2011/10/31" in G.node[n]['label']: # actual seeding date                                     
                    seed_shift=G.node[n]['order']
                    seed=n   

            elif G.node[n]['type']=="A":
                if n not in list_A:
                    list_A.append(n)
                    G.node[n]["adoption_vector"]=random.random()*threshold  #values from [0,0.75)
                    G.node[n]["status"]="NonAdopter"  # initially non-Adopters
                    
            elif G.node[n]['type']=="F":
                if n not in list_F:
                    list_F.append(n)
                    G.node[n]["adoption_vector"]=random.random()*threshold
                    G.node[n]["status"]="NonAdopter"  
                   
    
        max_shift=max(list_s)
       
         
           
        list_Adopters=[]                 
        
        for doctor in G.nodes():    #         (SOLO WUNDERINK & WEISS SON ADOPTERS  SEGUROS AL PRINCIPIO...)
           
           if G.node[doctor]["label"]=="Wunderink"  or G.node[doctor]["label"]=="Weiss":  # for sure, only those two, then Sporn and Smith were told...   or G.node[doctor]["label"]=="Sporn"    or G.node[doctor]["label"]=="Smith"
              G.node[doctor]["status"]="Adopter"  
              G.node[doctor]["adoption_vector"]=1.0
              if G.node[doctor]["label"] not in list_Adopters:
                 list_Adopters.append(G.node[doctor]["label"])

           
       
        return float(len(list_Adopters)),seed_shift,max_shift

###########################################

def persuasion(G,damping,doctor1,doctor2,alpha_A,alpha_F,threshold):

    if G.node[doctor1]["adoption_vector"]>=threshold or G.node[doctor2]["adoption_vector"]>=threshold :  # only if at least one doctor is Adopter

        
        if (G.node[doctor1]['type']=="A") and (G.node[doctor2]['type']=="F"):
            delta_AF=G.node[doctor1]["adoption_vector"]-G.node[doctor2]["adoption_vector"]
            
            if float(delta_AF)>=0.0:
                G.node[doctor1]["adoption_vector"]=G.node[doctor1]["adoption_vector"]-delta_AF*alpha_A*damping  #from YES to NO
                G.node[doctor2]["adoption_vector"]=G.node[doctor2]["adoption_vector"]+delta_AF*alpha_F  #from NO to YES
            else:
                G.node[doctor1]["adoption_vector"]=G.node[doctor1]["adoption_vector"]-delta_AF*alpha_A
                G.node[doctor2]["adoption_vector"]=G.node[doctor2]["adoption_vector"]+delta_AF*alpha_F*damping
                
        elif (G.node[doctor1]['type']=="F") and (G.node[doctor2]['type']=="A"):
            delta_FA=G.node[doctor1]["adoption_vector"]-G.node[doctor2]["adoption_vector"]
            
            if float(delta_FA)>=0.0:
                G.node[doctor1]["adoption_vector"]=G.node[doctor1]["adoption_vector"]-delta_FA*alpha_F*damping
                G.node[doctor2]["adoption_vector"]=G.node[doctor2]["adoption_vector"]+delta_FA*alpha_A
            else:
                G.node[doctor1]["adoption_vector"]=G.node[doctor1]["adoption_vector"]-delta_FA*alpha_F
                G.node[doctor2]["adoption_vector"]=G.node[doctor2]["adoption_vector"]+delta_FA*alpha_A*damping
                
                
        elif  (G.node[doctor1]['type']=="F") and (G.node[doctor2]['type']=="F"):
            delta_FF=G.node[doctor1]["adoption_vector"]-G.node[doctor2]["adoption_vector"]
            if float(delta_FF)>=0.0:
                G.node[doctor1]["adoption_vector"]=G.node[doctor1]["adoption_vector"]-delta_FF*alpha_F*damping
                G.node[doctor2]["adoption_vector"]=G.node[doctor2]["adoption_vector"]+delta_FF*alpha_F
            else:
                G.node[doctor1]["adoption_vector"]=G.node[doctor1]["adoption_vector"]-delta_FF*alpha_F
                G.node[doctor2]["adoption_vector"]=G.node[doctor2]["adoption_vector"]+delta_FF*alpha_F*damping
                
                
        elif  (G.node[doctor1]['type']=="A") and (G.node[doctor2]['type']=="A"):
            delta_AA=G.node[doctor1]["adoption_vector"]-G.node[doctor2]["adoption_vector"]
            if float(delta_AA)>=0.0:
                G.node[doctor1]["adoption_vector"]=G.node[doctor1]["adoption_vector"]-delta_AA*alpha_A*damping
                G.node[doctor2]["adoption_vector"]=G.node[doctor2]["adoption_vector"]+delta_AA*alpha_A
            else:
                G.node[doctor1]["adoption_vector"]=G.node[doctor1]["adoption_vector"]-delta_AA*alpha_A
                G.node[doctor2]["adoption_vector"]=G.node[doctor2]["adoption_vector"]+delta_AA*alpha_A*damping
                

            

#####################################



def update_opinions(G,threshold,doctor1,doctor2):

    if float(G.node[doctor1]["adoption_vector"])>=threshold: 
        G.node[doctor1]['status']="Adopter"               
        if  float(G.node[doctor1]["adoption_vector"])>1.0:   # i make sure the values of the vectors stay between [0,1]    
            G.node[doctor1]["adoption_vector"]=1.0  
    else:                                       
        
        G.node[doctor1]['status']="NonAdopter"                                   
        if float(G.node[doctor1]["adoption_vector"])<0.0:    # i make sure the values of the vectors stay between [0,1]     
            G.node[doctor1]["adoption_vector"]=0.0
            
                
                                
    if float(G.node[doctor2]["adoption_vector"])>=threshold:
        G.node[doctor2]['status']="Adopter"                            
        if  float(G.node[doctor2]["adoption_vector"])>1.0:                                            
            G.node[doctor2]["adoption_vector"]=1.0
                        
    else:                                       
        G.node[doctor2]['status']="NonAdopter"
        if float(G.node[doctor2]["adoption_vector"])<0.0:                                          
            G.node[doctor2]["adoption_vector"]=0.0
            

########################################################



def mutual_reinforcement(G,mutual_encouragement,doctor1,doctor2):


    if G.node[doctor1]['status'] =='Adopter'  and G.node[doctor2]['status']=='Adopter':
        G.node[doctor1]["adoption_vector"]=G.node[doctor1]["adoption_vector"]+mutual_encouragement
        G.node[doctor2]["adoption_vector"]=G.node[doctor2]["adoption_vector"]+mutual_encouragement

        if  float(G.node[doctor1]["adoption_vector"])>1.0:                                             
            G.node[doctor1]["adoption_vector"]=1.0  
        if  float(G.node[doctor2]["adoption_vector"])>1.0:                                             
            G.node[doctor2]["adoption_vector"]=1.0  
                




##################################################
######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
   
        main(graph_filename)
    else:
        print "Usage: python script.py path/network.gml"

    
