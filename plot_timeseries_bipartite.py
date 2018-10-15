#!/usr/bin/env python

'''
Given a .gml file, i plot the network.
Created by Julia Poncela, on August 2011.
'''

import sys
import os
import networkx as nx
import matplotlib.pyplot as plot
from matplotlib.patches import Wedge, Polygon
import matplotlib.ticker as ticker
from matplotlib import patches as patches
import random
from optparse import OptionParser
import dateutil.parser as dparser


def main(graph_name, wname, o):
    G = nx.read_gml(graph_name)
    H=nx.Graph()   # MAKE a COPY of the network so GRAGHVIZ doest freak out.. 
    H.add_edges_from(G.edges())
    calc_graph_statistics(G)
    date_groupings=subset_dates(G, o.amt_groups)
    for group in date_groupings:
        wfname=wname+'-%s.png'%(str(group))
        newnet=subset_network(G.copy(), date_groupings[group])
        newnet_dup=nx.Graph()
        newnet_dup.add_edges_from(newnet.edges())
        list_F,list_A,list_s=order_nodes(newnet,newnet_dup)
        position_modified,y_A,y_F=calculate_node_positioning(newnet_dup, newnet, list_F,
                                                             list_A, list_s)
        plot_network(newnet_dup, list_A, list_F, list_s, position_modified, y_A, y_F, wfname)
        nn=newnet.copy()
        nx.write_gml(nn, wfname[:-4]+'.gml')

def calc_graph_statistics(G):
    max=0.0
    hub=None
    for n in G.nodes():
        if len(G.neighbors(n))>max:
            max=G.degree(n)
            hub=n
    print hub, max

def subset_dates(G, amt_groups):
    date_trans,date_groups={},{}
    for n in G.nodes():
        if G.node[n]['type']=='shift':
            date_trans[G.node[n]['label']]=dparser.parse(G.node[n]['label'].split()[0])
    dates=date_trans.values()
    dates.sort()
    groupings=len(dates)/amt_groups
    prev_month=dates[0].month
    for g in range(amt_groups):
        date_groups[g]=[]
        for d in dates[:]:
            if len(date_groups[g])>groupings and prev_month!=d.month:
                pass
            else:
               date_groups[g].append(d)
               prev_month=d.month
               dates.remove(d)
    date_name_groups={}
    for g in date_groups:
        date_name_groups[g]=[]
        for k,v in date_trans.items():
            if v in date_groups[g]:
                date_name_groups[g].append(k)
    return date_name_groups

def order_nodes(G,H):
    max_order=0
    list_orderings=[]
    list_A=[]
    list_F=[]
    list_s=[]
    for n in G.nodes():
        if n in H.nodes():
            if G.node[n]['type']=="A":
                list_A.append(n)
            elif G.node[n]["type"]=="F":
                list_F.append(n)
            else:
              
                list_s.append(n)
                list_orderings.append(G.node[n]["order"])
                if G.node[n]["order"]>max_order:
                    max_order=G.node[n]["order"]
    print "# Att:",len(list_A),"# F:",len(list_F),"# shifts:",len(list_s),max_order
    return list_F,list_A,list_s

def subset_network(Gp, allow_dates):
    for n in Gp.nodes():
        if Gp.node[n]['type']=='shift':
            if not Gp.node[n]['label'] in allow_dates:
                Gp.remove_node(n)
    return Gp

def calculate_node_positioning(H, G, list_F,list_A, list_s):
    positions={}
    x_A=len(list_F)
    x_F=len(list_F)
    y_A=len(list_s)*2
    y_F=0
    y_s=len(list_s)
    shift_order=[]
    for n in H.nodes():
        if G.node[n]["type"]=='shift':
            shift_order.append(G.node[n]["order"])
    for n in H.nodes():
        if G.node[n]["type"]=="A":                     
            x_A=x_A+float(len(list_s))/len(list_A) 
            positions[n]=(x_A,y_A)
           
        elif G.node[n]["type"]=="F":                   
            x_F=x_F+float(len(list_s))/len(list_F)
            positions[n]=(x_F,y_F)
        else:
            x_s=len(list_F)+float(G.node[n]["order"])-min(shift_order)
            positions[n]=(x_s,y_s)
    return positions,y_A,y_F

def plot_network(net,attend_nodes,fellow_nodes,shift_nodes,positions,y_A,y_F,wfname):
    #first draw all the edges:
    nx.draw_networkx_edges(net, positions, edgelist=None, alpha=0.5)    
    # diff types of doctors=diff colors      
    nx.draw_networkx_nodes(net, positions, nodelist=shift_nodes, node_shape = 's', 
                           node_color='g', node_size=40) 
    nx.draw_networkx_nodes(net, positions, nodelist=fellow_nodes, node_shape = 'o', 
                           node_color='b', node_size=300)   
    nx.draw_networkx_nodes(net,positions,nodelist=attend_nodes, node_shape = 'o', 
                           node_color='r', node_size=300)
    ### i create the legend:
    plot.text(-20,y_A, "Attendings", family='sans-serif', size=14)   # for the hierarchy layout
    plot.text(-20,y_F, "Fellows", family='sans-serif', size=14)
    plot.axis('off')  # to not show the axis
    plot.savefig(wfname)
    plot.clf()

if __name__ == '__main__':
    usage='%prog path/network.gml save_file_basename'
    parser=OptionParser(usage=usage)
    parser.add_option('-g', '--amt_groups', action='store', type=int, default=1,
                      help='The number of date groupings/networks that you desire to be produced')
    (options,args)=parser.parse_args()
    if not len(args)==2:
        parser.error('This program requires an input network and a savefilename')
    main(args[0],args[1],options)

    
