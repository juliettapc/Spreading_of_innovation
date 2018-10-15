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
import itertools
import random
import csv
import compare_real_evol_vs_simus_to_be_called
import histograma_gral_negv_posit
import operator




 ########OJO~!!!!!!!!!! COMENTAR LA ESCRITURA DE ARCHIVOS INDIVIDUALES (LINEA 149...)  ESTO CUANDO ESTOY BARRIENDO TOOOOOOOOOODO EL ESPACIO DE PARAMETROS





def main(graph_name):
 

   G = nx.read_gml(graph_name)
 


   cutting_day=125  # to separate   training-testing

   Niter_training=100
   Niter_testing= 100





   delta_end=3  # >= than + or -  dr difference at the end of the evolution

   dir_real_data='../Results/'



   all_team="NO"   # as adopters or not




  # output_file3=dir_real_data+"Landscape_parameters_persuasion_"+str(Niter)+"iter.dat" 
   #file3 = open(output_file3,'wt')        



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
  

   list_actual_evol_training=list_actual_evol[:cutting_day]
   list_actual_evol_testing=list_actual_evol[(cutting_day-1):]


##################################################################


#../Results/network_final_schedule_withTeam3/Time_evolutions_Persuasion_alpha0.2_damping0.0_mutual_encourg0.7_threshold0.4_unif_distr_50iter_2012_seed31Oct_finalnetwork.dat


   alpha_F_min=0.0   # alpha=0: nobody changes their mind
   alpha_F_max=1.001
   delta_alpha_F=0.1
   

   min_damping=0.0     #its harder to go back from YES to NO again. =1 means no effect, =0.5 half the movement from Y->N than the other way around, =0 never go back from Y to N
   max_damping=1.01
   delta_damping=0.1
   
   
   min_mutual_encouragement=0.0  # when two Adopters meet, they convince each other even more
   max_mutual_encouragement=1.01
   delta_mutual_encouragement=0.1
   
  
   
   
   print "\n\nPersuasion process on network, with Niter:",Niter_training
   
   
   dict_filenames_tot_distance={}   # i will save the filename as key and the tot distance from that curve to the original one


   dict_filenames_list_dict_network_states={} 

  

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
            output_file=dir+"Time_evolutions_Persuasion_training_alpha"+str(alpha_F)+"_damping"+str(damping)+"_mutual_encourg"+str(mutual_encouragement)+"_"+str(Niter_training)+"iter_distributed_thresholds.dat"        
            file = open(output_file,'wt')    
            file.close()
            


            time_evol_number_adopters_ITER=[]  # list of complete single realizations of the dynamics
            list_dist_fixed_parameters=[]           
            list_dist_abs_at_ending_point_fixed_parameters=[]

            list_dict_network_states=[]
            list_networks_at_cutting_day=[]



            for iter in range(Niter_training):

                print "         ",iter
                list_t=[]
           
                time_evol_number_adopters=[]   # for a single realization of the dynamics

                dict_network_states={}

               
                num_adopters , seed_shift ,max_shift= set_ic(G)   # i establish who is Adopter and NonAdopter initially, and count how many shifts i have total
                

                time_evol_number_adopters.append(float(num_adopters))               
                list_t.append(0)



                
               ########### the dynamics starts:                 
                t=int(seed_shift)+1   # the first time step is just IC.???


                while t< cutting_day:  # loop over shifts, in chronological order  (the order is the day index since seeding_day) 
                         
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
                                        persuasion(G,damping,doctor1,doctor2,alpha_A,alpha_F)   # i move their values of opinion                  
                                        update_opinions(G,doctor1,doctor2) #  i update status and make sure the values of the vectors stay between [0,1] 
                                  
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
   

                ############## end while loop over t
               


                for n in G.nodes():            
                   if   G.node[n]['type']!="shift":                  
                      dict_network_states[G.node[n]["label"]]=G.node[n]["status"]

          
                list_dict_network_states.append(dict_network_states)

                time_evol_number_adopters_ITER.append(time_evol_number_adopters)


   
               
                list_dist_fixed_parameters.append(compare_real_evol_vs_simus_to_be_called.compare_two_curves( list_actual_evol_training,time_evol_number_adopters))
               
                list_dist_abs_at_ending_point_fixed_parameters.append( abs(time_evol_number_adopters[-1]-list_actual_evol_training[-1]) )

               


               
              
             

            #######################   end loop Niter for the training fase


            list_pair_dist_std_delta_end=[]
        
            list_pair_dist_std_delta_end.append(numpy.mean(list_dist_fixed_parameters) )   # average dist between the curves over Niter
            list_pair_dist_std_delta_end.append(numpy.std(list_dist_fixed_parameters) )

            list_pair_dist_std_delta_end.append(numpy.mean(list_dist_abs_at_ending_point_fixed_parameters))

         

                          

            if (numpy.mean(list_dist_abs_at_ending_point_fixed_parameters)) <= delta_end:  # i only consider situations close enough at the ending point   

               dict_filenames_tot_distance[output_file]=list_pair_dist_std_delta_end 

               #print >> file3, alpha_F,damping,mutual_encouragement,threshold,dict_filenames_tot_distance[output_file][0],dict_filenames_tot_distance[output_file][1]

               dict_filenames_list_dict_network_states[output_file]=list_dict_network_states




   
            file = open(output_file,'wt')        
            for i in range(len(time_evol_number_adopters)):  #time step by time step
                list_fixed_t=[]
                for iteracion in range (Niter_training): #loop over all independent iter of the process
                    list_fixed_t.append(time_evol_number_adopters_ITER[iteracion][i])  # i collect all values for the same t, different iter  

                print >> file, list_t[i],numpy.mean(list_fixed_t),numpy.std(list_fixed_t), alpha_F,damping,mutual_encouragement       
            file.close()

           

          
            damping += delta_damping
          mutual_encouragement += delta_mutual_encouragement
        alpha_F += delta_alpha_F
      
    


   list_order_dict=  compare_real_evol_vs_simus_to_be_called.pick_minimum_same_end(dict_filenames_tot_distance,"Persuasion_training_distributed_thresholds",all_team,Niter_training)




