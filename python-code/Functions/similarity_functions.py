from math import *

# Takes in a playlist id and counts how many songs are similar between every
# combination of 2 playlists
#    playlist_similarity: key = (playlist_to_split, playlist_id_x), value = list of similar songs, for each playlist
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
            if len(similar_tracks) > 0:
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
        for similar_track in playlist_similarity[key]:
            popularity_values_key_0.append(similar_track[0]['value'])
            popularity_values_key_1.append(similar_track[1]['value'])
        print('------------------------------------------------------------------------------')
        print(playlist_dict[key[0]]['name'] + " VS " + playlist_dict[key[1]]['name'])
        print(popularity_values_key_0)
        print(popularity_values_key_1)
        numerator = sum(a * b for a, b in zip(popularity_values_key_0, popularity_values_key_1))
        print("Numerator: " + str(numerator))
        denominator = square_rooted(popularity_values_key_0) * square_rooted(popularity_values_key_1)
        print("Denominator: " + str(denominator))
        cosine_sim = round(numerator / float(denominator), 3)
        print("Cosine Similarity: " + str(cosine_sim))
        similarity_metrics.append((key[1], cosine_sim))

    return similarity_metrics
