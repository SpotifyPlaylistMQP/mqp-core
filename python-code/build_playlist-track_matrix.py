from Functions import similarity_functions, authorization, spotify_api, matrix_visualizer
from math import *

# Playlist IDs to be examined
playlist_ids = [
    '37i9dQZF1DX0XUsuxWHRQd', '37i9dQZF1DWY4xHQp97fN6',
    '37i9dQZF1DX2RxBh64BHjQ', '3dBCdkBZsr8fJZ2WduKwDN',
    '37i9dQZF1DX0Tkc6ltcBfU', '37i9dQZF1DX1YPTAhwehsC',
    '7kdOsNnHtzwncTBnI3J17w', '5HYnMEFnXw6j9Xj8DIth0f',
    '5dmLJqg5TVfbvQFiTpyxxN', '37i9dQZF1DXaxIqwkEGFEh',
    '37i9dQZF1DWYfVy6zzMSPv', '3ZSq7rHkmA5m0suVh5z8lM',
    '37i9dQZF1DXcA6dRp8rwj6', '2HmppYpekiuOMZaS4xxubl'
]

# Playlist to be split and given recommendations
playlist_to_split = '37i9dQZF1DX0XUsuxWHRQd'

# Get the auth_token from the node server and test it
authorization.get_auth_token_from_node_server()
#TODO: Test / refresh the auth token on the node server

# Make the playlist dictionary from the playlist_ids, and find the unique tracks
#   playlist_dict: key = playlist_id, value = playlist
playlist_dict, unique_tacks = spotify_api.make_playlist_dictionary(playlist_ids)


# square root helper function to find denominator of cosine_similarity function
def square_rooted(x):
    return round(sqrt(sum([a*a for a in x])),3)

similarity_metric_array = []
print(playlist_similarity)
for key in playlist_similarity.keys():
    popularity_values_playlist_0 = []
    popularity_values_playlist_1 = []
    print(playlist_similarity[key])
    for track in playlist_similarity[key]:
        for full_track in playlists[key[0]]['tracks']:
            if track['track_id'] == full_track['track_id']:
                popularity_values_playlist_0.append(full_track['position'] * full_track['popularity'])
        for full_track in playlists[key[1]]['tracks']:
            if track['track_id'] == full_track['track_id']:
                popularity_values_playlist_1.append(full_track['position'] * full_track['popularity'])

    print(popularity_values_playlist_0)
    print(popularity_values_playlist_1)

    numerator = sum(a * b for a, b in zip(popularity_values_playlist_0, popularity_values_playlist_1))
    denominator = square_rooted(popularity_values_playlist_0) * square_rooted(popularity_values_playlist_1)

    similarity_metric = round(numerator / float(denominator), 3)

    similarity_metric_array.append((key[1], similarity_metric))

print(similarity_metric_array)



# Populate the matrix
matrix = []
for key in playlists.keys():
    matrix_row = []
    for track in tracks:
        if track in playlists[key]['tracks']:
            matrix_row.append(track['popularity'])
        else:
            matrix_row.append("--")
    matrix.append(matrix_row)

matrix_visualizer.visualize_matrix(matrix, playlists, tracks)

#Call stove and sams for testing
similarity_functions.count_similar('37i9dQZF1DX0XUsuxWHRQd', playlists)

'''
# Takes in a dictionary object containing the input playlist and all other playlists along with
# a list of similar songs between the input playlist & all other playlists
# Output:most_similar_playlistID  similarity_metric = playlistID for most similar playlist, number representing the similarity between input playlist and other playlists
def cosine_similarity(playlist_dictionary):
    similarity_metric_array = []

    for i in len(y):
        #popularity_values = list of popularity values for a given 'column' of similar songs shared with the input playlist
        popularity_values = [] #fill this list with popularity values of all similar tracks for each different playlist in dictionary

        numerator = sum(a*b for a,b in zip(popularity_values,popularity_values))
        denominator = square_rooted(popularity_values)*square_rooted(popularity_values)

        similarity_metric = round(numerator/float(denominator),3)

        similarity_metric_array.append(similarity_metric)

    best_similarity = max([similarity_metric_array])
    #find which playlist has the best similarity = most_similar_playlistID

    return most_similar_playlistID, best_similarity


# Takes in playlistID of most similar playlist to the input, along with the 80% and 20% splits of the original playlist
# returns list of recommended songs that total 20% of original playlist
def recommended_songs(most_similar_playlistID, split80, split20):
    similar_playlist = spotify_api.get_playlist(most_similar_playlistID)
    count = 0
    recommend_songs_list = []
    tracks = []

    for track in similar_playlist['tracks']:
            tracks.append(track)


    set_80 = set(split80)
    set_20 = set(split20)
    set_spotify_playlist = set(tracks)

    length_of_20 = len(set_20)

    #symmetric difference
    symmetric_difference = (set_spotify_playlist ^ set_80)
    # set difference
    possible_songs_to_recommend = (symmetric_difference - set_80)

    for i in symmetric_difference:
        if (count < length_of_20):
            recommend_songs_list.append(i)
            count = count + 1
        else:
            break
    

    return recommend_songs_list


# Takes in 20% split from original playlist and compares it to the 20% equivalent of recommended songs
# returns the R-precision metric between the omitted songs and the recommended songs
def r_precision(split20, recommended_songs):

    size_of_20_split = len(split20)
    matches = set(split20).intersection(recommended_songs)

    eval_metric = len(matches) / size_of_20_split

    return (eval_metric)


# Master function that handles all other function calls
# Takes in a playlist ID and returns:
#   - 20% of the input playlist that was omitted during recommendation processing
#   - Songs from the most similar playlist the system recommended equaling 20% 
#     of the input playlist
#   - The cosine-similarity metric determined between the input playlist and most similar
#     playlist used for recommendation
#   - The R-precision evluation metric calculated by finding the similarity between 
#     the omitted 20% of songs from the input playlist and the recommended songs

def masterFunction(playlistID):
 
    # Get a dictionary of playlistID's and their similar tracks with the input playlist
    playlist_similarity_dict = count_similar(playlistID)

    # Find most similar playlist in cluster to input playlist and obtain cosine metric for the pair
    most_similar_playlistID, highest_cosine_metric = cosine_similarity(playlist_similarity_dict)

    # Recommend songs totalling 20% of input playlist from most similar playlist
    list_of_recommended_songs = recommended_songs(most_similar_playlistID, split_dictionary['input_playlist_id']['80'], split_dictionary['input_playlist_id']['20'])

    # Evaluate the precision of the recommend songs versus the omitted 20% of songs at the beginning of the test
    eval_metric = r_precision(split_dictionary['input_playlist_id']['20'], list_of_recommended_songs)

    print ("The 20 percent of songs omitted from recommendation processing from the input playlist are: " split_dictionary['input_playlist_id']['20'])
    print ("The recommended songs totalling 20 percent of the input playlist are: " list_of_recommended_songs)
    print ("The cosine similarity metric determined between the input playlist and the most similar playlist used for recommendation was: " highest_cosine_metric)
    print ("The R-precision evaluation metric for the recommended songs was: " + eval_metric)
'''
