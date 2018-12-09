import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time
import pprint

# Function compare_ndcg(): mf_dict, mf_feat_dict, playlist_name -> Image
# Creates a figure graph comparing
#       - X Value: N (the number of songs recommended)
#       - Y Value: Average NDCG Score
# var mf_dict: A dictionary containing tuples of [N Value: NDCG Score] for Normal Matrix Factorization
# var mf_feat_dict: A dictionary containing tuples of [N Value: NDCG Score] for Matrix Factorization w/ Additional Features
# var playlist_name: A string of the current playlist name
def compare_ndcg(mf_dict, mf_feat_dict, playlist_name):
    x_value = list(mf_dict.keys()) # X values
    mf_y = list(mf_dict.values()) # Y Values for normal Matrix Factorization
    mf_feat_y = list(mf_feat_dict.values()) # Y Values for Feature Matrix Factorization

    # Create the graph figure
    plt.figure(1)
    fig = plt.gcf().set_size_inches(28,16)

    # Graph setup
    plt.xlabel('K Value (# of songs recommended)', fontsize=12)
    plt.ylabel('NDCG Precision', fontsize=12)
    plt.title('N Values vs NDCG Precision for Normal and Additional Feature Matrix Factorization', fontsize=16)

    # Plotting
    plt.plot(x_value, mf_y, marker='o', color='r', label='Matrix Factorization') # User Based Jaccard Values RED
    plt.plot(x_value, mf_feat_y, marker='o', color='b', label='Matrix Factorization w/ Addl. Features') # Item Based Jaccard Values BLUE

    # Finalize and display the graph
    plt.legend()
    graph_name = playlist_name + time.strftime('-%d-%m-%Y') + '_vsfeatMF_ndcg.png'
    plt.savefig('./output_images/matrix_graphs/' + graph_name)
    print('\nGenerated the graph: \'' + graph_name + '\'')
    print('Saving to ./graphing/output_images/matrix_graphs/...')

# Function super_ndcg(): mf_dict, mf_feat_dict, user_dict, item_dict, playlist_name -> Image
# Creates a figure graph comparing
#       - X Value: N (the number of songs recommended)
#       - Y Value: Average NDCG Score
# var mf_dict: A dictionary containing tuples of [N Value: NDCG Score] for Normal Matrix Factorization
# var mf_feat_dict: A dictionary containing tuples of [N Value: NDCG Score] for Matrix Factorization w/ Additional Features
# var playlist_name: A string of the current playlist name
def super_ndcg(mf_dict, mf_feat_dict, user_dict, item_dict, playlist_name):
    x_value = list(mf_dict.keys()) # X values
    mf_y = list(mf_dict.values()) # Y Values for normal Matrix Factorization
    mf_feat_y = list(mf_feat_dict.values()) # Y Values for Feature Matrix Factorization
    user_y = list(user_dict.values()) # Y Values for normal Matrix Factorization
    item_y = list(item_dict.values()) # Y Values for Feature Matrix Factorization

    # Create the graph figure
    plt.figure(2)
    fig = plt.gcf().set_size_inches(28,16)

    # Graph setup
    plt.xlabel('K Value (# of songs recommended)', fontsize=12)
    plt.ylabel('NDCG Precision', fontsize=12)
    plt.title('N Values vs NDCG Precision for Recommender Systems', fontsize=16)

    # Plotting
    plt.plot(x_value, mf_y, marker='o', color='r', label='Normal MF') # RED
    plt.plot(x_value, mf_feat_y, marker='o', color='b', label='Additional Feature MF') # BLUE
    plt.plot(x_value, user_y, marker='o', color='g', label='User Based') # GREEN
    plt.plot(x_value, item_y, marker='o', color='y', label='Item Based') # YELLOW

    # Finalize and display the graph
    plt.legend()
    graph_name = playlist_name + time.strftime('-%d-%m-%Y') + '_superndcg.png'
    plt.savefig('./output_images/matrix_graphs/' + graph_name)
    print('\nGenerated the graph: \'' + graph_name + '\'')
    print('Saving to ./graphing/output_images/matrix_graphs/...')
