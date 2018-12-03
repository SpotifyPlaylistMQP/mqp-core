from recommender_systems.modules import similarities, evaluation, matrix, helpers
import time

# For each input track, get the list of the other tracks ordered by similarity
def create_similarity_dictionaries(input_tid, indexed_tids, matrix_rows):
    input_track_row = None
    for track_index, track_row in enumerate(matrix_rows):
        if indexed_tids[track_index] == input_tid:
            input_track_row = track_row
            break

    cosine_similarity_tuples = []  # List of tuples where tuple[0] = tid, tuple[1] = cosine_similarity_value
    jaccard_similarity_tuples = []  # List of tuples where tuple[0] = tid, tuple[1] = jaccard_similarity_value
    for comparison_track_index, comparison_track_row in enumerate(matrix_rows):
        comparison_tid = indexed_tids[comparison_track_index]
        if input_tid != comparison_tid:
            cosine_similarity_tuples.append((comparison_tid, similarities.cosine(input_track_row, comparison_track_row)))
            jaccard_similarity_tuples.append((comparison_tid, similarities.jaccard(input_track_row, comparison_track_row)))
    cosine_similarity_tuples.sort(reverse=True, key=helpers.sort_by_second_tuple)
    jaccard_similarity_tuples.sort(reverse=True, key=helpers.sort_by_second_tuple)

    return cosine_similarity_tuples, jaccard_similarity_tuples

def train(playlist_dict, unique_track_dict, track_playlist_matrix, indexed_pids, indexed_tids, sample_size_for_avg, N, test_values):
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
        T, new_playlist_tracks = matrix.split_playlist(input_pid, playlist_dict)
        matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks, track_playlist_matrix, unique_track_dict)

        for K in test_values['k_set']:
            cosine_similar_track_dict = {}  # Key = similar_tid, Value = Sum total of cosine_similarities for this playlist
            jaccard_similar_track_dict = {} # Key = similar_tid, Value = Sum total of jaccard_similarities for this playlist
            for input_tid in new_playlist_tracks:
                cosine_similar_track_tuples, jaccard_similar_track_tuples = create_similarity_dictionaries(input_tid, indexed_tids, track_playlist_matrix)
                for cosine_sim_tuple in cosine_similar_track_tuples[:K]:
                    if cosine_sim_tuple[0] not in cosine_similar_track_dict.keys():
                        cosine_similar_track_dict[cosine_sim_tuple[0]] = 0
                    cosine_similar_track_dict[cosine_sim_tuple[0]] += cosine_sim_tuple[1]
                for jaccard_sim_tuple in jaccard_similar_track_tuples[:K]:
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

            sum_cosine_ndcg_by_k[K] += evaluation.ndcg_precision(cosine_sim_recommended_tracks, T, N, unique_track_dict)
            sum_cosine_r_by_k[K] += evaluation.r_precision(cosine_sim_recommended_tracks, T)
            sum_jaccard_ndcg_by_k[K] += evaluation.ndcg_precision(jaccard_sim_recommended_tracks, T, N, unique_track_dict)
            sum_jaccard_r_by_k[K] += evaluation.r_precision(jaccard_sim_recommended_tracks, T)

        matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks + T, track_playlist_matrix, unique_track_dict)

    filename = "item_training" + time.strftime("_%m-%d-%Y__%Hh%Mm") + ".txt"
    output = open(filename, "a")
    output.write("K, cosine_ndcg, cosine_r, jaccard_ndcg, jaccard_r\n")
    for k in test_values['k_set']:
        output.write("{}, {}, {}, {}, {}\n".format(k,
                                                   sum_cosine_ndcg_by_k[k] / sample_size_for_avg,
                                                   sum_cosine_r_by_k[k] / sample_size_for_avg,
                                                   sum_jaccard_ndcg_by_k[k] / sample_size_for_avg,
                                                   sum_jaccard_r_by_k[k] / sample_size_for_avg))
    print("Wrote results to " + filename)


def run(playlist_dict, unique_track_dict, track_playlist_matrix, indexed_pids, indexed_tids, max_N, params):
    print("Item-based collaborative filtering...")
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
            T, new_playlist_tracks = matrix.split_playlist(input_pid, playlist_dict)
            matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks, track_playlist_matrix, unique_track_dict)

            cosine_similar_track_dict = {}  # Key = similar_tid, Value = Sum total of cosine_similarities for this playlist
            for input_tid in new_playlist_tracks:
                cosine_similar_track_tuples, jaccard_similar_track_tuples = create_similarity_dictionaries(input_tid, indexed_tids, track_playlist_matrix)
                for cosine_sim_tuple in cosine_similar_track_tuples[:params['K']]:
                    if cosine_sim_tuple[0] not in cosine_similar_track_dict.keys():
                        cosine_similar_track_dict[cosine_sim_tuple[0]] = 0
                    cosine_similar_track_dict[cosine_sim_tuple[0]] += cosine_sim_tuple[1]

            # Transform those sum similarity scores into an ordered list of tuples
            cosine_similar_track_tuples = []  # List of tuples: (similar_tid, Sum total of cosine_similarities for this playlist)
            for similar_tid in cosine_similar_track_dict.keys():
                cosine_similar_track_tuples.append((similar_tid, cosine_similar_track_dict[similar_tid]))
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
