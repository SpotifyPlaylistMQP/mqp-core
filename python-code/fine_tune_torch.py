import sys
from recommender_systems import torch_matrix_factorization
from recommender_systems.modules import matrix, helpers, evaluation
from mongodb import mongodb_communicate

params = {
    "mpd_square_100": [
(1E+11, 50, 1.00E-15, 0.5,  "SGD"),
(100000000, 200, 1.00E-12, 0.5,  "SGD"),
(1000000000, 150, 1.00E-13, 0.5,  "SGD"),
(1000000000, 100, 1.00E-13, 0.5,  "SGD"),
(1000000, 75, 1.00E-10, 0.5,  "SGD"),
(100000000, 100, 1.00E-12, 0.5,  "SGD"),
(1000000, 100, 1.00E-10, 0.5,  "SGD"),
(1000, 50, 1.00E-07, 0.5,  "SGD"),
(1000000, 300, 1.00E-10, 0.5,  "SGD"),
(10000000, 200, 1.00E-11, 0.5,  "SGD"),
(100000000, 150, 1.00E-12, 0.5,  "SGD"),
(1E+11, 75, 1.00E-15, 0.5,  "SGD"),
(100000, 150, 1.00E-09, 0.5,  "SGD"),
(10000000, 500, 1.00E-11, 0.5,  "SGD"),
(10000000000, 150, 1.00E-14, 0.5,  "SGD"),
(10000, 300, 1.00E-08, 0.5,  "SGD"),
(1E+11, 150, 1.00E-15, 0.5,  "SGD"),
(1000000000, 75, 1.00E-13, 0.5,  "SGD"),
(1000000, 500, 1.00E-10, 0.5,  "SGD"),
(1E+11, 300, 1.00E-15, 0.5,  "SGD"),
(100000, 500, 1.00E-09, 0.5,  "SGD"),
(10000, 75, 1.00E-08, 0.5,  "SGD"),
(1000000000, 300, 1.00E-13, 0.5,  "SGD"),
(1000, 300, 1.00E-07, 0.5,  "SGD"),
(10000000, 75, 1.00E-11, 0.5,  "SGD"),
(1E+11, 100, 1.00E-15, 0.5,  "SGD"),
(10000000, 100, 1.00E-11, 0.5,  "SGD"),
(1000000, 200, 1.00E-10, 0.5,  "SGD"),
(10000, 150, 1.00E-08, 0.5,  "SGD"),
(10000000000, 75, 1.00E-14, 0.5,  "SGD"),
(10000000, 50, 1.00E-11, 0.5,  "SGD"),
(1000, 100, 1.00E-07, 0.5,  "SGD"),
(10000000000, 50, 1.00E-14, 0.5,  "SGD"),
(1000000000, 10, 1.00E-13, 0.5,  "SGD"),
(10000000000, 500, 1.00E-14, 0.5,  "SGD"),
(10000000000, 100, 1.00E-14, 0.5,  "SGD"),
(1000, 200, 1.00E-07, 0.5,  "SGD"),
(100000, 100, 1.00E-09, 0.5,  "SGD"),
(10000000, 150, 1.00E-11, 0.5,  "SGD"),
(1000000000, 200, 1.00E-13, 0.5,  "SGD"),
(10000, 100, 1.00E-08, 0.5,  "SGD"),
(1000000000, 50, 1.00E-13, 0.5,  "SGD"),
(1E+11, 200, 1.00E-15, 0.5,  "SGD"),
(100000, 200, 1.00E-09, 0.5,  "SGD"),
(10000, 50, 1.00E-08, 0.5,  "SGD"),
(1000000, 50, 1.00E-10, 0.5,  "SGD"),
(1000000, 150, 1.00E-10, 0.5,  "SGD"),
(100000, 300, 1.00E-09, 0.5,  "SGD"),
(100000000, 75, 1.00E-12, 0.5,  "SGD"),
(1000, 75, 1.00E-07, 0.5,  "SGD"),
(1000, 150, 1.00E-07, 0.5,  "SGD"),
(100000, 50, 1.00E-09, 0.5,  "SGD"),
(10000000000, 5, 1.00E-13, 0.5,  "SGD"),
(100000, 75, 1.00E-09, 0.5,  "SGD"),
(1E+11, 500, 1.00E-15, 0.5,  "SGD"),
(10000, 200, 1.00E-08, 0.5,  "SGD"),
(100000000, 500, 1.00E-12, 0.5,  "SGD"),
(10000, 500, 1.00E-08, 0.5,  "SGD"),
(100000000, 300, 1.00E-12, 0.5,  "SGD"),
(1000000, 10, 1.00E-10, 0.5,  "SGD"),
(10000, 10, 1.00E-08, 0.5,  "SGD"),
(1E+12, 75, 1.00E-15, 0.5,  "SGD"),
(1000, 5, 1.00E-07, 0.5,  "SGD"),
(1000, 10, 1.00E-07, 0.5,  "SGD"),
(100000000, 50, 1.00E-12, 0.5,  "SGD"),
(1000, 500, 1.00E-07, 0.5,  "SGD"),
(100000000, 10, 1.00E-12, 0.5,  "SGD"),
(10000000000, 10, 1.00E-14, 0.5,  "SGD"),
(1E+12, 200, 1.00E-15, 0.5,  "SGD"),
(1E+11, 10, 1.00E-14, 0.5,  "SGD"),
(10000000, 300, 1.00E-11, 0.5,  "SGD"),
(1E+12, 100, 1.00E-15, 0.5,  "SGD"),
(100000, 10, 1.00E-09, 0.5,  "SGD"),
(1E+11, 10, 1.00E-15, 0.5,  "SGD"),
(10000000000, 10, 1.00E-13, 0.5,  "SGD"),
(1000000000, 500, 1.00E-13, 0.5,  "SGD"),
(10000000000, 200, 1.00E-14, 0.5,  "SGD"),
(10000000, 10, 1.00E-11, 0.5,  "SGD"),
(10000000, 5, 1.00E-11, 0.5,  "SGD"),
(1E+12, 5, 1.00E-15, 0.5,  "SGD"),
(10000000000, 300, 1.00E-14, 0.5,  "SGD"),
(1E+11, 50, 1.00E-14, 0.5,  "SGD"),
(1E+12, 50, 1.00E-15, 0.5,  "SGD"),
(1E+12, 500, 1.00E-15, 0.5,  "SGD"),
(100, 50, 1.00E-06, 0.5,  "SGD"),
(100000000, 5, 1.00E-12, 0.5,  "SGD")
    ],
    "mpd_square_1000": [

    ]
}

