import sys
from recommender_systems import torch_matrix_factorization
from recommender_systems.modules import matrix, helpers, evaluation
from mongodb import mongodb_communicate

all_params = {
    "mpd_square_100": {
        "alpha_set": [100000, 10000, 1000, 100, 10, 1, 0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001],
        "latent_features_set": [6, 10, 15, 20, 30, 50, 80, 100, 200],
        "learning_rate_set": [1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9, 1e-10, 1e-11, 1e-12],
        "number_of_playlists_to_test": 5,
    },
    "mpd_square_1000": {
        "alpha_set": [100],
        "latent_features_set": [5, 10, 15],
        "learning_rate_set": [1e-8, 1e-9, 1e-10, 1e-11],
        "number_of_playlists_to_test": 5,
    }
}

mongo_collection = sys.argv[1]
params = all_params[mongo_collection]

filename = "torch_mf_" + mongo_collection + ".txt"
open("train_data/" + filename, "w").close()
output = open("train_data/" + filename, "a")
output.write("alpha, latent_features, learning_rate, NDCG\n")

playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
track_playlist_matrix = matrix.create(playlist_dict, unique_track_dict)

N = 15

for alpha in params["alpha_set"]:
    for latent_features in params["latent_features_set"]:
        for learning_rate in params["learning_rate_set"]:
            train_params = {
                "alpha": alpha,
                "latent_features": latent_features,
                "learning_rate": learning_rate
            }
            results = 0
            for input_playlist_index in range(params["number_of_playlists_to_test"]):
                input_pid = indexed_pids[input_playlist_index]

                T, new_playlist_tracks = matrix.split_playlist_not_random(input_pid, playlist_dict)
                matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks, track_playlist_matrix, unique_track_dict)

                ranked_tracks = torch_matrix_factorization.train_run(input_playlist_index, indexed_tids, indexed_pids, track_playlist_matrix, train_params)
                recommended_tracks = helpers.recommend_n_tracks(N, ranked_tracks, new_playlist_tracks)
                results += evaluation.ndcg_precision(recommended_tracks, T, N, unique_track_dict)

                matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks + T, track_playlist_matrix, unique_track_dict)

            avg_ndcg = results / params['number_of_playlists_to_test']
            print("{}, {}, {}, NDCG:{}".format(alpha, latent_features, learning_rate, avg_ndcg))
            output.write("{}, {}, {}, {}\n".format(alpha, latent_features, learning_rate, avg_ndcg))

print("Wrote results to train_data/" + filename)