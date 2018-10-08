from collaborative_filtering.modules.shared import evaluation, matrix
from collaborative_filtering.modules.user_based import cosine_similarity, jaccard_similarity

def run(playlist_dict, unique_track_dict, playlist_ids, playlist_track_matrix):
    K = 3  # Number of top similar playlists to the input playlist
    N = 10  # Number of songs to recommend
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

        cosine_sim_recommendations, cosine_sim_results = cosine_similarity.run(playlist_dict, playlist_ids, input_playlist_id, playlist_track_matrix, new_playlist_tracks, K, N)
        cosine_sim_data.append(cosine_sim_results)
        cosine_sim_r_precision = evaluation.r_precision(cosine_sim_recommendations, T, N, unique_track_dict)
        cosine_sim_r_precision_results.append(cosine_sim_r_precision)

        jaccard_recommendations, jaccard_results = jaccard_similarity.run(playlist_ids, playlist_dict, new_playlist_tracks, input_playlist_id, playlist_track_matrix, K, N)
        jaccard_sim_data.append(jaccard_results)
        jaccard_sim_r_precision = evaluation.r_precision(jaccard_recommendations, T, N, unique_track_dict)
        jaccard_sim_r_precision_results.append(jaccard_sim_r_precision)

        playlist_track_matrix = matrix.update_input_playlist_tracks(input_playlist_index, playlist_dict[input_playlist_id]["tracks"], playlist_track_matrix, unique_track_dict)

    cosine_sim_avg_precision = evaluation.avg_precision(cosine_sim_r_precision_results)
    print("\tCosine Similarity Average Precision =", cosine_sim_avg_precision)
    cosine_sim_avg_data = evaluation.avg_data(cosine_sim_data)

    jaccard_sim_avg_precision = evaluation.avg_precision(jaccard_sim_r_precision_results)
    print("\tJaccard Similarity Average Precision =", jaccard_sim_avg_precision)
    jaccard_sim_avg_data = evaluation.avg_data(jaccard_sim_data)

    return cosine_sim_avg_data, jaccard_sim_avg_data