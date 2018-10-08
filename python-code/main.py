from collaborative_filtering import user_based
from collaborative_filtering.modules.shared import matrix
from mongodb import mongodb_communicate
from graphing import graph
import sys

graph_data = {}

mongo_collection = sys.argv[1]

playlist_dict, unique_track_dict, playlist_ids = mongodb_communicate.get(mongo_collection)

playlist_track_matrix = matrix.create(playlist_dict, unique_track_dict)


graph_data["cosine_sim"], graph_data["jaccard_sim"] = user_based.run(playlist_dict, unique_track_dict, playlist_ids, playlist_track_matrix)

graph.create_graph(graph_data, mongo_collection)