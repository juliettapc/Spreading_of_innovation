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


def main(filename_residents,filename_AttgFellow):

   

    G=nx.Graph()


#HOW DO I IGNORE THE FIRST ROW???


##Adding the nodes:

   #for the Residents:
    list_residents=[]
    result_residents= csv.reader(open(filename_residents, 'rb'), delimiter=',')


   
    for row in result_residents:
        resident=str(row[0])

        if len(resident)>0:      #just in case the field is empty
            if resident not in list_residents:            
                list_residents.append(resident)
                G.add_node(resident)
                G.node[resident]["type_doctor"]="R"
               #print resident
   

    
  


   
   #for the attendings and fellows:
   
    result_att_fellows= csv.reader(open(filename_AttgFellow, 'rb'), delimiter=',')


    list_colums_att=[1,3,6,7] # colums with Attending last_names
    list_colums_fellow=[2,4,8] # colums with Fellow  last_names  
 
    list_atts=[]
    list_fellows=[]
    for row in result_att_fellows:       
        for i in list_colums_att:
            att=str(row[i])     

            if len(att)>0:     #just in case the field is empty
                if att not in list_atts:           
                    list_atts.append(att)
                    G.add_node(att)
                    G.node[att]["type_doctor"]="A"
                    print att

              

        for i in list_colums_fellow:
            fellow=str(row[i])

            if len(fellow)>0:     #just in case the field is empty
                if fellow not in list_fellows:           
                    list_fellows.append(fellow)
                    G.add_node(fellow)
                    G.node[fellow]["type_doctor"]="F"
                    print fellow


## EN ALGUNAS FILAS HAY DOS NOMBRES EN UNA MISMA CASILLA, CON FECHAS Y SEPARADOS POR COMAS! Cuttica Kalhan Budinger Wunderink  Jan


    print list_residents
    print list_fellows
    print list_atts

    print "total # of residents:", len(list_residents)
    print "total # of fellows:", len(list_fellows)
    print "total # of attendings:", len(list_atts)
    print "total # doctors:",len(G.nodes())   



    
    network_name=filename_residents.split("/")[-1]   
    network_name=network_name.split(".csv")[0]
    nx.write_gml(G,"../Results/Doctors_network.gml") #  you are in Idea-Spread-Hospital/Code

    print G.nodes()








########################################
if __name__== "__main__":   
    
    if len(sys.argv) > 2:
        filename_residents = sys.argv[1]
        filename_AttgFellow = sys.argv[2]

        main(filename_residents,filename_AttgFellow)
    else:
        print "usage: python script_name path/csv_filename_residents  path/csv_filename_AttgFellow "

######################################
