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
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt


def main(cvs_filename_orders,csv_filename_schedule):
 
   

# OJO!! primero tengo que limpiar la hoja de EXCEll (quitar texto blablabla), y tb ordenar por la fecha del pedido del Procalcitonin (columna "Order Time procalcitonin"), y despues guardar en formato .csv para leerlo desde aki.

    list_Attendings_ICU=["Russell","Budinger","Dematte","Weiss","Kamp","Moore","Sporn","Prickett","Wolfe","Rosenberg","Gillespie","Hawkins","Glassroth","Radigan","Corbridge","Cuttica","Jain","Lam","Wunderink","Kalhan","Mutlu","Becker","Gates",]   # to compare and exclude outside-ICU personnel


    list_Fellows_ICU=["Smith","Rosario","Osher","Hutchison","Schroedl","Shah","Luqman","Go","Marouni","Jaitovich","Keller",]


    

    dir="../Results/"

    output_file=dir +"Real_Time_evolution_number_adopters.txt"      
    output_fileICU=dir +"Real_Time_evolution_number_adopters_ICU.txt"      
    output_file1=dir +"list_dates_and_names_current_adopters.txt"        

    output_file_orders=dir +"simple_list_order_dates_drs.txt"        
    


    


    year=2011   #real seeding date
    month=10
    day=31
    seeding_date=datetime(year, month, day)
   

    end_date=datetime(2012, 9, 2)   #end schedule file






    ################### # i create a dictionary dates:num_dr_on_call_so_far
    results= csv.reader(open(csv_filename_schedule, 'r'), delimiter=',')   
    reader = csv.DictReader(open(csv_filename_schedule))
    csv_header = reader.fieldnames

    dicc_days_cumul_num_dr={}  # i create a dicc of dates and cummulative number of dr that have worked until that day
    dicc_days_cumul_num_Att={} 
    dicc_days_cumul_num_F={}

    list_on_call_dr_so_far=[]    
    list_on_call_Att_so_far=[]    
    list_on_call_F_so_far=[]    
    


   
    date=seeding_date
    while date <= end_date:
        
        dicc_days_cumul_num_dr[date]=0  # i create an empty dicc of dates for the cummulative number of dr that have worked until that day
        dicc_days_cumul_num_Att[date]=0
        dicc_days_cumul_num_F[date]=0

        date=date+relativedelta(days=+1)


        

    for row in results:  

 
        try:
            date_raw=str(row[0])  # date and time both ##  OJO!!!!!! REVISAR EL NUMERO DE ESTA COLUMNA PQ PUEDE SER DISTINTO DE UN ARCHIVO DE DATOS A OTROS       
            
            
            parts=date_raw.split("/")
            mm=int(parts[0])
            dd=int(parts[1])
            yy=int(parts[2])                    
            date=datetime(2000+yy,mm,dd)

