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


def main(filename_AttgFellow):

   

    G=nx.Graph()



#######################
#####Adding the nodes:#
#######################


   
  

   
   #adding nodes for the Attendings and Fellows:   
    result_att_fellows= csv.reader(open(filename_AttgFellow, 'rb'), delimiter=',')
   

    reader = csv.DictReader(open(filename_AttgFellow))
    csv_att_fellow_headers = reader.fieldnames
    print   csv_att_fellow_headers

    list_colums_att=[1,3,6,7] # colums with Attending last_names
    list_colums_fellow=[2,4,8] # colums with Fellow  last_names  

    
    contador_lineas=-1
    list_atts=[]
    list_fellows=[]
    for row in result_att_fellows:  

        contador_lineas=contador_lineas+1

        if contador_lineas>0:#row != csv_att_fellow_headers  : # i exclude the first row  (how to do it more efficintly???)
            
            print row


            for i in list_colums_att:
                  
                #print att, i
                att=str(row[i])  
                print att, i


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
                               
               
                                if a in list_fellows:
                                    print "attending:",a,"listed before as fellow"

                    else:
                        if att not in list_atts:           
                            list_atts.append(att)
                            G.add_node(att)
                            G.node[att]["type"]="A" 
                            
               
       
                   
                            if att in list_fellows:
                                print "attending:",att,"listed before as fellow"
                   


            for i in list_colums_fellow:
                fellow=str(row[i])

                if len(fellow)>0:   #just in case the field is empty               
                   
                    if fellow not in list_fellows:           
                        list_fellows.append(fellow)
                        G.add_node(fellow)
                        G.node[fellow]["type"]="F"
                       
               

                   
                        if fellow in list_atts:
                            print "fellows:",fellow,"listed before as attending"



   
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
    contador_lineas=-1

    for row in result_att_fellows: 

        contador_lineas=contador_lineas+1

        if contador_lineas>0:# if row != csv_att_fellow_headers:
            print row
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
               


   






##################################
#writing the network into a file:#
##################################

  
    nx.write_gml(G,"../Results/Doctors_network_2012_No_residents_No_shifts.gml") #  you run the code from  Idea-Spread-Hospital/Code

   


########################
# plotting the network:#
########################



   


    nx.write_gml(G,"../Results/Doctors_network_without_working_times.gml") #  you run the code from  Idea-Spread-Hospital/Code




    print "\n# links:",len(G.edges()),"# nodes:",len(G.nodes())




    setA=set(list_atts)
    setF=set(list_fellows)
  

    interceptAF=setA & setF
    
   



            

########################################
if __name__== "__main__":   
    
    if len(sys.argv) > 1:
        
        filename_AttgFellow = sys.argv[1]

        main(filename_AttgFellow)
    else:
        print "usage: python script_name   path/csv_filename_AttgFellow "

######################################
