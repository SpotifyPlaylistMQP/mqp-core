from math import *

# Takes in a playlist id and counts how many songs are similar between every
# combination of 2 playlists
# Output: playlist_similarity = {(playlist_id_1, playlist_id_2): [(similar_songs_from_playlist_1, similar_songs_from_playlist_2)]}
def count_similar(input_playlist_id, playlist_dict, split_dictionary):
    playlist_similarity = {}
    for second_key in playlist_dict.keys():
        similar_tracks = []
        if input_playlist_id != second_key:
            for key_0_track in split_dictionary[(input_playlist_id, '80')]:
                for key_1_track in playlist_dict[second_key]['tracks']:
                    if key_0_track['track_id'] == key_1_track['track_id']:
                        similar_tracks.append((key_0_track, key_1_track))
            playlist_similarity[(input_playlist_id, second_key)] = similar_tracks
            print(playlist_dict[second_key]['name'] + " similar tracks: " + str(len(similar_tracks)))

    return playlist_similarity

# square root helper function to find denominator of cosine_similarity function
def square_rooted(x):
    return round(sqrt(sum([a*a for a in x])),3)

# Calculates the similarity_metric using the cosine similarity math shit for each similar playlist
def calculate_similarity_metrics(playlist_dict, playlist_similarity):
    similarity_metrics = []
    for key in playlist_similarity.keys():
        popularity_values_key_0 = []
        popularity_values_key_1 = []
        for key_0_track in playlist_dict[key[0]]['tracks']:
            popularity_values_key_0.append(key_0_track['value'])
        for key_1_track in playlist_dict[key[1]]['tracks']:
            popularity_values_key_1.append(key_1_track['value'])

        numerator = sum(a * b for a, b in zip(popularity_values_key_0, popularity_values_key_1))
        denominator = square_rooted(popularity_values_key_0) * square_rooted(popularity_values_key_1)
        similarity_metrics.append((key[1], round(numerator / float(denominator), 3)))

    return similarity_metrics
