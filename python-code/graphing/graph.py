import numpy as np
import matplotlib.pyplot as plt
from matplotlib import figure
import pylab
import time

def create_graph(graph_data, playlist_name):
    # User Based Cosine
    ubc_x = graph_data["cosine_sim"]["x"]
    ubc_y = graph_data["cosine_sim"]["y"]
    # Item Based Cosine
    #TODO
    # ibc_x =
    # ibc_y =
    # User Based Jaccard
    ubj_x = graph_data["jaccard_sim"]["x"]
    ubj_y = graph_data["jaccard_sim"]["y"]
    # Item Based Jaccard
    # TODO
    # ibj_u =
    # ibj_y =

    # Number of playlists/values sampled
    num_playlists = max(len(ubc_x), len(ubj_x))
    max_y_val = max(max(ubc_y), max(ubj_y))

    # creating the graph visual
    plt.xlabel('Playlists', fontsize=14)
    plt.ylabel('Average Cosine Similarity Value', fontsize=14)
    plt.title('Comparison of Recommender System Techniques', fontsize=20)

    # Plotting the data
    plt.plot(ubc_x, ubc_y, 'or') # User Based Cosine Values RED
    # plt.plot(ibc_x, ibc_y, 'ob') # Item Based Cosine Values BLUE
    plt.plot(ubj_x, ubj_y, 'og') # User Based Jaccard Values GREEN
    #plt.plot(ibc_x, ibc_y, 'oy') # Item Based Jaccard Values YELLOW

    # Creating best fit lines
    z = np.polyfit(ubc_x, ubc_y, 1)
    p = np.poly1d(z)
    plt.plot(ubc_x,p(ubc_x),"r--", label='User Based Cosine')
    #TODO
    # z = np.polyfit(ubj_x, ubc_y, 1)
    # p = np.poly1d(z)
    # plt.plot(ubc_x,p(ubc_x),"b--", label='Item Based Cosine')
    #TODO
    z = np.polyfit(ubj_x, ubj_y, 1)
    p = np.poly1d(z)
    plt.plot(ubj_x,p(ubj_x),"g--", label='User Based Jaccard')
    # TODO
    # z = np.polyfit(ubc_x, ubc_y, 1)
    # p = np.poly1d(z)
    # plt.plot(ubc_x,p(ubc_x),"y--", label='Item Based Jaccard')


    # Create and display the graph
    plt.axis([0, num_playlists+1, 0, max_y_val+0.1]) # [0, 1] y-axis, [0, number of playlists] x-axis
    pylab.legend(loc='upper left')
    plt.savefig('./graphing/output_images/'+playlist_name + time.strftime("-%d-%m-%Y") + '.png')
    # plt.show()
