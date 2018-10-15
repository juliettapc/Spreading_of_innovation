#!/usr/bin/env python

"""
Code to read the csv with the info of who is ordering Procalcitonin
and create a data file with the evolution of the number of adopter doctors.


Created by Julia Poncela, November 2011.

"""

import csv
import networkx as nx
import numpy
import sys
from datetime import *
import matplotlib.pyplot as plt


def main(data_filename):
 
   

# OJO!! primero tengo que limpiar la hoja de EXCEll (quitar texto blablabla), y tb ordenar por la fecha del pedido del Procalcitonin (columna "Order Time procalcitonin"), y despues guardar en formato .csv para leerlo desde aki.

    list_Attendings_ICU=["Russell","Budinger","Dematte","Weiss","Kamp","Moore","Sporn","Prickett","Wolfe","Rosenberg","Gillespie","Hawkins","Glassroth","Radigan","Corbridge","Cuttica","Jain","Lam","Wunderink","Kalhan","Mutlu","Becker","Gates",]   # to compare and exclude outside-ICU personnel


    list_Fellows_ICU=["Smith","Rosario","Osher","Hutchison","Schroedl","Shah","Luqman","Go","Marouni","Jaitovich","Keller",]


    results= csv.reader(open(data_filename, 'r'), delimiter=',')   
    reader = csv.DictReader(open(data_filename))
    csv_resident_headers = reader.fieldnames

    dir="../Results/"

    output_file=dir +"Real_Time_evolution_number_adopters.txt"      
    output_fileICU=dir +"Real_Time_evolution_number_adopters_ICU.txt"      
    output_file1=dir +"list_dates_and_names_current_adopters.txt"        
    


    


    year=2011   #real seeding date
    month=10
    day=31
    seeding_date=datetime(year, month, day)



    dicc_days_num_orders={}  # i create a dicc of dates and number of orders that day
    dicc_days_num_adopters={}  # i create a dicc of dates and cummulative number of adopters that day
    dicc_days_NEW_adopters={}  # i create a dicc of dates and list of adopters that day
    dicc_days_cumul_num_orders={}

    dicc_days_num_ICU_orders={} 
    dicc_days_num_ICU_adopters={}
    dicc_days_cumul_num_ICU_orders={}

    for row in results:
        #if row != csv_resident_headers:  # i exclude the first row 
        try:


            date=str(row[12])           
  
          #  print date
            parts=date.split(" ")[0]  
            parts=parts.split("/")
            mm=int(parts[0])
            dd=int(parts[1])
            yy=int(parts[2])                    
            date_order=datetime(yy,mm,dd)
            
            
            dicc_days_num_orders[date_order]=0  # to count how many orders are made in every day
            dicc_days_num_adopters[date_order]=0  # to count how many doctors are adopters in every day
            dicc_days_cumul_num_orders[date_order]=0

            
            dicc_days_num_ICU_orders[date_order]=0  # to count how many orders are made in every day
            dicc_days_num_ICU_adopters[date_order]=0  # to count how many doctors are adopters in every day
            dicc_days_cumul_num_ICU_orders[date_order]=0


        except ValueError: pass
        

