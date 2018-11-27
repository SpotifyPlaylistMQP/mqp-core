import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt2
import matplotlib.patches as mpatches2
import time

# Function n_vs_ndcg(): Dictionary_1, Dictionary_2, Dictionary_3 -> Image
# Creates a figure graph comparing
#       - X Value: N (the number of songs to recommend)
#       - Y Value: NDCG Score
# var Dictionary_1: A dictionary containing tuples of [N Value: NDCG Score] for User_Based
# var Dictionary_2: A dictionary containing tuples of [N Value: NDCG Score] for Item_Based
# var Dictionary_3: A dictionary containing tuples of [N Value: NDCG Score] for Matrix_Factorization
def n_vs_ndcg(Dictionary_1, Dictionary_2, Dictionary_3, playlist_name):
    # User Values
    user_x = list(Dictionary_1.keys())
    user_y = list(Dictionary_1.values())
    # Item Values
    item_x = list(Dictionary_2.keys())
    item_y = list(Dictionary_2.values())
    # Matrix Values
    matrix_x = list(Dictionary_3.keys())
    matrix_y = list(Dictionary_3.values())

    # Create the graph figure
    plt.figure(1)
    fig = plt.gcf().set_size_inches(28,16)

    # Create the legend
    red_patch = mpatches.Patch(color='red', label='User Based Values')
    blue_patch = mpatches.Patch(color='blue', label='Item Based Values')
    green_patch = mpatches.Patch(color='green', label='Matrix Factorization Values')
    plt.legend(handles=[red_patch, blue_patch, green_patch])

    # Graph setup
    plt.xlabel('N Value (# of songs recommended)', fontsize=12)
    plt.ylabel('NDCG Precision', fontsize=12)
    plt.title('N Values vs NDCG Precision for User, Item, and Matrix Factorization Metrics', fontsize=16)

    # Plotting
    plt.plot(user_x, user_y, marker='o', color='r', label='User Based') # User Based Jaccard Values RED
    plt.plot(item_x, item_y, marker='o', color='b', label='Item Based') # Item Based Jaccard Values BLUE
    plt.plot(matrix_x, matrix_y, marker='o', color='g', label='Matrix Factorization') # Item Based Jaccard Values BLUE

    plt.legend(bbox_to_anchor=(0.02, 0.975, .22, 0), ncol=2, borderaxespad=0)
    z = np.polyfit(user_x, user_y, 1)
    p = np.poly1d(z)
    #UBJ_plot = plt.plot(uj_x,p(uj_x), "r--", label='User Based')
    z = np.polyfit(item_x, item_y, 1)
    p = np.poly1d(z)
    #UBC_plot = plt.plot(uc_x,p(uc_x), "b--", label='Item Based')
    z = np.polyfit(matrix_x, matrix_y, 1)
    p = np.poly1d(z)
    #UBC_plot = plt.plot(uc_x,p(uc_x), "b--", label='Matrix Factorization')

    # Finalize and display the graph
    graph_name = playlist_name + time.strftime("-%d-%m-%Y") + '_NDCG.png'
    plt.savefig('./graphing/output_images/evaluation_graphs/' + graph_name)
    print("Generated the graph: \"" + graph_name + "\"")
    print("Saving to ./graphing/output_images/evaluation_graphs/...")


# Function n_vs_r_precision(): Dictionary_1, Dictionary_2, Dictionary_3 -> Image
# Creates a figure graph comparing
#       - X Value: N (the number of songs to recommend)
#       - Y Value: NDCG Score
# var Dictionary_1: A dictionary containing tuples of [N Value: NDCG Score] for User_Based
# var Dictionary_2: A dictionary containing tuples of [N Value: NDCG Score] for Item_Based
# var Dictionary_3: A dictionary containing tuples of [N Value: NDCG Score] for Matrix_Factorization
def n_vs_r_precision(Dictionary_1, Dictionary_2, Dictionary_3, playlist_name):
    import matplotlib.pyplot as plt2
    import matplotlib.patches as mpatches2

    # User Values
    user_x = list(Dictionary_1.keys())
    user_y = list(Dictionary_1.values())
    # Item Values
    item_x = list(Dictionary_2.keys())
    item_y = list(Dictionary_2.values())
    # Matrix Values

    matrix_x = list(Dictionary_3.keys())
    matrix_y = list(Dictionary_3.values())

    # Create the graph figure
    plt2.figure(1)
    fig = plt2.gcf().set_size_inches(28,16)

    # Create the legend
    red_patch = mpatches2.Patch(color='red', label='User Based Values')
    blue_patch = mpatches2.Patch(color='blue', label='Item Based Values')
    green_patch = mpatches2.Patch(color='green', label='Matrix Factorization Values')
    plt2.legend(handles=[red_patch, blue_patch, green_patch])

    # Graph setup
    plt2.xlabel('N Value (# of songs recommended)', fontsize=12)
    plt2.ylabel('NDCG Precision', fontsize=12)
    plt2.title('N Values vs R Precision for User, Item, and Matrix Factorization Metrics', fontsize=16)

    # Plotting
    plt2.plot(user_x, user_y, marker='o', color='r', label='User Based') # User Based Jaccard Values RED
    plt2.plot(item_x, item_y, marker='o', color='b', label='Item Based') # Item Based Jaccard Values BLUE
    plt2.plot(matrix_x, matrix_y, marker='o', color='g', label='Matrix Factorization') # Item Based Jaccard Values BLUE

    plt2.legend(bbox_to_anchor=(0.02, 0.975, .22, 0), ncol=2, borderaxespad=0)
    z = np.polyfit(user_x, user_y, 1)
    p = np.poly1d(z)
    # UBJ_plot = plt.plot(uj_x,p(uj_x), "r--", label='User Based')
    z = np.polyfit(item_x, item_y, 1)
    p = np.poly1d(z)
    #UBC_plot = plt.plot(uc_x,p(uc_x), "b--", label='Item Based')
    z = np.polyfit(matrix_x, matrix_y, 1)
    p = np.poly1d(z)
    # UBC_plot = plt.plot(uc_x,p(uc_x), "b--", label='Matrix Factorization')

    # Finalize and display the graph
    graph_name = playlist_name + time.strftime("-%d-%m-%Y") + '_Rprecision.png'
    plt2.savefig('./graphing/output_images/evaluation_graphs/' + graph_name)
    print("Generated the graph: \"" + graph_name + "\"")
    print("Saving to ./graphing/output_images/evaluation_graphs/...")
