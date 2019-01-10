import sys
from recommender_systems import matrix_factorization, feature_matrix_factorization
from recommender_systems.modules import matrix, helpers, evaluation
from mongodb import mongodb_communicate

params = {
    "mpd_square_100": {
        "alpha_set": [100, 1, 0.01, 0.0001, 0.000001],
        "beta_set": [100, 1, 0.01, 0.0001, 0.000001],
        "c_set": [100, 10, 1, 0.1, 0.01],
        "latent_features_set": [3, 10, 30, 50, 70, 90, 110],
        "steps_set": [100, 150, 200, 250],
        "number_of_playlists_to_test": 100,
    },
    "mpd_square_1000": {
        "alpha_set": [100, 1, 0.01, 0.0001, 0.000001],
        "beta_set": [100, 1, 0.01, 0.0001, 0.000001],
        "c_set": [100, 10, 1, 0.1, 0.01, 0.001],
        "latent_features_set": [3, 10, 30, 50],
        "steps_set": [50, 100, 150],
        "number_of_playlists_to_test": 100,
    }

}

mongo_collection = sys.argv[1]
params = params[mongo_collection]

filename = mongo_collection + "_mf_vs_feature_mf.txt"
open("train_data/" + filename, "w").close()
output = open("train_data/" + filename, "a")
output.write("alpha, beta, c, latent_features, steps, NDCG\n")

playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
track_playlist_matrix = matrix.create(playlist_dict, unique_track_dict)

feature_matrix = []
for tid in unique_track_dict.keys():
    feature_matrix.append([
        unique_track_dict[tid]["danceability"],
        unique_track_dict[tid]["energy"],
        unique_track_dict[tid]["valence"]
    ])

N = 10

for alpha in params["alpha_set"]:
    for beta in params["beta_set"]:
        for c in params["c_set"]:
            for latent_features in params["latent_features_set"]:
                for steps in params["steps_set"]:
                    train_params = {
                        "alpha": alpha,
                        "beta": beta,
                        "c": c,
                        "latent_features": latent_features,
                        "steps": steps
                    }
                    results = 0
                    for input_playlist_index in range(params["number_of_playlists_to_test"]):
                        input_pid = indexed_pids[input_playlist_index]

                        T, new_playlist_tracks = matrix.split_playlist(input_pid, playlist_dict)
                        matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks, track_playlist_matrix, unique_track_dict)

                        ranked_tracks = feature_matrix_factorization.train_run(input_playlist_index, indexed_tids, track_playlist_matrix, feature_matrix, train_params)
                        recommended_tracks = helpers.recommend_n_tracks(N, ranked_tracks, new_playlist_tracks)
                        results += evaluation.ndcg_precision(recommended_tracks, T, N, unique_track_dict)

                        matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks + T, track_playlist_matrix, unique_track_dict)

                    avg_ndcg = results / params['number_of_playlists_to_test']
                    print("{}, {}, {}, {}, {}, NDCG:{}".format(alpha, beta, c, latent_features, steps, avg_ndcg))
                    output.write("{}, {}, {}, {}, {}, {}\n".format(alpha, beta, c, latent_features, steps, avg_ndcg))

print("Wrote results to evaluation_data/" + filename)