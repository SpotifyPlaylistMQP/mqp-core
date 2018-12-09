from recommender_systems import matrix_factorization
import time


def run(mongo_collection, playlist_dict, unique_track_dict, track_playlist_matrix, indexed_tids, indexed_pids, max_N):
    start = time.time()

    mf_params = {
        "mpd_square_100": {
            "alpha": 0.1,
            "beta": 1,
            "latent_features": 90,
            "steps": 150,
            "number_of_runs": 10,
            "sample_size_for_avg": 100
        },
        "mpd_square_1000": {
            "alpha": 1,
            "beta": 1e-4,
            "latent_features": 10,
            "steps": 100,
            "number_of_runs": 5,
            "sample_size_for_avg": 100
        }
    }
    print("Params:")
    print(mf_params[mongo_collection])

    ndcg_dict, r_dict = matrix_factorization.run(playlist_dict, unique_track_dict, max_N, track_playlist_matrix, indexed_tids, indexed_pids, mf_params[mongo_collection])

    print("Time in Seconds: ", time.time() - start)
    return ndcg_dict, r_dict

"""
mongo_collection = sys.argv[1]

playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
track_playlist_matrix = matrix.create(playlist_dict, unique_track_dict)
print("\tSparsity: ", matrix.sparsity(track_playlist_matrix))

run(mongo_collection, playlist_dict, unique_track_dict, track_playlist_matrix, indexed_tids, indexed_pids, 5)
"""