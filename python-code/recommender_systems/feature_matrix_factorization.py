from recommender_systems.modules import evaluation, matrix, helpers
import scipy.sparse as sparse
import numpy as np
import time
from scipy.sparse.linalg import spsolve

def train(playlist_dict, unique_track_dict, feature_matrix, N, track_playlist_matrix, indexed_tids, indexed_pids, params):
    filename = str(len(playlist_dict.keys())) + "feature_mf_training" + time.strftime("_%m-%d-%Y__%Hh%Mm") + ".txt"
    output = open(filename, "a")
    output.write("Alpha, Beta, c, Latent Features, Steps, NDCG, R-Precision\n")
    runs_for_avg = 5
    input_playlist_index = 0

    T, new_playlist_tracks = matrix.split_playlist_not_random(indexed_pids[input_playlist_index], playlist_dict)
    matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks, track_playlist_matrix,
                                        unique_track_dict)

    for alpha in params["alpha_set"]:
        for beta in params["beta_set"]:
            for latent_features in params["latent_features_set"]:
                for steps in params["steps_set"]:
                    for c in params["c_set"]:
                        c_feature_matrix = (np.array(feature_matrix) * c).tolist()
                        sum_ndcg = 0
                        sum_r = 0
                        for run in range(runs_for_avg):
                            factorized_matrix = matrix_factorization(track_playlist_matrix, alpha, beta, latent_features, steps, c_feature_matrix)

                            prediction_tuples = []
                            for track_index, prediction in enumerate(factorized_matrix[input_playlist_index]):
                                prediction_tuples.append((indexed_tids[track_index], prediction))
                            prediction_tuples.sort(reverse=True, key=helpers.sort_by_second_tuple)

                            recommended_tracks = helpers.recommend_n_tracks(N, prediction_tuples, new_playlist_tracks)

                            sum_ndcg += evaluation.ndcg_precision(recommended_tracks, T, N, unique_track_dict)
                            sum_r += evaluation.r_precision(recommended_tracks, T)
                        print("Alpha:{}, Beta:{}, C:{}, Latent_Features:{}, steps:{},  NDCG:{}, R:{}".format(alpha, beta, c, latent_features, steps, sum_ndcg / runs_for_avg, sum_r / runs_for_avg))
                        output.write("{}, {}, {}, {}, {}, {}, {}\n".format(alpha, beta, c, latent_features, steps, sum_ndcg / runs_for_avg, sum_r / runs_for_avg))
    print("Wrote results to " + filename)

def run(playlist_dict, unique_track_dict, feature_matrix, N, track_playlist_matrix, indexed_tids, indexed_pids, params):
    print("Feature matrix factorization...")
    start = time.time()

    sum_iteration_ndcg = 0
    sum_iteration_r = 0
    for test_iteration in range(params['number_of_runs']):
        print("Run #", test_iteration)
        sum_ndcg = 0
        sum_r = 0
        for input_playlist_index in helpers.get_random_input_playlist_indexes(params['sample_size_for_avg'], len(indexed_pids)):
            T, new_playlist_tracks = matrix.split_playlist(indexed_pids[input_playlist_index], playlist_dict)
            matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks, track_playlist_matrix, unique_track_dict)

            factorized_matrix = matrix_factorization(track_playlist_matrix, params['alpha'], params['beta'], params['latent_features'], params['steps'], feature_matrix)

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

