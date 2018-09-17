from Functions import authorization, spotify_api, matrix_visualizer
#import numpy as np

playlist_ids = [
    '37i9dQZF1DX0XUsuxWHRQd', '37i9dQZF1DWY4xHQp97fN6',
    '37i9dQZF1DX2RxBh64BHjQ', '3dBCdkBZsr8fJZ2WduKwDN',
    '37i9dQZF1DX0Tkc6ltcBfU', '37i9dQZF1DX1YPTAhwehsC',
    '7kdOsNnHtzwncTBnI3J17w', '5HYnMEFnXw6j9Xj8DIth0f',
    '5dmLJqg5TVfbvQFiTpyxxN', '37i9dQZF1DXaxIqwkEGFEh',
    '37i9dQZF1DWYfVy6zzMSPv', '3ZSq7rHkmA5m0suVh5z8lM',
    '37i9dQZF1DXcA6dRp8rwj6', '2HmppYpekiuOMZaS4xxubl'
]

# Get the auth_token from the node server and test it
authorization.get_auth_token_from_node_server()
#TODO: Test / refresh the auth token on the node server

# Get each playlist_id's playlist, and a set of distinct songs in each playlist
playlists = {}
tracks = []
total_track_num = 0
for playlist_id in playlist_ids:
    spotify_playlist = spotify_api.get_playlist(playlist_id)
    playlists[playlist_id] = spotify_playlist
    for track in spotify_playlist['tracks']:
        total_track_num += 1
        if track not in tracks:
            tracks.append(track)

print("Total Playlists: " + str(len(playlists)))
print("Total Tracks: " + str(total_track_num))
print("Distinct Tracks: " + str(len(tracks)))

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


# Function to get a list of unique song names in a playlist
# string -> list
def get_unique_songs(input_playlist):
    tracks = []
    spotify_playlist = spotify_api.get_playlist(input_playlist)
    for track in spotify_playlist['tracks']:
        if track not in tracks:
            tracks.append(track)
    return tracks


# split_playlist(array)
#   Takes the entered playlist by the user and removes a randomly selected 20%
#   for comparison. Stores the 20% and 80% split in two arrays locally accessible.
# input_playlist = the playlist for comparison
#   the format of {key: playlist_id, value: [track_list]}
#   each elements is {playlist_id: tracklist[]}
# array -> array, array
split_dictionary = {}
def split_playlist(input_playlist_id):
    # print("split_playlist called")
    all_tracks = get_unique_songs(input_playlist_id) #local lists for playlist tracks
    list_80split = [] #80% of the songs
    list_20split = [] #20% of the songs (for removal, non-inclusive)
    spotify_playlist = spotify_api.get_playlist(input_playlist_id) #Get the given playlist


    #shuffled_array = np.random.shuffle(all_tracks) ##Randomly shuffle the array
    all_tracks_length = len(all_tracks)/5
    count = 0
    for song in all_tracks: #Takes the first 20 (0 to 1/5 of the array)
            count+=1
            if (count <= all_tracks_length):
                list_20split.append(song)
                all_tracks.pop(count) #Removes the song from the shuffled_array after adding it to the 20% split array

    for remaining_song in all_tracks: #Adds the remaining songs to the comparison array
        list_80split.append(remaining_song)


    split_dictionary[(input_playlist_id, '80')]= list_80split
    split_dictionary[(input_playlist_id, '20')] = list_20split
    print(split_dictionary)
    #   print("Input Playlist ID: " + input_playlist_id)
    #   print("The 20'%' of songs removed: '" + split_dictionary[(input_playlist_id, '20')])
    #   print("The 80'%' of songs kept: '" + split_dictionary[(input_playlist_id, '80')])

    return list_80split, list_20split


# Takes in a playlist id and counts how many songs are similar between every
# combination of 2 playlists
# Output: playlist_similarity = {(playlist_id_1, playlist_id_2), list_of_similar_songs}
playlist_similarity = {}
def count_similar(input_playlist_id):
    # Find which playlists are similar
    split_playlist(input_playlist_id)
    similar_tracks = []

    for second_key in playlists.keys():
        similar_tracks.clear()
        if input_playlist_id != second_key:
            for track in split_dictionary[(input_playlist_id, '80')]:
                if track in playlists[second_key]['tracks']:
                    similar_tracks.append(track)
                    playlist_similarity[(input_playlist_id, second_key)] = similar_tracks

    print("My function")
    print(playlist_similarity)
    return playlist_similarity
count_similar('37i9dQZF1DX0XUsuxWHRQd')


# square root helper function to find denominator of cosine_similarity function
def square_rooted(x):
    return round(sqrt(sum([a*a for a in x])),3)


# Takes in a dictionary object containing the input playlist and all other playlists along with
# a list of similar songs between the input playlist & all other playlists
# Output:most_similar_playlistID  similarity_metric = playlistID for most similar playlist, number representing the similarity between input playlist and other playlists
def cosine_similarity(playlist_dictionary):
    similarity_metric_array = []

    
    # y = number of playlist song columns being compared

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
"""
def recommended_songs(most_similar_playlistID, 80_split, 20_split):
    similar_playlist = spotify_api.get_playlist(most_similar_playlistID)
    count = 0
    recommend_songs_list = []
    tracks = []

    for track in similar_playlist['tracks']:
            tracks.append(track)


    set_80 = set(80_split)
    set_20 = set(80_split)
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
def r_precision(20_split, recommended_songs):

    size_of_20_split = len(20_split)
    matches = set(20_split).intersection(recommended_songs)

    eval_metric = len(matches) / size_of_20_split

    return (eval_metric)


# Master function that handles all other function calls
# Takes in a playlist ID and returns:
#   - 20% of the input playlist that was omitted during recommendation processing
#   - Songs from the most similar playlist the system recommended equaling 20% 
#     of the input playlist
#   - The cosine-similarity metric determined between the input playlist and most similar
#     playlist used for recommendation
#   - The R-precision evaluation metric calculated by finding the similarity between
#     the omitted 20% of songs from the input playlist and the recommended songs

def masterFunction(playlistID):

    # Obtain 80 and 20 split of songs from input playlist
    80_split, 20_split = split_playlist(playlistID)
    
    # Get a dictionary of playlistID's and their similar tracks with the input playlist
    playlist_similarity_dict = count_similar(playlistID)

    # Find most similar playlist in cluster to input playlist and obtain cosine metric for the pair
    most_similar_playlistID, highest_cosine_metric = cosine_similarity(playlist_similarity_dict)

    # Recommend songs totalling 20% of input playlist from most similar playlist
    list_of_recommended_songs = recommended_songs(most_similar_playlistID, 80_split, 20_split)

    # Evaluate the precision of the recommend songs versus the omitted 20% of songs at the beginning of the test
    eval_metric = r_precision(20_split, list_of_recommended_songs)

    print ("The 20 percent of songs omitted from recommendation processing from the input playlist are: " 20_split)
    print ("The recommended songs totalling 20 percent of the input playlist are: " list_of_recommended_songs)
    print ("The cosine similarity metric determined between the input playlist and the most similar playlist used for recommendation was: " highest_cosine_metric)
    print ("The R-precision evaluation metric for the recommended songs was: " eval_metric)
"""