#remember!!! every time that i wanna read the csv file, i must read it AGAIN!!
    results= csv.reader(open(data_filename, 'r'), delimiter=',')   
    reader = csv.DictReader(open(data_filename))
    csv_resident_headers = reader.fieldnames

    cont_lines=0

    list_attendings=[]
    for row in results:       
        try:          

            cont_lines+=1 

            date=str(row[12])          ##  OJO!!!!!! REVISAR EL NUMERO DE ESTA COLUMNA PQ PUEDE SER DISTINTO DE UN ARCHIVO DE DATOS A OTROS       
            parts=date.split(" ")[0]  
            parts=parts.split("/")
           
            mm=int(parts[0])
            dd=int(parts[1])
            yy=int(parts[2])                    
            date_order=datetime(yy,mm,dd)                                  

            
            time_diff=(date_order-seeding_date)           

            attending=str(row[10]).split(" ")[0].strip(",").capitalize() #attenging in charge of the shift
            dr_who_ordered=str(row[11]).split(" ")[0].strip(",").capitalize() #actual doctor ordering procalcitonin 


            

            dicc_days_num_orders[date_order]+=1  # i add one order to the count of that day

            print date_order, dicc_days_num_orders[date_order]

            if attending in list_Attendings_ICU:
                dicc_days_num_ICU_orders[date_order]+=1


           # if (dr_who_ordered in list_Fellows_ICU) or (dr_who_ordered in list_Attendings_ICU):                
               # print "we've got a fellow!", dr_who_ordered,date_order,(date_order-seeding_date).days
               
                
    

            for key in sorted(dicc_days_cumul_num_orders):      # cumulative counts                
                if key >=  date_order:                          
                    dicc_days_cumul_num_orders[key]+=1 # (i add one adopter to the count of that day all all following days)

                    if (attending in list_Attendings_ICU) or (dr_who_ordered in list_Fellows_ICU):
                        dicc_days_cumul_num_ICU_orders[key]+=1
                         
           
            if attending not in list_attendings:
                list_attendings.append(attending) 
                dicc_days_NEW_adopters[date_order]=[]
                for i in list_attendings:
                    dicc_days_NEW_adopters[date_order].append(i)  # to count how many doctors are adopters in every day

                #print list_attendings, date_order # i print the date when a new adopter appears, and also the whole list of adopters at that point

                for key in sorted(dicc_days_num_adopters):                      
                    if key >=  date_order:                          
                        dicc_days_num_adopters[key]+=1 # i add one adopter to the count of that day all all following days
                       
                        if attending in list_Attendings_ICU:
                            dicc_days_num_ICU_adopters[key]+=1
                        if (dr_who_ordered in list_Fellows_ICU) or ((dr_who_ordered in list_Attendings_ICU) and attending!= dr_who_ordered):
                            dicc_days_num_ICU_adopters[key]+=1
                            dicc_days_num_adopters[key]+=1


        except ValueError: pass
   

   
    file = open(output_file,'wt')      
    for key in sorted(dicc_days_num_orders):   #the index is the keys, not the pairs key:value !!!!!
        print "day",(key-seeding_date).days,":   ",dicc_days_num_adopters[key], dicc_days_num_orders[key],dicc_days_cumul_num_orders[key], key
        print >> file, (key-seeding_date).days, dicc_days_num_adopters[key],dicc_days_num_orders[key],dicc_days_cumul_num_orders[key],key
    file.close()  

    print "\n ICU only:"
    

    file = open(output_fileICU,'wt')      
    for key in sorted(dicc_days_num_ICU_orders):   #the index is the keys, not the pairs key:value !!!!!
        print "day",(key-seeding_date).days,":   ",dicc_days_num_ICU_adopters[key], dicc_days_num_ICU_orders[key],dicc_days_cumul_num_ICU_orders[key], key
        print >> file, (key-seeding_date).days, dicc_days_num_ICU_adopters[key],dicc_days_num_ICU_orders[key],dicc_days_cumul_num_ICU_orders[key],key
    file.close()  

   
    print "# lines: ",cont_lines, "dict. lenght: ",len(dicc_days_num_orders)



   # print list_attendings


    file1 = open(output_file1,'wt')  
    for key in sorted(dicc_days_NEW_adopters):           
        print >> file1,"\n",key,
       # print"\n",key,
        for i in dicc_days_NEW_adopters[key]:
            print >> file1, i.split(" ")[0].strip(",").capitalize(),
            #print  i.split(" ")[0].strip(",").capitalize(),

    file1.close()



##################################################
######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        data_filename = sys.argv[1]
   
        main(data_filename)
    else:
        print "Usage: python script.py path/datafile.csv"



    
