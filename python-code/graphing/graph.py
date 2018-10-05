import numpy as np
import matplotlib.pyplot as plt
# y axis: cosine similarity
# x axis: playlist
def avg_cosine(dict):

    # User Based Cosine
    ubc_x = avg_cosine_data["x"]
    ubc_y = avg_cosine_data["y"]
    # Item Based Cosine
    # ibc_x = [1,2,3,4,5,6,7,8,9,10]
    # ibc_y = [.98,0.92,0.81,0.60,0.57,0.31,0.25,0.11,0.03,0.01]
    # User Based Jaccard
    # TODO
    # ubj_x = []
    # ubj_y = []
    # Item Based Jaccard
    # TODO
    # ibj_u = []
    # ibj_y = []

    # Number of playlists sampled
    num_playlists = len(ubc_x);

    # creating the graph visual
    plt.xlabel('Playlists', fontsize=18)
    plt.ylabel('Average Cosine Similarity Value', fontsize=18)
    plt.title('Comparison of Recommender System Techniques', fontsize=24)

    # Plotting the data
    plt.plot(ubc_x, ubc_y, 'ob') # User Based Cosine Values BLUE
    plt.plot(ibc_x, ibc_y, 'or') # Item Based Cosine Values RED
    z = np.polyfit(ubc_x, ubc_y, 1)
    p = np.poly1d(z)
    plt.plot(ubc_x,p(ubc_x),"r--")
    #plt.plot(ibc_x, ibc_y, 'og') # User Based Jaccard Values GREEN
    #plt.plot(ibc_x, ibc_y, 'oy') # Item Based Jaccard Values YELLOW

    #
    plt.axis([0, num_playlists+1, 0, 1.1]) # [0, 1] y-axis, [0, number of playlists] x-axis
    plt.show()

avg_cosine();