#./Results/network_final_schedule_withTeam3_local/Time_evolutions_Persuasion_alpha0.4_damping0.4_mutual_encourg0.6_threshold0.5_unif_distr_2iter_2012_seed31Oct_finalnetwork.dat


   optimum_filename=list_order_dict[0][0]
   
   alpha_F=float(list_order_dict[0][0].split("_alpha")[1][0:3])
   alpha_A=0.5*alpha_F
   damping=float(list_order_dict[0][0].split("_damping")[1][0:3])
   mutual_encouragement=float(list_order_dict[0][0].split("_mutual_encourg")[1][0:3])
  
                                 



#   raw_input()
   print "starting testing fase with:"
   print "alpha=", alpha_F, " damping=",damping," mutual encourag=",mutual_encouragement," distributed threshold"
   
   
  
   #  i already know the optimum, now i run the dynamics with those values, starting from the average state on the cutting point, and test: 

   time_evol_number_adopters_ITER=[]  # list of complete single realizations of the dynamics
  
   
   list_dict_network_states=[]
  
  

   list_dist_fixed_parameters=[]
   list_dist_at_ending_point_fixed_parameters=[]       
   list_dist_abs_at_ending_point_fixed_parameters=[]       

   list_lists_t_evolutions=[]    





   lista_num_adopters=[]
   lista_Adopters=[]
   dict_tot_Adopters={}

   
   for dictionary in dict_filenames_list_dict_network_states[optimum_filename]:
       # dictionary={Dr1:status, Dr2:status,}  # one dict per iteration
      num_Adopters=0.
     
      for key in dictionary:
         if dictionary[key]=="Adopter":
            num_Adopters+=1.
            if key not in lista_Adopters:
               lista_Adopters.append(key)
               dict_tot_Adopters[key]=1.
            else:
               dict_tot_Adopters[key]+=1.

        


      lista_num_adopters.append(num_Adopters)
    


  
   avg_adopters=int(numpy.mean(lista_num_adopters))   # i find out the average num Adopters
   print numpy.mean(lista_num_adopters),avg_adopters,numpy.std(lista_num_adopters)

   if numpy.mean(lista_num_adopters)-avg_adopters>=0.5:
      avg_adopters+=1.0
      print avg_adopters





# i sort the list from more frequently infected to less
   list_sorted_dict = sorted(dict_tot_Adopters.iteritems(), key=operator.itemgetter(1))

   new_list_sorted_dict=list_sorted_dict
   new_list_sorted_dict.reverse() 

   print "Adopters:",new_list_sorted_dict
  
#list_sorted_dict=[(u'Weiss', 5.0), (u'Wunderink', 5.0), (u'Keller', 4.0), (u'Go', 3.0), (u'Cuttica', 3.0), (u'Rosario', 2.0), (u'Radigan', 2.0), (u'Smith', 2.0), (u'RosenbergN', 2.0), (u'Gillespie', 1.0), (u'Osher', 1.0), (u'Mutlu', 1.0), (u'Dematte', 1.0), (u'Hawkins', 1.0), (u'Gates', 1.0)]



   lista_avg_Adopters=[]  # i create the list of Drs that on average are most likely infected by the cutting day

   i=1 
   for item in new_list_sorted_dict:
      if (item[0] not in lista_avg_Adopters) and (i <=avg_adopters):
      
         lista_avg_Adopters.append(item[0])
         i+=1


   print lista_avg_Adopters

  




   for iter in range(Niter_testing):

      print "         ",iter

      dict_dr_status_current_iter= dict_filenames_list_dict_network_states[optimum_filename][iter]

     

      time_evol_number_adopters=[]   # for a single realization of the dynamics

      dict_network_states={}



      list_t=[]
  


         
    
