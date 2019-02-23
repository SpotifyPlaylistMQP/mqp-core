import sys
from recommender_systems import torch_matrix_factorization
from recommender_systems.modules import matrix, helpers, evaluation
from mongodb import mongodb_communicate
import time

all_params = {
    "mpd_square_100": {
        "alpha_set": [1],
        "latent_features_set": [50, 100, 150, 200, 250, 300, 400, 500],
        "steps_set": [200, 300, 400, 500, 600, 700, 800, 900, 1000],
        "learning_rate_set": [1, 5e-1, 1e-1, 5e-2],
        "number_of_playlists_to_test": 100,
        "number_of_runs": 10
    },
    "mpd_square_1000": {
        "alpha_set": [1e6, 1e4, 1e2, 1, 1e-2, 1e-4],
        "beta_set": [0], #[1e8, 1e6, 1e4, 1e2, 1, 1e-2, 1e-4, 1e-6, 1e-8, 1e-10, 1e-12],
        "latent_features_set": [100],
        "learning_rate_set": [1e-8, 1e-10, 1e-12, 1e-14],
        "percent_zeros_set": [0.5, 0.25],
        "optimizer_set": ["SGD"],
        "embeddings_set": [0],
        "number_of_playlists_to_test": 1000,
        "number_of_runs": 1
    }
}

mongo_collection = sys.argv[1]
params = all_params[mongo_collection]

filename = "torch_mf_" + mongo_collection + ".txt"
open("train_data/" + filename, "w").close()
output = open("train_data/" + filename, "a")
output.write("alpha, latent_features, steps, learning_rate, NDCG\n")

playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
track_playlist_matrix = matrix.create(playlist_dict, unique_track_dict)

N = 10

for alpha in params["alpha_set"]:
    for latent_features in params["latent_features_set"]:
        for steps in params["steps_set"]:
            for learning_rate in params["learning_rate_set"]:
                train_params = {
                    "alpha": alpha,
                    "steps": steps,
                    "latent_features": latent_features,
                    "learning_rate": learning_rate
                }
                results = 0
                for run in range(params["number_of_runs"]):
                    T = {}
                    new_playlist_tracks = {}
                    for input_playlist_index in range(params["number_of_playlists_to_test"]):
                        input_pid = indexed_pids[input_playlist_index]
                        T[input_pid], new_playlist_tracks[input_pid] = matrix.split_playlist(input_pid, playlist_dict)
                        matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks[input_pid], track_playlist_matrix, unique_track_dict)

                    factorized_matrix = torch_matrix_factorization.get_factorized_matrix(mongo_collection, track_playlist_matrix, train_params)

                    for input_playlist_index in range(params["number_of_playlists_to_test"]):
                        input_pid = indexed_pids[input_playlist_index]

                        ranked_tracks = torch_matrix_factorization.get_ranked_tracks(factorized_matrix, input_playlist_index, indexed_tids)
                        recommended_tracks = helpers.recommend_n_tracks(N, ranked_tracks, new_playlist_tracks[input_pid])
                        results += evaluation.ndcg_precision(recommended_tracks, T[input_pid], N, unique_track_dict)

                        matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks[input_pid] + T[input_pid], track_playlist_matrix, unique_track_dict)

                avg_ndcg = results / (params['number_of_playlists_to_test'] * params["number_of_runs"])
                print("{}, {}, {}, {}, NDCG:{}".format(alpha, latent_features, steps, learning_rate, avg_ndcg))
                output.write("{}, {}, {}, {}, {}\n".format(alpha, latent_features, steps, learning_rate, avg_ndcg))

print("Wrote results to train_data/" + filename)