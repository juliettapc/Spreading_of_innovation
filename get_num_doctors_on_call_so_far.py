#!/usr/bin/env python

import networkx as nx

G = nx.read_gml("../Results/Doctors_shifts_network_withT3_independent_weekends.gml")

outputfile="../Results/Num_doctors_on_call_so_far_.txt"
file=open(outputfile, "wt")


list_drs_on_call=[]
list_Att_on_call=[]
list_F_on_call=[]

dict_days_drs={}
dict_days_Att={}
dict_days_F={}

t=1
while t <= 243:        # ojo!! cambiar a mano el valor nulo de los 4 primero diase en el archivo final!!!!
    for node in G.nodes():
        if G.node[node]["type"]=="shift":
            if G.node[node]["order"]== t:
                for neighbor in G.neighbors(node):
                    dr=G.node[neighbor]["label"]                   
                    if dr not in list_drs_on_call:
                        list_drs_on_call.append(dr)

                    if G.node[neighbor]["type"]=="A":
                        if dr not in list_Att_on_call:
                            list_Att_on_call.append(dr)

                    elif G.node[neighbor]["type"]=="F":
                        if dr not in list_F_on_call:
                            list_F_on_call.append(dr)
                

    dict_days_drs[t]=list_drs_on_call
    dict_days_Att[t]=list_Att_on_call
    dict_days_F[t]=list_F_on_call
    print t, "tot:",len(dict_days_drs[t]), "Att:",len(dict_days_Att[t]), "F:",len(dict_days_F[t])
    print >> file,  t, len(dict_days_drs[t]),len(dict_days_Att[t]),len(dict_days_F[t])

    t+=1


file.close()

print "writen file:",outputfile
