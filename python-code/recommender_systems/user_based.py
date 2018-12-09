from recommender_systems.modules import similarities, evaluation, matrix, helpers
import time

def create_similarity_dictionaries(input_playlist_index, input_pid, playlist_dict, track_playlist_matrix):
    # For each input playlist, get the list of the other playlists ordered by similarity
    cosine_similarity_tuples = []  # List of tuples where tuple[0] = pid, tuple[1] = cosine_similarity_value
    jaccard_similarity_tuples = []  # List of tuples where tuple[0] = pid, tuple[1] = jaccard_similarity_value
    for comparison_playlist_index, comparison_pid in enumerate(playlist_dict.keys()):
        if input_pid != comparison_pid:
            input_playlist_column, comparison_playlist_column = helpers.get_two_playlist_column(input_playlist_index, comparison_playlist_index, track_playlist_matrix)
            cosine_similarity_tuples.append((comparison_pid, similarities.cosine(input_playlist_column, comparison_playlist_column)))
            jaccard_similarity_tuples.append((comparison_pid, similarities.jaccard(input_playlist_column, comparison_playlist_column)))
    cosine_similarity_tuples.sort(reverse=True, key=helpers.sort_by_second_tuple)
    jaccard_similarity_tuples.sort(reverse=True, key=helpers.sort_by_second_tuple)

    return cosine_similarity_tuples, jaccard_similarity_tuples

def train(playlist_dict, unique_track_dict, track_playlist_matrix, indexed_pids, sample_size_for_avg, N, test_values):
    sum_cosine_ndcg_by_k = {}
    sum_cosine_r_by_k = {}
    sum_jaccard_ndcg_by_k = {}
    sum_jaccard_r_by_k = {}
    for k in test_values['k_set']:
        sum_cosine_ndcg_by_k[k] = 0
        sum_cosine_r_by_k[k] = 0
        sum_jaccard_ndcg_by_k[k] = 0
        sum_jaccard_r_by_k[k] = 0
    for input_playlist_index in range(sample_size_for_avg):
        input_pid = indexed_pids[input_playlist_index]
        # Calculate the sum similarity score for each potential tid to recommend
        cosine_similar_track_dict = {} # Key = potential tid to recommend, Value = Sum total of cosine_similarities
        jaccard_similar_track_dict = {} # Key = potential tid to recommend, Value = Sum total of jaccard_similarities
        T, new_playlist_tracks = matrix.split_playlist(input_pid, playlist_dict)
        matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks, track_playlist_matrix, unique_track_dict)
        cosine_similarity_tuples, jaccard_similarity_tuples = create_similarity_dictionaries(input_playlist_index, input_pid, playlist_dict, track_playlist_matrix)
        for K in test_values['k_set']:
            for cosine_sim_playlist_tuple in cosine_similarity_tuples[:K]:
                for tid in playlist_dict[cosine_sim_playlist_tuple[0]]['tracks']:
                    if tid not in cosine_similar_track_dict.keys():
                        cosine_similar_track_dict[tid] = 0
                    cosine_similar_track_dict[tid] += cosine_sim_playlist_tuple[1]
            for jaccard_sim_playlist_tuple in jaccard_similarity_tuples[:K]:
                for tid in playlist_dict[jaccard_sim_playlist_tuple[0]]['tracks']:
                    if tid not in jaccard_similar_track_dict.keys():
                        jaccard_similar_track_dict[tid] = 0
                    jaccard_similar_track_dict[tid] += jaccard_sim_playlist_tuple[1]

            # Transform those sum similarity scores into an ordered list of tuples
            cosine_similar_track_tuples = [] # List of tuples where tuple[0] = tid, tuple[1] = sum total cosine similarity score
            jaccard_similar_track_tuples = [] # List of tuples where tuple[0] = tid, tuple[1] = sum total jaccard similarity score
            for cosine_similar_tid in cosine_similar_track_dict.keys():
                cosine_similar_track_tuples.append((cosine_similar_tid, cosine_similar_track_dict[cosine_similar_tid]))
            for jaccard_similar_tid in jaccard_similar_track_dict.keys():
                jaccard_similar_track_tuples.append((jaccard_similar_tid, jaccard_similar_track_dict[jaccard_similar_tid]))
            cosine_similar_track_tuples.sort(reverse=True, key=helpers.sort_by_second_tuple)
            jaccard_similar_track_tuples.sort(reverse=True, key=helpers.sort_by_second_tuple)

            # Recommend N tracks to the input playlist and evaluate
            cosine_sim_recommended_tracks = helpers.recommend_n_tracks(N, cosine_similar_track_tuples, new_playlist_tracks)
            jaccard_sim_recommended_tracks = helpers.recommend_n_tracks(N, jaccard_similar_track_tuples, new_playlist_tracks)

            sum_cosine_ndcg_by_k[K] += evaluation.ndcg_precision(cosine_sim_recommended_tracks, T, N, unique_track_dict)
            sum_cosine_r_by_k[K] += evaluation.r_precision(cosine_sim_recommended_tracks, T)
            sum_jaccard_ndcg_by_k[K] += evaluation.ndcg_precision(jaccard_sim_recommended_tracks, T, N, unique_track_dict)
            sum_jaccard_r_by_k[K] += evaluation.r_precision(jaccard_sim_recommended_tracks, T)
            print(evaluation.ndcg_precision(cosine_sim_recommended_tracks, T, N, unique_track_dict))

        matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks + T, track_playlist_matrix, unique_track_dict)

    filename = "user_training" + time.strftime("_%m-%d-%Y__%Hh%Mm") + ".txt"
    output = open(filename, "a")

    output.write("K, cosine_ndcg, cosine_r, jaccard_ndcg, jaccard_r\n")
    for k in test_values['k_set']:
        output.write("{}, {}, {}, {}, {}\n".format(k,
                                                 sum_cosine_ndcg_by_k[k] / sample_size_for_avg,
                                                 sum_cosine_r_by_k[k] / sample_size_for_avg,
                                                 sum_jaccard_ndcg_by_k[k] / sample_size_for_avg,
                                                 sum_jaccard_r_by_k[k] / sample_size_for_avg))
    print("Wrote results to " + filename)


