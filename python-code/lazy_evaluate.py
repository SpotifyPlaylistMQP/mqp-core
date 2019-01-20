import sys
from recommender_systems import user_based, item_based, matrix_factorization, feature_matrix_factorization, torch_matrix_factorization
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
        "number_of_runs": 5,
        "number_of_playlists_to_test": 1000,
        "max_N": 100
    }
}

mongo_collection = sys.argv[1]
params = params[mongo_collection]

rec_systems = []
for i in range(2, len(sys.argv)):
    rec_systems.append(sys.argv[i])

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
for rec_system in rec_systems:
    ndcg_results[rec_system] = {}
    r_results[rec_system] = {}
    for N in range(1, params["max_N"] + 1):
        ndcg_results[rec_system][N] = 0
        r_results[rec_system][N] = 0

for run in range(params["number_of_runs"]):
    print("Run #", run + 1)
    start = time.time()

    T = {}
    new_playlist_tracks = {}
    for input_playlist_index in range(params["number_of_playlists_to_test"]):
        input_pid = indexed_pids[input_playlist_index]
        T[input_pid], new_playlist_tracks[input_pid] = matrix.split_playlist(input_pid, playlist_dict)
        matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks[input_pid], track_playlist_matrix, unique_track_dict)

    factorized_matrices = {}
    if 'mf' in rec_systems:
        factorized_matrices['mf'] = matrix_factorization.get_factorized_matrix(mongo_collection, track_playlist_matrix)
    if 'feature_mf' in rec_systems:
        factorized_matrices['feature_mf'] = feature_matrix_factorization.get_factorized_matrix(mongo_collection, track_playlist_matrix, feature_matrix)
    if 'torch_mf' in rec_systems:
        factorized_matrices['torch_mf'] = torch_matrix_factorization.get_factorized_matrix(mongo_collection, track_playlist_matrix)

    for input_playlist_index in range(params["number_of_playlists_to_test"]):
        input_pid = indexed_pids[input_playlist_index]

        for rec_system in rec_systems:
            ranked_tracks = []
            if rec_system == 'item':
                ranked_tracks = item_based.get_ranked_tracks(new_playlist_tracks[input_pid], indexed_tids, track_playlist_matrix, mongo_collection)
            elif rec_system == 'user':
                ranked_tracks = user_based.get_ranked_tracks(input_pid, input_playlist_index, playlist_dict, unique_track_dict, track_playlist_matrix, mongo_collection)
            elif rec_system == 'mf':
                ranked_tracks = matrix_factorization.get_ranked_tracks(factorized_matrices['mf'], input_playlist_index, indexed_tids)
            elif rec_system == 'feature_mf':
                ranked_tracks = feature_matrix_factorization.get_ranked_tracks(factorized_matrices['feature_mf'], input_playlist_index, indexed_tids)
            elif rec_system == 'torch_mf':
                ranked_tracks = torch_matrix_factorization.get_ranked_tracks(factorized_matrices['torch_mf'], input_playlist_index, indexed_tids)
            for N in range(1, params["max_N"] + 1):
                recommended_tracks = helpers.recommend_n_tracks(N, ranked_tracks, new_playlist_tracks[input_pid])
                ndcg_results[rec_system][N] += evaluation.ndcg_precision(recommended_tracks, T[input_pid], N, unique_track_dict)
                r_results[rec_system][N] += evaluation.r_precision(recommended_tracks, T[input_pid])

    for input_playlist_index in range(params["number_of_playlists_to_test"]):
        input_pid = indexed_pids[input_playlist_index]
        matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks[input_pid] + T[input_pid], track_playlist_matrix, unique_track_dict)
    print("\ttook {} seconds".format(time.time() - start))

for rec_system in rec_systems:
    for N in range(1, params["max_N"] + 1):
        ndcg_results[rec_system][N] = ndcg_results[rec_system][N] / (params['number_of_runs'] * params['number_of_playlists_to_test'])
        r_results[rec_system][N] = r_results[rec_system][N] / (params['number_of_runs'] * params['number_of_playlists_to_test'])
    print("\t" + rec_system + ":")
    print("\t\tAvg NDCG:", ndcg_results[rec_system])
    print("\t\tAvg R-Precision:", r_results[rec_system])

    filename = rec_system + "_" + mongo_collection
    open("evaluation_data/" + filename, "w").close()
    output = open("evaluation_data/" + filename, "a")
    output.write("N, NDCG, R\n")
    for N in range(1, params["max_N"] + 1):
        output.write("{}, {}, {}\n".format(N, ndcg_results[rec_system][N], r_results[rec_system][N]))
    print("Wrote results to evaluation_data/" + filename)
