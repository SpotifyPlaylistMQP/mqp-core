from recommender_systems import feature_matrix_factorization
from mongodb import mongodb_communicate
from recommender_systems.modules import matrix, helpers, evaluation
import sys
import time

mongo_collection = sys.argv[1]
N = 15

playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
track_playlist_matrix = matrix.create(playlist_dict, unique_track_dict)

feature_matrix = []
for tid in unique_track_dict.keys():
    feature_matrix.append([
        unique_track_dict[tid]["danceability"],
        unique_track_dict[tid]["energy"],
        unique_track_dict[tid]["valence"]
    ])

filename = "feature_mf_training_results" + mongo_collection + ".txt"
open(filename, "w").close()
output = open(filename, "a")
output.write("alpha, beta, c, latent_features, steps, NDCG, R\n")

params = {
    "mpd_square_100": {
        "alpha_set": [0.1],
        "beta_set": [1],
        "c_set": [1, 0.1, 0.01, 0.05],
        "latent_features_set": [90],
        "steps_set": [150, 200, 250],
        "number_of_runs": 5,
        "number_of_playlists_to_test": 50
    },
    "mpd_square_1000": {
        "alpha_set": [1],
        "beta_set": [1e-4],
        "c_set": [10, 1, 1e-1, 1e-2, 1e-3, 1e-4],
        "latent_features_set": [10],
        "steps_set": [100, 150, 200],
        "number_of_runs": 5,
        "number_of_playlists_to_test": 50
    }
}
print("Params:")
print(params[mongo_collection])

for alpha in params[mongo_collection]["alpha_set"]:
    for beta in params[mongo_collection]["beta_set"]:
        for latent_features in params[mongo_collection]["latent_features_set"]:
            for steps in params[mongo_collection]["steps_set"]:
                for c in params[mongo_collection]["c_set"]:
                    train_params = {
                        "alpha": alpha,
                        "beta": beta,
                        "latent_features": latent_features,
                        "steps": steps,
                        "c": c
                    }
                    ndcg_result = 0
                    r_result = 0
                    for run in range(params[mongo_collection]["number_of_runs"]):
                        for input_playlist_index in range(params[mongo_collection]["number_of_playlists_to_test"]):
                            input_pid = indexed_pids[input_playlist_index]

                            T, new_playlist_tracks = matrix.split_playlist(input_pid, playlist_dict)
                            matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks, track_playlist_matrix, unique_track_dict)

                            ranked_tracks = feature_matrix_factorization.train_run(input_playlist_index, indexed_tids, track_playlist_matrix, feature_matrix, train_params)

                            recommended_tracks = helpers.recommend_n_tracks(N, ranked_tracks, new_playlist_tracks)
                            ndcg_result += evaluation.ndcg_precision(recommended_tracks, T, N, unique_track_dict)
                            r_result += evaluation.r_precision(recommended_tracks, T)

                            matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks + T, track_playlist_matrix, unique_track_dict)

                    ndcg = ndcg_result / (params[mongo_collection]['number_of_runs'] * params[mongo_collection]['number_of_playlists_to_test'])
                    r = r_result / (params[mongo_collection]['number_of_runs'] * params[mongo_collection]['number_of_playlists_to_test'])
                    output.write("{},{},{},{},{},{},{}\n".format(alpha, beta, c, latent_features, steps, ndcg, r))
                    print("{},{},{},{},{},{},{}".format(alpha, beta, c, latent_features, steps, ndcg, r))
