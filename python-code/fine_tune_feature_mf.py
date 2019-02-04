import sys
from recommender_systems import feature_matrix_factorization
from recommender_systems.modules import matrix, helpers, evaluation
from mongodb import mongodb_communicate

params = {
    "mpd_square_100": [
(1, 1, 3, 100, 0.01),
(1, 1, 3, 50, 1.00E-06),
(1, 1, 3, 150, 0.001),
(1, 0.01, 3, 50, 1.00E-05),
(1, 1, 3, 200, 0.0001),
(1, 1, 3, 200, 0.001),
(1, 1, 3, 50, 0.01),
(1, 1, 3, 150, 0.0001),
(1, 1, 3, 200, 0.1),
(1, 1, 3, 100, 0),
(1, 1, 3, 50, 1.00E-05),
(1, 0.01, 3, 50, 0),
(1, 1, 3, 50, 0.001),
(1, 1, 3, 200, 1.00E-05),
(1, 1, 3, 100, 0.0001),
(1, 0.01, 3, 200, 1.00E-05),
(1, 0.01, 3, 150, 1.00E-06),
(1, 1, 3, 50, 0),
(1, 1, 3, 150, 0),
(1, 1, 3, 150, 0.01),
(1, 1, 3, 150, 1.00E-05),
(1, 1, 3, 150, 1.00E-06),
(1, 1, 3, 150, 0.1),
(1, 1, 3, 50, 0.1),
(1, 1, 3, 200, 0),
(1, 1, 3, 200, 0.01),
(1, 1, 3, 100, 1.00E-06),
(1, 1, 3, 200, 1.00E-06),
(1, 1, 3, 100, 1.00E-05),
(1, 0.01, 3, 100, 1.00E-06),
(1, 0.01, 3, 200, 0.0001),
(1, 1, 5, 150, 0),
(1, 0.01, 3, 200, 1.00E-06),
(1, 0.01, 3, 100, 1.00E-05),
(1, 0.01, 3, 150, 1.00E-05),
(1, 0.01, 3, 50, 0.0001),
(1, 0.0001, 3, 50, 1.00E-06),
(1, 0.01, 3, 200, 0),
(1, 1, 3, 100, 0.1),
(1, 0.01, 3, 100, 0),
(1, 0.0001, 3, 100, 1.00E-06),
(1, 0.01, 3, 100, 0.0001),
(1, 0.01, 3, 150, 0),
(1, 1, 5, 150, 1.00E-06),
(1, 1, 5, 150, 0.01),
(1, 0.0001, 3, 50, 0),
(1, 1, 5, 100, 0.001),
(1, 1, 5, 150, 0.001),
(1, 0.01, 3, 150, 0.0001),
(1, 1, 5, 100, 1.00E-06),
(1, 1, 5, 50, 0),
(1, 1, 5, 50, 0.01),
(1, 1, 5, 200, 0.001),
(1, 1, 5, 200, 0),
(1, 1, 5, 50, 1.00E-06),
(1, 1, 5, 100, 1.00E-05),
(1, 1, 5, 100, 0.0001)
    ],
    "mpd_square_1000": [

    ]
}

mongo_collection = sys.argv[1]
params = params[mongo_collection]

filename = mongo_collection + "_feature_mf_fine_tuning.txt"
open("train_data/" + filename, "w").close()
output = open("train_data/" + filename, "a")
output.write("alpha, beta, latent_features, steps, c, NDCG\n")

playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
track_playlist_matrix = matrix.create(playlist_dict, unique_track_dict)

N = 10
number_of_runs = 100
number_of_playlists_to_test = 100
for param in params:
    train_params = {
        "alpha": param[0],
        "beta": param[1],
        "latent_features": param[2],
        "steps": param[3],
        "c": param[4]
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

        feature_matrix = []
        for tid in unique_track_dict.keys():
            feature_matrix.append([
                unique_track_dict[tid]["danceability"],
                unique_track_dict[tid]["energy"],
                unique_track_dict[tid]["valence"]
            ])
        factorized_matrix = feature_matrix_factorization.get_factorized_matrix(mongo_collection, track_playlist_matrix, feature_matrix,
                                                                            train_params)

        for input_playlist_index in range(number_of_playlists_to_test):
            input_pid = indexed_pids[input_playlist_index]

            ranked_tracks = feature_matrix_factorization.get_ranked_tracks(factorized_matrix, input_playlist_index,
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