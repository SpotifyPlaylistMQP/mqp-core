from recommender_system import playlist, matrix, evaluation, cosine_similarity
from mongodb import mongodb_communicate
from graphing import graph
import sys

if sys.argv[1] is None:
    print("Incorrect arguments!")
    print("Execute the program like so:")
    print("  py user_based_collaborative_filtering.py {mongodb_collection}")
    print("Where:")
    print("  -mongodb_collection is the mongodb collection you wish to read from")
    print("    Mongo collections are formatted as so:")
    print("      mpd_{track_relevancy_threshold}_{playlist_relevancy_threshold}")
    exit()

mongo_collection = sys.argv[1]
K = 3 # Number of top similar playlists to the input playlist
N = 10 # Number of recommended songs

playlist_dict, unique_track_dict, playlist_ids = mongodb_communicate.get(mongo_collection)
playlist.pretty_print(playlist_dict, unique_track_dict)

playlist_track_matrix = matrix.create(playlist_dict, unique_track_dict)
print("Sparsity:", matrix.sparsity(playlist_track_matrix))

top_k_cosine_data = []

r_precision_results = [] # List of tuples: (input_playlist_id, r_precision)
for input_playlist_index, input_playlist_id in enumerate(playlist_dict.keys()):
    print("---------------------------------------------------------------")
    print("Input playlist:", playlist_dict[input_playlist_id]['name'], ": ", input_playlist_id)

    T, new_playlist_tracks = playlist.split(input_playlist_id, playlist_dict) # List of tracks removed from the 20%
    playlist_track_matrix = matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks, playlist_track_matrix, unique_track_dict)
    print("Number of tracks in 20%:", len(T))
    cosine_similarities = cosine_similarity.create(playlist_ids, input_playlist_id, playlist_track_matrix)

    top_k_most_similar_playlists, ranked_cosine_sims = cosine_similarity.find_top_k(cosine_similarities, K)
    top_k_cosine_data.append(ranked_cosine_sims)

    unique_track_scores_in_top_k = cosine_similarity.top_k_track_scores(top_k_most_similar_playlists, playlist_dict)
    recommended_tracks = cosine_similarity.recommend_n_tracks(unique_track_scores_in_top_k, N, new_playlist_tracks)

    matching_tracks, r_precision = evaluation.r_precision(recommended_tracks, T, N, unique_track_dict)
    r_precision_results.append((input_playlist_id, r_precision))
    print("Number of matching tracks: ", matching_tracks)

    playlist_track_matrix = matrix.update_input_playlist_tracks(input_playlist_index, playlist_dict[input_playlist_id]["tracks"], playlist_track_matrix, unique_track_dict)

print("---------------------------------------------------------------")

r_precision_sums = 0.0
for result in r_precision_results:
    r_precision_sums += result[1]
    print(playlist_dict[result[0]]['name'], result[1])
print("Average precision:", r_precision_sums / len(r_precision_results))

avg_cosine_data = {
    "x": [],
    "y": []
}
for i in range(len(top_k_cosine_data[0])):
    sum_of_row = 0
    for cosine_ranks in top_k_cosine_data:
        sum_of_row += cosine_ranks[i]
    avg_cosine_data["y"].append(sum_of_row / len(top_k_cosine_data))
    avg_cosine_data["x"].append(i + 1)

#print(avg_cosine_data)
graph.avg_cosine(avg_cosine_data)
