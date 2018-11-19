from recommender_systems import item_based
from recommender_systems.modules import matrix
from mongodb import mongodb_communicate
import sys
import time

start = time.time()
mongo_collection = sys.argv[1]
N = 20  # Number of songs to recommend
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

item_based.run(playlist_dict, unique_track_dict, track_playlist_matrix, indexed_pids, indexed_tids, sample_size_for_avg, N, user_params[mongo_collection]['K'])

print("Time in Seconds: ", time.time() - start)