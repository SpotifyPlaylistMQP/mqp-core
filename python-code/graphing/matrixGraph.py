import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time

# Function create_graph(): Dictionary, String -> Image
# var graph_data: A dictionary containing tuples
# var playlist_name: A string of the playlist name
def create_graph(graph_data, playlist_name):
    print("Generating Matrix Factorization Evaluation Graph from " + playlist_name)
    data = graph_data['mf']
    print(data)

    x_value = list(data.keys())
    y_value = list(data.values())

    # Create the graph figure
    plt.figure(1)
    fig = plt.gcf().set_size_inches(28,16)

    # Create the legend
    red_patch = mpatches.Patch(color='red', label='Average Matrix Values')
    plt.legend(handles=[red_patch])

    # Plotting User Based Subgraph
    print("Plotting MF graph...")
    plt.xlabel('Step Value', fontsize=12)
    plt.ylabel('Average DCG Precision', fontsize=12)
    plt.title('Average DCG Precision vs Step Value for Matrix Factorization Evaluation', fontsize=16)
    plt.plot(x_value, y_value, marker='o', color='r', label='Matrix Factorization')
    plt.legend(bbox_to_anchor=(0.02, 0.975, .22, 0), ncol=2, borderaxespad=0)

    z = np.polyfit(x_value, y_value, 1)
    p = np.poly1d(z)
    UBJ_plot = plt.plot(x_value,p(x_value), "r--", label='Matrix Factorization')

    # Finalize and display the graph
    print("Saving to ./graphing/output_images/matrix_graphs/...")
    graph_name = playlist_name + time.strftime("-%d-%m-%Y") + '.png'
    plt.savefig('./graphing/output_images/matrix_graphs/' + graph_name)
    print("Generated the graph: \"" + graph_name + "\"")
