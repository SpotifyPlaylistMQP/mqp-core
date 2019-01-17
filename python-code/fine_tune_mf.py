import sys
from recommender_systems import matrix_factorization
from recommender_systems.modules import matrix, helpers, evaluation
from mongodb import mongodb_communicate

params = {
    "mpd_square_100": [
(0.1, 1, 110, 150),
(0.1, 1, 50, 100),
(0.1, 1, 90, 100),
(0.1, 1, 70, 150),
(0.1, 1, 30, 150),
(0.1, 1, 30, 50),
(0.1, 1, 90, 200),
(0.1, 1, 30, 200),
(0.1, 1, 50, 150),
(0.1, 1, 30, 50),
(0.1, 1, 30, 100),
(0.1, 1, 10, 50),
(0.1, 1, 30, 10),
(0.1, 1, 90, 50),
(0.1, 1, 20, 100),
(0.1, 1, 10, 200),
(0.1, 1, 30, 100),
(0.1, 1, 90, 150),
(0.1, 1, 20, 50),
(0.1, 1, 10, 150),
(0.1, 1, 10, 10),
(0.1, 1, 10, 100),
(0.1, 1, 10, 50),
(0.1, 1, 20, 10)
    ],
    "mpd_square_1000": [

    ]
}

mongo_collection = sys.argv[1]
params = params[mongo_collection]

filename = mongo_collection + "_mf_fine_tuning.txt"
open("train_data/" + filename, "w").close()
output = open("train_data/" + filename, "a")
output.write("alpha, beta, latent_features, steps, NDCG\n")

playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
track_playlist_matrix = matrix.create(playlist_dict, unique_track_dict)

N = 10

for param in params:
    train_params = {
        "alpha": param[0],
        "beta": param[1],
        "latent_features": param[2],
        "steps": param[3]
    }
    num_tests = 10
    num_playlists = 100
    avg_ndcg = 0
    for test in range(num_tests):
        results = 0
        for input_playlist_index in range(num_playlists):
            input_pid = indexed_pids[input_playlist_index]

            T, new_playlist_tracks = matrix.split_playlist(input_pid, playlist_dict)
            matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks, track_playlist_matrix, unique_track_dict)

            ranked_tracks = matrix_factorization.train_run(input_playlist_index, indexed_tids, track_playlist_matrix, train_params)
            recommended_tracks = helpers.recommend_n_tracks(N, ranked_tracks, new_playlist_tracks)
            results += evaluation.ndcg_precision(recommended_tracks, T, N, unique_track_dict)

            matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks + T, track_playlist_matrix, unique_track_dict)

        avg_ndcg += results / num_playlists

    print("{}, {}, {}, {}, NDCG:{}".format(param[0], param[1], param[2], param[3], avg_ndcg / num_tests))
    output.write("{}, {}, {}, {}, {}\n".format(param[0], param[1], param[2], param[3], avg_ndcg / num_tests))

print("Wrote results to evaluation_data/" + filename)