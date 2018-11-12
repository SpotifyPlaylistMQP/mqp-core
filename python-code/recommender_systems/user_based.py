from recommender_systems.modules import evaluation, matrix, helpers
from scipy.spatial import distance
import numpy as np
import time

def playlist_similarities(playlist_matrix):
    start = time.time()
    print("Playlist similarities...")
    cosine_sims = []
    jaccard_sims = []
    for playlist1 in playlist_matrix:
        cosine_row = []
        jaccard_row = []
        for playlist2 in playlist_matrix:
            if np.array_equal(playlist1, playlist2):
                cosine_row.append(1)
                jaccard_row.append(1)
            else:
                cosine_row.append(distance.cosine(playlist1, playlist2))
                jaccard_row.append(distance.jaccard(playlist1, playlist2))
        cosine_sims.append(cosine_row)
        jaccard_sims.append(jaccard_row)
    print("-Seconds elapsed:", time.time() - start)
    return np.asarray(cosine_sims), np.asarray(jaccard_sims)

def run(cosine_sims, jaccard_sims, playlist_matrix, tids, N):
    start = time.time()
    max_K = 30 # Number of top similar playlists to the input playlist
    print("User-based collaborative filtering...")

    # For each input playlist, recommend N tracks to it, and evaluate the recommendation
    cosine_sim_k_evaluation_results = {} # Key = k, Value = list of r_precision_results
    jaccard_sim_k_evaluation_results = {} # Key = k, Value = list of r_precision_results'

    #for playlist_index in range(0, playlist_matrix.shape[0]):
        #for K in range(1, max_K + 1):
    playlist_index = 0
    K = 4
    top_k_cosine_sims = np.sort(cosine_sims[playlist_index])[1:K +1].tolist()
    top_k_playlists = []
    for similar_index, cosine_sim in np.ndenumerate(cosine_sims[playlist_index]):
        if top_k_cosine_sims.size == 0:
            break
        if cosine_sim in top_k_cosine_sims:
            top_k_cosine_sims.remove(cosine_sim)
            top_k_playlists.append((cosine_sim * playlist_matrix[similar_index]).tolist())
    top_k_playlists = np.asarray(top_k_playlists)
    track_relevancy_scores = np.sum(top_k_playlists, axis=0)
    sorted_track_relevancy_scores = np.sort(track_relevancy_scores)

    new_playlist = playlist_matrix[playlist_index]
    evaluation_sample = []
    for track_index, cell in np.ndenumerate(playlist_matrix[playlist_index]):
        if len(evaluation_sample) < N and cell == 1:
            evaluation_sample.append(track_index)
            new_playlist[track_index] = 0

    recommended_tracks = []
    for track_index, track_score in np.ndenumerate(track_relevancy_scores):
        if sorted_track_relevancy_scores.size == 0:
            break
        if track_score in top_n_track_relevancy_scores:
            top_n_track_relevancy_scores.remove(track_score)
            recommended_tracks.append(track_index)





    """
    for input_pid in np.asarray(list(playlist_dict.keys())):
        for K in range(1, max_K + 1):
            # Calculate the sum similarity score for each potential tid to recommend
            cosine_similar_track_dict = {} # Key = potential tid to recommend, Value = Sum total of cosine_similarities
            jaccard_similar_track_dict = {} # Key = potential tid to recommend, Value = Sum total of jaccard_similarities
            for cosine_sim_playlist_tuple in np.asarray(cosine_similarity_dict[input_pid][:K]):
                for tid in np.asarray(playlist_dict[cosine_sim_playlist_tuple[0]]['tracks']):
                    if tid not in cosine_similar_track_dict.keys():
                        cosine_similar_track_dict[tid] = 0
                    cosine_similar_track_dict[tid] += cosine_sim_playlist_tuple[1]
            for jaccard_sim_playlist_tuple in np.asarray(jaccard_similarity_dict[input_pid][:K]):
                for tid in np.asarray(playlist_dict[jaccard_sim_playlist_tuple[0]]['tracks']):
                    if tid not in jaccard_similar_track_dict.keys():
                        jaccard_similar_track_dict[tid] = 0
                    jaccard_similar_track_dict[tid] += jaccard_sim_playlist_tuple[1]

            # Transform those sum similarity scores into an ordered list of tuples
            cosine_similar_track_tuples = [] # List of tuples where tuple[0] = tid, tuple[1] = sum total cosine similarity score
            jaccard_similar_track_tuples = [] # List of tuples where tuple[0] = tid, tuple[1] = sum total jaccard similarity score
            for cosine_similar_tid in np.asarray(cosine_similar_track_dict.keys()):
                cosine_similar_track_tuples.append((cosine_similar_tid, cosine_similar_track_dict[cosine_similar_tid]))
            for jaccard_similar_tid in np.asarray(jaccard_similar_track_dict.keys()):
                jaccard_similar_track_tuples.append((jaccard_similar_tid, jaccard_similar_track_dict[jaccard_similar_tid]))
            cosine_similar_track_tuples.sort(reverse=True, key=helpers.sort_by_second_tuple)
            jaccard_similar_track_tuples.sort(reverse=True, key=helpers.sort_by_second_tuple)

            # Recommend N tracks to the input playlist and evaluate
            T, new_playlist_tracks = matrix.split_playlist(input_pid, playlist_dict)
            cosine_sim_recommended_tracks = helpers.recommend_n_tracks(N, cosine_similar_track_tuples, new_playlist_tracks)
            jaccard_sim_recommended_tracks = helpers.recommend_n_tracks(N, jaccard_similar_track_tuples, new_playlist_tracks)


            if K not in cosine_sim_k_evaluation_results.keys(): cosine_sim_k_evaluation_results[K] = []
            if K not in jaccard_sim_k_evaluation_results.keys(): jaccard_sim_k_evaluation_results[K] = []
            cosine_sim_k_evaluation_results[K].append(evaluation.dcg_precision(cosine_sim_recommended_tracks, T, N, unique_track_dict))
            jaccard_sim_k_evaluation_results[K].append(evaluation.dcg_precision(jaccard_sim_recommended_tracks, T, N, unique_track_dict))

    cosine_results_by_K = {}
    jaccard_results_by_K = {}
    for K in range(1, max_K + 1):
        cosine_results_by_K[K] = evaluation.avg_precision(cosine_sim_k_evaluation_results[K])
        jaccard_results_by_K[K] = evaluation.avg_precision(jaccard_sim_k_evaluation_results[K])
        print("\tK = " + str(K) + ": cosine = " + str(cosine_results_by_K[K]) + ", jaccard = " + str(jaccard_results_by_K[K]))

    print("User-based time:", time.time() - t1)
    return cosine_results_by_K, jaccard_results_by_K
    """
    return 1
