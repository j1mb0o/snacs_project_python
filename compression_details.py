import os
import pandas as pd
import rustworkx as rx

stats = {"Network":[], "bits/node":[], "bits/node(compressed)":[], "Size reduction (%)":[] }

for filename in os.listdir('random-graphs'):
    print(filename.split('.')[0])
    g = rx.PyGraph.read_edge_list('random-graphs/' + filename)
    print('Number of nodes: ', len(g.node_indices()))
    # print('Number of edges: ', len(g.edge_indices()))
    stats["Network"].append(filename.split('.')[0])
    bits_node = os.path.getsize('random-graphs/' + filename) * 8 / len(g.node_indices())
    stats["bits/node"].append(bits_node)
    bits_node_compressed = os.path.getsize('random-compressed-networks/' + filename+ '.graph') * 8 / len(g.node_indices())
    stats["bits/node(compressed)"].append(bits_node_compressed)
    diff = (bits_node - bits_node_compressed) / bits_node * 100
    stats["Size reduction (%)"].append(diff)

df = pd.DataFrame(stats)
df.to_csv('random_compression_details.csv', index=False)
# df.to_latex('compression_details.tex', index=False)