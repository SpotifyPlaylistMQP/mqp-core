import sys
from recommender_systems import matrix_factorization
from recommender_systems.modules import matrix, helpers, evaluation
from mongodb import mongodb_communicate
import time

all_params = {
    "mpd_square_100": {
        "number_of_runs": 1,
        "alpha_set": [1],
        "latent_features_set": [10, 50, 100, 200, 400, 600, 800, 1000, 1500, 2000],
        "steps_set": [50, 100, 200, 300, 400, 500, 600],
        "learning_rate_set": [1e-2, 1e-4, 1e-6, 1e-8],
        "number_of_playlists_to_test": 100,
    },
    "mpd_square_1000": {
        "number_of_runs": 1,
        "alpha_set": [10000],
        "latent_features_set": [15, 16, 17, 18, 19, 20, 21],
        "steps_set": [50, 100, 150, 200, 250],
        "learning_rate_set": [1e-6],
        "number_of_playlists_to_test": 1000,
    }
}

mongo_collection = sys.argv[1]
params = all_params[mongo_collection]

filename = "mf_" + mongo_collection + ".txt"
open("train_data/" + filename, "w").close()
output = open("train_data/" + filename, "a")
output.write("alpha, beta, latent_features, steps, error_limit, fit_error_limit, learning_rate, NDCG\n")

playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
track_playlist_matrix = matrix.create(playlist_dict, unique_track_dict)

N = 10

for alpha in params["alpha_set"]:
    for latent_features in params["latent_features_set"]:
        for steps in params["steps_set"]:
            for learning_rate in params["learning_rate_set"]:
                train_params = {
                    "alpha": alpha,
                    "latent_features": latent_features,
                    "steps": steps,
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

                    factorized_matrix = matrix_factorization.get_factorized_matrix(mongo_collection, track_playlist_matrix, train_params)

                    for input_playlist_index in range(params["number_of_playlists_to_test"]):
                        input_pid = indexed_pids[input_playlist_index]

                        ranked_tracks = matrix_factorization.get_ranked_tracks(factorized_matrix, input_playlist_index, indexed_tids)
                        recommended_tracks = helpers.recommend_n_tracks(N, ranked_tracks, new_playlist_tracks[input_pid])
                        results += evaluation.ndcg_precision(recommended_tracks, T[input_pid])

                        matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks[input_pid] + T[input_pid], track_playlist_matrix, unique_track_dict)

                avg_ndcg = results / (params['number_of_playlists_to_test'] * params["number_of_runs"])
                print("{}, {}, {}, {}, NDCG:{}".format(alpha, latent_features, steps, learning_rate, avg_ndcg))
                output.write("{}, {}, {}, {}, {}\n".format(alpha, latent_features, steps, learning_rate, avg_ndcg))

print("Wrote results to train_data/" + filename)