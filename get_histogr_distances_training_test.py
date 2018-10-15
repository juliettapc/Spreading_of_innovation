#!/usr/bin/env python


import histograma_gral
import scipy
from  scipy import stats

def main():


    bootstrap_Niter=1000



   ############## lists of total distances, infection

    file_name="../Results/List_tot_distances_training_segment_infection_p0.9_Immune0.7_1000iter_end_point.dat"
    file1=open(file_name,'r')
    lista1=file1.readlines()   # each element is a line of the file  STRING TYPE!!


    Niter_inf=file_name.split("iter_")[0].split("_")[-1]
 
    list_tot_dist_test_infect=[]

    for line in lista1:
        list_tot_dist_test_infect.append(float(line))
       
 



    file_name="../Results/List_distances_ending_training_segment_infection_p0.9_Immune0.7_1000iter_end_point.dat"
    file1=open(file_name,'r')
    lista1=file1.readlines()   # each element is a line of the file  STRING TYPE!!

   
    list_tot_dist_test_infect_avg_ic=[]

    for line in lista1:
        list_tot_dist_test_infect_avg_ic.append(float(line))
       



############## lists of total distances, persuasion

    file_name="../Results/List_tot_distances_training_segment_persuasion_alpha0.7_damping0.0_mutual_encourg0.3_threshold0.9_100iter_same_end_point.dat"
    file1=open(file_name,'r')
    lista1=file1.readlines()  

    Niter_pers=file_name.split("iter_")[0].split("_")[-1]
 



    print Niter_inf, Niter_pers
    list_tot_dist_test_persuasion=[]

    for line in lista1:
        list_tot_dist_test_persuasion.append(float(line))
       
 



    file_name="../Results/List_tot_distances_training_segment_persuasion_alpha0.1_damping0.2_mutual_encourg0.1_threshold0.2_100iter_avg_ic.dat"
    file1=open(file_name,'r')
    lista1=file1.readlines()   

   
    list_tot_dist_test_persuasion_avg_ic=[]

    for line in lista1:
        list_tot_dist_test_persuasion_avg_ic.append(float(line))
       





 
###################




   ############## lists of ending point distances, infection

    file_name="../Results/List_distances_ending_training_segment_infection_p1.0_Immune0.7_1000iter_same_end_point.dat"
    file1=open(file_name,'r')
    lista1=file1.readlines()   # each element is a line of the file  STRING TYPE!!

 
    list_dist_ending_test_infect=[]

    for line in lista1:
        list_dist_ending_test_infect.append(float(line))
       




 
    file_name="../Results/List_distances_ending_training_segment_infection_p0.9_Immune0.7_1000iter_avg_ic.dat"
    file1=open(file_name,'r')
    lista1=file1.readlines()   # each element is a line of the file  STRING TYPE!!

 
    list_dist_ending_test_infect_avg_ic=[]

    for line in lista1:
        list_dist_ending_test_infect_avg_ic.append(float(line))
       





   ############## lists of ending point distances, persuasion

    file_name="../Results/List_distances_ending_training_segment_persuasion_alpha0.7_damping0.0_mutual_encourg0.3_threshold0.9_100iter_same_end_point.dat"
    file1=open(file_name,'r')
    lista1=file1.readlines()   # each element is a line of the file  STRING TYPE!!

 
    list_dist_ending_test_persuasion=[]

    for line in lista1:
        list_dist_ending_test_persuasion.append(float(line))
       




 
    file_name="../Results/List_distances_ending_training_segment_persuasion_alpha0.1_damping0.2_mutual_encourg0.1_threshold0.2_100iter_avg_ic.dat"
    file1=open(file_name,'r')
    lista1=file1.readlines()   # each element is a line of the file  STRING TYPE!!

 
    list_dist_ending_test_persuasion_avg_ic=[]

    for line in lista1:
        list_dist_ending_test_persuasion_avg_ic.append(float(line))
       







    print "KS test tot distances inf. vs pers.:",scipy.stats.ks_2samp(list_tot_dist_test_infect,list_tot_dist_test_persuasion)
    print "KS test tot distances inf. vs pers.  (avg ic):",scipy.stats.ks_2samp(list_tot_dist_test_infect_avg_ic,list_tot_dist_test_persuasion_avg_ic)

    print "KS test ending distances inf. vs pers.:",scipy.stats.ks_2samp(list_dist_ending_test_infect,list_dist_ending_test_persuasion)
    print "KS test ending distances inf. vs pers.  (avg ic):",scipy.stats.ks_2samp(list_dist_ending_test_infect_avg_ic,list_dist_ending_test_persuasion_avg_ic), "\n\n"




   


    histograma_gral.histograma(list_tot_dist_test_infect,"../Results/histogram_tot_distances_testing_infection_"+str(Niter_inf)+"iter.dat",max(list_tot_dist_test_infect))
    histograma_gral.histograma(list_tot_dist_test_infect_avg_ic,"../Results/histogram_tot_distances_testing_infection_avg_ic_"+str(Niter_inf)+"iter.dat",max(list_tot_dist_test_infect_avg_ic))
    histograma_gral.histograma(list_tot_dist_test_persuasion,"../Results/histogram_tot_distances_testing_persuasion_"+str(Niter_pers)+"iter.dat",max(list_tot_dist_test_persuasion))
    histograma_gral.histograma(list_tot_dist_test_persuasion_avg_ic,"../Results/histogram_tot_distances_testing_persuasion_avg_ic_"+str(Niter_pers)+"iter.dat",max(list_tot_dist_test_persuasion_avg_ic))





    histograma_gral.histograma(list_dist_ending_test_infect,"../Results/histogram_distances_ending_testing_infection_"+str(Niter_inf)+"iter.dat",max(list_dist_ending_test_infect))
    histograma_gral.histograma(list_dist_ending_test_infect_avg_ic,"../Results/histogram_distances_ending_testing_infection_avg_ic_"+str(Niter_inf)+"iter.dat",max(list_dist_ending_test_infect_avg_ic))
    histograma_gral.histograma(list_dist_ending_test_persuasion,"../Results/histogram_distances_ending_testing_persuasion_"+str(Niter_pers)+"iter.dat",max(list_dist_ending_test_persuasion))
    histograma_gral.histograma(list_dist_ending_test_persuasion_avg_ic,"../Results/histogram_distances_ending_testing_persuasion_avg_ic_"+str(Niter_pers)+"iter.dat",max(list_dist_ending_test_persuasion_avg_ic))


    list_avg_tot_dist_bootstrap=[]
    list_avg_dist_ending_bootstrap=[]

    sum_populations_tot_dist= list_tot_dist_test_infect + list_tot_dist_test_persuasion
    sum_populations_tot_dist_avg_ic= list_tot_dist_test_infect_avg_ic + list_tot_dist_test_persuasion_avg_ic

    sum_populations_dist_ending= list_dist_ending_test_infect + list_dist_ending_test_persuasion
    sum_populations_dist_ending_avg_ic= list_dist_ending_test_infect_avg_ic + list_dist_ending_test_persuasion_avg_ic




   # for i in range(bootstrap_Niter):

    #    list_avg_tot_dist_bootstrap.append(scipy.mean(sample_with_replacement()))





###############################

def sample_with_replacement(population, k):
    "Chooses k random elements (with replacement) from a population"
    n = len(population)
    _random, _int = random.random, int  # speed hack 
    result = [None] * k
    for i in xrange(k):
        j = _int(_random() * n)
        result[i] = population[j]
    return result




##################################################
######################################
if __name__ == '__main__':
    
    main()
   
