from recommender_system import cosine_similarity, jaccard_similarity

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