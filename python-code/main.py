from recommender_system import matrix
from mongodb import mongodb_communicate
from graphing import graph
import user_based_collaborative_filtering
import sys

mongo_collection = sys.argv[1]

playlist_dict, unique_track_dict, playlist_ids = mongodb_communicate.get(mongo_collection)
# playlist.pretty_print(playlist_dict, unique_track_dict)

playlist_track_matrix = matrix.create(playlist_dict, unique_track_dict)
# print("Sparsity:", matrix.sparsity(playlist_track_matrix))

cosine_sim_avg_data, jaccard_sim_avg_data = user_based_collaborative_filtering.run(playlist_dict, unique_track_dict, playlist_ids, playlist_track_matrix)

avg_data = {}
avg_data["cosine_sim"] = cosine_sim_avg_data
avg_data["jaccard_sim"] = jaccard_sim_avg_data

graph.create_graph(avg_data, mongo_collection)