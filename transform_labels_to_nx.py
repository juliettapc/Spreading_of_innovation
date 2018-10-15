import networkx as nx

def transform_labels_to_nx(G):
    H = nx.Graph()
    label_mapping={}
        #add the nodes by label from G to H
    for node in G.nodes(data=True):
        H.add_node(node[1]['label'])
        label_mapping[node[0]] = node[1]['label']   
        
        if len(node[1]) > 2:
            for key in node[1]:
                H.node[node[1]['label']][key] = node[1][key]
    #add the appropriate edges
    for edge in G.edges(data=True):
        H.add_edge(label_mapping[edge[0]], label_mapping[edge[1]])
        if len(edge[2]) > 0:
            for key in edge[2]:
                H[label_mapping[edge[0]]][label_mapping[edge[1]]][key] = edge[2][key]            
    return H

if __name__=="__main__":pass
