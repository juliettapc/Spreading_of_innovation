#! /usr/bin/env python


"""
Code to read the csv with the attending+fellow schedule and create a (bipartite) network with shifts and doctors working together.
It takes the filename.csv from command line and returns a .gml file.


Created by Julia Poncela, July 2011.

"""

import csv
import networkx as nx
import numpy
import sys
from datetime import *
import matplotlib.pyplot as plt


def main(filename_AttgFellow):

   

    G=nx.Graph()


###############################################
# adding nodes for the Attendings and Fellows:#   
###############################################

    result_att_fellows= csv.reader(open(filename_AttgFellow, 'rb'), delimiter=',')
   


    reader = csv.DictReader(open(filename_AttgFellow))
    csv_att_fellow_headers = reader.fieldnames
   

    cont_shifts=0
    list_atts=[]
    list_fellows=[]
    list_shifts=[]
    for row in result_att_fellows:  

        if row != csv_att_fellow_headers  : # i exclude the first row  (how to do it more efficintly???)
                
         
            
            if len(row[0])>0:     #just in case the field is empty (for the fist week, it is)

              #labels for the nodes:
                shift1=str(row[0]) +" T1"            
                att1=str(row[1])  
                fellow1=str(row[2]) 
                
                shift2=str(row[0])  +" T2"
                att2=str(row[3])  
                fellow2=str(row[4])  
                
                weekend_shift=str(row[8]) 
                att_w1=str(row[9])  
                att_w2=str(row[10])  
                fellow_w=str(row[11])  
                
                

              
            
             
                if "," in att2:    # in some fields we have: att1 mm/dd-dd, att2 mm/dd-dd


                  #team2:
                    parts=att2.split(" ")                        
                    att2a=parts[0]
                    att2b=parts[2]   
                    date1=parts[1]
                    date2=parts[3]   


                    part_times=date1.split("/")                                     
                    mm=int(part_times[0])
                    
                    part_times[1]=part_times[1].strip(",")                       
                    dd_start=int(part_times[1].split("-")[0])         
                    dd_end=int(part_times[1].split("-")[1])
                                             
                    
                    date_start_week_att2a=datetime(yy,mm,dd_start)
                    date_end_week_att2a=datetime(yy,mm,dd_end)

                    shift2a=str(mm)+"/"+str(dd_start)+"/"+str(yy)+" T2"                   
                    G.add_node(shift2a)

                   
                    G.node[shift2a]["type"]="shift" 
                    G.node[shift2a]["start"]=date_start_week
                    G.node[shift2a]["stop"]=date_end_week
                    G.node[shift2a]["order"]=cont_shifts
                    G.node[shift2a]["team"]=2

                    list_shifts.append(shift2a)
                    cont_shifts+=1


                    if att2a not in list_atts:           
                        list_atts.append(att2a)                            
                        G.add_node(att2a)
                        G.node[att2a]["type"]="A"                               
                    G.add_edge(shift2a,att2a)       
                    G.add_edge(shift2a,fellow2)       
    
                   

                    part_times=date2.split("/")                                     
                    mm=int(part_times[0])
                                        
                    dd_start=int(part_times[1].split("-")[0])         
                    dd_end=int(part_times[1].split("-")[1])
                    
                    date_start_week_att2b=datetime(yy,mm,dd_start)
                    date_end_week_att2b=datetime(yy,mm,dd_end)
                    
                    shift2b=str(mm)+"/"+str(dd_start)+"/"+str(yy)+" T2"
                    G.add_node(shift2b)



                    G.node[shift2b]["type"]="shift" 
                    G.node[shift2b]["start"]=date_start_week
                    G.node[shift2b]["stop"]=date_end_week
                    G.node[shift2b]["order"]=cont_shifts
                    G.node[shift2b]["team"]=2

                    list_shifts.append(shift2b)
                    cont_shifts+=1


                    if att2b not in list_atts:           
                        list_atts.append(att2b)                            
                        G.add_node(att2b)
                        G.node[att2b]["type"]="A"                               
                    G.add_edge(shift2b,att2b)       
                    G.add_edge(shift2b,fellow2)    
    
                 
                    
                   #team1:
                    if att1 not in list_atts:           
                        list_atts.append(att1)
                        G.add_node(att1)
                        G.node[att1]["type"]="A"                                        
                    G.add_edge(shift2a,att1)
                    G.add_edge(shift2b,att1)
                        

                    if fellow1 not in list_fellows:           
                        list_fellows.append(fellow1)
                        G.add_node(fellow1)
                        G.node[fellow1]["type"]="F"                         
                    G.add_edge(shift2a,fellow1)
                    G.add_edge(shift2b,fellow1)






                else:  # for most of the lines



                  #dates:                Week:
                    start_week= row[0]                            
                    part_times=start_week.split("/")                
                    mm=int(part_times[0])
                    dd=int(part_times[1])
                    yy=2000+int(part_times[2])                    
                    date_start_week=datetime(yy,mm,dd)


                    end_week= row[8] # always CLOSED interval to describe the shifts
                    part_times=end_week.split("/")                  
                    mm=int(part_times[0])
                    dd=int(part_times[1])
                    yy=2000+int(part_times[2])                    
                    date_end_week=datetime(yy,mm,dd)-timedelta(days=1)
                    
                                       # Weekend:
                    date_start_weeked=datetime(yy,mm,dd)
                    date_end_weeked=datetime(yy,mm,dd)+timedelta(days=1)
                    
                    

                    
                  #team1:               
                    G.add_node(shift1)
                    G.node[shift1]["type"]="shift" 
                    G.node[shift1]["start"]=date_start_week
                    G.node[shift1]["stop"]=date_end_week
                    G.node[shift1]["order"]=cont_shifts
                    G.node[shift1]["team"]=1
                    
                    list_shifts.append(shift1)
                    cont_shifts+=1     
                    
                     
                    if att1 not in list_atts:           
                        list_atts.append(att1)
                        G.add_node(att1)
                        G.node[att1]["type"]="A"                                        
                    G.add_edge(shift1,att1)
                        

                    if fellow1 not in list_fellows:           
                        list_fellows.append(fellow1)
                        G.add_node(fellow1)
                        G.node[fellow1]["type"]="F"                         
                    G.add_edge(shift1,fellow1)
                  
                  #team2:
                    if att2 not in list_atts:           
                        list_atts.append(att1)
                        G.add_node(att2)
                        G.node[att2]["type"]="A"                     

                    shift2=shift2+" T2"
                    G.add_node(shift2)

                    G.node[shift2]["type"]="shift" 
                    G.node[shift2]["start"]=date_start_week
                    G.node[shift2]["stop"]=date_end_week
                    G.node[shift2]["order"]=cont_shifts
                    G.node[shift2]["team"]=2

                    list_shifts.append(shift2)
                    cont_shifts+=1

                    G.add_edge(shift2,att2)
                                           

                    if fellow2 not in list_fellows:           
                        list_fellows.append(fellow2)
                        G.add_node(fellow2)
                        G.node[fellow2]["type"]="F"                       
                    G.add_edge(shift2,fellow2)
                
               

             #weekends:        

                G.add_node(weekend_shift)
                

                end_week= row[8] 
                part_times=end_week.split("/")                  
                mm=int(part_times[0])
                dd=int(part_times[1])
                yy=2000+int(part_times[2])                    
               
                date_start_weeked=datetime(yy,mm,dd)
                date_end_weeked=datetime(yy,mm,dd)+timedelta(days=1) 
     

                if fellow_w not in list_fellows:           
                    list_fellows.append(fellow_w)
                    G.add_node(fellow_w)
                    G.node[fellow_w]["type"]="F"                     
                G.add_edge(weekend_shift,fellow_w)
                                
               
                if att_w1 not in list_atts:           
                    list_atts.append(att_w1)
                    G.add_node(att_w1)
                    G.node[att_w1]["type"]="A"                                         
                G.add_edge(weekend_shift,att_w1)
                        

                if att_w2 not in list_atts:           
                    list_atts.append(att_w2)
                    G.add_node(att_w2)
                    G.node[att_w2]["type"]="A"                                         
                G.add_edge(weekend_shift,att_w2)
                        


                G.node[weekend_shift]["type"]="shift" 
                G.node[weekend_shift]["start"]=date_start_weeked
                G.node[weekend_shift]["stop"]=date_end_weeked
                G.node[weekend_shift]["order"]=cont_shifts
                G.node[weekend_shift]["team"]="w"

                list_shifts.append(weekend_shift)
                cont_shifts+=1


            else:  # to deal with the first line, that only has weekend shift     

                weekend_shift=str(row[8]) 
                att_w1=str(row[9])  
                att_w2=str(row[10])  
                fellow_w=str(row[11])  

                G.add_node(weekend_shift)
                

                end_week= row[8] 
                part_times=end_week.split("/")                  
                mm=int(part_times[0])
                dd=int(part_times[1])
                yy=2000+int(part_times[2])                    
               
                date_start_weeked=datetime(yy,mm,dd)
                date_end_weeked=datetime(yy,mm,dd)+timedelta(days=1) 
     

                if fellow_w not in list_fellows:           
                    list_fellows.append(fellow_w)
                    G.add_node(fellow_w)
                    G.node[fellow_w]["type"]="F"                     
                G.add_edge(weekend_shift,fellow_w)
                                
               
                if att_w1 not in list_atts:           
                    list_atts.append(att_w1)
                    G.add_node(att_w1)
                    G.node[att_w1]["type"]="A"                                         
                G.add_edge(weekend_shift,att_w1)
                        

                if att_w2 not in list_atts:           
                    list_atts.append(att_w2)
                    G.add_node(att_w2)
                    G.node[att_w2]["type"]="A"                                         
                G.add_edge(weekend_shift,att_w2)
                        


                G.node[weekend_shift]["type"]="shift" 
                G.node[weekend_shift]["start"]=date_start_weeked
                G.node[weekend_shift]["stop"]=date_end_weeked
                G.node[weekend_shift]["order"]=cont_shifts
                G.node[weekend_shift]["team"]="w"

                list_shifts.append(weekend_shift)
                cont_shifts+=1





