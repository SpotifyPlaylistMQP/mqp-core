import sys
from recommender_systems import user_based, item_based, matrix_factorization, feature_matrix_factorization
from recommender_systems.modules import matrix, helpers, evaluation
from mongodb import mongodb_communicate
import time

mongo_collection = sys.argv[1]

playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
track_playlist_matrix = matrix.create(playlist_dict, unique_track_dict)

mongodb_communicate.delete_matrix(mongo_collection)
mongodb_communicate.post_matrix(track_playlist_matrix, mongo_collection)