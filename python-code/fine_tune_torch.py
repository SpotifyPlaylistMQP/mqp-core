import sys
from recommender_systems import torch_matrix_factorization
from recommender_systems.modules import matrix, helpers, evaluation
from mongodb import mongodb_communicate

params = {
    "mpd_square_100": [
(1, 150, 900, 0.1),
(1, 150, 900, 0.006),
(1, 150, 600, 0.06),
(1, 150, 900, 0.008),
(1, 150, 1000, 0.006),
(1, 150, 1000, 0.008),
(1, 150, 400, 0.1),
(1, 150, 700, 0.1),
(1, 150, 500, 0.06),
(1, 150, 400, 0.06),
(1, 150, 800, 0.006),
(1, 150, 500, 0.008),
(1, 150, 900, 0.06),
(1, 150, 400, 0.01),
(1, 150, 600, 0.01),
(1, 150, 500, 0.1),
(1, 150, 1000, 0.1),
(1, 150, 100, 0.06),
(1, 150, 300, 0.1),
(1, 150, 100, 0.1),
(1, 150, 1000, 0.06),
(1, 150, 700, 0.06),
(1, 150, 800, 0.008),
    ],
    "mpd_square_1000": [

    ]
}

mongo_collection = sys.argv[1]
params = params[mongo_collection]

filename = mongo_collection + "_torch_mf_fine_tuning.txt"
open("train_data/" + filename, "w").close()
output = open("train_data/" + filename, "a")
output.write("alpha, latent_features, steps, learning_rate NDCG\n")

playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
track_playlist_matrix = matrix.create(playlist_dict, unique_track_dict)

N = 10
number_of_runs = 10
number_of_playlists_to_test = 100
for param in params:
    train_params = {
        "alpha": param[0],
        "latent_features": param[1],
        "steps": param[2],
        "learning_rate": param[3]
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
        "{}, {}, {}, {}, NDCG:{}".format(param[0], param[1], param[2], param[3], avg_ndcg))
    output.write(
        "{}, {}, {}, {}, {}\n".format(param[0], param[1], param[2], param[3], avg_ndcg))

print("Wrote results to evaluation_data/" + filename)