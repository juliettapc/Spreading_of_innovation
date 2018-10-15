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
from datetime import *
import matplotlib.pyplot as plt


def main(filename_residents,filename_AttgFellow):

   

    G=nx.Graph()



#######################
#####Adding the nodes:#
#######################


   
   #adding nodes for the Residents:
    list_residents=[]
    result_residents= csv.reader(open(filename_residents, 'r'), delimiter=',')
   
    reader = csv.DictReader(open(filename_residents))
    csv_resident_headers = reader.fieldnames

    particular_time=timedelta(0)

    list_lists_rows_start_stop=[[1,2,3],[4,5,6],[7,8],[9,10],[11,12],[13,14],[15,16],[17,18],[19,20]]

   
    for row in result_residents:
        if row != csv_resident_headers:  # i exclude the first row  (how to do it more efficintly???)
           
            resident=str(row[0])
            list_time_weekdays=[]
           


            if resident not in list_residents:            
                list_residents.append(resident)   

                G.add_node(resident)
                G.node[resident]["type"]="R"
                G.node[resident]["working_times"]=[]
               
   
     # Assigning start-end working times and teams as attributes for Residents:
            for  shift in list_lists_rows_start_stop:
                
                list1=[]
                   
                start=row[shift[0]]
                stop=row[shift[1]] # CLOSED interval to describe the shifts
                if len(shift)==3:
                    team=row[shift[2]] #rotation start-stop
                else:
                    team=[1,2]  #float start-stop
                    
              
                if len(start)>0:
                   
                    part_times=start.split("/")                
                    mm=int(part_times[0])
                    dd=int(part_times[1])
                    yy=int(part_times[2])                    
                    date_start_week=datetime(yy,mm,dd)
                                        
                    
                    part_times=stop.split("/")                  
                    mm=int(part_times[0])
                    dd=int(part_times[1])
                    yy=int(part_times[2])                    
                    date_end_week=datetime(yy,mm,dd)
                    
                    list1.append(date_start_week)
                    list1.append(date_end_week)      
                    list1.append(team)          
                    G.node[resident]["working_times"].append(list1)
                   
 

   
   #adding nodes for the Attendings and Fellows:   
    result_att_fellows= csv.reader(open(filename_AttgFellow, 'rb'), delimiter=',')
   

    reader = csv.DictReader(open(filename_AttgFellow))
    csv_att_fellow_headers = reader.fieldnames
   

    list_colums_att=[1,3,6,7] # colums with Attending last_names
    list_colums_fellow=[2,4,8] # colums with Fellow  last_names  
 
    list_atts=[]
    list_fellows=[]
    for row in result_att_fellows:  

        if row != csv_att_fellow_headers  : # i exclude the first row  (how to do it more efficintly???)
            



            for i in list_colums_att:
                att=str(row[i])     

                if len(att)>0:     #just in case the field is empty
                    if ","  in att:       # in some fields we have: att1 mm/dd-dd, att2 mm/dd-dd
                        parts=att.split(" ")                        
                        atts=[]
                        atts.append(parts[0])
                        atts.append(parts[2])
                       
                        for a in atts:
                            if a not in list_atts:           
                                list_atts.append(a)

                                G.add_node(a)
                                G.node[a]["type"]="A"                   
                                G.node[a]["working_times"]=[]
               
                                if a in list_fellows:
                                    print "attending:",a,"listed before as fellow"

                    else:
                        if att not in list_atts:           
                            list_atts.append(att)
                            G.add_node(att)
                            G.node[att]["type"]="A" 
                            G.node[att]["working_times"]=[]
               
       
                   
                            if att in list_fellows:
                                print "attending:",att,"listed before as fellow"
                   


            for i in list_colums_fellow:
                fellow=str(row[i])

                if len(fellow)>0:   #just in case the field is empty               
                   
                    if fellow not in list_fellows:           
                        list_fellows.append(fellow)
                        G.add_node(fellow)
                        G.node[fellow]["type"]="F"
                        G.node[fellow]["working_times"]=[]
               

                   
                        if fellow in list_atts:
                            print "fellows:",fellow,"listed before as attending"



 # Assigning start-end working times and teams as attributes for Atts & Fellows:
            if len(row[0])>0:

                att1=str(row[1])   # weekday personnel
                fellow1=str(row[2])
                att2=str(row[3])
                fellow2=str(row[4])

                w_att1=str(row[6])  # weekend personnel               
                w_att2=str(row[7])
                w_fellow=str(row[8])

                #print att1,fellow1,att2,fellow2, w_att1, w_att2,w_fellow

               
                list_time_weekdays=[]
                list_time_weekend=[]     


                start_week= row[0]                            
                part_times=start_week.split("/")                
                mm=int(part_times[0])
                dd=int(part_times[1])
                yy=2000+int(part_times[2])                    
                date_start_week=datetime(yy,mm,dd)


                end_week= row[5] # CLOSED interval to describe the shifts
                part_times=end_week.split("/")                  
                mm=int(part_times[0])
                dd=int(part_times[1])
                yy=2000+int(part_times[2])                    
                date_end_week=datetime(yy,mm,dd)-timedelta(days=1)


                date_start_weeked=datetime(yy,mm,dd)
                date_end_weeked=datetime(yy,mm,dd)+timedelta(days=1) # CLOSED interval to describe the shifts

                list_time_weekdays.append(date_start_week)
                list_time_weekdays.append(date_end_week)
                
                list_time_weekend.append(date_start_weeked)
                list_time_weekend.append(date_end_weeked)
                

                list1=list(list_time_weekdays)  #OJO!!! forma correcta de copiar lista
                list1.append(1)           # para que sean INDEPENDIENTES!!
                G.node[att1]["working_times"].append(list1)
                G.node[fellow1]["working_times"].append(list1)

                list2=list(list_time_weekdays)
                list2.append(2)              
                G.node[fellow2]["working_times"].append(list2)
                                       
                    
                list3=list(list_time_weekend)  
                list3.append(1)          
                G.node[w_att1]["working_times"].append(list3)
                
                list4=list(list_time_weekend)
                list4.append(2)
                G.node[w_att2]["working_times"].append(list4)
                
                
                list5=list(list_time_weekend)  
                list5.append([1,2])
                G.node[w_fellow]["working_times"].append(list5)
                


                if "/" not in att2:  # (for most of the rows, the normal ones)
                                                                                    
                     G.node[att2]["working_times"].append(list2)

                else:  # (for the few special rows: att2 mm/dd-dd, aat2 mm/dd-dd)

                    if "," in att2:
                                           
                       
                        parts=att2.split(" ")                        
                        att2a=parts[0]
                        att2b=parts[2]   
                        date1=parts[1]
                        date2=parts[3]                  
                             
                        list_time_weekdays_special_att2=[]                                  
                        part_times=date1.split("/")                                     
                        mm=int(part_times[0])
                                              
                        part_times[1]=part_times[1].strip(",")                       
                        dd_start=int(part_times[1].split("-")[0])         
                        dd_end=int(part_times[1].split("-")[1])
                        yy=2010         


                        date_start_week_special_att2=datetime(yy,mm,dd_start)
                        date_end_week_special_att2=datetime(yy,mm,dd_end) # CLOSED interval to describe the shifts 
                        
                        
                        list_time_weekdays_special_att2.append(date_start_week_special_att2)
                        list_time_weekdays_special_att2.append(date_end_week_special_att2)
                        list_time_weekdays_special_att2.append(2)  
                        G.node[att2a]["working_times"].append(list_time_weekdays_special_att2)
                        

                        list_time_weekdays_special_att2=[]                                      
                        part_times=date2.split("/")                                     
                        mm=int(part_times[0])
                                              
                                          
                        dd_start=int(part_times[1].split("-")[0])         
                        dd_end=int(part_times[1].split("-")[1])

                        date_start_week_special_att2=datetime(yy,mm,dd_start)
                        date_end_week_special_att2=datetime(yy,mm,dd_end) # CLOSED interval to describe the shifts 

                        list_time_weekdays_special_att2.append(date_start_week_special_att2)
                        list_time_weekdays_special_att2.append(date_end_week_special_att2)
                        list_time_weekdays_special_att2.append(2)  
                        G.node[att2b]["working_times"].append(list_time_weekdays_special_att2)
                         
                    

                    elif "/" in att2:

                        parts=att2.split("/")                        
                        att2a=parts[0]
                        att2b=parts[1]   
                        
                        G.node[att2a]["working_times"].append(list2)
                        G.node[att2b]["working_times"].append(list2)                        
                        
                    
                   

            else:  #for the first row, that only has weekend info:

                w_att1=str(row[6])  # weekend personnel               
                w_att2=str(row[7])
                w_fellow=str(row[8])
                list_time_weekend=[] 
 
                start_weeked= row[5] # CLOSED interval to describe the shifts
                part_times=start_weeked.split("/")                  
                mm=int(part_times[0])
                dd=int(part_times[1])
                yy=2000+int(part_times[2])                    
               

                date_start_weeked=datetime(yy,mm,dd)
                date_end_weeked=datetime(yy,mm,dd)+timedelta(days=1) # CLOSED interval to describe the shifts
                               
                list_time_weekend.append(date_start_weeked)
                list_time_weekend.append(date_end_weeked)

                list3=list(list_time_weekend)  
                list3.append(1)          
                G.node[w_att1]["working_times"].append(list3)
                
                list4=list(list_time_weekend)
                list4.append(2)
                G.node[w_att2]["working_times"].append(list4)
                
                
                list5=list(list_time_weekend)  
                list5.append([1,2])
                G.node[w_fellow]["working_times"].append(list5)
                




                    
      
   # for n in G.nodes():
    #    print n,G.node[n]["working_times"],"\n"

    print "total # of residents:", len(list_residents)
    print "total # of fellows:", len(list_fellows)
    print "total # of attendings:", len(list_atts)
    print "total # doctors:",len(G.nodes())   




