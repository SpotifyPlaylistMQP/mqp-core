from .process import *

def run(playlist_ids, playlist_dict, new_playlist_tracks, input_playlist_id, playlist_track_matrix, K, N):
    jaccard_similarities = create(playlist_ids, input_playlist_id, playlist_track_matrix)
    top_k_most_similar_playlists, ranked_jaccard_sims = find_top_k(jaccard_similarities, K)
    unique_track_scores_in_top_k = top_k_track_scores(top_k_most_similar_playlists, playlist_dict)
    recommended_tracks = recommend_n_tracks(unique_track_scores_in_top_k, N, new_playlist_tracks)

    return recommended_tracks, ranked_jaccard_sims

# Returns jaccard_sim_dict, the jaccard_sim of each playlist_id compared to the playlist_id_of_interest
def create(playlist_ids, playlist_id_of_interest, playlist_track_matrix):
    def calculate(col1, col2):
        numerator = 0
        denominator = 0

        for a, b in zip(col1, col2):
            if (a == b) and (a == 1) and (b == 1):
                numerator += 1
                denominator += 1
            elif (a == 1) and (b == 0):
                denominator += 1
            elif (a == 0) and (b == 1):
                denominator += 1

        return numerator / denominator

    jaccard_similarities = [] # List of tuples (playlist_id, jaccard_sim)
    index_of_interest = playlist_ids.index(playlist_id_of_interest)
    for playlist_id in playlist_ids:
        if playlist_id != playlist_id_of_interest:
            column_of_interest = []
            column_being_compared = []
            for t in range(len(playlist_track_matrix)):
                column_of_interest.append(playlist_track_matrix[t][index_of_interest])
                column_being_compared.append(playlist_track_matrix[t][playlist_ids.index(playlist_id)])
                # print("interest", column_of_interest)
                # print("compared", column_being_compared)
            jaccard_similarities.append((playlist_id, calculate(column_of_interest, column_being_compared)))
    return jaccard_similarities