#!/usr/bin/env python


"""
Given a bunch of  curves, it calculates the envelope that includes  the X % of them.

Created by Julia Poncela, sept 2012.
"""


def calculate_envelope(list_of_lists, percent_included,dynamics,parameters):

    if dynamics=="Infection":
        prob_infection=parameters[0]
        prob_Immune=parameters[1]

    elif dynamics=="Infection_memory_fixed":
        prob_infection=parameters[0]
        prob_Immune=parameters[1]
        infect_threshold=parameters[2]
        dose=parameters[3]


    elif dynamics=="Persuasion":      
       alpha_F=parameters[0]
       damping=parameters[1]
       mutual_encouragement=parameters[2]
       threshold=parameters[3]

    elif dynamics=="Persuasion_intervention":      
       alpha_F=parameters[0]
       damping=parameters[1]
       mutual_encouragement=parameters[2]
       threshold=parameters[3]
       bump=parameters[4]
       time_window_ahead=parameters[5]

    elif dynamics=="Persuasion_intervention_2A_1F":      
       alpha_F=parameters[0]
       damping=parameters[1]
       mutual_encouragement=parameters[2]
       threshold=parameters[3]
       bump=parameters[4]
       time_window_ahead=parameters[5]



    else:
        print "wrong name for the type of dynamics"
        exit()


    lenght_one_series=len(list_of_lists[0])   # = Number time steps (243)


  


    list_low_envelope=[]
    list_high_envelope=[]
    max_percent_included=100.0-(100.0-percent_included)/2.0
    min_percent_included=0.0+(100.0-percent_included)/2.0

    for i in  range(lenght_one_series):
        lista_fixed_t=[]
        for item in list_of_lists:  #loop over all individual time evolutions
            lista_fixed_t.append(item[i])
        sorted_lista_fixed_t=sorted(lista_fixed_t)

      #  print len(lista_fixed_t)  # = Niter
        Niter=len(lista_fixed_t)

        min_index=int(len(lista_fixed_t)*min_percent_included/100.)  # of the sorted values to include in the envelope

        max_index=int(len(lista_fixed_t)*max_percent_included/100.)  -1   



    
        list_low_envelope.append(sorted_lista_fixed_t[min_index])
        list_high_envelope.append(sorted_lista_fixed_t[max_index])
       



    if dynamics=="Infection":
        output_file="../Results/weight_shifts/Low_high_"+str(percent_included)+"percent_envelope_"+str(dynamics)+"_p"+str(prob_infection)+"_Immune"+str(prob_Immune)+"_"+str(Niter)+"iter.dat"  

    elif dynamics=="Infection_memory_fixed":
        output_file="../Results/weight_shifts/Low_high_"+str(percent_included)+"percent_envelope_"+str(dynamics)+"_p"+str(prob_infection)+"_"+"Immune"+str(prob_Immune)+"_threshold"+str(infect_threshold)+"_dose"+str(dose)+"_"+str(Niter)+"iter.dat"



    elif dynamics=="Persuasion":          
        output_file="../Results/weight_shifts/Low_high_"+str(percent_included)+"percent_envelope_"+str(dynamics)+"_alpha"+str(alpha_F)+"_damping"+str(damping)+"_mutual_encourg"+str(mutual_encouragement)+"_threshold"+str(threshold)+"_"+str(Niter)+"iter_alphaA_eq_alphaF.dat" 

    elif dynamics=="Persuasion_intervention":    
             
        output_file="../Results/weight_shifts/Low_high_"+str(percent_included)+"percent_envelope_"+str(dynamics)+"_alpha"+str(alpha_F)+"_damping"+str(damping)+"_mutual_encourg"+str(mutual_encouragement)+"_threshold"+str(threshold)+"_"+str(Niter)+"iter_window"+str(time_window_ahead)+"_bump"+str(bump)+"_alphaA_eq_alphaF_comparison_to_simu_without_interv.dat" 

    elif dynamics=="Persuasion_intervention_2A_1F":    
             
        output_file="../Results/weight_shifts/Low_high_"+str(percent_included)+"percent_envelope_"+str(dynamics)+"_alpha"+str(alpha_F)+"_damping"+str(damping)+"_mutual_encourg"+str(mutual_encouragement)+"_threshold"+str(threshold)+"_"+str(Niter)+"iter_window"+str(time_window_ahead)+"_bump"+str(bump)+"_alphaA_eq_alphaF_2A_1F.dat" 


    file = open(output_file,'wt')  
    for i in range(len(list_low_envelope)):       
      print >> file,i, list_low_envelope[i],list_high_envelope[i]

    file.close()


    print "\nwritten:",output_file
