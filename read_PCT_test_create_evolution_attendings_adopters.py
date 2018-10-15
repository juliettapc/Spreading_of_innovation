#!/usr/bin/env python

'''

Created by Julia Poncela, on January 2013.

'''


import sys
import os
import csv
from datetime import *







def main(filename):



    include_fellows="YES"


    if  include_fellows=="YES":   
        output_file1="../Results/Actual_evolution_adopters_with_fellows.dat"         
    elif  include_fellows=="NO":   
        output_file1="../Results/Actual_evolution_adopters_NO_fellows_only_attendings.dat"        

    file1 = open(output_file1,'wt')    
    


   # list_fellows=["SMITH","OSHER","ROSARIO","HUTCHISON","MAROUNI","LENNON","SCHROEDL","GO","SHAH","LUQMAN","DELACRUZ","JAITOVICH","KELLER"]


    seeding_datetime=datetime(2011,10,31)
    old_date=seeding_datetime

    list_adopters=['WUNDERINK','WEISS']   # initially
    old_num_adopters=2


    result_actual_file= csv.reader(open(filename, 'rb'), delimiter=',')
    
    list_pairs_day_num_tot_num_adopters=[]
    list_pairs_day_num_tot_num_adopters.append([1,2])  # initial conditions: Weiss and Wunderink as adopters at day one


    list_fellows=[]
    list_attendings=['WUNDERINK','WEISS']
    dict_days_num_adopt={}
    for row in result_actual_file: 
        list_pairs=[]
        type_dr=str(row[-1])
        
        adopter=row[0].split(",")[0]


        if type_dr=="A":
            if adopter not in list_attendings:
                list_attendings.append(adopter)
            
            if adopter not in list_adopters:
                list_adopters.append(adopter)

        elif type_dr=="F":                   
            if include_fellows=="YES":   
                if adopter not in list_adopters:
                    list_adopters.append(adopter)          
                if adopter not in list_fellows:
                    list_fellows.append(adopter)
               

        string_date=row[1].split(" ")[0]
        parts_date=string_date.split("/")                
        yy=int(parts_date[2])                    
        mm=int(parts_date[0])
        dd=int(parts_date[1])
        date_order=datetime(yy,mm,dd)

        print date_order,(date_order-seeding_datetime).days+1, adopter,len(list_adopters)


       # print string_date,date_order, (date_order-seeding_datetime).days+1,adopter,len(list_adopters)

        list_pairs.append((date_order-seeding_datetime).days+1)
        list_pairs.append(len(list_adopters))

        list_pairs_day_num_tot_num_adopters.append(list_pairs)

        dict_days_num_adopt[(date_order-seeding_datetime).days+1]=len(list_adopters)  # this overwrites, old lover number of adopters if several orders the same day




    # i am done reading the file, now i process it


    raw_input()
    maximo=0
    for item in dict_days_num_adopt:   # i find the last day of the datafile
        if item>=maximo:
            maximo=item

    print maximo


  
  
   
    old_num_adopt=2
    maximo+=2  # i need at time=0 and t=max+1 to match the way the persuasion/infection dynamics codes are written
    for time in range(maximo):   # cos rage(i) goes until i-1
        
            print  time,
            print >> file1, time,
            try:
                print dict_days_num_adopt[time]
                print >> file1,dict_days_num_adopt[time]
                old_num_adopt=dict_days_num_adopt[time]
            except KeyError:
                print   old_num_adopt,"nothing new"
                print   >> file1,old_num_adopt
          

        
    print "printed out file: ",output_file1
    file1.close()
   

    print "fellows:",len(list_fellows),"  attendings:",len(list_attendings)

##################################################
######################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
   
        main(filename)
    else:
        print "Usage: python script.py path/csv_filename"

    
