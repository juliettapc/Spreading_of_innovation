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
import operator



def main(graph_name):
 


   cutting_day=125  # to separate   training-testing


   G = nx.read_gml(graph_name)


   all_team="NO"   # as adopters or not




   dir_real_data='../Results/'


   delta_end=3  # >= than + or -  dr difference at the end of the evolution (NO realization ends up closer than this!!!! if 2, i get and empty list!!!)

   Niter_training=100
   Niter_testing= 100




   output_file3=dir_real_data+"Landscape_parameters_infection_train_test_"+str(Niter_training)+"iter.dat" 
   file3 = open(output_file3,'wt')        

   file3.close()


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

   prob_min=0.0
   prob_max=1.001
   delta_prob=0.01
   
   

   prob_Immune_min=0.00
   prob_Immune_max=1.001
   delta_prob_Immune=0.01
   




   dir="../Results/network_final_schedule_withTeam3_local/infection/"   

   dict_filenames_tot_distance={}   # i will save the filename as key and the tot distance from that curve to the original one

   dict_filenames_list_dict_network_states={}   # i will save the filename as key and the list of networks at cutting day as value

   prob_Immune=prob_Immune_min
   while prob_Immune<= prob_Immune_max:
        
      print "prom Immune:",prob_Immune        

      prob_infection=prob_min
      while prob_infection<= prob_max:
                 
        print "  p:",prob_infection        


        output_file2=dir+"Average_time_evolution_Infection_training_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter_training)+"iter_2012_avg_ic_day"+str(cutting_day)+".dat"
        file2 = open(output_file2,'wt')                                       
        file2.close()
        


# i create the empty list of list for the Niter temporal evolutions
        num_shifts=0
        num_Drs=0.
        for n in G.nodes():
            G.node[n]["status"]="S" 
            if G.node[n]['type']=="shift":
                num_shifts+=1
            else:
               num_Drs+=1.




      #  list_final_I_values_fixed_p=[]  # i dont care about the final values right now, but about the whole time evol
        list_lists_t_evolutions=[]    

        list_dist_fixed_parameters=[]
        list_dist_abs_at_ending_point_fixed_parameters=[]
        list_final_num_infected=[]
        list_dict_network_states=[]
       

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
            ######## end t loop
   
           
            for n in G.nodes():            
               if   G.node[n]['type']!="shift":                  
                  dict_network_states[G.node[n]["label"]]=G.node[n]["status"]

          
            list_dict_network_states.append(dict_network_states)

        



         


  

            list_lists_t_evolutions.append(list_single_t_evolution)
             
 
            list_dist_fixed_parameters.append(compare_real_evol_vs_simus_to_be_called.compare_two_curves( list_actual_evol_training,list_single_t_evolution))
               
            list_dist_abs_at_ending_point_fixed_parameters.append( abs(list_single_t_evolution[-1]-list_actual_evol_training[-1]) )   # i save the distance at the ending point between the current simu and actual evol

          #  print "actual:",len(list_actual_evol_training),"  simu:",len(list_single_t_evolution)   # 125, 125

            
            list_final_num_infected.append(list_single_t_evolution[-1])



        ######## end loop Niter for the training fase
      

    
       
       
        list_pair_dist_std_delta_end=[]
        
        list_pair_dist_std_delta_end.append(numpy.mean(list_dist_fixed_parameters) )   # average dist between the curves over Niter
        list_pair_dist_std_delta_end.append(numpy.std(list_dist_fixed_parameters) )

        list_pair_dist_std_delta_end.append(numpy.mean(list_dist_abs_at_ending_point_fixed_parameters))




        file3 = open(output_file3,'at')          # i print out the landscape           
        print >> file3, prob_infection,prob_Immune,numpy.mean(list_dist_abs_at_ending_point_fixed_parameters), numpy.mean(list_dist_fixed_parameters), numpy.mean(list_final_num_infected),numpy.std(list_final_num_infected), numpy.std(list_final_num_infected)/numpy.mean(list_final_num_infected)
        file3.close()






      
        if (numpy.mean(list_dist_abs_at_ending_point_fixed_parameters)) <= delta_end:  # i only consider situations close enough at the ending point   
          
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

   list_order_dict=  compare_real_evol_vs_simus_to_be_called.pick_minimum_same_end(dict_filenames_tot_distance,"Infection_training",all_team,Niter_training,cutting_day)

