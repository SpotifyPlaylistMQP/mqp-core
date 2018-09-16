from Functions import authorization, spotify_api, matrix_visualizer
import random

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

    shuffled_array = random.shuffle(all_tracks) ##Randomly shuffle the array
    for song in (0, (len(shuffled_array)/5)): #Takes the first 20 (0 to 1/5 of the array)
        list_20split.append(song)
        shuffled_array.pop(song) #Removes the song from the shuffled_array after adding it to the 20% split array

    for remaining_song in shuffled_array: #Adds the remaining songs to the comparison array
        list_80split.append(remaining_song)

    split_dictionary['input_playlist_id']['80'] = list_80split
    split_dictionary['input_playlist_id']['20'] = list_20split
    #   print("Input Playlist ID: " + input_playlist_id)
    #   print("The 20'%' of songs removed: '" + split_dictionary['input_playlist_id']['20'])
    #   print("The 80'%' of songs kept: '" + split_dictionary['input_playlist_id']['20'])

    return list_80split, list_20split


# Takes in a playlist id and counts how many songs are similar between every
# combination of 2 playlists
# Output: playlist_similarity = {(playlist_id_1, playlist_id_2), list_of_similar_songs}
playlist_similarity = {}
def count_similar(input_playlist_id):
    # Find which playlists are similar

    similar_tracks = []

    for second_key in playlists.keys():
        similar_tracks.clear()
        if input_playlist_id != second_key:
            for track in playlists[input_playlist_id]['tracks']:
                if track in playlists[second_key]['tracks']:
                    similar_tracks.append(track)
                    playlist_similarity[(input_playlist_id, second_key)] = similar_tracks

    print(playlist_similarity)
    
    return playlist_similarity



###### START JACKSON CODE #######

# square root helper function to find denominator of cosine_similarity function
def square_rooted(x):
    return round(sqrt(sum([a*a for a in x])),3)

# Takes in a dictionary object containing the input playlist and all other playlists along with
# a list of similar songs between the input playlist & all other playlists
# Output: similarity_metric = number representing the similarity between input playlist and other playlists
def cosine_similarity(playlist_dictionary):
    similarity_metric_array = []

    for 
    for i in len():
        numerator = sum(a*b for a,b in zip(x,y))
        denominator = square_rooted(x)*square_rooted(y)

        similarity_metric = round(numerator/float(denominator),3)

        similarity_metric_array.append(similarity_metric)

    best_similarity = max([similarity_metric_array])
    #find which playlist has the best similarity = most_similar_playlistID

    return most_similar_playlistID, best_similarity


# Takes in playlistID of most similar aplylist to the input, along with the 80 and 20% splits of the original playlist
# returns (and prints) list of recommended songs that total 20% of original playlist
def recommended_songs(most_similar_playlistID, 80_split, 20_split):
    # Take 20% of songs from most similar playlist & print out their values



# Takes in 20% split from original playlist and compares it to the 20% equivalent of recommended songs
# returns the R-precision metric between the omitted songs and the recommended songs
def r_precision(20_split, recommended_songs):
    # compare the 20% of most similar suggestions to actual 20% ommitted from selected playlist
    # using r-precision

    size_of_20_split = len(20_split)
    set_matches = set(20_split).intersection(recommended_songs)

    for i in matches:
        int_matches = i
    
    eval_metric = int_matches / size_of_20_split

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

    80_split, 20_split = split_playlist(playlistID)
    
    playlist_similarity_dict = count_similar(playlistID)

    most_similar_playlistID, highest_cosine_metric = cosine_similarity(playlist_similarity_dict)

    list_of_recommended_songs = recommended_songs(most_similar_playlistID, 80_split, 20_split)

    eval_metric = r_precision(20_split, list_of_recommended_songs)

    print ("The 20 percent of songs omitted from recommendation processing from the input playlist are: " 20_split)
    print ("The recommended songs totalling 20 percent of the input playlist are: " list_of_recommended_songs)
    print ("The cosine similarity metric determined between the input playlist and the most similar playlist used for recommendation was: " highest_cosine_metric)
    print ("The R-precision evaluation metric for the recommended songs was: " eval_metric)
