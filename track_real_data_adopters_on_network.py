#!/usr/bin/env python

"""
Code to track the real evolution of Adopters, and determine whether or not
they got infected at work or outside it.


Created by Julia Poncela, November 2011.

"""

import csv
import networkx as nx
import numpy
import sys
from datetime import *
import matplotlib.pyplot as plt
from transform_labels_to_nx import *


def main(graph_filename,data_file):


    seeding_datetime=datetime(2011,10,31)
    initial_adopters=["Wunderink", "Sporn","Smith","Weiss"]
    print "seeding date:",seeding_datetime
    print "initial adopters:",initial_adopters


   

    G = nx.read_gml(graph_filename)
    
   

    for node in G.nodes():
        G.node[node]["status"]="NonAdopter"
       # print node # numbers!
    for doctor in initial_adopters:
        for node in G.nodes():
            if G.node[node]["label"]==doctor:
                G.node[node]["status"]="Adopter"

                print doctor  # labels with names!!



    max_number_doctors=35

    file=open(data_file,'r')         ## i read the file:  list_dates_and_names_current_adopters.txt  (created with: extract_real_evolution_number_adopters.py)
    list_lines_file=file.readlines()
            

    dicc_doctors={} 
    list_doctors=[] 
    for line in list_lines_file [1:]:   # i exclude the first row                    
        
        parts=line.split(" ")#[0]#.split("-")                              
        parts_date=parts[0].split("-")
        
        
        yy=int(parts_date[0])                    
        mm=int(parts_date[1])
        dd=int(parts_date[2])
        date_order=datetime(yy,mm,dd)
                
        # i get the dicc of adopter doctors and date of first adoption    
        for i in range(2,max_number_doctors):   # to account for the diff. lengh of every line  and exclude the second colum that is just 00:00:00 
            try:                   
                doctor=parts[i]
                if doctor not in dicc_doctors and doctor != "\n":
                    dicc_doctors[doctor]=date_order
                    list_doctors.append(doctor)
            except: pass


    print "sorted list of adopters:",list_doctors

   



    for doctor in list_doctors:
        print "\n\n",doctor,":"
       
        if doctor not in initial_adopters:  # i dont want to track the doctors initially seeded

            flag=0
            for n in G.nodes():
                if G.node[n]["label"]==doctor:
                    doctor_node_number=n    # i find the new doctor's node number   
                    flag=1
                    break
            if flag==0:
                print " doesnt belong to the department!"

            else:
                for node in G.nodes():       
                    if G.node[node]['type']=="shift" :
                        if doctor_node_number in G.neighbors(node):  # i check all shifts the new adopter was working on                            
                            
                            date=G.node[node]["label"] # i get the date of that particular shift
                            if " " in date:            # for the weekday shifts
                                date_parts=date.split(" ")[0].split("/")
                                mm=int(date_parts[0])                    
                                dd=int(date_parts[1])
                                yy=2000+int(date_parts[2])
                                date_shift=datetime(yy,mm,dd)
                                
                            else:                     # for the weekends
                                date_parts=date.split("/")
                                mm=int(date_parts[0])                    
                                dd=int(date_parts[1])
                                yy=2000+int(date_parts[2])
                                date_shift=datetime(yy,mm,dd)
                                

                            if  date_shift >= seeding_datetime:  # i only care if they have worked together AFTER the seeding_date         
                       
                                print doctor,"was working on:", G.node[node]['label'],  "and date_shift >= seeding_datetime"

                                new_adopter_date= dicc_doctors[doctor] #i get the adoption date for the new adopter (it is type datetime already)
                                   

                                count_adopters=0
                                for adopter in initial_adopters:
                                    for n in G.nodes():
                                        if G.node[n]["label"]==adopter:
                                            adopter_node_number=n     # i find the new adopter's node number                                      
                                            break

                                    if adopter_node_number in G.neighbors(node):  # an adopter was working with the new adopter
                                        count_adopters+=1                                                                       
                                        print adopter,"(initial adopter) and", doctor, "(new adopter) where working together on ", date_shift
                                                                        
                                                                                                     
                                        if date_shift <= new_adopter_date:
                                            print adopter, "       PROBABLY TOLD", doctor,"!!!!!"
                                                                                                                        
                                        else:
                                            print "       date_common_shift > new_adopter_date, so we dont know who told ",doctor
                               
                                if  count_adopters==0:
                                    print "      but he wasnt in contact with any adopters, so we dont know who told ",doctor           

                            else:
                                pass
                                #print "      but date_shift < seeding_datetime, so we dont know who told ",doctor
                                #print "shift date:",date_shift ,"seeding datetime:",seeding_datetime
            
            

            initial_adopters.append(doctor) # once i have studied an new adopter, he becomes and initial adopter for the other new adopters
            print "initial_adopters",initial_adopters
            raw_input()
        
        else:
            print "was initially seeded on", seeding_datetime               
                     
                        

       












##################################################
######################################
if __name__ == '__main__':
    if len(sys.argv) > 2:
        graph_filename = sys.argv[1]
        data_file=sys.argv[2]
   
        main(graph_filename,data_file)
    else:
        print "Usage: python script.py path/network.gml path/datafile"

    
 ## the datafile is:  list_dates_and_names_current_adopters.txt  (created with: extract_real_evolution_number_adopters.py)
