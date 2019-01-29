import sys
from recommender_systems import matrix_factorization
from recommender_systems.modules import matrix, helpers, evaluation
from mongodb import mongodb_communicate
import time

all_params = {
    "mpd_square_100": {
        "number_of_runs": 5,
        "alpha_set": [100, 10, 1, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
        "beta_set": [100, 10, 1, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
        "latent_features_set": [5, 10, 20, 30, 50, 80, 100],
        "steps_set": [50, 100, 150, 200],
        "number_of_playlists_to_test": 100,
    },
    "mpd_square_1000": {
        "number_of_runs": 1,
        "alpha_set": [100, 10, 1, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
        "beta_set": [100, 10, 1, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
        "latent_features_set": [5, 10, 20, 30, 50, 80, 100],
        "steps_set": [50, 100, 150, 200],
        "number_of_playlists_to_test": 1000,
    }
}

mongo_collection = sys.argv[1]
params = all_params[mongo_collection]

filename = "mf_" + mongo_collection + ".txt"
open("train_data/" + filename, "w").close()
output = open("train_data/" + filename, "a")
output.write("alpha, beta, latent_features, steps, NDCG\n")

playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
track_playlist_matrix = matrix.create(playlist_dict, unique_track_dict)

N = 10

for alpha in params["alpha_set"]:
    for beta in params["beta_set"]:
        for latent_features in params["latent_features_set"]:
            for steps in params["steps_set"]:
                train_params = {
                    "alpha": alpha,
                    "beta": beta,
                    "latent_features": latent_features,
                    "steps": steps
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
                        results += evaluation.ndcg_precision(recommended_tracks, T[input_pid], N, unique_track_dict)

                        matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks[input_pid] + T[input_pid], track_playlist_matrix, unique_track_dict)

                avg_ndcg = results / (params['number_of_playlists_to_test'] * params["number_of_runs"])
                print("{}, {}, {}, {}, NDCG:{}".format(alpha, beta, latent_features, steps, avg_ndcg))
                output.write("{}, {}, {}, {}, {}\n".format(alpha, beta, latent_features, steps, avg_ndcg))

print("Wrote results to train_data/" + filename)