mongo_collection = sys.argv[1]
params = params[mongo_collection]

filename = mongo_collection + "_torch_mf_fine_tuning.txt"
open("train_data/" + filename, "w").close()
output = open("train_data/" + filename, "a")
output.write("alpha, latent_features, learning_rate, percent_zeros, optimizer, NDCG\n")

playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
track_playlist_matrix = matrix.create(playlist_dict, unique_track_dict)

N = 10
number_of_runs = 10
number_of_playlists_to_test = 100
for param in params:
    train_params = {
        "alpha": param[0],
        "latent_features": param[1],
        "learning_rate": param[2],
        "percent_zeros": param[3],
        "optimizer": param[4]
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

        factorized_matrix = torch_matrix_factorization.get_factorized_matrix(mongo_collection, track_playlist_matrix,
                                                                             train_params)

        for input_playlist_index in range(number_of_playlists_to_test):
            input_pid = indexed_pids[input_playlist_index]

            ranked_tracks = torch_matrix_factorization.get_ranked_tracks(factorized_matrix, input_playlist_index,
                                                                         indexed_tids)
            recommended_tracks = helpers.recommend_n_tracks(N, ranked_tracks, new_playlist_tracks[input_pid])
            results += evaluation.ndcg_precision(recommended_tracks, T[input_pid], N, unique_track_dict)

            matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks[input_pid] + T[input_pid],
                                                track_playlist_matrix, unique_track_dict)

    avg_ndcg = results / (number_of_playlists_to_test * number_of_runs)
    print(
        "{}, {}, {}, {}, {}, NDCG:{}".format(param[0], param[1], param[2], param[3], param[4], avg_ndcg))
    output.write(
        "{}, {}, {}, {}, {}, {}\n".format(param[0], param[1], param[2], param[3], param[4], avg_ndcg))

print("Wrote results to evaluation_data/" + filename)