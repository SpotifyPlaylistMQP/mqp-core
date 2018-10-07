from math import *
#%matplotlib inline
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np

# Returns cosine_sim_dict, the cosine_sim of each playlist_id compared to the playlist_id_of_interest
def create(playlist_ids, playlist_id_of_interest, playlist_track_matrix):
    def calculate(col1, col2):
        numerator = sum(a * b for a, b in zip(col1, col2))
        denominator = sqrt(sum(a * a for a in col1)) * sqrt(sum(b * b for b in col2))
        return round(numerator / denominator, 5)

    cosine_similarities = [] # List of tuples (playlist_id, cosine_sim)
    index_of_interest = playlist_ids.index(playlist_id_of_interest)
    for playlist_id in playlist_ids:
        if playlist_id != playlist_id_of_interest:
            column_of_interest = []
            column_being_compared = []
            for t in range(len(playlist_track_matrix)):
                column_of_interest.append(playlist_track_matrix[t][index_of_interest])
                column_being_compared.append(playlist_track_matrix[t][playlist_ids.index(playlist_id)])
            cosine_similarities.append((playlist_id, calculate(column_of_interest, column_being_compared)))
    return cosine_similarities

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




