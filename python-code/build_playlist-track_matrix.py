from Functions import authorization, spotify_api, matrix_visualizer

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
playlists = []
tracks = []
total_tracks = 0
for playlist_id in playlist_ids:
    spotify_playlist = spotify_api.get_playlist(playlist_id)
    playlists.append(spotify_playlist)
    for track in spotify_playlist['tracks']:
        total_tracks += 1
        if track not in tracks:
            tracks.append(track)

print("Total Playlists: " + str(len(playlists)))
print("Total Tracks: " + str(total_tracks))
print("Distinct Tracks: " + str(len(tracks)))

# Populate the matrix
matrix = []
for playlist in playlists:
    matrix_row = []
    for track in tracks:
        if track in playlist['tracks']:
            matrix_row.append(track['popularity'])
        else:
            matrix_row.append("--")
    matrix.append(matrix_row)

matrix_visualizer.visualize_matrix(matrix, playlists, tracks)

