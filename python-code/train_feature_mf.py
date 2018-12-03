from recommender_systems import feature_matrix_factorization
from recommender_systems.modules import matrix
from mongodb import mongodb_communicate
import numpy as np
import sys
import time

start = time.time()
mongo_collection = sys.argv[1]
N = 10

playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
track_playlist_matrix = matrix.create(playlist_dict, unique_track_dict)
print("\tSparsity: ", matrix.sparsity(track_playlist_matrix))

mf_params = {
    "mpd_square_100": {
        "alpha_set": [100, 10, 1, 0.1, 0.01, 0.001],
        "beta_set": [100, 10, 1, 0.1, 0.01, 0.001],
        "latent_features_set": [3, 5, 8, 11, 15],
        "steps_set": [10, 20, 30],
        "number_of_runs": 1,
        "sample_size_for_avg": 10
    },
    "mpd_square_1000": {
        "alpha": 1e-06,
        "beta": 0.001,
        "latent_features": 70,
        "steps": 200,
        "number_of_runs": 10,
        "sample_size_for_avg": 1000
    }
}
print("Params:")
print(mf_params[mongo_collection])

#Get features
feature_matrix = []

for tid in unique_track_dict.keys():
    feature_matrix.append([
        unique_track_dict[tid]["danceability"],
        unique_track_dict[tid]["energy"],
        unique_track_dict[tid]["tempo"],
        unique_track_dict[tid]["valence"]
    ])

# feature_matrix = np.array(feature_matrix).transpose()

feature_matrix_factorization.train(playlist_dict, unique_track_dict, feature_matrix, N, track_playlist_matrix, indexed_tids, indexed_pids, mf_params[mongo_collection])

print("Time in Seconds: ", time.time() - start)
