import sys
import run_mf, run_user, run_item # Recommender System Functions
from recommender_systems.modules import matrix
from mongodb import mongodb_communicate
from graphing import versusN

mongo_collection = sys.argv[1] # Get the mongo collection name

playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
track_playlist_matrix = matrix.create(playlist_dict, unique_track_dict)
print("\tSparsity: ", matrix.sparsity(track_playlist_matrix))

max_N = 1000

mf_ndcg, mf_r = run_mf.run(mongo_collection, playlist_dict, unique_track_dict, track_playlist_matrix, indexed_tids, indexed_pids, max_N)
item_ndcg, item_r = run_item.run(mongo_collection, playlist_dict, unique_track_dict, track_playlist_matrix, indexed_pids, indexed_tids, max_N)
user_ndcg, user_r = run_user.run(mongo_collection, playlist_dict, unique_track_dict, track_playlist_matrix, indexed_pids, max_N)

print("Completed data collection... Creating graphs...")
versusN.n_vs_ndcg(user_ndcg, item_ndcg, mf_ndcg, mongo_collection)
versusN.n_vs_r_precision(user_r, item_r, mf_r, mongo_collection)
print("Done!")
