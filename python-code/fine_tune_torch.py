import sys
from recommender_systems import torch_matrix_factorization
from recommender_systems.modules import matrix, helpers, evaluation
from mongodb import mongodb_communicate

params = {
    "mpd_square_100": [
(25, 2000, 300, 500),
(30, 500, 350, 125),
(30, 2000, 350, 500),
(25, 700, 250, 200),
(30, 800, 450, 150),
(30, 800, 350, 200),
(30, 700, 300, 200),
(25, 600, 450, 100),
(30, 800, 500, 125),
(30, 700, 400, 150),
(30, 500, 300, 125),
(30, 700, 450, 125),
(30, 300, 500, 50),
(30, 500, 400, 100),
(30, 500, 450, 100),
(25, 800, 450, 125),
(30, 600, 300, 175),
(25, 800, 400, 150),
(30, 600, 350, 150),
(30, 700, 350, 175),
(25, 600, 300, 150),
(25, 800, 250, 200),
(30, 500, 300, 150),
(25, 800, 350, 175),
(25, 500, 400, 100),
(30, 800, 350, 150),
(30, 400, 350, 100),
(30, 600, 400, 125),
(30, 500, 250, 175),
(25, 300, 350, 50),
(25, 400, 400, 75),
(25, 700, 400, 125),
(25, 600, 250, 175),
(25, 500, 250, 150),
(25, 500, 250, 125),
(30, 400, 250, 125),
(30, 800, 400, 150),
(30, 600, 500, 100),
(25, 600, 400, 100),
(30, 800, 450, 125),
(25, 800, 500, 125),
(25, 700, 450, 100),
(25, 400, 350, 75),
(30, 300, 300, 75),
(25, 400, 300, 100),
(30, 600, 450, 100),
(30, 2000, 300, 500),
(25, 700, 500, 100),
(25, 700, 350, 150),
(25, 300, 450, 50),
(25, 2000, 250, 500),
(30, 600, 350, 75),
(25, 600, 500, 75),
(25, 600, 350, 125),
(25, 700, 350, 125),
(30, 600, 300, 100),
(25, 800, 300, 175),
(30, 200, 250, 50),
(30, 300, 450, 50),
(30, 400, 400, 75),
(25, 500, 400, 50),
(30, 800, 500, 50),
(30, 300, 350, 75),
(25, 300, 300, 75),
(30, 2000, 300, 200),
(25, 700, 300, 75),
(30, 700, 300, 125),
(25, 600, 400, 125),
(30, 700, 350, 125),
(25, 500, 300, 75),
(25, 2000, 500, 200),
(30, 400, 300, 50),
(25, 800, 450, 100),
(30, 500, 400, 75),

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

N = 5
number_of_runs = 100
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