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


# Find which playlists are similar
playlist_similarity = {}
for key in playlists.keys():
    similar = 0
    for second_key in playlists.keys():
        if key !=second_key:
            for track in playlists[key]['tracks']:
                if track in playlists[second_key]['tracks']:
                    similar+=1
                    playlist_similarity[(key, second_key)] = similar

print(playlist_similarity)

# split_playlist(array)
#   Takes the entered playlist by the user and removes a randomly selected 20%
#   for comparison. Stores the 20% and 80% split in two arrays locally accessible.
# input_playlist = the playlist for comparison
# array -> array, array
playlist_80split = []
playlist_20split = []
def split_playlist(input_playlist):
    print("split_playlist called")
    shuffled_array = random.shuffle(input_playlist) ##Randomly shuffle the array
    for song in (0, (len(shuffled_array)/5)): #Takes the first 20 (0 to 1/5 of the array)
        playlist_20split.append(song)
        shuffled_array.pop(song) #Removes the song from the shuffled_array after adding it to the 20% split array
    for remaining_song in shuffled_array: #Adds the remaining songs to the comparison array
        playlist_80split.append(remaining_song)
