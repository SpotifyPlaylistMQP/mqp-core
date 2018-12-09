import sys
import run_mf, run_user, run_item, run_feature_mf # Recommender System Functions
from recommender_systems.modules import matrix
from mongodb import mongodb_communicate

mongo_collection = sys.argv[1]
rec_system = sys.argv[2]

playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
track_playlist_matrix = matrix.create(playlist_dict, unique_track_dict)
print("\tSparsity: ", matrix.sparsity(track_playlist_matrix))

max_N = 100 if mongo_collection == 'mpd_square_100' else 1000
filename = rec_system + "_" + mongo_collection
open("evaluation_data/" + filename, "w").close()

ndcg = None
r = None
if rec_system == 'item':
    ndcg, r = run_item.run(mongo_collection, playlist_dict, unique_track_dict, track_playlist_matrix, indexed_pids, indexed_tids, max_N)
elif rec_system == 'user':
    ndcg, r = run_user.run(mongo_collection, playlist_dict, unique_track_dict, track_playlist_matrix, indexed_pids, max_N)
elif rec_system == 'mf':
    ndcg, r = run_mf.run(mongo_collection, playlist_dict, unique_track_dict, track_playlist_matrix, indexed_tids, indexed_pids, max_N)
elif rec_system == 'feature_mf':
    ndcg, r = run_feature_mf.run(mongo_collection, playlist_dict, unique_track_dict, track_playlist_matrix, indexed_tids, indexed_pids, max_N)
else:
    print("Incorrect second argument, " + rec_system + " does not exist")
    print("csv_N_evaluation.py mongo_collection rec_system")
    exit()

output = open("evaluation_data/" + filename, "a")
output.write("N, NDCG, R\n")

for N in range(1, max_N + 1):
    output.write("{}, {}, {}\n".format(N, ndcg[N], r[N]))

print("Wrote results to evaluation_data/" + filename)