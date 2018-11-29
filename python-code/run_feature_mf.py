from recommender_systems import feature_matrix_factorization
from recommender_systems.modules import matrix
from mongodb import mongodb_communicate
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
        "alpha": 1e-06,
        "beta": 0.001,
        "latent_features": 70,
        "steps": 100,
        "number_of_runs": 10,
        "sample_size_for_avg": 100
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


feature_matrix_factorization.run(playlist_dict, unique_track_dict, N, track_playlist_matrix, indexed_tids, indexed_pids, mf_params[mongo_collection])

print("Time in Seconds: ", time.time() - start)