#  date=datetime.strptime(date_raw, "%m/%d/%y")  #another way of doint it
        
        
        except ValueError: pass
        
        
        if ( (row != csv_header )  and (date >= seeding_date)  ):  # i exclude the first row  and all entries prior to the seeding date
            
  
           
            attending1=str(row[1])
            fellow1=str(row[2])
            attending2=str(row[3])
            fellow2=str(row[4])

           
            num_new_dr_that_week=0           # for the weekdays
            num_new_Att_that_week=0
            num_new_F_that_week=0
            if  (attending1 not in  list_on_call_dr_so_far):
                num_new_dr_that_week+=1               
                list_on_call_dr_so_far.append(attending1)

            if  (attending1 not in  list_on_call_Att_so_far):
                num_new_Att_that_week+=1
                list_on_call_Att_so_far.append(attending1)


            if (attending2 not in  list_on_call_dr_so_far):
                num_new_dr_that_week+=1                
                list_on_call_dr_so_far.append(attending2)

            if  (attending2 not in  list_on_call_Att_so_far):
                num_new_Att_that_week+=1
                list_on_call_Att_so_far.append(attending2)


            if (fellow1 not in  list_on_call_dr_so_far):
                num_new_dr_that_week+=1
                list_on_call_dr_so_far.append(fellow1)

            if  (fellow1 not in  list_on_call_F_so_far):
                num_new_F_that_week+=1
                list_on_call_F_so_far.append(fellow1)

            if (fellow2 not in  list_on_call_dr_so_far) :
                num_new_dr_that_week+=1               
                list_on_call_dr_so_far.append(fellow2)
 
            if  (fellow2 not in  list_on_call_F_so_far):
                num_new_F_that_week+=1
                list_on_call_F_so_far.append(fellow2)


            #print "tot:",list_on_call_dr_so_far, date
            #print "Att:",list_on_call_Att_so_far
            #print "F:",list_on_call_F_so_far

          

            aux_date=date           
            while aux_date <= end_date:
                try:
                    dicc_days_cumul_num_dr[aux_date]+=num_new_dr_that_week    # i add one new doctor on call so far to that date and all the following dates
                    dicc_days_cumul_num_Att[aux_date]+=num_new_Att_that_week  
                    dicc_days_cumul_num_F[aux_date]+=num_new_F_that_week

                except KeyError: pass

                aux_date=aux_date+relativedelta(days=+1)

        ###

            date_raw=str(row[8])  # date and time both ##  OJO!!!!!! REVISAR EL NUMERO DE ESTA COLUMNA PQ PUEDE SER DISTINTO DE UN ARCHIVO DE DATOS A OTROS       
         
            
            parts=date_raw.split("/")
            mm=int(parts[0])
            dd=int(parts[1])
            yy=int(parts[2])                    
            date=datetime(2000+yy,mm,dd)

            attending_w1=str(row[9])    #for the weekend
            attending_w2=str(row[10])
            fellow_w=str(row[11])
            

            num_new_dr_that_weekend=0
            num_new_Att_that_weekend=0
            num_new_F_that_weekend=0
            if  (attending_w1 not in  list_on_call_dr_so_far):
                num_new_dr_that_weekend+=1               
                list_on_call_dr_so_far.append(attending_w1)

            if  (attending_w1 not in  list_on_call_Att_so_far):
                num_new_Att_that_weekend+=1
                list_on_call_Att_so_far.append(attending_w1)


            if (attending_w2 not in  list_on_call_dr_so_far):
                num_new_dr_that_weekend+=1                
                list_on_call_dr_so_far.append(attending_w2)

            if  (attending_w2 not in  list_on_call_Att_so_far):
                num_new_Att_that_weekend+=1
                list_on_call_Att_so_far.append(attending_w2)


            if (fellow_w not in  list_on_call_dr_so_far):
                num_new_dr_that_weekend+=1
                list_on_call_dr_so_far.append(fellow_w)

            if  (fellow_w not in  list_on_call_F_so_far):
                num_new_F_that_weekend+=1
                list_on_call_F_so_far.append(fellow_w)



           # print "w tot:",list_on_call_dr_so_far, date
            #print "w Att:",list_on_call_Att_so_far
            #print "w F:",list_on_call_F_so_far

            #raw_input()

            aux_date=date           
            while aux_date <= end_date:

                
                try:
                    dicc_days_cumul_num_dr[aux_date]+=num_new_dr_that_weekend    # i add one new doctor on call so far to that date and all the following dates
                    dicc_days_cumul_num_Att[aux_date]+=num_new_Att_that_weekend  
                    dicc_days_cumul_num_F[aux_date]+=num_new_F_that_weekend


                    #print aux_date,num_new_dr_that_week,num_new_dr_that_weekend ,dicc_days_cumul_num_dr[aux_date]
                    #raw_input()

                except KeyError: pass

 
                aux_date=aux_date+relativedelta(days=+1)







           
           

   # for key in sorted(dicc_days_cumul_num_dr) :
    #    print key, dicc_days_cumul_num_dr[key]
     #   raw_input()

     
    ###################   


    ################### # i create empty dictionaries  dates:num_orders etc
    results= csv.reader(open(cvs_filename_orders, 'r'), delimiter=',')   
    reader = csv.DictReader(open(cvs_filename_orders))
    csv_header = reader.fieldnames

    dicc_days_num_orders={}  # i create a dicc of dates and number of orders that day
    dicc_days_num_adopters={}  # i create a dicc of dates and cummulative number of adopters that day
    dicc_days_NEW_adopters={}  # i create a dicc of dates and list of adopters that day
    dicc_days_cumul_num_orders={}

    dicc_days_num_ICU_orders={} 
    dicc_days_num_ICU_adopters={}
    dicc_days_cumul_num_ICU_orders={}

    for row in results:  

        #if row != csv_header:  # i exclude the first row 
        try:



            date=str(row[12])  # date and time both ##  OJO!!!!!! REVISAR EL NUMERO DE ESTA COLUMNA PQ PUEDE SER DISTINTO DE UN ARCHIVO DE DATOS A OTROS       
         
  
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
    ###################   i fill the dictionaries


                                                           
    results= csv.reader(open(cvs_filename_orders, 'r'), delimiter=',')   #remember!!! every time that i wanna access the csv file, i must read it AGAIN!!
    reader = csv.DictReader(open(cvs_filename_orders))
    csv_header = reader.fieldnames
   




    file_orders = open(output_file_orders,'wt')      
          

    previous_date=None   
    cont=0
    list_attendings=[]
    for row in results:       
        if row != csv_header:  # i exclude the first row
                      
              

                     ##  OJO!!!!!! REVISAR EL NUMERO DE ESTAs COLUMNAs PQ PUEDE SER DISTINTO DE UN ARCHIVO DE DATOS A OTRO       

            date=str(row[12])       # date and time both    
            parts=date.split(" ")[0]  
            parts=parts.split("/")
           
            mm=int(parts[0])
            dd=int(parts[1])
            yy=int(parts[2])                    
            date_order=datetime(yy,mm,dd)                                  

            
            time_diff=(date_order-seeding_date)           

            attending=str(row[10]).split(" ")[0].strip(",").capitalize() #attenging in charge of the shift
            dr_who_ordered=str(row[11]).split(" ")[0].strip(",").capitalize() #actual doctor ordering procalcitonin 
            patient=str(row[0])
            PCT_result=row[13]
            

            if ("NEIL"  in row[11]):  # Neil Rosenberg is not the same Rosenberg from the ATTENDING LIST
                dr_who_ordered=str(row[11])
               

              

            if (date != previous_date):# with this condition is enough to remove duplicated order!  

                print date, previous_date    

          



                dicc_days_num_orders[date_order]+=1  # i add one order to the count of that day

                if attending in list_Attendings_ICU:
                    dicc_days_num_ICU_orders[date_order]+=1



                    if "Emergency" not in attending:
                        print >> file_orders, attending, date.split(" ")[0]




                if (dr_who_ordered in list_Fellows_ICU) or (dr_who_ordered in list_Attendings_ICU):                
                    print "we've got a fellow!", dr_who_ordered,date_order,(date_order-seeding_date).days

                    if "Emergency" not in attending:
                        print >> file_orders, dr_who_ordered, date.split(" ")[0]
        

                for key in sorted(dicc_days_cumul_num_orders):      # cumulative counts                
                    if key >=  date_order:                          
                        dicc_days_cumul_num_orders[key]+=1 # (i add one adopter to the count of that day all all following days)

                        if (  (attending in list_Attendings_ICU) or (dr_who_ordered in list_Fellows_ICU)  ):
                            dicc_days_cumul_num_ICU_orders[key]+=1

                       
                         
           
                if (   (attending not in list_attendings)   and ("Emergency" not in attending)  ):
                    list_attendings.append(attending) 
                    dicc_days_NEW_adopters[date_order]=[]
                    for i in list_attendings:
                        dicc_days_NEW_adopters[date_order].append(i)  # to count how many doctors are adopters in every day

            
                    for key in sorted(dicc_days_num_adopters):                      
                        if key >=  date_order:                          
                            dicc_days_num_adopters[key]+=1 # i add one adopter to the count of that day all all following days
                       
                            if attending in list_Attendings_ICU:
                                dicc_days_num_ICU_adopters[key]+=1
                            if (dr_who_ordered in list_Fellows_ICU) or ((dr_who_ordered in list_Attendings_ICU) and attending!= dr_who_ordered):
                                dicc_days_num_ICU_adopters[key]+=1
                                dicc_days_num_adopters[key]+=1



            
            previous_date=date   # to check if i have duplicated entries of the same order! (every time but the first row)           
            cont+=1


   
    file_orders.close()  




    file = open(output_file,'wt')      
    for key in sorted(dicc_days_num_orders):   #the index is the keys, not the pairs key:value !!!!!
        print "day",(key-seeding_date).days,":   ",dicc_days_num_adopters[key], dicc_days_num_orders[key],dicc_days_cumul_num_orders[key], key
        print >> file, (key-seeding_date).days, dicc_days_num_adopters[key],dicc_days_num_orders[key],dicc_days_cumul_num_orders[key],key
    file.close()  

    print "\n ICU only:"
    

    file = open(output_fileICU,'wt')      
    for key in sorted(dicc_days_num_ICU_orders):   #the index is the keys, not the pairs key:value !!!!!
        print "day",(key-seeding_date).days,":   ", dicc_days_num_ICU_adopters[key],dicc_days_cumul_num_dr[key],dicc_days_cumul_num_Att[key],dicc_days_cumul_num_F[key],float(dicc_days_num_ICU_adopters[key])/float(dicc_days_cumul_num_Att[key]),dicc_days_num_ICU_orders[key],dicc_days_cumul_num_ICU_orders[key],key

        print >> file, (key-seeding_date).days, dicc_days_num_ICU_adopters[key],dicc_days_cumul_num_dr[key],dicc_days_cumul_num_Att[key],dicc_days_cumul_num_F[key],float(dicc_days_num_ICU_adopters[key])/float(dicc_days_cumul_num_Att[key]),dicc_days_num_ICU_orders[key],dicc_days_cumul_num_ICU_orders[key],key
    file.close()  

   
    



    print list_attendings


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
    if len(sys.argv) > 2:
        cvs_filename_orders = sys.argv[1]
        csv_filename_schedule = sys.argv[2]
   

        main(cvs_filename_orders,csv_filename_schedule)
    else:
        print "Usage: python   script.py   path/datafile_orders.csv   path/datafile_schedule.csv"



    
