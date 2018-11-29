from recommender_systems import item_based
from recommender_systems.modules import matrix
from mongodb import mongodb_communicate
import sys
import time

def run(mongo_collection, playlist_dict, unique_track_dict, track_playlist_matrix, indexed_pids, indexed_tids, max_N):
    start = time.time()

    item_params = {
        "mpd_square_100": {
            "K": 20,
            "number_of_runs": 10,
            "sample_size_for_avg": 100
        },
        "mpd_square_1000": {
            "K": 40,
            "number_of_runs": 10,
            "sample_size_for_avg": 1000
        }
    }

    ndcg_dict, r_dict = item_based.run(playlist_dict, unique_track_dict, track_playlist_matrix, indexed_pids, indexed_tids, max_N, item_params[mongo_collection])

    print("Time in Seconds: ", time.time() - start)
    return ndcg_dict, r_dict


mongo_collection = sys.argv[1]

playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
track_playlist_matrix = matrix.create(playlist_dict, unique_track_dict)
print("\tSparsity: ", matrix.sparsity(track_playlist_matrix))

ndcg_dict, r_dict = run(mongo_collection, playlist_dict, unique_track_dict, track_playlist_matrix, indexed_pids, indexed_tids, 5)

print(ndcg_dict)
print(r_dict)