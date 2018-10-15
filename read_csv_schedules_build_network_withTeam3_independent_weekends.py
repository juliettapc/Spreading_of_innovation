#! /usr/bin/env python


"""
Code to read the csv with the resident schedule and the Attendings+Fellow schedule and create the network corresponding to the shifts and according to the doctor's hierarchy.
It takes the filename.csv from command line and returns a .gml file.


Created by Julia Poncela, July 2011.

"""

import csv
import networkx as nx
import numpy
import sys
import datetime 
import matplotlib.pyplot as plt


def main(filename_AttgFellow):

   

    G=nx.Graph()



#######################
#####Adding the nodes:#
#######################


   
    dict_months={}
    dict_months['Oct.']=10
    dict_months['Nov.']=11
    dict_months['Dec.']=12
    dict_months['Jan.']=1
    dict_months['Feb.']=2
    dict_months['Mar.']=3
    dict_months['Apr.']=4
    dict_months['May ']=5
    dict_months['June']=6
   
    year=2011
   
    seeding_date=datetime.datetime(2011,10,31)   # to give shift a chronological  order
    first_date_csv=datetime.datetime(2011,10,3)
    last_date_csv=datetime.datetime(2012,6,30)

    print "tot number days csv schedule: ", (last_date_csv-first_date_csv).days+1    # 272 days

    print "tot number days since seeding: ", (last_date_csv-seeding_date).days+1    # 244 days

    print "time difference between first date and seeding date: ", (seeding_date-first_date_csv).days+1   #27 dias

   #OJO!!! PQ LAS SIMULACIONES DE NICOLAS PEYATTE VAN DESDE EL PRINCIPIO DEL ARCHIVO CSV, NO DESDE EL SEEDING DATE
   #adding nodes for the Attendings and Fellows:   
    result_att_fellows= csv.reader(open(filename_AttgFellow, 'rb'), delimiter=',')
 
    list_colums_att=[3,7,10] # colums with Attending last_names
    list_colums_fellow=[1,5,9] # colums with Fellow  last_names  

    
    contador_lineas=-1
    list_atts=[]
    list_fellows=[]
   

  
    for row in result_att_fellows:        
        if len(row[0]) >0:
            #raw_input()
            
            period_time=row[0]

            first_day= period_time.split("-")[0]
            print first_day
            month=first_day[0:4]  # the first part of the string is the month
            month=int(dict_months[month])   # i transform the string of the month into the corresponding number
            if month==1 or month==2 or  month==3 or month==4 or  month==5 or month==6 :
                year=2012
            else:
                year=2011

            day=int(first_day[4:].strip())  # i remove any spaces
            date1=datetime.datetime(year,month, day)
            label_date1=str(year)+"/"+str(month)+"/"+str(day)
            print date1
            


            last_day= period_time.split("-")[1]
            #print last_day
            month=last_day[0:4]  # the first part of the string is the month
            month=int(dict_months[month])   # i transform the string of the month into the corresponding number
            if month==1 or month==2 or  month==3 or month==4 or  month==5 or month==6 :
                year=2012
            else:
                year=2011

            day=int(last_day[4:].strip())  # i remove any spaces
            date2=datetime.datetime(year,month, day)
            label_date2=str(year)+"/"+str(month)+"/"+str(day)
           # print date2
           



            F1=row[1]   # in the weekends, F1=F2!!!!!!!! so it is just one team
            A1=row[3]

            F2=row[5]
            A2=row[7]



            G.add_node(F1)                    
            G.node[F1]["type"]="F"          
            G.add_node(A1)
            G.node[A1]["type"]="A"  

            G.add_node(F2)          # if F1=F2, it doesnt add a duplicate node, it just overwrites it   
            G.node[F2]["type"]="F"     
            G.add_node(A2)
            G.node[A2]["type"]="A" 


            label_date1_T1=label_date1+" T1"
            label_date1_T2=label_date1+" T2"   # two teams for weekdays
            #label_date1_T1T2=label_date1+" T1T2"   # one team for weekends

           
           



           
            if len(row[8])>0:  #if there is a T3  (that only affects the weekday schedules)
                F3=row[9]
                A3=row[10]

               


                G.add_node(F3)                    
                G.node[F3]["type"]="F"          
                G.add_node(A3)
                G.node[A3]["type"]="A"    
                

                label_date1_T3=label_date1+" T3"   # because Team3 is completely independent!!!!
                G.add_node(label_date1_T3)

                G.node[label_date1_T3]["type"]="shift" 
                G.node[label_date1_T3]["team"]="T3"
                G.node[label_date1_T3]["shift_lenght"]=(date2-date1).days+1
                G.node[label_date1_T3]["order"]=(date1-seeding_date).days

               # print "week with T3: ",label_date1_T3,"  ",G.node[label_date1_T3]["shift_lenght"],G.node[label_date1_T3]["order"]
                    

                G.add_edge(F3,label_date1_T3)
                G.add_edge(A3,label_date1_T3)

                print "link:", F3,label_date1_T3
                print "link:", A3,label_date1_T3,G.node[label_date1_T3]["order"]

                #print "  ", F3, A3, "working together on shift", label_date1_T3
           



##                if F1==F2: #weekend                                                                  
##
##                    G.add_node(label_date1_T1T2)
##
##
##                    G.node[label_date1_T1T2]["type"]="shift"     
##                    G.node[label_date1_T1T2]["team"]="T1T2_w" 
##                    G.node[label_date1_T1T2]["shift_lenght"]=(date2-date1).days+1            
##                    G.node[label_date1_T1T2]["order"]=(date1-seeding_date).days

           

##                    G.add_edge(F1,label_date1_T1T2)
##                    G.add_edge(A1,label_date1_T1T2)
##                   G.add_edge(A2,label_date1_T1T2)