# it returns a list of tuples like this :  ('../Results/network_final_schedule_withTeam3_local/infection/Average_time_evolution_Infection_training_p0.7_Immune0.0_2iter_2012.dat', [2540.0, 208.0, 1.0])  the best set of parameters  being the fist one of the elements in the list.






   optimum_filename=list_order_dict[0][0]
   prob_infection=float(list_order_dict[0][0].split("_p")[1].split("_")[0])
   prob_Immune=float(list_order_dict[0][0].split("_Immune")[1].split("_")[0])


   print "starting testing fase with:"
   print "p=",prob_infection," and Pimmune=",prob_Immune
   
 
   #  i already know the optimum, now i run the dynamics with those values, starting from the average state on the cutting point, and test: 




  

   list_dist_fixed_parameters=[]
   list_dist_abs_at_ending_point_fixed_parameters=[]
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
   print "I",numpy.mean(lista_num_infect),numpy.mean(lista_num_infect)/num_Drs,avg_inf_drs,numpy.std(lista_num_infect)

   if numpy.mean(lista_num_infect)-avg_inf_drs>=0.5:  # correccion de truncamiento
      avg_inf_drs+=1.0
    #  print avg_inf_drs



   avg_imm_drs=int(numpy.mean(lista_num_imm))  # i find out the average num Immune
   print "Imm",numpy.mean(lista_num_imm),numpy.mean(lista_num_imm)/num_Drs,avg_imm_drs,numpy.std(lista_num_imm)

   if numpy.mean(lista_num_imm)-avg_imm_drs>=0.5: # correccion de truncamiento
      avg_imm_drs+=1.0
     # print avg_imm_drs



  
# i sort the list from more frequently infected to less
   list_sorted_dict = sorted(dict_tot_I_doctors.iteritems(), key=operator.itemgetter(1))

   new_list_sorted_dict=list_sorted_dict
   new_list_sorted_dict.reverse() 

   print "I:",new_list_sorted_dict




# i sort the list from more frequently imm to less
   list_sorted_dict_imm = sorted(dict_tot_Imm_doctors.iteritems(), key=operator.itemgetter(1))

   new_list_sorted_dict_imm=list_sorted_dict_imm
   new_list_sorted_dict_imm.reverse() 

   print "Immunes:",new_list_sorted_dict_imm


#   raw_input()

