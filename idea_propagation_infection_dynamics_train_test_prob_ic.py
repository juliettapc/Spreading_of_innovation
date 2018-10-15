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
import histograma_gral
import operator



def main(graph_name):
 


   cutting_day=125  # to separate   training-testing


   G = nx.read_gml(graph_name)


   all_team="NO"   # as adopters or not




   dir_real_data='../Results/'


   delta_end=3  # >= than + or -  dr difference at the end of the evolution (NO realization ends up closer than this!!!! if 2, i get and empty list!!!)

   Niter_training=5
   Niter_testing= 5





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

#../Results/network_final_schedule_withTeam3/infection/Average_time_evolution_Infection_p0.9_Immune0.5_1000iter_2012.dat

   prob_min=0.00
   prob_max=1.01
   delta_prob=0.1
   
   

   prob_Immune_min=0.00
   prob_Immune_max=1.01
   delta_prob_Immune=0.1
   




   dir="../Results/network_final_schedule_withTeam3_local/infection/"   

   dict_filenames_tot_distance={}   # i will save the filename as key and the tot distance from that curve to the original one

   dict_filenames_list_dict_network_states={}   # i will save the filename as key and the list of networks at cutting day as value

   prob_Immune=prob_Immune_min
   while prob_Immune<= prob_Immune_max:
        
      print "prom Immune:",prob_Immune        

      prob_infection=prob_min
      while prob_infection<= prob_max:
                 
        print "  p:",prob_infection        


        output_file2=dir+"Average_time_evolution_Infection_training_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter_training)+"iter_2012.dat"
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

        list_dist_fixed_parameters=[]
        list_dist_at_ending_point_fixed_parameters=[]

        list_dict_network_states=[]
        list_networks_at_cutting_day=[]

        for iter in range(Niter_training):
            
            print "     iter:",iter

            dict_network_states={}

     




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
            while t< cutting_day:  # loop over shifts, in order   just until cutting day (training segment)        
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
   
           
            for n in G.nodes():            
               if   G.node[n]['type']!="shift":                  
                  dict_network_states[G.node[n]["label"]]=G.node[n]["status"]

          
            list_dict_network_states.append(dict_network_states)

        


            ######## end t loop

         


  

            list_lists_t_evolutions.append(list_single_t_evolution)
             
 
            list_dist_fixed_parameters.append(compare_real_evol_vs_simus_to_be_called.compare_two_curves( list_actual_evol_training,list_single_t_evolution))
               
            list_dist_at_ending_point_fixed_parameters.append( abs(list_single_t_evolution[-1]-list_actual_evol_training[-1]) )   # i save the distance at the ending point between the current simu and actual evol

         
           

        ######## end loop Niter for the training fase
      

    
       
       
        list_pair_dist_std_delta_end=[]
        
        list_pair_dist_std_delta_end.append(numpy.mean(list_dist_fixed_parameters) )   # average dist between the curves over Niter
        list_pair_dist_std_delta_end.append(numpy.std(list_dist_fixed_parameters) )

        list_pair_dist_std_delta_end.append(numpy.mean(list_dist_at_ending_point_fixed_parameters))


      
        if (numpy.mean(list_dist_at_ending_point_fixed_parameters)) <= delta_end:  # i only consider situations close enough at the ending point   
          
           dict_filenames_tot_distance[output_file2]=list_pair_dist_std_delta_end
         
           dict_filenames_list_dict_network_states[output_file2]=list_dict_network_states

        

        file2 = open(output_file2,'at')        
        for s in range(len(list_single_t_evolution)):           
            list_fixed_t=[]
            for iter in range (Niter_training):
                list_fixed_t.append(list_lists_t_evolutions[iter][s])        
            print >> file2, s,numpy.mean(list_fixed_t)                    
        file2.close()






        prob_infection+= delta_prob
      prob_Immune+= delta_prob_Immune

   list_order_dict=  compare_real_evol_vs_simus_to_be_called.pick_minimum_same_end(dict_filenames_tot_distance,"Infection_training",all_team,Niter_training)
# it returns a list of tuples like this :  ('../Results/network_final_schedule_withTeam3_local/infection/Average_time_evolution_Infection_training_p0.7_Immune0.0_2iter_2012.dat', [2540.0, 208.0, 1.0])  the best set of parameters  being the fist one of the elements in the list.






   optimum_filename=list_order_dict[0][0]
   
   prob_infection=float(list_order_dict[0][0].split("_p")[1][0:3])
   prob_Immune=float(list_order_dict[0][0].split("_Immune")[1][0:3])


