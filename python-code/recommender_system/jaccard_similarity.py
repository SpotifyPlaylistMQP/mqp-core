from math import *
import numpy as np


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

# Helper function for sorting a list of tuples
def sort_by_second_tuple(input):
    return input[1]

# Returns a list of playlist_ids of the top k most similar playlists
def find_top_k(jaccard_similarities, K):
    jaccard_similarities.sort(reverse=True, key=sort_by_second_tuple)

    top_k = []
    ranked_jaccard_sims = []
    for i in range(len(jaccard_similarities)):
        if i < K:
            top_k.append(jaccard_similarities[i][0])
        ranked_jaccard_sims.append(jaccard_similarities[i][1])

    return top_k, ranked_jaccard_sims



# Returns the a list of each unique track's score in the top_k playlists
def top_k_track_scores(top_k, playlist_dict):
    def get_unique_tracks(top_k_list):
        unique_track_list = []
        for top_k_playlist_id in top_k_list:
            for tid in playlist_dict[top_k_playlist_id]['tracks']:
                if tid not in unique_track_list:
                    unique_track_list.append(tid)
        return unique_track_list

    track_scores = []
    unique_tracks = get_unique_tracks(top_k)
    for tid in unique_tracks:
        score = 0
        for playlist_id in top_k:
            if tid in playlist_dict[playlist_id]['tracks']:
                score += 1
        track_scores.append((tid, score))

    #createPlot(track_scores)
    return track_scores

def createPlot(track_scores):
    plt.plot([1,2,3,4], [1,4,9,16], 'ro')
    plt.axis([0, 6, 0, 20])
    plt.show()


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
