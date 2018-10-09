import numpy as np
import matplotlib.pyplot as plt
from matplotlib import figure
import pylab
import time

def create_graph(graph_data, playlist_name):
    # Jaccard
    uj = graph_data["uj"]
    ij = graph_data["ij"]
    # Cosine
    uc = graph_data["uc"]
    ic = graph_data["ic"]

    # Number of playlists/values sampled
    max_jaccard_val = max(uj, ij)
    max_cos_val = max(uc, ic)
    max_val = max(max_jaccard_val, max_cos_val)

    objects = ('User Based Jaccard', 'User Based Cosine', 'Item Based Jaccard', 'Item Based Cosine')
    y_pos = np.arange(len(objects))
    performance = [uj, uc, ij, ic]

    plt.bar(y_pos, performance, align='center', alpha=0.5, color=['black', 'red', 'green', 'blue', 'cyan'])
    plt.xticks(y_pos, objects)
    plt.ylabel('Average R Precision')
    plt.xlabel('System Used')
    plt.title('Recommender System Average R Precision Comparison')
    fig = plt.gcf().set_size_inches(18,10)
    plt.savefig('./graphing/output_images/bar_graphs/' + playlist_name + time.strftime("-%d-%m-%Y") + '.png')

    # plt.show()
