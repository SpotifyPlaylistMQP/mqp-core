import sys
from recommender_systems import user_based, item_based, matrix_factorization, feature_matrix_factorization, torch_matrix_factorization
from recommender_systems.modules import matrix, helpers, evaluation
from mongodb import mongodb_communicate

input_pid = sys.argv[1]
mongo_collection = sys.argv[2]
rec_system = sys.argv[3]

playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get_no_print(mongo_collection)
track_playlist_matrix = mongodb_communicate.get_matrix(mongo_collection)

max_N = 20

input_playlist_index = 0
for index, pid in enumerate(indexed_pids):
    if pid == input_pid:
        input_playlist_index = index
        break

avg_ndcg = {}
avg_r = {}
for N in range(1, max_N + 1):
    avg_ndcg[N] = 0
    avg_r[N] = 0

num_runs = 10
for run in range(num_runs):
    T, new_playlist_tracks = matrix.split_playlist(input_pid, playlist_dict)
    matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks, track_playlist_matrix, unique_track_dict)

    ranked_tracks = []
    if rec_system == 'item':
        ranked_tracks = item_based.get_ranked_tracks(new_playlist_tracks, indexed_tids, track_playlist_matrix, mongo_collection)
    elif rec_system == 'user':
        ranked_tracks = user_based.get_ranked_tracks(input_pid, input_playlist_index, playlist_dict, unique_track_dict, track_playlist_matrix, mongo_collection)
    elif rec_system == 'mf':
        factorized_matrix = matrix_factorization.get_factorized_matrix(mongo_collection, track_playlist_matrix)
        ranked_tracks = matrix_factorization.get_ranked_tracks(factorized_matrix, input_playlist_index, indexed_tids)
    elif rec_system == 'feature_mf':
        feature_matrix = []
        for tid in unique_track_dict.keys():
            feature_matrix.append([
                unique_track_dict[tid]["danceability"],
                unique_track_dict[tid]["energy"],
                unique_track_dict[tid]["valence"]
            ])
        factorized_matrix = feature_matrix_factorization.get_factorized_matrix(mongo_collection, track_playlist_matrix, feature_matrix)
        ranked_tracks = feature_matrix_factorization.get_ranked_tracks(factorized_matrix, input_playlist_index, indexed_tids)
    elif rec_system == 'torch_mf':
        factorized_matrix = torch_matrix_factorization.get_factorized_matrix(mongo_collection, track_playlist_matrix)
        ranked_tracks = torch_matrix_factorization.get_ranked_tracks(factorized_matrix, input_playlist_index, indexed_tids)

    for N in range(1, max_N + 1):
        recommended_tracks = helpers.recommend_n_tracks(N, ranked_tracks, new_playlist_tracks)
        avg_ndcg[N] += evaluation.ndcg_precision(recommended_tracks, T, N, unique_track_dict)
        avg_r[N] += evaluation.r_precision(recommended_tracks, T)

    matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks + T, track_playlist_matrix, unique_track_dict)

output = "N, NDCG, R\n"
for N in range(1, max_N + 1):
    output += "{}, {}, {}\n".format(N, avg_ndcg[N] / num_runs, avg_r[N] / num_runs)

print(output)
sys.stdout.flush()