#list_sorted_dict=[(u'Weiss', 5.0), (u'Wunderink', 5.0), (u'Keller', 4.0), (u'Go', 3.0), (u'Cuttica', 3.0), (u'Rosario', 2.0), (u'Radigan', 2.0), (u'Smith', 2.0), (u'RosenbergN', 2.0), (u'Gillespie', 1.0), (u'Osher', 1.0), (u'Mutlu', 1.0), (u'Dematte', 1.0), (u'Hawkins', 1.0), (u'Gates', 1.0)]


   lista_avg_I_drs=[]  # i create the list of Drs that on average are most likely infected by the cutting day

   i=1 
   for item in new_list_sorted_dict:
      if (item[0] not in lista_avg_I_drs) and (i <=avg_inf_drs):
      
         lista_avg_I_drs.append(item[0])
         i+=1


   print lista_avg_I_drs,len(lista_avg_I_drs),float(len(lista_avg_I_drs))/num_Drs

   lista_avg_Imm_drs=[]  # i create the list of Drs that on average are most likely immune by the cutting day

   i=1 
   for item in new_list_sorted_dict_imm:
      if (item[0] not in lista_avg_Imm_drs) and (i <=avg_imm_drs) and (item[0] not in lista_avg_I_drs):
      
         lista_avg_Imm_drs.append(item[0])
         i+=1




   print lista_avg_Imm_drs,len(lista_avg_Imm_drs),float(len(lista_avg_Imm_drs))/num_Drs



  # raw_input()
   for iter in range(Niter_testing):


      # i establish the initial conditions (as the average of the cutting point)
    
      list_I=[]  #list infected doctors
      list_Immune=[] 
      for node in G.nodes():
         if   G.node[node]['type']!="shift":
            label=G.node[node]['label']
            G.node[node]["status"]="S"   #by default, all are susceptible
       

            if label in lista_avg_I_drs:            
               G.node[node]["status"]="I"
               list_I.append(label)
            elif  label in lista_avg_Imm_drs:                                       
               G.node[node]["status"]="Immune"
               list_Immune.append(label)
            if label in lista_avg_I_drs and label in lista_avg_Imm_drs:  

               print label, "is in the top most infected AND immune!"
               raw_input()
                  
      print "# I at the beginning of the testing fase:", len(list_I), float(len(list_I))/num_Drs, " and # Immune:",len(list_Immune),float(len(list_Immune))/num_Drs


     # print "     iter:",iter, len(list_I)

     
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
#         print t, len(list_I)        
         t+=1
   


       
      list_lists_t_evolutions.append(list_single_t_evolution)
     
      

      list_I=[]
      list_Immune=[]
      for node in G.nodes():
         if   G.node[node]['type']!="shift":
            label=G.node[node]['label']          
                    
            if  G.node[node]["status"]=="I":
               list_I.append(label)
            elif  G.node[node]["status"]=="Immune":
               list_Immune.append(label)
            
                  
      print "  # I at the END of the testing fase:", len(list_I), float(len(list_I))/num_Drs, " and # Immune:",len(list_Immune),float(len(list_Immune))/num_Drs,"\n"







      list_dist_fixed_parameters.append(compare_real_evol_vs_simus_to_be_called.compare_two_curves( list_actual_evol_testing,list_single_t_evolution))

 
     # print  " dist:",list_dist_fixed_parameters[-1]

     


      list_dist_abs_at_ending_point_fixed_parameters.append( abs(list_single_t_evolution[-1]-list_actual_evol_testing[-1]) )   # i save the distance at the ending point between the current simu and actual evol

      list_dist_at_ending_point_fixed_parameters.append( list_single_t_evolution[-1]-list_actual_evol_testing[-1])    # i save the distance at the ending point between the current simu and actual evol
   
     



   ############### end loop Niter  for the testing 


   num_valid_endings=0.
   for item in list_dist_abs_at_ending_point_fixed_parameters:
      if item <= delta_end:  # i count how many realizations i get close enough at the ending point         
         num_valid_endings+=1.
     

   print "average distance of the optimum in the testing segment:",numpy.mean(list_dist_fixed_parameters),numpy.std(list_dist_fixed_parameters),list_dist_fixed_parameters
   print "fraction of realizations that end within delta_doctor:",num_valid_endings/Niter_testing,list_dist_abs_at_ending_point_fixed_parameters
    



   histograma_gral_negv_posit.histograma(list_dist_at_ending_point_fixed_parameters,"../Results/histogr_raw_distances_ending_test_train_infection_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter_training)+"iter_avg_ic_day"+str(cutting_day)+".dat"        )



   output_file8="../Results/List_tot_distances_training_segment_infection_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter_training)+"iter_avg_ic_day"+str(cutting_day)+".dat"        
   file8 = open(output_file8,'wt')    

   for item in list_dist_fixed_parameters:
      print >> file8, item
   file8.close()




   output_file9="../Results/List_distances_ending_training_segment_infection_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter_training)+"iter_avg_ic_day"+str(cutting_day)+".dat"        
   file9 = open(output_file9,'wt')    

   for item in list_dist_abs_at_ending_point_fixed_parameters:
      print >> file9, item
   file9.close()










   output_file5=dir+"Average_time_evolution_Infection_testing_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter_testing)+"iter_2012_avg_ic_day"+str(cutting_day)+".dat"
    
   file5 = open(output_file5,'wt')        
   for s in range(len(list_single_t_evolution)):           
      list_fixed_t=[]
      for iter in range (Niter_testing):
         list_fixed_t.append(list_lists_t_evolutions[iter][s])        
      print >> file5, s+cutting_day,numpy.mean(list_fixed_t)     
    #  print  s+cutting_day,numpy.mean(list_fixed_t)     
   file5.close()

   


   print "written training segment file:",optimum_filename
   print "written testing segment file:",output_file5


   print "printed out landscape file:",output_file3






   output_file10="../Results/Summary_results_training_segment_infection_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_"+str(Niter_training)+"iter_avg_ic_day"+str(cutting_day)+".dat"          
   file10 = open(output_file10,'wt')    

   print >> file10, "Summary results from train-testing persuasion with",Niter_training, Niter_testing, "iter (respectively), using all the individual cutting points as IC, and with values for the parameters:  prob_inf ",prob_infection," prob immune: ",prob_Immune,"\n"

   print >> file10, "average distance of the optimum in the testing segment:",numpy.mean(list_dist_fixed_parameters),numpy.std(list_dist_fixed_parameters),list_dist_fixed_parameters,"\n"
   print >> file10,  "fraction of realizations that end within delta_doctor:",num_valid_endings/Niter_testing,list_dist_abs_at_ending_point_fixed_parameters,"\n"


   print >> file10,  "written training segment file:",optimum_filename
   print >> file10,  "written testing segment file:",output_file5


   file10.close()





######################################
###############################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_filename = sys.argv[1]
   
        main(graph_filename)
    else:
        print "Usage: python script.py path/network.gml"

    
