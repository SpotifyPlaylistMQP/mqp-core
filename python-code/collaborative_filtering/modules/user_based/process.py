# Helper function for sorting a list of tuples
def sort_by_second_tuple(input):
    return input[1]

# Returns a list of playlist_ids of the top k most similar playlists
def find_top_k(cosine_similarities, K):
    cosine_similarities.sort(reverse=True, key=sort_by_second_tuple)

    top_k = [] # Tuple: (playlist_id, cosine_sim)
    ranked_cosine_sims = []
    for i in range(len(cosine_similarities)):
        if i < K:
            top_k.append(cosine_similarities[i])
        ranked_cosine_sims.append(cosine_similarities[i][1])

    return top_k, ranked_cosine_sims

# Returns the a list of each unique track's score in the top_k playlists
def top_k_track_scores(top_k, playlist_dict):
    def get_unique_tracks(top_k_list):
        unique_track_list = []
        for top_k_tuple in top_k_list:
            for tid in playlist_dict[top_k_tuple[0]]['tracks']:
                if tid not in unique_track_list:
                    unique_track_list.append(tid)
        return unique_track_list

    track_scores = []
    unique_tracks = get_unique_tracks(top_k)
    for tid in unique_tracks:
        score = 0
        for top_k_tuple in top_k:
            if tid in playlist_dict[top_k_tuple[0]]['tracks']:
                score += top_k_tuple[1]
        track_scores.append((tid, score))

    return track_scores

# Returns a list of n tracks that have been recommended to the input playlsit
def recommend_n_tracks(unique_track_scores_in_top_k, n, input_playlist_tracks):
    unique_track_scores_in_top_k.sort(reverse=True, key=sort_by_second_tuple)
    recommended_tracks = []
    index = 0
    while len(recommended_tracks) < n:
        if unique_track_scores_in_top_k[index][0] not in input_playlist_tracks:
            recommended_tracks.append(unique_track_scores_in_top_k[index][0])
        index += 1
    return recommended_tracks