######################
## Adding the links: #
######################

# Between Attendings and Fellows:

    result_att_fellows= csv.reader(open(filename_AttgFellow, 'rb'), delimiter=',')
   

    reader = csv.DictReader(open(filename_AttgFellow))
    csv_att_fellow_headers = reader.fieldnames


    for row in result_att_fellows: 
        if row != csv_att_fellow_headers:
            
            if len(row[1])>0:
                att1=row[1]
                fellow1=row[2]
                G.add_edge(att1,fellow1)
                         
            
                att2=row[3]
                fellow2=row[4]
                if ","  in att2: #in some fields we have: att1 mm/dd-dd, att2 mm/dd-dd     
                    parts=att2.split(" ")                                            
                    att2a=parts[0]
                    att2b=parts[2]

                    G.add_edge(att2a,fellow2)
                    G.add_edge(att2b,fellow2)
                   

                elif "/" in att2:    # in some fields we have: att1/att2
                    parts=att2.split("/")                  
                    att2a=parts[0]
                    att2b=parts[1]
                    
                    G.add_edge(att2a,fellow2)
                    G.add_edge(att2b,fellow2)  
                   
                else:
                    G.add_edge(att2,fellow2)  
                   
            
                w_att1=row[6]
                w_att2=row[7]
                w_fellow=row[8]
                G.add_edge(w_att1,w_fellow)
                G.add_edge(w_att2,w_fellow)
               


    #Links Between Fellows and Residents:


    for resident in list_residents:
      for shift_r in G.node[resident]["working_times"]: # i go over the list of lists
          start_r=shift_r[0]
          stop_r=shift_r[1]

          if type(shift_r[2])== list:
              team_r=shift_r[2]
          else:
              try:
                  team_r=int(shift_r[2])
              except ValueError:   # SOME RESIDENTS DO NOT HAVE A TEAM!!!!Marinelli, Mathur, Pirotte and Patel S
                  team_r=[1,2]
                  
                 
                  
          #print "\nr:",resident,  start_r, stop_r, team_r

          for fellow in list_fellows:
              for shift_f in G.node[fellow]["working_times"]:# i go over the list of lists
                  start_f=shift_f[0]
                  stop_f=shift_f[1]

                  if type(shift_f[2])== list:
                      team_f=shift_f[2]
                  else:
                      team_f=int(shift_f[2])
                      
                 
                 # print "f",fellow,"'s shift:",shift_f#,type(team_f),type(team_r)#,"and resident",resident,"'s shift:",shift_r
                  if ((start_f >= start_r) and (start_f <= stop_r)):
                      if ((team_r == team_f) or (type(team_r) == list) or (type(team_f) == list)):
                         # print "    f:",fellow,  start_f, stop_f, team_f
                          G.add_edge(resident,fellow)
                          if G.node[resident]["type"]==G.node[fellow]["type"]:
                              print G.node[resident]["type"],"--",G.node[fellow]["type"], "line 461"



                  elif ((stop_f >= start_r) and (stop_f <= stop_r)):
                      if ((team_r == team_f) or (type(team_r) == list) or (type(team_f) ==list)):
                          #print "    f:",fellow,  start_f, stop_f, team_f
                          G.add_edge(resident,fellow)
                          if G.node[resident]["type"]==G.node[fellow]["type"]:
                              print G.node[resident]["type"],"--",G.node[fellow]["type"], "line 470"









