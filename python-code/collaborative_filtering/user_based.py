from collaborative_filtering.modules.shared import evaluation, matrix
from collaborative_filtering.modules.user_based import cosine_similarity, jaccard_similarity

def run(playlist_dict, unique_track_dict, indexed_pids, playlist_track_matrix, N):
    K = 3  # Number of top similar playlists to the input playlist
    print("User-based collaborative filtering...")
    print("\tK = ", K)
    print("\tN = ", N)

    cosine_sim_data = []
    jaccard_sim_data = []
    cosine_sim_r_precision_results = []  # List of tuples: (input_playlist_id, r_precision)
    jaccard_sim_r_precision_results = []  # List of tuples: (input_playlist_id, r_precision)

    for input_playlist_index, input_playlist_id in enumerate(playlist_dict.keys()):
        T, new_playlist_tracks = matrix.split_playlist(input_playlist_id, playlist_dict)
        playlist_track_matrix = matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks, playlist_track_matrix, unique_track_dict)

        cosine_sim_recommendations, cosine_sim_results = cosine_similarity.run(playlist_dict, indexed_pids, input_playlist_id, playlist_track_matrix, new_playlist_tracks, K, N)
        cosine_sim_data.append(cosine_sim_results)
        cosine_sim_r_precision_results.append(evaluation.r_precision(cosine_sim_recommendations, T, N, unique_track_dict))

        jaccard_recommendations, jaccard_results = jaccard_similarity.run(indexed_pids, playlist_dict, new_playlist_tracks, input_playlist_id, playlist_track_matrix, K, N)
        jaccard_sim_data.append(jaccard_results)
        jaccard_sim_r_precision_results.append(evaluation.r_precision(jaccard_recommendations, T, N, unique_track_dict))

        playlist_track_matrix = matrix.update_input_playlist_tracks(input_playlist_index, playlist_dict[input_playlist_id]["tracks"], playlist_track_matrix, unique_track_dict)

    cosine_sim_avg_precision = evaluation.avg_precision(cosine_sim_r_precision_results)
    print("\tCosine Similarity Average Precision =", cosine_sim_avg_precision)
    cosine_sim_avg_data = evaluation.avg_data(cosine_sim_data)

    jaccard_sim_avg_precision = evaluation.avg_precision(jaccard_sim_r_precision_results)
    print("\tJaccard Similarity Average Precision =", jaccard_sim_avg_precision)
    jaccard_sim_avg_data = evaluation.avg_data(jaccard_sim_data)

    return cosine_sim_avg_data, jaccard_sim_avg_data, cosine_sim_avg_precision, jaccard_sim_avg_precision