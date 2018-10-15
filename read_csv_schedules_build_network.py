#! /usr/bin/env python


"""
Code to read the csv with the resident's schedule.
It takes the filename.csv from command line.


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

   #for the Residents:
    list_residents=[]
    result_residents= csv.reader(open(filename_residents, 'r'), delimiter=',')
   
    reader = csv.DictReader(open(filename_residents))
    csv_resident_headers = reader.fieldnames

    particular_time=timedelta(0)

   
    for row in result_residents:
        if row != csv_resident_headers:  # i exclude the first row  (how to do it more efficintly???)
           
            resident=str(row[0])
           
            if len(resident)>0:      #just in case the field is empty
                if resident not in list_residents:            
                    list_residents.append(resident)
                    G.add_node(resident)
                    G.node[resident]["type_doctor"]="R"
                   
   

   
   #for the Attendings and Fellows:
   
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
                                G.node[a]["type_doctor"]="A"                   
                               



                    elif "/" in att:    # in some fields we have: att1/att2
                        parts=att.split("/") 
                        atts=[]
                        atts.append(parts[0])
                        atts.append(parts[1])
                        for a in atts:
                            if a not in list_atts:           
                                list_atts.append(a)
                                G.add_node(a)
                                G.node[a]["type_doctor"]="A"        
                               


                    else:
                        if att not in list_atts:           
                            list_atts.append(att)
                            G.add_node(att)
                            G.node[att]["type_doctor"]="A" 
                           
       
                   

                   


            for i in list_colums_fellow:
                fellow=str(row[i])

                if len(fellow)>0:   #just in case the field is empty               
                    if "," not in fellow: # in some fields we could have: fellow1 mm/dd-dd, fellow2 mm/dd-dd
                        if fellow not in list_fellows:           
                            list_fellows.append(fellow)
                            G.add_node(fellow)
                            G.node[fellow]["type_doctor"]="F"
                           

                        #print fellow
                    else:
                       
                        parts=fellow.split(" ")
                        
                        fellows=[]
                        fellows.append(parts[0])
                        fellows.append(parts[2])
                        
                        for f in fellows:
                            if f not in list_fellows:           
                                list_fellows.append(f)
                                G.add_node(f)
                                G.node[f]["type_doctor"]="F"             
       

                

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







    print "# links:",len(G.edges())

##################################
#writing the network into a file:#
##################################

    network_name=filename_residents.split("/")[-1]   
    network_name=network_name.split(".csv")[0]
    nx.write_gml(G,"../Results/Doctors_network.gml") #  you are in Idea-Spread-Hospital/Code

   


########################
# plotting the network:#
########################


    #layout = nx.random_layout(G)
    #layout = nx.circular_layout(G)
    #layout=nx.spring_layout(G)
    layout=nx.graphviz_layout(G,prog='twopi',root=None,args='')

    nx.draw(G,layout,with_labels=False)
    plt.show()

   








########################################
if __name__== "__main__":   
    
    if len(sys.argv) > 2:
        filename_residents = sys.argv[1]
        filename_AttgFellow = sys.argv[2]

        main(filename_residents,filename_AttgFellow)
    else:
        print "usage: python script_name path/csv_filename_residents  path/csv_filename_AttgFellow "

######################################
