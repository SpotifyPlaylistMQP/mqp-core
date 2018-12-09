from recommender_systems import matrix_factorization
from recommender_systems.modules import matrix
from mongodb import mongodb_communicate
import sys
import time

start = time.time()
mongo_collection = sys.argv[1]
N = 20  # Number of songs to recommend

playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
track_playlist_matrix = matrix.create(playlist_dict, unique_track_dict)
print("\tSparsity: ", matrix.sparsity(track_playlist_matrix))

sample_size_for_avg = 100
test_values = {
    "alpha_set": [100, 10, 1, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9],
    "beta_set": [100, 10, 1, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9],
    "latent_features_set": [10, 30, 50, 70, 90, 110],
    "steps_set": [50, 100, 150, 200]
}
matrix_factorization.train(playlist_dict, unique_track_dict, N, track_playlist_matrix, indexed_tids, indexed_pids, sample_size_for_avg, test_values)

print("Time in Seconds: ", time.time() - start)
