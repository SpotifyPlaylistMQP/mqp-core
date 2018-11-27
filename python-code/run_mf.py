from recommender_systems import matrix_factorization
from recommender_systems.modules import matrix
from mongodb import mongodb_communicate
import sys
import time


def run(mongo_collection, max_N):
    start = time.time()

    ndcg_dict = {}
    r_dict = {}

    playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
    track_playlist_matrix = matrix.create(playlist_dict, unique_track_dict)
    print("\tSparsity: ", matrix.sparsity(track_playlist_matrix))

    mf_params = {
        "mpd_square_100": {
            "alpha": 1e-06,
            "beta": 0.001,
            "latent_features": 70,
            "steps": 200,
            "number_of_runs": 1,
            "sample_size_for_avg": 50
        },
        "mpd_square_1000": {
            "alpha": 1e-06,
            "beta": 0.001,
            "latent_features": 70,
            "steps": 200,
            "number_of_runs": 1,
            "sample_size_for_avg": 50
        }
    }
    print("Params:")
    print(mf_params[mongo_collection])

    for N in range(1, max_N + 1):
        ndcg_dict[N], r_dict[N] = matrix_factorization.run(playlist_dict, unique_track_dict, N, track_playlist_matrix, indexed_tids, indexed_pids, mf_params[mongo_collection])


    print("Time in Seconds: ", time.time() - start)

    return ndcg_dict, r_dict


mongo_collection = sys.argv[1]
