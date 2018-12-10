import sys
from recommender_systems import user_based, item_based, matrix_factorization, feature_matrix_factorization
from recommender_systems.modules import matrix, helpers, evaluation
from mongodb import mongodb_communicate
import time

params = {
    "mpd_square_100": {
        "number_of_runs": 10,
        "number_of_playlists_to_test": 100,
        "max_N": 100
    },
    "mpd_square_1000": {
        "number_of_runs": 10,
        "number_of_playlists_to_test": 1000,
        "max_N": 1000
    }
}

mongo_collection = sys.argv[1]
rec_system = sys.argv[2]
params = params[mongo_collection]

playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
track_playlist_matrix = matrix.create(playlist_dict, unique_track_dict)

feature_matrix = []
for tid in unique_track_dict.keys():
    feature_matrix.append([
        unique_track_dict[tid]["danceability"],
        unique_track_dict[tid]["energy"],
        unique_track_dict[tid]["valence"]
    ])

ndcg_results = {}
r_results = {}
for N in range(1, params["max_N"] + 1):
    ndcg_results[N] = 0
    r_results[N] = 0

for run in range(params["number_of_runs"]):
    print("Run #", run + 1)
    start = time.time()
    for input_playlist_index in range(params["number_of_playlists_to_test"]):
        input_pid = indexed_pids[input_playlist_index]

        T, new_playlist_tracks = matrix.split_playlist(input_pid, playlist_dict)
        matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks, track_playlist_matrix, unique_track_dict)

        ranked_tracks = []
        if rec_system == 'item':
            ranked_tracks = item_based.get_ranked_tracks(new_playlist_tracks, indexed_tids, track_playlist_matrix, mongo_collection)
        elif rec_system == 'user':
            ranked_tracks = user_based.get_ranked_tracks(input_pid, input_playlist_index, playlist_dict, unique_track_dict, track_playlist_matrix, mongo_collection)
        elif rec_system == 'mf':
            ranked_tracks = matrix_factorization.get_ranked_tracks(input_playlist_index, indexed_tids, track_playlist_matrix, mongo_collection)
        elif rec_system == 'feature_mf':
            ranked_tracks = feature_matrix_factorization.get_ranked_tracks(input_playlist_index, indexed_tids, track_playlist_matrix, feature_matrix, mongo_collection)

        for N in range(1, params["max_N"] + 1):
            recommended_tracks = helpers.recommend_n_tracks(N, ranked_tracks, new_playlist_tracks)
            ndcg_results[N] += evaluation.ndcg_precision(recommended_tracks, T, N, unique_track_dict)
            r_results[N] += evaluation.r_precision(recommended_tracks, T)

        matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks + T, track_playlist_matrix, unique_track_dict)
    print("\ttook {} seconds".format(time.time() - start))

for N in range(1, params["max_N"] + 1):
    ndcg_results[N] = ndcg_results[N] / (params['number_of_runs'] * params['number_of_playlists_to_test'])
    r_results[N] = r_results[N] / (params['number_of_runs'] * params['number_of_playlists_to_test'])
print("\tAvg NDCG:", ndcg_results)
print("\tAvg R-Precision:", r_results)

filename = rec_system + "_" + mongo_collection
open("evaluation_data/" + filename, "w").close()
output = open("evaluation_data/" + filename, "a")
output.write("N, NDCG, R\n")
for N in range(1, params["max_N"] + 1):
    output.write("{}, {}, {}\n".format(N, ndcg_results[N], r_results[N]))
print("Wrote results to evaluation_data/" + filename)