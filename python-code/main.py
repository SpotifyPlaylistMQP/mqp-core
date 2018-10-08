from collaborative_filtering import user_based, item_based
from collaborative_filtering.modules.shared import matrix
from mongodb import mongodb_communicate
from graphing import graph
import sys

mongo_collection = sys.argv[1]
N = 10  # Number of songs to recommend

playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
matrix = matrix.create(playlist_dict, unique_track_dict)

graph_data = {}
graph_data["cosine_sim"], graph_data["jaccard_sim"] = user_based.run(playlist_dict, unique_track_dict, indexed_pids, matrix, N)
item_based.run(playlist_dict, unique_track_dict, indexed_tids, matrix, N)
graph.create_graph(graph_data, mongo_collection)

print("---------------------------------------------------------------------------------------------------------------")