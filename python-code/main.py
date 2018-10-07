from recommender_system import playlist, matrix, evaluation, cosine_similarity, jaccard_similarity
from mongodb import mongodb_communicate
from graphing import graph
import user_based_collaborative_filtering
import sys

mongo_collection = sys.argv[1]
K = 3 # Number of top similar playlists to the input playlist
N = 10 # Number of recommended songs

playlist_dict, unique_track_dict, playlist_ids = mongodb_communicate.get(mongo_collection)
playlist.pretty_print(playlist_dict, unique_track_dict)

playlist_track_matrix = matrix.create(playlist_dict, unique_track_dict)
print("Sparsity:", matrix.sparsity(playlist_track_matrix))

cosine_sim_data = []
jaccard_sim_data = []

cosine_sim_r_precision_results = [] # List of tuples: (input_playlist_id, r_precision)
jaccard_sim_r_precision_results = [] # List of tuples: (input_playlist_id, r_precision)
for input_playlist_index, input_playlist_id in enumerate(playlist_dict.keys()):
    T, new_playlist_tracks = playlist.split(input_playlist_id, playlist_dict) # List of tracks removed from the 20%
    playlist_track_matrix = matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks, playlist_track_matrix, unique_track_dict)

    cosine_sim_recommendations, cosine_sim_results = user_based_collaborative_filtering.cosine_sim(playlist_dict, playlist_ids, input_playlist_id, playlist_track_matrix, new_playlist_tracks, K, N)
    cosine_sim_data.append(cosine_sim_results)
    cosine_sim_r_precision = evaluation.r_precision(cosine_sim_recommendations, T, N, unique_track_dict)
    cosine_sim_r_precision_results.append(cosine_sim_r_precision)

    jaccard_recommendations, jaccard_results = user_based_collaborative_filtering.jaccard(playlist_ids, playlist_dict, new_playlist_tracks, input_playlist_id, playlist_track_matrix, K, N)
    jaccard_sim_data.append(jaccard_results)
    jaccard_sim_r_precision = evaluation.r_precision(jaccard_recommendations, T, N, unique_track_dict)
    jaccard_sim_r_precision_results.append(jaccard_sim_r_precision)

    playlist_track_matrix = matrix.update_input_playlist_tracks(input_playlist_index, playlist_dict[input_playlist_id]["tracks"], playlist_track_matrix, unique_track_dict)

cosine_sim_avg_precision = evaluation.avg_precision(cosine_sim_r_precision_results)
print("Cosine Similarity Average Precision:", cosine_sim_avg_precision)
cosine_sim_avg_data = evaluation.avg_data(cosine_sim_data)

jaccard_sim_avg_precision = evaluation.avg_precision(jaccard_sim_r_precision_results)
print("Jaccard Similarity Average Precision:", jaccard_sim_avg_precision)
jaccard_sim_avg_data = evaluation.avg_data(jaccard_sim_data)


avg_data = {}
avg_data["cosine_sim"] = cosine_sim_avg_data
avg_data["jaccard_sim"] = jaccard_sim_avg_data
<<<<<<< HEAD
# print(avg_data)
graph.create_graph(avg_data, mongo_collection)
=======
>>>>>>> 0808547361aa3061c3dd2cb1ae3787cf06990e01

#print(avg_cosine_data)
# graph.avg_cosine(avg_cosine_data)
