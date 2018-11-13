from recommender_systems import user_based, item_based
from recommender_systems.modules import matrix, helpers
from mongodb import mongodb_communicate
from graphing import precisionGraph
import sys
import time
from graphing import timing

start = time.time()
mongo_collection = sys.argv[1]
N = 10  # Number of songs to recommend

number_of_times_to_run = 20
iteration_dcg_graph_data = []

playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
track_playlist_matrix = matrix.create(playlist_dict, unique_track_dict)
print("\tSparsity: ", matrix.sparsity(track_playlist_matrix))

# Both have Key = track_id, Value = Ordered (L -> G) list of similar track tuples
cosine_sim_playlist_dict, jaccard_sim_playlist_dict = user_based.create_similarity_dictionaries(playlist_dict, track_playlist_matrix)

# Both have Key = track_id, Value = Ordered (L -> G) list of similar track tuples
cosine_sim_track_dict, jaccard_sim_track_dict = item_based.create_similarity_dictionaries(indexed_tids, track_playlist_matrix)

for i in range(number_of_times_to_run):
    print("Iteration " + str(i + 1) + "-----------------------------------------------------------------------")
    uc, uj, user_final_time = user_based.run(playlist_dict, unique_track_dict, cosine_sim_playlist_dict, jaccard_sim_playlist_dict, N)
    ic, ij, item_final_time = item_based.run(playlist_dict, unique_track_dict, N, cosine_sim_track_dict, jaccard_sim_track_dict)
    print("Iteration " + str(i + 1) + " Timings Results:")
    print("User_Based Runtime: " + str(user_final_time))
    print("Item_Based Runtime: " + str(item_final_time))
    timing.save_time(user_final_time, "user_based")
    timing.save_time(item_final_time, "item_based")

    # R-precision graph
    dcg_data = {}
    dcg_data["uc"] = uc
    dcg_data["uj"] = uj
    dcg_data["ic"] = ic
    dcg_data["ij"] = ij
    iteration_dcg_graph_data.append(dcg_data)

dcg_graph_data = {}
uc_data = {}
uj_data = {}
ic_data = {}
ij_data = {}
for iteration in iteration_dcg_graph_data:
    for K in iteration['uc'].keys():
        if K not in uc_data.keys(): uc_data[K] = []
        if K not in uj_data.keys(): uj_data[K] = []
        uc_data[K].append(iteration['uc'][K])
        uj_data[K].append(iteration['uj'][K])
    for K in iteration['ic'].keys():
        if K not in ic_data.keys(): ic_data[K] = []
        if K not in ij_data.keys(): ij_data[K] = []
        ic_data[K].append(iteration['ic'][K])
        ij_data[K].append(iteration['ij'][K])

avg_uc = {}
avg_uj = {}
avg_ic = {}
avg_ij = {}
print("------RESULTS-------")
print("User Based:")
for K in iteration_dcg_graph_data[0]['uc'].keys():
    avg_uc[K] = helpers.get_avg_of_list(uc_data[K])
    avg_uj[K] = helpers.get_avg_of_list(uj_data[K])
    print("\tK = " + str(K) + ": cosine = " + str(avg_uc[K]) + ", jaccard = " + str(avg_uj[K]))
print("Item Based:")
for K in iteration_dcg_graph_data[0]['ic'].keys():
    avg_ic[K] = helpers.get_avg_of_list(ic_data[K])
    avg_ij[K] = helpers.get_avg_of_list(ij_data[K])
    print("\tK = " + str(K) + ": cosine = " + str(avg_ic[K]) + ", jaccard = " + str(avg_ij[K]))

dcg_graph_data['uc'] = avg_uc
dcg_graph_data['uj'] = avg_uj
dcg_graph_data['ic'] = avg_ic
dcg_graph_data['ij'] = avg_ij

#graph.create_graph(k_graph_data, mongo_collection)
#bar_graph.create_graph(r_precision_graph_data, mongo_collection)
precisionGraph.create_graph(dcg_graph_data, mongo_collection, N, number_of_times_to_run)

print("Time in Seconds: ", time.time() - start)
