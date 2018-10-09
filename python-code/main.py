from collaborative_filtering import user_based, item_based
from collaborative_filtering.modules.shared import matrix
from mongodb import mongodb_communicate
from graphing import graph, bar_graph
import sys

mongo_collection = sys.argv[1]
N = 10  # Number of songs to recommend

number_of_times_to_run = 15
iteration_r_precision_graph_data = []
k_graph_data = {}

playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
matrix = matrix.create(playlist_dict, unique_track_dict)

for i in range(number_of_times_to_run):
    print("Iteration " + str(i + 1) + "------------------------_-_-_-_-_-_-_-_-_-_-_")
    k_graph_data["cosine_sim"], k_graph_data["jaccard_sim"], uc, uj = user_based.run(playlist_dict, unique_track_dict, indexed_pids, matrix, N)

    ic, ij = item_based.run(playlist_dict, unique_track_dict, indexed_tids, matrix, N)

    # R-precision graph
    r_precision_graph_data = {}
    r_precision_graph_data["uc"] = uc
    r_precision_graph_data["uj"] = uj
    r_precision_graph_data["ic"] = ic
    r_precision_graph_data["ij"] = ij
    iteration_r_precision_graph_data.append(r_precision_graph_data)


r_precision_graph_data = {}
avg_uc = 0
avg_uj = 0
avg_ic = 0
avg_ij = 0
for iteration in iteration_r_precision_graph_data:
    avg_uc += iteration['uc']
    avg_uj += iteration['uj']
    avg_ic += iteration['ic']
    avg_ij += iteration['ij']
r_precision_graph_data['uc'] = avg_uc / number_of_times_to_run
r_precision_graph_data['uj'] = avg_uj / number_of_times_to_run
r_precision_graph_data['ic'] = avg_ic / number_of_times_to_run
r_precision_graph_data['ij'] = avg_ij / number_of_times_to_run
print("Average R-Precision for User Based Cosine Similarity: ", r_precision_graph_data['uc'])
print("Average R-Precision for User Based Jaccard Similarity: ", r_precision_graph_data['uj'])
print("Average R-Precision for Item Based Cosine Similarity: ", r_precision_graph_data['ic'])
print("Average R-Precision for Item Based Jaccard Similarity: ", r_precision_graph_data['ij'])

# graph.create_graph(k_graph_data, mongo_collection)
bar_graph.create_graph(r_precision_graph_data, mongo_collection)

