import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time

# Function create_graph(): Dictionary, String -> Image
# Creates a two figure graph comparing
#       - User Jaccard vs User Cosine && Item Jaccard vs Item Cosine
#       - Plots the line of best fit for all metrics
# var graph_data: A dictionary containing tuples of [K Value: Avg R Precision] for all four systems
# var playlist_name: A string of the playlist name
def create_graph(graph_data, playlist_name, N, number_of_times_to_run):
    print("Generating Precision Evaluation Graph from " + playlist_name)
    # Individual Result Dictionaries
    uj = graph_data["uj"]
    ij = graph_data["ij"]
    uc = graph_data["uc"]
    ic = graph_data["ic"]
    # User Jaccard Values
    uj_x = list(uj.keys())
    uj_y = list(uj.values())
    # User Cosine Values
    uc_x = list(uc.keys())
    uc_y = list(uc.values())
    # Item Jaccard Values
    ij_x = list(ij.keys())
    ij_y = list(ij.values())
    # Item Cosine Values
    ic_x = list(ic.keys())
    ic_y = list(ic.values())

    # Create the graph figure
    plt.figure(1)
    fig = plt.gcf().set_size_inches(28,16)

    # Create the legend
    red_patch = mpatches.Patch(color='red', label='Jaccard Values')
    blue_patch = mpatches.Patch(color='blue', label='Cosine Values')
    plt.legend(handles=[red_patch, blue_patch])

    # Plotting User Based Subgraph
    print("Plotting User Based Values...")
    plt.subplot(211)
    plt.xlabel('K Value', fontsize=12)
    plt.ylabel('Average DCG Precision', fontsize=12)
    plt.title('K Values vs Average DCG Precision for User Based Evaluation over ' + number_of_times_to_run + ' iterations where N = ' + str(N), fontsize=16)
    plt.plot(uj_x, uj_y, marker='o', color='r', label='User Based Jaccard') # User Based Jaccard Values RED
    plt.plot(uc_x, uc_y, marker='o', color='b', label='User Based Cosine') # Item Based Jaccard Values BLUE
    plt.legend(bbox_to_anchor=(0.02, 0.975, .22, 0), ncol=2, borderaxespad=0)
    z = np.polyfit(uj_x, uj_y, 1)
    p = np.poly1d(z)
    UBJ_plot = plt.plot(uj_x,p(uj_x), "r--", label='User Based Jaccard')
    z = np.polyfit(uc_x, uc_y, 1)
    p = np.poly1d(z)
    UBC_plot = plt.plot(uc_x,p(uc_x), "b--", label='User Based Cosine')

    # Plotting Item Based Subgraph
    print("Plotting Item Based Values...")
    plt.subplot(212)
    plt.xlabel('K Value', fontsize=12)
    plt.ylabel('Average DCG Precision', fontsize=12)
    plt.title('K Values vs Average DCG Precision for Item Based Evaluation over ' + number_of_times_to_run + ' iterations where N = ' + str(N), fontsize=16)
    plt.plot(ij_x, ij_y, marker='o', color='r', label='Item Based Jaccard') # User Based Jaccard Values RED
    plt.plot(ic_x, ic_y, marker='o', color='b', label='Item Based Cosine') # Item Based Jaccard Values BLUE
    plt.legend(bbox_to_anchor=(0.02, 0.975, 1, 0), ncol=2, borderaxespad=0)
    z = np.polyfit(ij_x, ij_y, 1)
    p = np.poly1d(z)
    UBJ_plot = plt.plot(ij_x,p(ij_x), "r--", label='Item Based Jaccard')
    z = np.polyfit(ic_x, ic_y, 1)
    p = np.poly1d(z)
    UBC_plot = plt.plot(ic_x,p(ic_x), "b--", label='Item Based Cosine')

    # Finalize and display the graph
    print("Saving to ./graphing/output_images/precision_graphs/...")
    graph_name = playlist_name + time.strftime("-%d-%m-%Y") + '.png'
    plt.savefig('./graphing/output_images/precision_graphs/' + graph_name)
    print("Generated the graph: \"" + graph_name + "\"")
