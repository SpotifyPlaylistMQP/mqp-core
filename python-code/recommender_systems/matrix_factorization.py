from recommender_systems.modules import evaluation, matrix, helpers
import scipy.sparse as sparse
import numpy as np
import time
import implicit

def train(playlist_dict, unique_track_dict, N, track_playlist_matrix, indexed_tids, indexed_pids, sample_size_for_avg, test_values):
    filename = "mf_training" + time.strftime("_%m-%d-%Y__%Hh%Mm") + ".txt"
    output = open(filename, "a")
    output.write("Alpha, Beta, Latent Features, Steps, NDCG, R-Precision\n")

    for alpha in test_values["alpha_set"]:
        for beta in test_values["beta_set"]:
            for latent_features in test_values["latent_features_set"]:
                for steps in test_values["steps_set"]:
                    params = {
                        "alpha": alpha,
                        "beta": beta,
                        "latent_features": latent_features,
                        "steps": steps,
                        "number_of_runs": 1,
                        "sample_size_for_avg": sample_size_for_avg
                    }
                    avg_ndcg, avg_r = run(playlist_dict, unique_track_dict, N, track_playlist_matrix, indexed_tids, indexed_pids, params)
                    print("Alpha:{}, Beta:{}, Latent_Features:{}, steps:{},  NDCG:{}, R:{}".format(alpha, beta, latent_features, steps, avg_ndcg, avg_r))
                    output.write("{}, {}, {}, {}, {}, {}\n".format(alpha, beta, latent_features, steps, avg_ndcg, avg_r))
    print("Wrote results to " + filename)

def run(playlist_dict, unique_track_dict, N, track_playlist_matrix, indexed_tids, indexed_pids, params):
    print("Matrix factorization...")
    start = time.time()

    sum_iteration_ndcg = 0
    sum_iteration_r = 0
    for test_iteration in range(params['number_of_runs']):
        sum_ndcg = 0
        sum_r = 0
        for input_playlist_index in range(params['sample_size_for_avg']):
            T, new_playlist_tracks = matrix.split_playlist(indexed_pids[input_playlist_index], playlist_dict)
            matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks, track_playlist_matrix, unique_track_dict)

            model = implicit.als.AlternatingLeastSquares(factors=params['latent_features'],
                                                         regularization=params['beta'],
                                                         iterations=params['steps'])
            model.fit(sparse.csr_matrix(track_playlist_matrix)* params['alpha'])

            factorized_matrix = np.dot(model.user_factors, model.item_factors.T).T.T.tolist()

            prediction_tuples = []
            for track_index, prediction in enumerate(factorized_matrix[input_playlist_index]):
                prediction_tuples.append((indexed_tids[track_index], prediction))
            prediction_tuples.sort(reverse=True, key=helpers.sort_by_second_tuple)

            recommended_tracks = helpers.recommend_n_tracks(N, prediction_tuples, new_playlist_tracks)
            matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks + T, track_playlist_matrix, unique_track_dict)
            sum_ndcg += evaluation.ndcg_precision(recommended_tracks, T, N, unique_track_dict)
            sum_r += evaluation.r_precision(recommended_tracks, T)
        sum_iteration_ndcg += sum_ndcg / params['sample_size_for_avg']
        sum_iteration_r += sum_r / params['sample_size_for_avg']

    print("Final Avg NDCG: {}      R: {}".format(sum_iteration_ndcg / params['number_of_runs'], sum_iteration_r / params['number_of_runs']))
    final = round(((time.time()) - start),2)
    print("Total time elapsed: " + str(final) + " seconds")
    # timing.save_time(final, "Matrix_Factorization")

    return sum_iteration_ndcg / params['number_of_runs'], sum_iteration_r / params['number_of_runs']