#   raw_input()
   print "starting testing fase with:"
   print "p=",prob_infection," and Pimmune=",prob_Immune
   
   
   
   #  i already know the optimum, now i run the dynamics with those values, starting from the average state on the cutting point, and test: 




  

   list_dist_fixed_parameters=[]
   list_dist_at_ending_point_fixed_parameters=[]

  
      
   list_lists_t_evolutions=[]    

   lista_num_infect=[]
   lista_I_drs=[]
   dict_tot_I_doctors={}

   lista_num_imm=[]
   lista_Imm_drs=[]
   dict_tot_Imm_doctors={}
   for dictionary in dict_filenames_list_dict_network_states[optimum_filename]:
      
       # dictionary={Dr1:status, Dr2:status,}  # one dict per iteration
      num_I=0.
      num_Imm=0.
     
      #raw_input()
      for key in dictionary:
         if dictionary[key]=="I":
            num_I+=1.
            if key not in lista_I_drs:
               lista_I_drs.append(key)
               dict_tot_I_doctors[key]=1.
            else:
               dict_tot_I_doctors[key]+=1.

         elif dictionary[key]=="Immune":
            num_Imm+=1.
            if key not in lista_Imm_drs:
               lista_Imm_drs.append(key)
               dict_tot_Imm_doctors[key]=1.
            else:
               dict_tot_Imm_doctors[key]+=1.


      lista_num_infect.append(num_I)
      lista_num_imm.append(num_Imm)


       

   avg_inf_drs=int(numpy.mean(lista_num_infect))   # i find out the average num I
   print "avg of inf:",numpy.mean(lista_num_infect),avg_inf_drs,numpy.std(lista_num_infect)

   if numpy.mean(lista_num_infect)-avg_inf_drs>=0.5:
      avg_inf_drs+=1.0
     # print avg_inf_drs



   avg_imm_drs=int(numpy.mean(lista_num_imm))  # i find out the average num Immune
   #print "avg of imm:", numpy.mean(lista_num_imm),avg_imm_drs,numpy.std(lista_num_imm)

   if numpy.mean(lista_num_imm)-avg_imm_drs>=0.5:
      avg_imm_drs+=1.0
    #  print avg_imm_drs




# i sort the list from more frequently infected to less
   list_sorted_dict = sorted(dict_tot_I_doctors.iteritems(), key=operator.itemgetter(1))

   new_list_sorted_dict=list_sorted_dict
   new_list_sorted_dict.reverse() 

 #  print "I:",new_list_sorted_dict





#list_sorted_dict=[(u'Weiss', 5.0), (u'Wunderink', 5.0), (u'Keller', 4.0), (u'Go', 3.0), (u'Cuttica', 3.0), (u'Rosario', 2.0), (u'Radigan', 2.0), (u'Smith', 2.0), (u'RosenbergN', 2.0), (u'Gillespie', 1.0), (u'Osher', 1.0), (u'Mutlu', 1.0), (u'Dematte', 1.0), (u'Hawkins', 1.0), (u'Gates', 1.0)]



   dict_infect_prob_being_so={}
   for item in new_list_sorted_dict:
      dict_infect_prob_being_so[item[0]]=0.

   tot_sum_inf_so_far=0.
   for item in new_list_sorted_dict:
      dict_infect_prob_being_so[item[0]]=item[1]+tot_sum_inf_so_far
      tot_sum_inf_so_far+=item[1]

  

   list_sorted_dict_infect_prob_being_so = sorted(dict_infect_prob_being_so.iteritems(), key=operator.itemgetter(1))

 #  new_list_sorted_dict_dict_infect_prob_being_so=list_sorted_dict_infect_prob_being_so
  # new_list_sorted_dict_dict_infect_prob_being_so.reverse() 

   print list_sorted_dict_infect_prob_being_so

   #print tot_sum_inf_so_far





