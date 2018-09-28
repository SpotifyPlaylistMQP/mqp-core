from .functions import matrix, playlist, cosine_similarity, evaluation
from .mongodb import mongoPlaylists
import pretty_prints
import sys


mongo_collection = sys.argv[1]


playlist_dict, unique_track_dict, playlist_ids = mongoPlaylists.make_playlist_and_track_dict(mongo_collection)
playlist_id_of_interest = mongoPlaylists.find_random_playlist_id_of_interest(playlist_dict)
pretty_prints.print_dataset_statistics(playlist_dict, unique_track_dict)
print("Playlist being recommended to:", playlist_dict[playlist_id_of_interest]['name'])

# Remove 20% of playlist_being_recommended_to's tracks and save the original 20% that were removed
original_20_percent = playlist.split(playlist_id_of_interest, playlist_dict)
print("Number of songs removed from playlist of interest:", len(original_20_percent))

# Create the matrix (visualized in matrix.txt)
playlist_track_matrix = matrix.create(playlist_dict, unique_track_dict)

# Calculate the sparsity of the matrix
sparsity = matrix.sparsity(playlist_track_matrix)
print("Sparsity:", sparsity)

# Calculate the cosine sim of each playlist that's not playlist_id_of_interest
cosine_sim_dict = cosine_similarity.create(playlist_ids, playlist_id_of_interest, playlist_track_matrix)

# Find the playlist that is most similar to playlist_id_of_interest
most_similar_playlist_id = cosine_similarity.most_similar(cosine_sim_dict)
print("Most similar playlist: ", playlist_dict[most_similar_playlist_id]['name'])

# Recommend tracks to playlist_id_of_interest based on the most_similar_playlist_id
recommended_tracks = playlist.recommend_tracks(playlist_dict, playlist_id_of_interest, most_similar_playlist_id, len(original_20_percent))

# Evaluate the recommended_tracks vs the original_20_percent
matching_tracks, r_precision = evaluation.r_precision(recommended_tracks, original_20_percent)
print("Number of matching tracks: ", len(matching_tracks), "/", len(original_20_percent))

evaluation.pretty_print(matching_tracks, unique_track_dict, r_precision)