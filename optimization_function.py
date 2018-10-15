#!/usr/bin/env python

'''
Given a .gml network, it simulates a disease-spreading-like process
in the bipartite network (doctors and shifts)

Created by Julia Poncela, on August 2011.

'''

import csv
import sys
import os
import numpy
from  scipy import stats
from  scipy import optimize


import idea_propagation_infection_simple_for_optimization
import idea_propagation_persuasion_simple_for_optimization


def main():
 


 #   prob_min=0.20
  #  prob_max=0.21
   # delta_prob=0.1
    
   
    
   # prob_Immune_min=0.2
    #prob_Immune_max=0.21
    #delta_prob_Immune=0.1
    

   


    #INFECTION 
 # parameters: prob_infection,  prob_Immune
    parameters=[0.2,0.2]   # initial guess for the parameters: prob_infection,prob_Immune
    
    
    print optimize.fmin(idea_propagation_infection_simple_for_optimization.dynamics,parameters, full_output = 1, maxfun=1e8, maxiter=1000, xtol=0.05,retall=1)
 #   print  "parameters: prob_infection,  prob_Immune , Niter:100,  maxfun=1000, maxiter=1000"

#,ftol=0.75


#[0.9,0.6,0.1,0.6]

# PERSUASION
   # parameters=[0.9,0.6,0.1,0.6] # initial guess for the parameters: alpha, damping, mutual_encourg, thershold
    #print optimize.fmin(idea_propagation_persuasion_simple_for_optimization.dynamics,parameters, full_output = 1, maxfun=1e8, maxiter=1000, xtol=0.05,ftol=0.8,retall=1)
#    print " parameters: alpha_F, damping, mutual_encouragement, threshold, Niter:100,  maxfun=1000, maxiter=1000"


    
   
   
########################





#######################################  THE MAIN GOES ALWAYS AT THE VERY END!!!
######################################
if __name__ == '__main__':
  #  if len(sys.argv) > 1:
   #     graph_filename = sys.argv[1]
   
    main()
      #  main(graph_filename)
    #else:
     #   print "Usage: python script.py path/network.gml"

    
##########################################