# i sort the list from more frequently imm to less
   list_sorted_dict_imm = sorted(dict_tot_Imm_doctors.iteritems(), key=operator.itemgetter(1))

   new_list_sorted_dict_imm=list_sorted_dict_imm
   new_list_sorted_dict_imm.reverse() 

  # print "Immunes:",new_list_sorted_dict_imm




   dict_imm_prob_being_so={}
   for item in new_list_sorted_dict_imm:
      dict_imm_prob_being_so[item[0]]=0.

   tot_sum_imm_so_far=0.
   for item in new_list_sorted_dict_imm:
      dict_imm_prob_being_so[item[0]]=item[1]+tot_sum_imm_so_far
      tot_sum_imm_so_far+=item[1]

  

   list_sorted_dict_imm_prob_being_so = sorted(dict_imm_prob_being_so.iteritems(), key=operator.itemgetter(1))

  # new_list_sorted_dict_dict_imm_prob_being_so=list_sorted_dict_imm_prob_being_so
   #new_list_sorted_dict_dict_imm_prob_being_so.reverse() 

   print list_sorted_dict_imm_prob_being_so   #new_list_sorted_dict_dict_imm_prob_being_so



   for iter in range(Niter_testing):

   #   print "     iter:",iter, len(list_I)
      raw_input()


      # i establish the initial conditions (as probabilistically, according to the cutting point distribution of status)


      dict_label_node={}
      list_I=[]  #list infected doctors
      list_Immune=[]  #list infected doctors
      for node in G.nodes():
         if   G.node[node]['type']!="shift":
            label=G.node[node]['label']
            G.node[node]["status"]="S"   #by default, all are susceptible
            dict_label_node[label]=node
      
      ii=0.
      while ii<= avg_inf_drs  :

         
         rand=random.random()*tot_sum_inf_so_far
         for i in range(len(list_sorted_dict_infect_prob_being_so)):
            if rand<=list_sorted_dict_infect_prob_being_so[i][1]:
               label=list_sorted_dict_infect_prob_being_so[i][0]
               
               current_prob_value=list_sorted_dict_infect_prob_being_so[i][1]
               node=dict_label_node[label]

               G.node[node]["status"]="I"
               print label, "got infected"
               list_I.append(label)

         #update the prob of being infected:               
         for jj in range(len(list_sorted_dict_infect_prob_being_so)):
            if list_sorted_dict_infect_prob_being_so[jj][1]>=current_prob_value:
               print list_sorted_dict_infect_prob_being_so[jj][1]
               list_sorted_dict_infect_prob_being_so[jj][1]-=current_prob_value

         list_sorted_dict_infect_prob_being_so[i][1]=0.   #so i don't pick it again
         ii+=1.

    
     

      ii=0.
      while ii<= avg_imm_drs  :

         
         rand=random.random()*tot_sum_imm_so_far
         for i in range(len(list_sorted_dict_imm_prob_being_so)):
            if rand<=list_sorted_dict_imm_prob_being_so[i][1]:
               label=list_sorted_dict_imm_prob_being_so[i][0]
               node=dict_label_node[label]

               G.node[node]["status"]="Immune"
               print label, "got immune"
               list_Immune.append(label)


         #update the prob of being infected:               
         for jj in range(len(list_sorted_dict_imm_prob_being_so)):
            if list_sorted_dict_imm_prob_being_so[jj][1]>=current_prob_value:
               list_sorted_dict_imm_prob_being_so[jj][1]-=current_prob_value

         list_sorted_dict_imm_prob_being_so[i][1]=0.   #so i don't pick it again
         ii+=1.

    





      list_single_t_evolution=[]
      list_single_t_evolution.append(len(list_I))
     



      t=cutting_day
      while t<= max_order:  # loop over shifts, in order   just until cutting day (training segment)        
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
                                           

         list_single_t_evolution.append(float(len(list_I)))
         print t, len(list_I)        
         t+=1
   




       
      list_lists_t_evolutions.append(list_single_t_evolution)
     
      
      list_dist_fixed_parameters.append(compare_real_evol_vs_simus_to_be_called.compare_two_curves( list_actual_evol_testing,list_single_t_evolution))

 
      print  " dist:",list_dist_fixed_parameters[-1]

     


      list_dist_at_ending_point_fixed_parameters.append( abs(list_single_t_evolution[-1]-list_actual_evol_testing[-1]) )   # i save the distance at the ending point between the current simu and actual evol

         
     



   ############### end loop Niter  for the testing 


   num_valid_endings=0.
   for item in list_dist_at_ending_point_fixed_parameters:
      if item <= delta_end:  # i count how many realizations i get close enough at the ending point         
         num_valid_endings+=1.
     

   print "average distance of the optimum in the testing segment:",numpy.mean(list_dist_fixed_parameters),numpy.std(list_dist_fixed_parameters),list_dist_fixed_parameters
   print "fraction of realizations that end within delta_doctor:",num_valid_endings/Niter_testing,list_dist_at_ending_point_fixed_parameters
    





   output_file5=dir+"Average_time_evolution_Infection_testing_prob_ic_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter_testing)+"iter_2012.dat"
    
   file5 = open(output_file5,'wt')        
   for s in range(len(list_single_t_evolution)):           
      list_fixed_t=[]
      for iter in range (Niter_testing):
         list_fixed_t.append(list_lists_t_evolutions[iter][s])        
      print >> file5, s+cutting_day,numpy.mean(list_fixed_t)     
    #  print  s+cutting_day,numpy.mean(list_fixed_t)     
   file5.close()

   print "written:",output_file5




   histograma_bines_gral.histograma_bins(list_dist_fixed_parameters,150, "../Results/histogr_tot_distances_testing_avg_ic_segment")
   histograma_gral.histograma(list_dist_at_ending_point_fixed_parameters, "../Results/histogr_distances_ending_testing_avg_ic_segment")



######################################
###############################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
   
        main(graph_filename)
    else:
        print "Usage: python script.py path/network.gml"

    
