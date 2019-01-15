import sys
from recommender_systems import torch_matrix_factorization
from recommender_systems.modules import matrix, helpers, evaluation
from mongodb import mongodb_communicate

params = {
    "mpd_square_100": [
        (10000000, 20, 1.00E-11),
        (10000000, 80, 1.00E-11),
        (1000000, 15, 1.00E-10),
        (1000000, 200, 1.00E-10),
        (10000, 6, 1.00E-08),
        (100000000, 200, 1.00E-12),
        (10000000, 100, 1.00E-11),
        (10000, 100, 1.00E-08),
        (10000, 10, 1.00E-08),
        (10000, 30, 1.00E-08),
        (10000, 10, 1.00E-08),
        (10000000, 10, 1.00E-11),
        (100000, 50, 1.00E-09),
        (100000000, 15, 1.00E-12),
        (100000, 80, 1.00E-09),
        (1000, 10, 1.00E-07)
    ],
    "mpd_square_1000": [

    ]
}

mongo_collection = sys.argv[1]
params = params[mongo_collection]

filename = mongo_collection + "_torch_mf_fine_tuning.txt"
open("train_data/" + filename, "w").close()
output = open("train_data/" + filename, "a")
output.write("alpha, latent_features, learning_rate, NDCG\n")

playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
track_playlist_matrix = matrix.create(playlist_dict, unique_track_dict)

N = 10

for param in params:
    train_params = {
        "alpha": param[0],
        "latent_features": param[1],
        "learning_rate": param[2]
    }
    num_tests = 5
    num_playlists = 100
    avg_ndcg = 0
    for test in range(num_tests):
        results = 0
        for input_playlist_index in range(num_playlists):
            input_pid = indexed_pids[input_playlist_index]

            T, new_playlist_tracks = matrix.split_playlist(input_pid, playlist_dict)
            matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks, track_playlist_matrix, unique_track_dict)

            ranked_tracks = torch_matrix_factorization.train_run(input_playlist_index, indexed_tids, indexed_pids, track_playlist_matrix, train_params)
            recommended_tracks = helpers.recommend_n_tracks(N, ranked_tracks, new_playlist_tracks)
            results += evaluation.ndcg_precision(recommended_tracks, T, N, unique_track_dict)

            matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks + T, track_playlist_matrix, unique_track_dict)

        avg_ndcg += results / num_playlists

    print("{}, {}, {}, NDCG:{}".format(param[0], param[1], param[2], avg_ndcg / num_tests))
    output.write("{}, {}, {}, {}\n".format(param[0], param[1], param[2], avg_ndcg / num_tests))

print("Wrote results to evaluation_data/" + filename)