#NOTE: the few exceptions (long weekends) are NOT taking into account for now.



##################################
#writing the network into a file:#
##################################

    network_name=filename_AttgFellow.split("/")[-1]   
    network_name=network_name.split(".csv")[0]
    nx.write_gml(G,"../Results/Doctors_Shifts_network2012.gml") #  you run the code from  Idea-Spread-Hospital/Code


    for n in G.nodes():  
       try:                    
            G.node[n]["stop"]=None
            G.node[n]["start"]=None

       except:       
          pass


    nx.write_gml(G,"../Results/Doctors_Shifts_network2012_without_times.gml") #  you run the code from  Idea-Spread-Hospital/Code






    num_A=0
    num_F=0
    num_s=0
    for n in G.nodes():

        try:
            if G.node[n]["type"]=="F":
                num_F+=1
            elif G.node[n]["type"]=="A":
                num_A+=1       
                
            else:  # for shift-like nodes
                num_s+=1
               
        except KeyError:
            print n

    print "total # of fellows:", num_F
    print "total # of attendings:", num_A
    print "total # shifts:",num_s   

    print "total # nodes:", len(G.nodes())




        

########################################
if __name__== "__main__":   
    
    if len(sys.argv) > 1:       
        filename_AttgFellow = sys.argv[1]

        main(filename_AttgFellow)
    else:
        print "usage: python script_name  path/csv_filename_AttgFellow "

######################################
