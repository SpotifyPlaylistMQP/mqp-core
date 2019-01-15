import random

# Helps sort tuples by their second value
def sort_by_second_tuple(input):
    return input[1]

# Helps recommend N tracks based on the ordered list of similar track tuples, and what is already in the input playlist's tracks
def recommend_n_tracks(N, similar_track_tuples, current_playlist_tracks):
    index = 0
    recommended_tracks = []
    while len(recommended_tracks) < N:
        if index >= len(similar_track_tuples):
            #print("Not enough tracks to recommend!")
            return recommended_tracks
        if similar_track_tuples[index][0] not in current_playlist_tracks:
            recommended_tracks.append(similar_track_tuples[index])
        index += 1
    return recommended_tracks

# Helps get two playlist's columns from the matrix
def get_two_playlist_column(playlist_index_one, playlist_index_two, playlist_track_matrix):
    playlist_column_one = []
    playlist_column_two = []
    for track_row in playlist_track_matrix:
        playlist_column_one.append(track_row[playlist_index_one])
        playlist_column_two.append(track_row[playlist_index_two])
    return playlist_column_one, playlist_column_two