def run(playlist_dict, unique_track_dict, track_playlist_matrix, indexed_pids, max_N, params):
    ndcg_N_dict = {}
    r_N_dict = {}
    for N in range(1, max_N + 1):
        ndcg_N_dict[N] = 0
        r_N_dict[N] = 0

    for run in range(params['number_of_runs']):
        print("Run #", run)
        for input_playlist_index in helpers.get_random_input_playlist_indexes(params['sample_size_for_avg'], len(indexed_pids)):
            input_pid = indexed_pids[input_playlist_index]
            # Calculate the sum similarity score for each potential tid to recommend
            cosine_similar_track_dict = {} # Key = potential tid to recommend, Value = Sum total of cosine_similarities
            T, new_playlist_tracks = matrix.split_playlist(input_pid, playlist_dict)
            matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks, track_playlist_matrix, unique_track_dict)
            cosine_similarity_tuples, jaccard_similarity_tuples = create_similarity_dictionaries(input_playlist_index, input_pid, playlist_dict, track_playlist_matrix)
            for cosine_sim_playlist_tuple in cosine_similarity_tuples[:params['K']]:
                for tid in playlist_dict[cosine_sim_playlist_tuple[0]]['tracks']:
                    if tid not in cosine_similar_track_dict.keys():
                        cosine_similar_track_dict[tid] = 0
                    cosine_similar_track_dict[tid] += cosine_sim_playlist_tuple[1]

            # Transform those sum similarity scores into an ordered list of tuples
            cosine_similar_track_tuples = [] # List of tuples where tuple[0] = tid, tuple[1] = sum total cosine similarity score
            for cosine_similar_tid in cosine_similar_track_dict.keys():
                cosine_similar_track_tuples.append((cosine_similar_tid, cosine_similar_track_dict[cosine_similar_tid]))
            cosine_similar_track_tuples.sort(reverse=True, key=helpers.sort_by_second_tuple)

            # Recommend N tracks to the input playlist and evaluate

            for N in range(1, max_N + 1):
                cosine_sim_recommended_tracks = helpers.recommend_n_tracks(N, cosine_similar_track_tuples, new_playlist_tracks)
                ndcg_N_dict[N] += evaluation.ndcg_precision(cosine_sim_recommended_tracks, T, N, unique_track_dict)
                r_N_dict[N] += evaluation.r_precision(cosine_sim_recommended_tracks, T)

            matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks + T, track_playlist_matrix, unique_track_dict)

    for N in range(1, max_N + 1):
        ndcg_N_dict[N] = ndcg_N_dict[N] / (params['number_of_runs'] * params['sample_size_for_avg'])
        r_N_dict[N] = r_N_dict[N] / (params['number_of_runs'] * params['sample_size_for_avg'])
    print("\tAvg NDCG:", ndcg_N_dict)
    print("\tAvg R-Precision:", r_N_dict)

    return ndcg_N_dict, r_N_dict
