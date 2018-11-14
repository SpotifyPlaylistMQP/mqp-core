from recommender_systems.modules import evaluation, matrix, helpers
from scipy.spatial import distance
import numpy as np
import time

def track_similarities(track_matrix):
    start = time.time()
    print("Track similarities...")
    cosine_sims = []
    jaccard_sims = []
    for track1 in track_matrix:
        cosine_row = []
        jaccard_row = []
        for track2 in track_matrix:
            if np.array_equal(track1, track2):
                cosine_row.append(1)
                jaccard_row.append(1)
            else:
                cosine_row.append(distance.cosine(track1, track2))
                jaccard_row.append(distance.jaccard(track1, track2))
        cosine_sims.append(cosine_row)
        jaccard_sims.append(jaccard_row)
    print("-Seconds elapsed:", time.time() - start)
    return np.asarray(cosine_sims), np.asarray(jaccard_sims)

def run(playlist_dict, unique_track_dict, N, cosine_similarity_dict, jaccard_similarity_dict):
    max_K = 300
    print("Item-based collaborative filtering...")

    # For each input playlist, recommend N tracks to it, and evaluate the recommendation
    cosine_sim_k_evaluation_results = {}  # Key = k, Value = list of r_precision_results
    jaccard_sim_k_evaluation_results = {}  # Key = k, Value = list of r_precision_results
    for input_pid in playlist_dict.keys():
        for K in range(1, max_K + 1):
            if K % 10 == 0:
                # Calculate the sum similarity score for each potential tid to recommend
                T, new_playlist_tracks = matrix.split_playlist(input_pid, playlist_dict)
                cosine_similar_track_dict = {}  # Key = similar_tid, Value = Sum total of cosine_similarities for this playlist
                jaccard_similar_track_dict = {} # Key = similar_tid, Value = Sum total of jaccard_similarities for this playlist
                for input_tid in new_playlist_tracks:
                    for cosine_sim_tuple in cosine_similarity_dict[input_tid][:K]:
                        if cosine_sim_tuple[0] not in cosine_similar_track_dict.keys():
                            cosine_similar_track_dict[cosine_sim_tuple[0]] = 0
                        cosine_similar_track_dict[cosine_sim_tuple[0]] += cosine_sim_tuple[1]
                    for jaccard_sim_tuple in jaccard_similarity_dict[input_tid][:K]:
                        if jaccard_sim_tuple[0] not in jaccard_similar_track_dict.keys():
                            jaccard_similar_track_dict[jaccard_sim_tuple[0]] = 0
                        jaccard_similar_track_dict[jaccard_sim_tuple[0]] += jaccard_sim_tuple[1]

                # Transform those sum similarity scores into an ordered list of tuples
                cosine_similar_track_tuples = []  # List of tuples: (similar_tid, Sum total of cosine_similarities for this playlist)
                jaccard_similar_track_tuples = [] # List of tuples: (similar_tid, Sum total of jaccard_similarities for this playlist)
                for similar_tid in cosine_similar_track_dict.keys():
                    cosine_similar_track_tuples.append((similar_tid, cosine_similar_track_dict[similar_tid]))
                for similar_tid in jaccard_similar_track_dict.keys():
                    jaccard_similar_track_tuples.append((similar_tid, jaccard_similar_track_dict[similar_tid]))
                cosine_similar_track_tuples.sort(reverse=True, key=helpers.sort_by_second_tuple)
                jaccard_similar_track_tuples.sort(reverse=True, key=helpers.sort_by_second_tuple)

                # Recommend N tracks to the input playlist and evaluate
                cosine_sim_recommended_tracks = helpers.recommend_n_tracks(N, cosine_similar_track_tuples, new_playlist_tracks)
                jaccard_sim_recommended_tracks = helpers.recommend_n_tracks(N, jaccard_similar_track_tuples, new_playlist_tracks)

                if K not in cosine_sim_k_evaluation_results.keys(): cosine_sim_k_evaluation_results[K] = []
                if K not in jaccard_sim_k_evaluation_results.keys(): jaccard_sim_k_evaluation_results[K] = []
                cosine_sim_k_evaluation_results[K].append(evaluation.dcg_precision(cosine_sim_recommended_tracks, T, N, unique_track_dict))
                jaccard_sim_k_evaluation_results[K].append(evaluation.dcg_precision(jaccard_sim_recommended_tracks, T, N, unique_track_dict))

    cosine_results_by_K = {}
    jaccard_results_by_K = {}
    for K in range(1, max_K + 1):
        if K % 10 == 0:
            cosine_results_by_K[K] = evaluation.avg_precision(cosine_sim_k_evaluation_results[K])
            jaccard_results_by_K[K] = evaluation.avg_precision(jaccard_sim_k_evaluation_results[K])
            print("\tK = " + str(K) + ": cosine = " + str(cosine_results_by_K[K]) + ", jaccard = " + str(jaccard_results_by_K[K]))

    return cosine_results_by_K, jaccard_results_by_K