##                    print "link:", F1,label_date1_T1T2
##                    print "link:", A1,label_date1_T1T2
##                    print "link:", A2,label_date1_T1T2


                   # print "week with T3: WEEKEND:  ",label_date1_T1T2,"  ",G.node[label_date1_T1T2]["shift_lenght"],G.node[label_date1_T1T2]["order"]
                    
                    #print "  ", F1, A1,A2, "working together on shift", label_date1_T1T2

##                else:  # weekday

                G.add_node(label_date1_T1)
                G.add_node(label_date1_T2)
                    
                    
                G.node[label_date1_T1]["type"]="shift"    #T1
                G.node[label_date1_T1]["team"]="T1" 
                G.node[label_date1_T1]["shift_lenght"]=(date2-date1).days+1            
                G.node[label_date1_T1]["order"]=(date1-seeding_date).days
                    
                    
                G.node[label_date1_T2]["type"]="shift"     #T2
                G.node[label_date1_T2]["team"]="T2"
                G.node[label_date1_T2]["shift_lenght"]=(date2-date1).days+1            
                G.node[label_date1_T2]["order"]=(date1-seeding_date).days
                    

    # what about the order???   does it need to be different for T1 and T2??


                G.add_edge(F1,label_date1_T1)
                G.add_edge(A1,label_date1_T1)
                G.add_edge(F2,label_date1_T2)
                G.add_edge(A2,label_date1_T2)  
                                          
                print "link:", F1,label_date1_T1
                print "link:", A1,label_date1_T1,G.node[label_date1_T1]["order"]
                print "link:", F2,label_date1_T2
                print "link:", A2,label_date1_T2,G.node[label_date1_T2]["order"]


                    #print "week with T3: WEEKDAY:  ",label_date1_T1,"  ",G.node[label_date1_T1]["shift_lenght"],G.node[label_date1_T1]["order"], "and",label_date1_T2,"  ",G.node[label_date1_T2]["shift_lenght"],G.node[label_date1_T2]["order"]
           
                    #print "  ", F1, A1, "working together on shift", label_date1_T1,"  and ", F2, A2, "working together on shift", label_date1_T2


            else:   # if there is NO T3

               
##                if F1==F2: #weekend      (special case on May 28, Rosario is working on a weekday on both teams!!)  


##                    G.add_node(label_date1_T1T2)


##                    G.node[label_date1_T1T2]["type"]="shift"     
##                    G.node[label_date1_T1T2]["team"]="T1T2_w" 
##                    G.node[label_date1_T1T2]["shift_lenght"]=(date2-date1).days+1            
##                    G.node[label_date1_T1T2]["order"]=(date1-seeding_date).days

           

##                    G.add_edge(F1,label_date1_T1T2)
##                    G.add_edge(A1,label_date1_T1T2)
##                    G.add_edge(A2,label_date1_T1T2)

##                    print "link:", F1,label_date1_T1T2
##                    print "link:", A1,label_date1_T1T2
##                    print "link:", A2,label_date1_T1T2

                   # print "week without T3: WEEKEND:  ",label_date1_T1T2,"  ",G.node[label_date1_T1T2]["shift_lenght"],G.node[label_date1_T1T2]["order"]
           
                    #print "  ", F1, A1,A2, "working together on shift", label_date1_T1T2

##                else: # weekday


                    G.add_node(label_date1_T1)
                    G.add_node(label_date1_T2)
                    
                    
                    G.node[label_date1_T1]["type"]="shift"    #T1
                    G.node[label_date1_T1]["team"]="T1" 
                    G.node[label_date1_T1]["shift_lenght"]=(date2-date1).days+1            
                    G.node[label_date1_T1]["order"]=(date1-seeding_date).days
                    
                    
                    G.node[label_date1_T2]["type"]="shift"     #T2
                    G.node[label_date1_T2]["team"]="T2"
                    G.node[label_date1_T2]["shift_lenght"]=(date2-date1).days+1            
                    G.node[label_date1_T2]["order"]=(date1-seeding_date).days
                    


        # what about the order???  does it need to be different for T1 and T2??




                    G.add_edge(F1,label_date1_T1)
                    G.add_edge(A1,label_date1_T1)
                    G.add_edge(F2,label_date1_T2)
                    G.add_edge(A2,label_date1_T2)   
    


                    print "link:", F1,label_date1_T1
                    print "link:", A1,label_date1_T1,G.node[label_date1_T1]["order"]
                    print "link:", F2,label_date1_T2
                    print "link:", A2,label_date1_T2,G.node[label_date1_T2]["order"]



                   # print "week without T3: WEEKDAY:  ",label_date1_T1,"  ",G.node[label_date1_T1]["shift_lenght"],G.node[label_date1_T1]["order"], "and",label_date1_T2,"  ",G.node[label_date1_T2]["shift_lenght"],G.node[label_date1_T2]["order"]
           
                    #print "  ", F1, A1, "working together on shift", label_date1_T1,"  and ", F2, A2, "working together on shift", label_date1_T2
           
                   







##################################
#writing the network into a file:#
##################################

    networkfile=  "../Results/Doctors_shifts_network_withT3_independent_weekends_.gml"
    nx.write_gml(G,networkfile) #  you run the code from  Idea-Spread-Hospital/Code/.

    print "\nwritten network file:",   networkfile


########################
# plotting the network:#
########################




            

########################################
if __name__== "__main__":   
    
    if len(sys.argv) > 1:
        
        filename_AttgFellow = sys.argv[1]

        main(filename_AttgFellow)
    else:
        print "usage: python script_name   path/csv_filename_AttgFellow "

######################################
