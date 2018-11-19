from recommender_systems import item_based
from recommender_systems.modules import matrix
from mongodb import mongodb_communicate
import sys
import time

start = time.time()
mongo_collection = sys.argv[1]
N = 20  # Number of songs to recommend

sample_size_for_avg = 20
test_values = {
    "k_set": [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
}

playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
track_playlist_matrix = matrix.create(playlist_dict, unique_track_dict)
print("\tSparsity: ", matrix.sparsity(track_playlist_matrix))

item_based.train(playlist_dict, unique_track_dict, track_playlist_matrix, indexed_pids, indexed_tids, sample_size_for_avg, N, test_values)

print("Time in Seconds: ", time.time() - start)