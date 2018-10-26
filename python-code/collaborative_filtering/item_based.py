from collaborative_filtering.modules import similarities, evaluation, matrix, helpers

# For each input track, get the list of the other tracks ordered by similarity
def create_similarity_dictionaries(indexed_tids, matrix_rows,):
    cosine_similarity_dict = {}  # Key = track_id, Value = Ordered (L -> G) list of cosine similar track tuples
    jaccard_similarity_dict = {}  # Key = track_id, Value = Ordered (L -> G) list of jaccard similar track tuples
    for input_track_index, input_track_row in enumerate(matrix_rows):
        input_tid = indexed_tids[input_track_index]
        cosine_similarity_tuples = []  # List of tuples where tuple[0] = tid, tuple[1] = cosine_similarity_value
        jaccard_similarity_tuples = []  # List of tuples where tuple[0] = tid, tuple[1] = jaccard_similarity_value
        for comparison_track_index, comparison_track_row in enumerate(matrix_rows):
            comparison_tid = indexed_tids[comparison_track_index]
            if input_tid != comparison_tid:
                cosine_similarity_tuples.append(
                    (comparison_tid, similarities.cosine(input_track_row, comparison_track_row)))
                jaccard_similarity_tuples.append(
                    (comparison_tid, similarities.jaccard(input_track_row, comparison_track_row)))
        cosine_similarity_tuples.sort(reverse=True, key=helpers.sort_by_second_tuple)
        jaccard_similarity_tuples.sort(reverse=True, key=helpers.sort_by_second_tuple)
        cosine_similarity_dict[input_tid] = cosine_similarity_tuples
        jaccard_similarity_dict[input_tid] = jaccard_similarity_tuples
    return cosine_similarity_dict, jaccard_similarity_dict

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
                cosine_sim_k_evaluation_results[K].append(evaluation.r_precision(cosine_sim_recommended_tracks, T, N, unique_track_dict))
                jaccard_sim_k_evaluation_results[K].append(evaluation.r_precision(jaccard_sim_recommended_tracks, T, N, unique_track_dict))

    cosine_results_by_K = {}
    jaccard_results_by_K = {}
    for K in range(1, max_K + 1):
        if K % 10 == 0:
            cosine_results_by_K[K] = evaluation.avg_precision(cosine_sim_k_evaluation_results[K])
            jaccard_results_by_K[K] = evaluation.avg_precision(jaccard_sim_k_evaluation_results[K])
            print("\tK = " + str(K) + ": cosine = " + str(cosine_results_by_K[K]) + ", jaccard = " + str(jaccard_results_by_K[K]))

    return cosine_results_by_K, jaccard_results_by_K