###############
# NECESITO GUARDAR RECORD DE LOS THERSHOLDS PERSONALES PARA USARLOS LUEGO aki???
########








      list_Adopters=[]  #set initial conditions
      for node in G.nodes():
         if   G.node[node]['type']!="shift":

            # personal threshold have been established for each dr at the beginning of the simu: set_ic()

                      
            G.node[node]["status"]="NonAdopter"  # by default,  non-Adopters

            label=G.node[node]['label']
           

            if label in lista_avg_Adopters:    
            
               G.node[node]["status"]="Adopter"
               G.node[node]["adoption_vector"]=random.random()*(1.0-G.node[node]["personal_threshold"])+G.node[node]["personal_threshold"]  #values from (threshold,1]
               if G.node[node]["adoption_vector"]>1.0:
                  G.node[node]["adoption_vector"]=1.0

               list_Adopters.append(G.node[node]["label"])



      time_evol_number_adopters.append(float(len(list_Adopters)))              
      list_t.append(cutting_day)





      ################# the dynamics starts for the testing fase:

      t=cutting_day


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
                        persuasion(G,damping,doctor1,doctor2,alpha_A,alpha_F)   # i move their values of opinion                  
                        update_opinions(G,doctor1,doctor2) #  i update status and make sure the values of the vectors stay between [0,1] 
                        
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
         print t, len(list_Adopters)

         t+=1
   

      ############## end while loop over t
               
      #raw_input()

      for n in G.nodes():            
         if   G.node[n]['type']!="shift":                  
            dict_network_states[G.node[n]["label"]]=G.node[n]["status"]

          
      list_dict_network_states.append(dict_network_states)

      time_evol_number_adopters_ITER.append(time_evol_number_adopters)


               
      list_dist_fixed_parameters.append(compare_real_evol_vs_simus_to_be_called.compare_two_curves(list_actual_evol_testing,time_evol_number_adopters))
      
      list_dist_abs_at_ending_point_fixed_parameters.append( abs(time_evol_number_adopters[-1]-list_actual_evol_testing[-1]) )

      list_dist_at_ending_point_fixed_parameters.append( time_evol_number_adopters[-1]-list_actual_evol_testing[-1])


      #######################end loop over Niter for the testing fase


               
              
             

   list_pair_dist_std_delta_end=[]
        
   list_pair_dist_std_delta_end.append(numpy.mean(list_dist_fixed_parameters) )   # average dist between the curves over Niter
   list_pair_dist_std_delta_end.append(numpy.std(list_dist_fixed_parameters) )
   
   list_pair_dist_std_delta_end.append(numpy.mean(list_dist_abs_at_ending_point_fixed_parameters))
   
         

                          

   if (numpy.mean(list_dist_abs_at_ending_point_fixed_parameters)) <= delta_end:  # i only consider situations close enough at the ending point   

      dict_filenames_tot_distance[output_file]=list_pair_dist_std_delta_end 

           

      dict_filenames_list_dict_network_states[output_file]=list_dict_network_states





   num_valid_endings=0.
   for item in list_dist_abs_at_ending_point_fixed_parameters:
      if item <= delta_end:  # i count how many realizations i get close enough at the ending point         
         num_valid_endings+=1.
     

   print "average distance of the optimum in the testing segment:",numpy.mean(list_dist_fixed_parameters),numpy.std(list_dist_fixed_parameters),list_dist_fixed_parameters
   print "fraction of realizations that end within delta_doctor:",num_valid_endings/Niter_testing,list_dist_abs_at_ending_point_fixed_parameters
    



   histograma_gral_negv_posit.histograma(list_dist_at_ending_point_fixed_parameters,"../Results/histogr_raw_distances_ending_test_train_persuasion_avg_ic_"+str(Niter_testing)+"iter_distributed_thresholds.dat")




   output_file8="../Results/List_tot_distances_training_segment_persuasion_alpha"+str(alpha_F)+"_damping"+str(damping)+"_mutual_encourg"+str(mutual_encouragement)+"_"+str(Niter_training)+"iter_avg_ic_distributed_thresholds.dat"        
   file8 = open(output_file8,'wt')    

   for item in list_dist_fixed_parameters:
      print >> file8, item
   file8.close()




   output_file9="../Results/List_distances_ending_training_segment_persuasion_alpha"+str(alpha_F)+"_damping"+str(damping)+"_mutual_encourg"+str(mutual_encouragement)+"_"+str(Niter_training)+"iter_avg_ic_distributed_thresholds.dat"        
   file9 = open(output_file9,'wt')    

   for item in list_dist_abs_at_ending_point_fixed_parameters:
      print >> file9, item
   file9.close()






               
   output_file=dir+"Time_evolutions_Persuasion_testing_avg_ic_alpha"+str(alpha_F)+"_damping"+str(damping)+"_mutual_encourg"+str(mutual_encouragement)+"_unif_distr_"+str(Niter_training)+"iter_2012_seed31Oct_finalnetwork_avg_ic_distributed_thresholds.dat"        
   file = open(output_file,'wt')       
  
   for i in range(len(time_evol_number_adopters)):  #time step by time step
         list_fixed_t=[]
         for iteracion in range (Niter_training): #loop over all independent iter of the process
            list_fixed_t.append(time_evol_number_adopters_ITER[iteracion][i])  # i collect all values for the same t, different iter  
            
         print >> file, list_t[i],numpy.mean(list_fixed_t),numpy.std(list_fixed_t), alpha_F,damping,mutual_encouragement       
   file.close()




   print "written training segment file:",optimum_filename
   print "written testing segment file:",output_file





   output_file10="../Results/Summary_results_train_test_persuasion_alpha"+str(alpha_F)+"_damping"+str(damping)+"_mutual_encourg"+str(mutual_encouragement)+"_"+str(Niter_training)+"iter_avg_ic_distributed_thresholds.dat"        
   file10 = open(output_file10,'wt')    

   print >> file10, "Summary results from train-testing persuasion with",Niter_training, Niter_testing, "iter (respectively), using the avg of the cutting points as IC, and with values for the parameters:  alpha ",alpha_F," damping: ",damping," mutual_encourg: ",mutual_encouragement," distributed threshold"

   print >> file10, "average distance of the optimum in the testing segment:",numpy.mean(list_dist_fixed_parameters),numpy.std(list_dist_fixed_parameters),list_dist_fixed_parameters
   print >> file10,  "fraction of realizations that end within delta_doctor:",num_valid_endings/Niter_testing,list_dist_at_ending_point_fixed_parameters


   print >> file10,  "written training segment file:",optimum_filename
   print >> file10,  "written testing segment file:",output_file


   file10.close()





