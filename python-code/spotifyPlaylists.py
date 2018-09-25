from functions import matrix, playlist, cosine_similarity, evaluation
from spotify_api import spotify_api
import pretty_prints

# Playlist IDs to be examined
playlist_ids = [
    '37i9dQZF1DX0XUsuxWHRQd', '37i9dQZF1DWY4xHQp97fN6',
    '37i9dQZF1DX2RxBh64BHjQ', '3dBCdkBZsr8fJZ2WduKwDN',
    '37i9dQZF1DX0Tkc6ltcBfU', '37i9dQZF1DX1YPTAhwehsC',
    '7kdOsNnHtzwncTBnI3J17w', '5HYnMEFnXw6j9Xj8DIth0f',
    '5dmLJqg5TVfbvQFiTpyxxN', '37i9dQZF1DXaxIqwkEGFEh',
    '37i9dQZF1DWYfVy6zzMSPv', '3ZSq7rHkmA5m0suVh5z8lM',
    '37i9dQZF1DXcA6dRp8rwj6', '2HmppYpekiuOMZaS4xxubl',
    '37i9dQZF1DX7YCknf2jT6s'
]

# Playlist to be split and given recommendations
playlist_id_of_interest = '37i9dQZF1DX0XUsuxWHRQd'

# Get the auth_token from the node server and test it
spotify_api.authorize()

# Get the playlist_dict and unique_track_dict from the spotify API
playlist_dict, unique_track_dict = spotify_api.make_playlist_and_track_dict(playlist_ids)
pretty_prints.print_dataset_statistics(playlist_dict, unique_track_dict)

# Remove 20% of playlist_being_recommended_to's tracks and save the original 20% that were removed
original_20_percent = playlist.split(playlist_id_of_interest, playlist_dict)

# Create the matrix (visualized in matrix.txt)
playlist_track_matrix = matrix.create(playlist_dict, unique_track_dict)

# Calculate the sparsity of the matrix
sparsity = matrix.sparsity(playlist_track_matrix)

# Calculate the cosine sim of each playlist that's not playlist_id_of_interest
cosine_sim_dict = cosine_similarity.create(playlist_ids, playlist_id_of_interest, playlist_track_matrix)
cosine_similarity.pretty_print(cosine_sim_dict, playlist_dict)

# Find the playlist that is most similar to playlist_id_of_interest
most_similar_playlist_id = cosine_similarity.most_similar(cosine_sim_dict)

# Recommend tracks to playlist_id_of_interest based on the most_similar_playlist_id
recommended_tracks = playlist.recommend_tracks(playlist_dict, playlist_id_of_interest, most_similar_playlist_id, len(original_20_percent))

# Evaluate the recommended_tracks vs the original_20_percent
matching_tracks, r_precision = evaluation.r_precision(recommended_tracks, original_20_percent)
evaluation.pretty_print(matching_tracks, unique_track_dict, r_precision)