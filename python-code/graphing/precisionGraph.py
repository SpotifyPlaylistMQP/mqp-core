import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time
# x: K
# y: R precision

def create_graph(graph_data, playlist_name):
    # Individual Result Dictionaries
    uj = graph_data["uj"]
    ij = graph_data["ij"]
    uc = graph_data["uc"]
    ic = graph_data["ic"]

    print('---- Graph Data ----')
    # User Jaccard Values
    print('** UJ Data **')
    # print(uj);
    uj_x = uj.keys()
    uj_y = uj.values()
    # Item Jaccard Values
    print('** IJ Data **')
    # print(ij);
    ij_x = ij.keys()
    ij_y = ij.values()
    # User Cosine Values
    print('** UC Data **')
    # print(uc);
    uc_x = uc.keys()
    uc_y = uc.values()
    # Item Cosine Values
    print('** IC Data **')
    # print(ic);
    ic_x = ic.keys()
    ic_y = ic.values()

    # Create the graphs
    plt.figure(1)
    fig = plt.gcf().set_size_inches(22,12)
    # Create the legend
    # red_patch = mpatches.Patch(color='red', label='Jaccard Values')
    # blue_patch = mpatches.Patch(color='blue', label='Cosine Values')
    # plt.legend(handles=[red_patch, blue_patch])

    # Plotting Jaccard Subgraph
    plt.subplot(211)
    plt.xlabel('K Value', fontsize=12)
    plt.ylabel('Average R Precision', fontsize=12)
    plt.title('K Values vs Average R Precision for Jaccard Evaluation', fontsize=16)
    plt.plot(uj_x, uj_y, 'or', label='User Based Jaccard') # User Based Jaccard Values RED
    plt.plot(ij_x, ij_y, 'ob', label='Item Based Jaccard') # Item Based Jaccard Values BLUE
    plt.legend(bbox_to_anchor=(0.02, 0.975, 1, 0), ncol=2, borderaxespad=0)

    # Plotting Cosine Subgraph
    plt.subplot(212)
    plt.xlabel('K Value', fontsize=12)
    plt.ylabel('Average R Precision', fontsize=12)
    plt.title('K Values vs Average R Precision for Cosine Evaluation', fontsize=16)
    plt.plot(uc_x, uc_y, 'or', label='User Based Cosine') # User Based Cosine Values RED
    plt.plot(ic_x, ic_y, 'ob', label='Item Based Cosine') # Item Based Cosine Values BLUE
    plt.legend(bbox_to_anchor=(0.02, 0.975, 1, 0), ncol=2, borderaxespad=0)

    # Finalize and display the graph
    graph_name = './graphing/output_images/precision_graphs/'+playlist_name + time.strftime("-%d-%m-%Y") + '.png'
    plt.savefig(graph_name)
    print("Generated the graph \"" + graph_name + "\"")
