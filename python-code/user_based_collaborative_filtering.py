from recommender_system import playlist, matrix, evaluation, cosine_similarity, jaccard_similarity

def cosine_sim(playlist_dict, playlist_ids, input_playlist_id, playlist_track_matrix, new_playlist_tracks, K, N):
    cosine_similarities = cosine_similarity.create(playlist_ids, input_playlist_id, playlist_track_matrix)
    top_k_most_similar_playlists, ranked_cosine_sims = cosine_similarity.find_top_k(cosine_similarities, K)
    unique_track_scores_in_top_k = cosine_similarity.top_k_track_scores(top_k_most_similar_playlists, playlist_dict)
    recommended_tracks = cosine_similarity.recommend_n_tracks(unique_track_scores_in_top_k, N, new_playlist_tracks)

    return recommended_tracks, ranked_cosine_sims

def jaccard(playlist_ids, playlist_dict, new_playlist_tracks, input_playlist_id, playlist_track_matrix, K, N):
    jaccard_similarities = jaccard_similarity.create(playlist_ids, input_playlist_id, playlist_track_matrix)
    top_k_most_similar_playlists, ranked_jaccard_sims = jaccard_similarity.find_top_k(jaccard_similarities, K)
    unique_track_scores_in_top_k = jaccard_similarity.top_k_track_scores(top_k_most_similar_playlists, playlist_dict)
    recommended_tracks = jaccard_similarity.recommend_n_tracks(unique_track_scores_in_top_k, N, new_playlist_tracks)

    return recommended_tracks, ranked_jaccard_sims

def run(playlist_dict, unique_track_dict, playlist_ids, playlist_track_matrix):
    K = 3  # Number of top similar playlists to the input playlist
    N = 10  # Number of songs to recommend

    cosine_sim_data = []
    jaccard_sim_data = []
    cosine_sim_r_precision_results = []  # List of tuples: (input_playlist_id, r_precision)
    jaccard_sim_r_precision_results = []  # List of tuples: (input_playlist_id, r_precision)

    for input_playlist_index, input_playlist_id in enumerate(playlist_dict.keys()):
        T, new_playlist_tracks = playlist.split(input_playlist_id, playlist_dict)
        playlist_track_matrix = matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks, playlist_track_matrix, unique_track_dict)

        cosine_sim_recommendations, cosine_sim_results = cosine_sim(playlist_dict, playlist_ids, input_playlist_id, playlist_track_matrix, new_playlist_tracks, K, N)
        cosine_sim_data.append(cosine_sim_results)
        cosine_sim_r_precision = evaluation.r_precision(cosine_sim_recommendations, T, N, unique_track_dict)
        cosine_sim_r_precision_results.append(cosine_sim_r_precision)

        jaccard_recommendations, jaccard_results = jaccard(playlist_ids, playlist_dict, new_playlist_tracks, input_playlist_id, playlist_track_matrix, K, N)
        jaccard_sim_data.append(jaccard_results)
        jaccard_sim_r_precision = evaluation.r_precision(jaccard_recommendations, T, N, unique_track_dict)
        jaccard_sim_r_precision_results.append(jaccard_sim_r_precision)

        playlist_track_matrix = matrix.update_input_playlist_tracks(input_playlist_index, playlist_dict[input_playlist_id]["tracks"], playlist_track_matrix, unique_track_dict)

    cosine_sim_avg_precision = evaluation.avg_precision(cosine_sim_r_precision_results)
    print("Cosine Similarity Average Precision:", cosine_sim_avg_precision)
    cosine_sim_avg_data = evaluation.avg_data(cosine_sim_data)

    jaccard_sim_avg_precision = evaluation.avg_precision(jaccard_sim_r_precision_results)
    print("Jaccard Similarity Average Precision:", jaccard_sim_avg_precision)
    jaccard_sim_avg_data = evaluation.avg_data(jaccard_sim_data)

    return cosine_sim_avg_data, jaccard_sim_avg_data