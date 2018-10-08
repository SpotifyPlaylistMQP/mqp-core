from .process import *
from math import *

def run(playlist_dict, indexed_pids, input_playlist_id, playlist_track_matrix, new_playlist_tracks, K, N):
    cosine_similarities = create(indexed_pids, input_playlist_id, playlist_track_matrix)
    top_k_most_similar_playlists, ranked_cosine_sims = find_top_k(cosine_similarities, K)
    unique_track_scores_in_top_k = top_k_track_scores(top_k_most_similar_playlists, playlist_dict)
    recommended_tracks = recommend_n_tracks(unique_track_scores_in_top_k, N, new_playlist_tracks)

    return recommended_tracks, ranked_cosine_sims

# Returns cosine_sim_dict, the cosine_sim of each playlist_id compared to the playlist_id_of_interest
def create(indexed_pids, playlist_id_of_interest, playlist_track_matrix):
    def calculate(col1, col2):
        numerator = sum(a * b for a, b in zip(col1, col2))
        denominator = sqrt(sum(a * a for a in col1)) * sqrt(sum(b * b for b in col2))
        return round(numerator / denominator, 5)

    cosine_similarities = [] # List of tuples (playlist_id, cosine_sim)
    index_of_interest = indexed_pids.index(playlist_id_of_interest)
    for playlist_id in indexed_pids:
        if playlist_id != playlist_id_of_interest:
            column_of_interest = []
            column_being_compared = []
            for t in range(len(playlist_track_matrix)):
                column_of_interest.append(playlist_track_matrix[t][index_of_interest])
                column_being_compared.append(playlist_track_matrix[t][indexed_pids.index(playlist_id)])
            cosine_similarities.append((playlist_id, calculate(column_of_interest, column_being_compared)))
    return cosine_similarities