def evaluate(playlist_dict, unique_track_dict, feature_matrix, max_N, track_playlist_matrix, indexed_tids, indexed_pids, params):
    print("Feature matrix factorization...")

    ndcg_N_dict = {}
    r_N_dict = {}
    for N in range(1, max_N + 1):
        ndcg_N_dict[N] = 0
        r_N_dict[N] = 0

    for run in range(params['number_of_runs']):
        print("Run #", run)
        for input_playlist_index in helpers.get_random_input_playlist_indexes(params['sample_size_for_avg'], len(indexed_pids)):
            T, new_playlist_tracks = matrix.split_playlist(indexed_pids[input_playlist_index], playlist_dict)
            matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks, track_playlist_matrix, unique_track_dict)

            c_feature_matrix = (np.array(feature_matrix) * params["c"]).tolist()
            factorized_matrix = matrix_factorization(track_playlist_matrix, params['alpha'], params['beta'], params['latent_features'], params['steps'], c_feature_matrix)

            prediction_tuples = []
            for track_index, prediction in enumerate(factorized_matrix[input_playlist_index]):
                prediction_tuples.append((indexed_tids[track_index], prediction))
            prediction_tuples.sort(reverse=True, key=helpers.sort_by_second_tuple)

            for N in range(1, max_N + 1):
                recommended_tracks = helpers.recommend_n_tracks(N, prediction_tuples, new_playlist_tracks)
                ndcg_N_dict[N] += evaluation.ndcg_precision(recommended_tracks, T, N, unique_track_dict)
                r_N_dict[N] += evaluation.r_precision(recommended_tracks, T)

            matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks + T, track_playlist_matrix, unique_track_dict)

    for N in range(1, max_N + 1):
        ndcg_N_dict[N] = ndcg_N_dict[N] / (params['number_of_runs'] * params['sample_size_for_avg'])
        r_N_dict[N] = r_N_dict[N] / (params['number_of_runs'] * params['sample_size_for_avg'])
    print("\tAvg NDCG:", ndcg_N_dict)
    print("\tAvg R-Precision:", r_N_dict)

    return ndcg_N_dict, r_N_dict

# https://jessesw.com/Rec-System/
def matrix_factorization(track_playlist_matrix, alpha, beta, latent_features, iterations, feature_matrix, seed=0):
    num_spotify_features = 3
    total_features = latent_features + num_spotify_features

    conf = (alpha * sparse.csr_matrix(track_playlist_matrix)).T

    num_user = conf.shape[0]
    num_item = conf.shape[1]

    rstate = np.random.RandomState(seed)

    X = sparse.csr_matrix(rstate.normal(size=(num_user, total_features)))
    Y = sparse.csr_matrix(rstate.normal(size=(num_item, latent_features)))

    Y = sparse.csr_matrix(sparse.hstack((Y, feature_matrix)))

    X_eye = sparse.eye(num_user)
    Y_eye = sparse.eye(num_item)
    lambda_eye = beta * sparse.eye(total_features)

    for iter_step in range(iterations):
        yTy = Y.T.dot(Y) #item
        xTx = X.T.dot(X) #user

        for u in range(num_user):
            conf_samp = conf[u, :].toarray()  # Grab user row from confidence matrix and convert to dense
            pref = conf_samp.copy()
            pref[pref != 0] = 1  # Create binarized preference vector
            CuI = sparse.diags(conf_samp, [0])  # Get Cu - I term, don't need to subtract 1 since we never added it
            yTCuIY = Y.T.dot(CuI).dot(Y)  # This is the yT(Cu-I)Y term
            yTCupu = Y.T.dot(CuI + Y_eye).dot(pref.T)  # This is the yTCuPu term, where we add the eye back in
            # Cu - I + I = Cu
            X[u] = spsolve(yTy + yTCuIY + lambda_eye, yTCupu)

        for i in range(num_item):
            conf_samp = conf[:, i].T.toarray()  # transpose to get it in row format and convert to dense
            pref = conf_samp.copy()
            pref[pref != 0] = 1  # Create binarized preference vector
            CiI = sparse.diags(conf_samp, [0])  # Get Ci - I term, don't need to subtract 1 since we never added it
            xTCiIX = X.T.dot(CiI).dot(X)  # This is the xT(Cu-I)X term
            xTCiPi = X.T.dot(CiI + X_eye).dot(pref.T)  # This is the xTCiPi term
            new_yi = list(np.array(spsolve(xTx + xTCiIX + lambda_eye, xTCiPi)))
            new_yi[total_features-3] = feature_matrix[i][0]
            new_yi[total_features-2] = feature_matrix[i][1]
            new_yi[total_features-1] = feature_matrix[i][2]
            Y[i] = sparse.csr_matrix(new_yi)

    return np.dot(X.toarray(), Y.toarray().T).tolist()
