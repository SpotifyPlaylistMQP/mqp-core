from Functions import sparsity_functions, authorization, spotify_api, matrix_functions, split_playlist, track_recommendation

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
playlist_to_split = '37i9dQZF1DX0XUsuxWHRQd'

# Get the auth_token from the node server and test it
authorization.initialize()

# Get the playlist_dict and unique_track_dict from the spotify API
playlist_dict, unique_track_dict = spotify_api.make_playlist_and_track_dict(playlist_ids)

# Create the matrix (visualized in matrix.txt)
matrix = matrix_functions.make_matrix(playlist_dict, unique_track_dict)

# Calculate the sparsity of the matrix
sparsity = sparsity_functions.calculate_sparsity(matrix)
print(sparsity)



'''
#TODO: sparsity : cells filled / unique_tracks * num_playlists

# Make the playlist dictionary from the playlist_ids, and find the unique tracks
#   playlist_dict: key = playlist_id, value = playlist
playlist_dict, unique_track_dict = 

# Visualize the matrix
matrix_visualizer.visualize_matrix(playlist_dict, unique_track_dict)

# Split the playlist_to_be_split into 80 20 and return the split dictionary
split_dict = split_playlist.split_playlist(playlist_to_split, playlist_dict)

# Find the similarity (same songs) between playlist_to_split and every other playlist
playlist_similarity = similarity_functions.count_similar(playlist_to_split, playlist_dict, split_dict)

# Create the similarity metrics for each similar playlist
#   similarity_metrics: key = playlist_id, value = similarity_metric
similarity_metrics = similarity_functions.calculate_similarity_metrics(playlist_dict, playlist_similarity)
print("Similarity Metrics for each playlist Vs. Rap Caviar: ")
for metric in similarity_metrics:
    print(playlist_dict[metric[0]]['name'] + ": " + str(metric[1]))

# Recommend tracks to be added to playlist_to_be_split based on the similarity_metrics
#recommended_tracks = track_recommendation.recommend_tracks(similarity_metrics, playlist_dict, split_dict, playlist_to_split)





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
