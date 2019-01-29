import sys
from recommender_systems import feature_matrix_factorization
from recommender_systems.modules import matrix, helpers, evaluation
from mongodb import mongodb_communicate
import time

all_params = {
    "mpd_square_100": {
        "number_of_runs": 1,
        "alpha_set": [1e8, 1e6, 1e4, 1e2, 1, 1e-2, 1e-4, 1e-6, 1e-8, 1e-10],
        "beta_set": [1e8, 1e6, 1e4, 1e2, 1, 1e-2, 1e-4, 1e-6, 1e-8, 1e-10],
        "latent_features_set": [3, 5, 10, 15, 20],
        "steps_set": [1, 50, 100, 150, 200],
        "c_set": [1000, 100, 1, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 0],
        "number_of_playlists_to_test": 100,
    },
    "mpd_square_1000": {
        "number_of_runs": 10,
        "alpha_set": [1],
        "beta_set": [10],
        "latent_features_set": [30],
        "steps_set": [200],
        "c_set": [10000, 1000, 100, 10, 1, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9, 1e-10, 1e-11, 1e-12, 1e-13, 0],
        "number_of_playlists_to_test": 1000,
    }
}

mongo_collection = sys.argv[1]
params = all_params[mongo_collection]

filename = "feature_mf_" + mongo_collection + ".txt"
open("train_data/" + filename, "w").close()
output = open("train_data/" + filename, "a")
output.write("alpha, beta, latent_features, steps, C, NDCG\n")

playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
track_playlist_matrix = matrix.create(playlist_dict, unique_track_dict)

N = 10

for alpha in params["alpha_set"]:
    for beta in params["beta_set"]:
        for latent_features in params["latent_features_set"]:
            for steps in params["steps_set"]:
                for c in params["c_set"]:
                    train_params = {
                        "alpha": alpha,
                        "beta": beta,
                        "latent_features": latent_features,
                        "steps": steps,
                        "c": c
                    }
                    results = 0
                    for run in range(params["number_of_runs"]):
                        T = {}
                        new_playlist_tracks = {}
                        for input_playlist_index in range(params["number_of_playlists_to_test"]):
                            input_pid = indexed_pids[input_playlist_index]
                            T[input_pid], new_playlist_tracks[input_pid] = matrix.split_playlist(input_pid, playlist_dict)
                            matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks[input_pid], track_playlist_matrix, unique_track_dict)

                        feature_matrix = []
                        for tid in unique_track_dict.keys():
                            feature_matrix.append([
                                unique_track_dict[tid]["danceability"],
                                unique_track_dict[tid]["energy"],
                                unique_track_dict[tid]["valence"]
                            ])
                        factorized_matrix = feature_matrix_factorization.get_factorized_matrix(mongo_collection, track_playlist_matrix, feature_matrix, train_params)

                        for input_playlist_index in range(params["number_of_playlists_to_test"]):
                            input_pid = indexed_pids[input_playlist_index]

                            ranked_tracks = feature_matrix_factorization.get_ranked_tracks(factorized_matrix, input_playlist_index, indexed_tids)
                            recommended_tracks = helpers.recommend_n_tracks(N, ranked_tracks, new_playlist_tracks[input_pid])
                            results += evaluation.ndcg_precision(recommended_tracks, T[input_pid], N, unique_track_dict)

                            matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks[input_pid] + T[input_pid], track_playlist_matrix, unique_track_dict)

                    avg_ndcg = results / (params['number_of_playlists_to_test'] * params["number_of_runs"])
                    print("{}, {}, {}, {}, {}, NDCG:{}".format(alpha, beta, latent_features, steps, c, avg_ndcg))
                    output.write("{}, {}, {}, {}, {}, {}\n".format(alpha, beta, latent_features, steps, c, avg_ndcg))

print("Wrote results to train_data/" + filename)