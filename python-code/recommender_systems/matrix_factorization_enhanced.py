from recommender_systems.modules import evaluation, matrix, helpers
import scipy.sparse as sparse
import numpy as np
import time
from scipy.sparse.linalg import spsolve

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

            factorized_matrix = matrix_factorization(track_playlist_matrix, params['alpha'], params['beta'], params['latent_features'], params['steps'])

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


# https://jessesw.com/Rec-System/
def matrix_factorization(track_playlist_matrix, alpha, beta, latent_features, iterations, seed=0):
    start = time.time()
    # first set up our confidence matrix
    conf = (alpha * sparse.csr_matrix(track_playlist_matrix))  # To allow the matrix to stay sparse, I will add one later when each row is taken

    # and converted to dense.
    num_user = conf.shape[0]
    num_item = conf.shape[1]  # Get the size of our original ratings matrix, m x n

    # initialize our X/Y feature vectors randomly with a set seed
    rstate = np.random.RandomState(seed)

    X = sparse.csr_matrix(rstate.normal(size=(num_user, latent_features)))  # Random numbers in a m x rank shape
    Y = sparse.csr_matrix(rstate.normal(size=(num_item, latent_features)))  # Normally this would be rank x n but we can
    # transpose at the end. Makes calculation more simple.
    X_eye = sparse.eye(num_user)
    Y_eye = sparse.eye(num_item)
    lambda_eye = beta * sparse.eye(latent_features)  # Our regularization term lambda*I.

    # We can compute this before iteration starts.

    # Begin iterations

    for iter_step in range(iterations):  # Iterate back and forth between solving X given fixed Y and vice versa
        # Compute yTy and xTx at beginning of each iteration to save computing time
        yTy = Y.T.dot(Y)
        xTx = X.T.dot(X)
        # Being iteration to solve for X based on fixed Y
        for u in range(num_user):
            conf_samp = conf[u, :].toarray()  # Grab user row from confidence matrix and convert to dense
            pref = conf_samp.copy()
            pref[pref != 0] = 1  # Create binarized preference vector
            CuI = sparse.diags(conf_samp, [0])  # Get Cu - I term, don't need to subtract 1 since we never added it
            yTCuIY = Y.T.dot(CuI).dot(Y)  # This is the yT(Cu-I)Y term
            yTCupu = Y.T.dot(CuI + Y_eye).dot(pref.T)  # This is the yTCuPu term, where we add the eye back in
            # Cu - I + I = Cu
            X[u] = spsolve(yTy + yTCuIY + lambda_eye, yTCupu)
            # Solve for Xu = ((yTy + yT(Cu-I)Y + lambda*I)^-1)yTCuPu, equation 4 from the paper
        # Begin iteration to solve for Y based on fixed X
        for i in range(num_item):
            conf_samp = conf[:, i].T.toarray()  # transpose to get it in row format and convert to dense
            pref = conf_samp.copy()
            pref[pref != 0] = 1  # Create binarized preference vector
            CiI = sparse.diags(conf_samp, [0])  # Get Ci - I term, don't need to subtract 1 since we never added it
            xTCiIX = X.T.dot(CiI).dot(X)  # This is the xT(Cu-I)X term
            xTCiPi = X.T.dot(CiI + X_eye).dot(pref.T)  # This is the xTCiPi term
            Y[i] = spsolve(xTx + xTCiIX + lambda_eye, xTCiPi)
            # Solve for Yi = ((xTx + xT(Cu-I)X) + lambda*I)^-1)xTCiPi, equation 5 from the paper
    # End iterations
    print("mf:", time.time() - start)
    return np.dot(X.toarray(), Y.toarray().T).T.tolist()  # Transpose at the end to make up for not being transposed at the beginning.
    # Y needs to be rank x n. Keep these as separate matrices for scale reasons.