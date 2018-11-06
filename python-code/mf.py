from recommender_systems import matrix_factorization
from recommender_systems.modules import matrix, helpers
from mongodb import mongodb_communicate
from graphing import matrixGraph
import sys
import time

start = time.time()
mongo_collection = sys.argv[1]
N = 10  # Number of songs to recommend

playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
track_playlist_matrix = matrix.create(playlist_dict, unique_track_dict)
print("\tSparsity: ", matrix.sparsity(track_playlist_matrix))

steps = 10
avg_mf = {}

mf = matrix_factorization.run(playlist_dict, unique_track_dict, N, track_playlist_matrix, indexed_tids, indexed_pids, steps)


print("Time in Seconds: ", time.time() - start)
