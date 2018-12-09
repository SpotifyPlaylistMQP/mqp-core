import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time

# Function compare_ndcg(): mf_dict, mf_feat_dict, playlist_name -> Image
# Creates a figure graph comparing
#       - X Value: N (the number of songs recommended)
#       - Y Value: Average NDCG Score
# var mf_dict: A dictionary containing tuples of [N Value: NDCG Score] for Normal Matrix Factorization
# var mf_feat_dict: A dictionary containing tuples of [N Value: NDCG Score] for Matrix Factorization w/ Additional Features
# var playlist_name: A string of the current playlist name
def compare_ndcg(mf_dict, mf_feat_dict, playlist_name):
    # User Values
    mf_x = list(mf_dict.keys())
    mf_y = list(mf_dict.values())
    # Item Values
    mf_feat_x = list(mf_feat_dict.keys())
    mf_feat_y = list(mf_feat_dict.values())

    # Test print statements
    print('---------- NDCG Graph ---------- ')
    print('Normal Matrix Factorization')
    print(mf_x)
    print(mf_y)
    print('Matrix Factorization w/ Additional Features')
    print(mf_feat_x)
    print(mf_feat_y)

    # Create the graph figure
    plt.figure(1)
    fig = plt.gcf().set_size_inches(28,16)

    # Create the legend
    red_patch = mpatches.Patch(color='red', label='Matrix Factorization')
    blue_patch = mpatches.Patch(color='blue', label='Matrix Factorization w/ Addl. Features')
    plt.legend(handles=[red_patch, blue_patch])

    # Graph setup
    plt.xlabel('K Value (# of songs recommended)', fontsize=12)
    plt.ylabel('NDCG Precision', fontsize=12)
    plt.title('N Values vs NDCG Precision for Normal and Additional Feature Matrix Factorization', fontsize=16)

    # Plotting
    plt.plot(mf_x, mf_y, marker='o', color='r', label='Normal MF') # User Based Jaccard Values RED
    plt.plot(mf_feat_x, mf_feat_y, marker='o', color='b', label='Additional Feature MF') # Item Based Jaccard Values BLUE

    plt.legend(bbox_to_anchor=(0.02, 0.975, .22, 0), ncol=2, borderaxespad=0)
    # z = np.polyfit(user_x, user_y, 1)
    # p = np.poly1d(z)
    # UBJ_plot = plt.plot(uj_x,p(uj_x), 'r--', label='User Based')
    # z = np.polyfit(item_x, item_y, 1)
    # p = np.poly1d(z)
    # UBC_plot = plt.plot(uc_x,p(uc_x), 'b--', label='Item Based')
    # z = np.polyfit(matrix_x, matrix_y, 1)
    # p = np.poly1d(z)
    # UBC_plot = plt.plot(uc_x,p(uc_x), 'g--', label='Matrix Factorization')

    # Finalize and display the graph
    graph_name = playlist_name + time.strftime('-%d-%m-%Y') + '_vsfeatMF_ndcg.png'
    plt.savefig('./graphing/output_images/matrix_graphs/' + graph_name)
    print('Generated the graph: \'' + graph_name + '\'')
    print('Saving to ./graphing/output_images/matrix_graphs/...')


# Function compare_rprec(): mf_dict, mf_feat_dict, playlist_name -> Image
# Creates a figure graph comparing
#       - X Value: N (the number of songs recommended)
#       - Y Value: Average NDCG Score
# var mf_dict: A dictionary containing tuples of [N Value: NDCG Score] for Normal Matrix Factorization
# var mf_feat_dict: A dictionary containing tuples of [N Value: NDCG Score] for Matrix Factorization w/ Additional Features
# var playlist_name: A string of the current playlist name
def compare_rprec(mf_dict, mf_feat_dict, playlist_name):
    # User Values
    mf_x = list(mf_dict.keys())
    mf_y = list(mf_dict.values())
    # Item Values
    mf_feat_x = list(mf_feat_dict.keys())
    mf_feat_y = list(mf_feat_dict.values())

    # Test print statements
    print('---------- NDCG Graph ---------- ')
    print('Matrix Factorization')
    print(mf_x)
    print(mf_y)
    print('Matrix Factorization w/ Additional Features')
    print(mf_feat_x)
    print(mf_feat_y)

    # Create the graph figure
    plt.figure(1)
    fig = plt.gcf().set_size_inches(28,16)

    # Create the legend
    red_patch = mpatches.Patch(color='red', label='Matrix Factorization')
    blue_patch = mpatches.Patch(color='blue', label='Matrix Factorization w/ Addl. Features')
    plt.legend(handles=[red_patch, blue_patch])

    # Graph setup
    plt.xlabel('K Value (# of songs recommended)', fontsize=12)
    plt.ylabel('NDCG Precision', fontsize=12)
    plt.title('N Values vs R Precision for Normal and Additional Feature Matrix Factorization', fontsize=16)

    # Plotting
    plt.plot(mf_x, mf_y, marker='o', color='r', label='Normal MF') # User Based Jaccard Values RED
    plt.plot(mf_feat_x, mf_feat_y, marker='o', color='b', label='Additional Feature MF') # Item Based Jaccard Values BLUE

    plt.legend(bbox_to_anchor=(0.02, 0.975, .22, 0), ncol=2, borderaxespad=0)
    # z = np.polyfit(user_x, user_y, 1)
    # p = np.poly1d(z)
    # UBJ_plot = plt.plot(uj_x,p(uj_x), 'r--', label='User Based')
    # z = np.polyfit(item_x, item_y, 1)
    # p = np.poly1d(z)
    # UBC_plot = plt.plot(uc_x,p(uc_x), 'b--', label='Item Based')
    # z = np.polyfit(matrix_x, matrix_y, 1)
    # p = np.poly1d(z)
    # UBC_plot = plt.plot(uc_x,p(uc_x), 'g--', label='Matrix Factorization')

    # Finalize and display the graph
    graph_name = playlist_name + time.strftime('-%d-%m-%Y') + '_vsfeatMF_ndcg.png'
    plt.savefig('./graphing/output_images/matrix_graphs/' + graph_name)
    print('Generated the graph: \'' + graph_name + '\'')
    print('Saving to ./graphing/output_images/matrix_graphs/...')
