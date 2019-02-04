import sys
from recommender_systems import matrix_factorization
from recommender_systems.modules import matrix, helpers, evaluation
from mongodb import mongodb_communicate

params = {
    "mpd_square_100": [
(10000, 1, 100, 500, 1.00E-06, 1.00E-05, 1.00E-07),
(10000, 0.0001, 100, 500, 1.00E-06, 1.00E-05, 1.00E-07),
(10000000, 10000, 100, 100, 1.00E-06, 1.00E-05, 1.00E-09),
(10000000, 0.01, 100, 100, 1.00E-06, 1.00E-05, 1.00E-09),
(10000, 0.01, 100, 500, 1.00E-06, 1.00E-05, 1.00E-07),
(10000, 100, 100, 500, 1.00E-06, 1.00E-05, 1.00E-07),
(10000000, 1.00E-10, 100, 100, 1.00E-06, 1.00E-05, 1.00E-09),
(10000, 1.00E-06, 100, 500, 1.00E-06, 1.00E-05, 1.00E-07),
(10000000, 1, 100, 100, 1.00E-06, 1.00E-05, 1.00E-09),
(10000000, 10000, 50, 100, 1.00E-06, 1.00E-05, 1.00E-09),
(10000000, 1.00E-10, 50, 100, 1.00E-06, 1.00E-05, 1.00E-09),
(10000000, 1.00E-06, 20, 100, 1.00E-06, 1.00E-05, 1.00E-09),
(10000, 1.00E-08, 100, 500, 1.00E-06, 1.00E-05, 1.00E-07),
(10000000, 1.00E-08, 20, 100, 1.00E-06, 1.00E-05, 1.00E-09),
(10000000, 100, 100, 100, 1.00E-06, 1.00E-05, 1.00E-09),
(10000, 1.00E-10, 100, 500, 1.00E-06, 1.00E-05, 1.00E-07),
(10000000, 1, 50, 100, 1.00E-06, 1.00E-05, 1.00E-09),
(10000000, 100, 50, 100, 1.00E-06, 1.00E-05, 1.00E-09),
(10000000, 1.00E-06, 50, 100, 1.00E-06, 1.00E-05, 1.00E-09),
(10000000, 0.01, 50, 100, 1.00E-06, 1.00E-05, 1.00E-09),
(10000000, 1.00E-08, 50, 100, 1.00E-06, 1.00E-05, 1.00E-09),
(10000000, 1, 20, 100, 1.00E-06, 1.00E-05, 1.00E-09)
    ],
    "mpd_square_1000": [

    ]
}

mongo_collection = sys.argv[1]
params = params[mongo_collection]

filename = mongo_collection + "_mf_fine_tuning.txt"
open("train_data/" + filename, "w").close()
output = open("train_data/" + filename, "a")
output.write("alpha, beta, latent_features, steps, error_limit, fit_error_limit, learning_rate, NDCG\n")


playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
track_playlist_matrix = matrix.create(playlist_dict, unique_track_dict)

N = 10
number_of_runs = 500
number_of_playlists_to_test = 100
for param in params:
    train_params = {
        "alpha": param[0],
        "regularization": param[1],
        "latent_features": param[2],
        "steps": param[3],
        "error_limit": param[4],
        "fit_error_limit": param[5],
        "learning_rate": param[6]
    }
    results = 0
    for run in range(number_of_runs):
        T = {}
        new_playlist_tracks = {}
        for input_playlist_index in range(number_of_playlists_to_test):
            input_pid = indexed_pids[input_playlist_index]
            T[input_pid], new_playlist_tracks[input_pid] = matrix.split_playlist(input_pid, playlist_dict)
            matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks[input_pid],
                                                track_playlist_matrix, unique_track_dict)

        factorized_matrix = matrix_factorization.get_factorized_matrix(mongo_collection, track_playlist_matrix, train_params)

        for input_playlist_index in range(number_of_playlists_to_test):
            input_pid = indexed_pids[input_playlist_index]

            ranked_tracks = matrix_factorization.get_ranked_tracks(factorized_matrix, input_playlist_index, indexed_tids)
            recommended_tracks = helpers.recommend_n_tracks(N, ranked_tracks, new_playlist_tracks[input_pid])
            results += evaluation.ndcg_precision(recommended_tracks, T[input_pid], N, unique_track_dict)

            matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks[input_pid] + T[input_pid],
                                                track_playlist_matrix, unique_track_dict)

    avg_ndcg = results / (number_of_playlists_to_test * number_of_runs)
    print("{}, {}, {}, {}, {}, {}, {}, NDCG:{}".format(param[0], param[1], param[2], param[3], param[4], param[5], param[6], avg_ndcg))
    output.write("{}, {}, {}, {}, {}, {}, {}, {}\n".format(param[0], param[1], param[2], param[3], param[4], param[5], param[6], avg_ndcg))

print("Wrote results to evaluation_data/" + filename)