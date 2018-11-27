from recommender_systems import item_based
from recommender_systems.modules import matrix
from mongodb import mongodb_communicate
import sys
import time

def run(mongo_collection, max_N):
    start = time.time()
    #mongo_collection = sys.argv[1]
    user_params = {
        "mpd_square_100": {
            "K": 20
        },
        "mpd_square_1000": {
            "K": 40
        }
    }

    sample_size_for_avg = 100

    playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
    track_playlist_matrix = matrix.create(playlist_dict, unique_track_dict)
    print("\tSparsity: ", matrix.sparsity(track_playlist_matrix))

    ndcg_dict = {}
    r_dict = {}
    for N in range(1, max_N + 1):
        ndcg, r = item_based.run(playlist_dict, unique_track_dict, track_playlist_matrix, indexed_pids, indexed_tids, sample_size_for_avg, N, user_params[mongo_collection]['K'])
        ndcg_dict[N] = ndcg
        r_dict[N] = r

    print("Time in Seconds: ", time.time() - start)
    return ndcg_dict, r_dict


mongo_collection = sys.argv[1]
ndcg_dict, r_dict = run(mongo_collection, 5)

print(ndcg_dict)
print(r_dict)