##################################
#writing the network into a file:#
##################################

    network_name=filename_residents.split("/")[-1]   
    network_name=network_name.split(".csv")[0]
    nx.write_gml(G,"../Results/Doctors_network.gml") #  you run the code from  Idea-Spread-Hospital/Code

   


########################
# plotting the network:#
########################



    for n in G.nodes():   # i remove the attributes that are list, cos pygraphviz doesnt like it
# and i remove the residents without any working times.
        if len(G.node[n]["working_times"])>0:                    
            G.node[n]["working_times"]=None
        else:       
           # print n,G.node[n]["type"], "is going down cos doesnt have working times!"
            G.remove_node(n)


    nx.write_gml(G,"../Results/Doctors_network_without_working_times.gml") #  you run the code from  Idea-Spread-Hospital/Code




    print "\n# links:",len(G.edges()),"# nodes:",len(G.nodes())




    setA=set(list_atts)
    setF=set(list_fellows)
    setR=set(list_residents)


    interceptAF=setA & setF
    print "interception A-F",interceptAF
    interceptAR=setA & setR
    print "interception A-R",interceptAR
    interceptFR=setF & setR
    print "interception F-R",interceptFR



            

########################################
if __name__== "__main__":   
    
    if len(sys.argv) > 2:
        filename_residents = sys.argv[1]
        filename_AttgFellow = sys.argv[2]

        main(filename_residents,filename_AttgFellow)
    else:
        print "usage: python script_name path/csv_filename_residents  path/csv_filename_AttgFellow "

######################################