###############################################
#####################################################

 

def set_ic(G):

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
                    personal_threshold=random.random()

                    G.node[n]["personal_threshold"]=personal_threshold

                    G.node[n]["adoption_vector"]=random.random()*personal_threshold  #values from [0,threshold) BUT NOW THAT THRESHOLD IS DIFF. FOR EACH DR, TOO!!
                    G.node[n]["status"]="NonAdopter"  # initially non-Adopters

                  #  print G.node[n]['label'], G.node[n]["personal_threshold"],G.node[n]["adoption_vector"] 
            elif G.node[n]['type']=="F":
                if n not in list_F:
                    list_F.append(n)

                    personal_threshold=random.random()
                    G.node[n]["personal_threshold"]=personal_threshold
                    G.node[n]["adoption_vector"]=random.random()*personal_threshold


                    G.node[n]["adoption_vector"]=random.random()*personal_threshold
                    G.node[n]["status"]="NonAdopter"  
                 #   print G.node[n]['label'], G.node[n]["personal_threshold"],G.node[n]["adoption_vector"] 
    
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


def persuasion(G,damping,doctor1,doctor2,alpha_A,alpha_F):

    if G.node[doctor1]["adoption_vector"]>=G.node[doctor1]["personal_threshold"] or G.node[doctor2]["adoption_vector"]>=G.node[doctor2]["personal_threshold"] :  # only if at least one doctor is Adopter

        
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



def update_opinions(G,doctor1,doctor2):

    if float(G.node[doctor1]["adoption_vector"])>=G.node[doctor1]["personal_threshold"]: 
        G.node[doctor1]['status']="Adopter"               
        if  float(G.node[doctor1]["adoption_vector"])>1.0:   # i make sure the values of the vectors stay between [0,1]    
            G.node[doctor1]["adoption_vector"]=1.0  
    else:                                       
        
        G.node[doctor1]['status']="NonAdopter"                                   
        if float(G.node[doctor1]["adoption_vector"])<0.0:    # i make sure the values of the vectors stay between [0,1]     
            G.node[doctor1]["adoption_vector"]=0.0
            
                
                                
    if float(G.node[doctor2]["adoption_vector"])>=G.node[doctor2]["personal_threshold"]:
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

    
