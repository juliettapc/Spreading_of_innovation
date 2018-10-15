#!/usr/bin/env python

import networkx as nx
from datetime import *

G=nx.read_gml("../Results/Doctors_Shifts_network2012_without_times.gml")

output_file="../Results/Edgelist_2012_names.txt"      
file = open(output_file,'wt')    

print "# links:", len(G.edges())
#raw_input()


year=2011   #real seeding date
month=10
day=31
seeding_date=datetime(year, month, day)




cont_num_links=0
list_pairs=[]
for node in G.nodes():
    if str(G.node[node]['type'])!="shift":

        for neighbor in G.neighbors(node):
            pair1=[]               
            pair2=[]
            pair1.append(node)
            pair1.append(neighbor)      
            pair2.append(neighbor)
            pair2.append(node)
            
            if (pair1 not in list_pairs)  and (pair2 not in list_pairs):
                list_pairs.append(pair1)

                parts_date_label=str(G.node[neighbor]["label"]).split(" ")[0].split("/")
                mm=int(parts_date_label[0])
                dd=int(parts_date_label[1])
                yy=int(parts_date_label[2])

                date=datetime(2000+yy,mm,dd)
               
                if (date >= seeding_date):  # i dont care about the shifts before the seeding
                                
                    #print pair1,G.node[node]["label"], G.node[neighbor]["label"] , G.node[neighbor]["order"]  
                    print >> file, G.node[node]["label"], G.node[neighbor]["label"], G.node[neighbor]["order"]  
                            
                    cont_num_links+=1
               

print "# links:", cont_num_links  #just checking

