from recommender_systems.modules import evaluation, matrix, helpers
import numpy as np
import pymf
from scipy import linalg
from numpy import dot

def run(playlist_dict, unique_track_dict, N, track_playlist_matrix, indexed_tids, indexed_pids, steps):
    print("Matrix factorization...")
    number_of_track = len(track_playlist_matrix)
    number_of_playlists = len(track_playlist_matrix[0])
    K = 1

    P = np.random.rand(number_of_track, K)
    Q = np.random.rand(number_of_playlists, K)

    factorized_matrix = matrix_factorization(track_playlist_matrix, K)

    avg_precision = 0
    total_precisions = 0
    for input_playlist_index, input_playlist_row in enumerate(factorized_matrix.T):
        input_pid = indexed_pids[input_playlist_index]
        prediction_tuples = [] # List of tuples: (tid, prediction)
        for track_index, prediction in enumerate(input_playlist_row):
            prediction_tuples.append((indexed_tids[track_index], prediction))
        prediction_tuples.sort(reverse=True, key=helpers.sort_by_second_tuple)

        T, new_playlist_tracks = matrix.split_playlist(input_pid, playlist_dict)
        recommended_tracks = helpers.recommend_n_tracks(N, prediction_tuples, new_playlist_tracks)
        avg_precision += evaluation.dcg_precision(recommended_tracks, T, N, unique_track_dict)
        total_precisions += 1

    avg_precision = avg_precision / total_precisions
    print("\tSteps: ", steps, " Avg precision: ", avg_precision)

    return avg_precision

def matrix_factorization(matrix):
    matrix = np.array(matrix)

    svd = pymf.SVD(matrix, num_bases=2, niter=10)
    svd.initialization()
    svd.factorize()

"""
#https://stackoverflow.com/questions/22767695/python-non-negative-matrix-factorization-that-handles-both-zeros-and-missing-dat
def matrix_factorization(X, latent_features, max_iter=200, error_limit=1e-6, fit_error_limit=1e-6):

    eps = 1e-5
    X = np.array(X)  # I am passing in a scipy sparse matrix

    # mask
    mask = np.sign(X)

    # initial matrices. A is random [0,1] and Y is A\X.
    rows, columns = X.shape
    A = np.random.rand(rows, latent_features)
    A = np.maximum(A, eps)

    Y = linalg.lstsq(A, X)[0]
    Y = np.maximum(Y, eps)

    masked_X = mask * X
    X_est_prev = dot(A, Y)
    for i in range(1, max_iter + 1):
        # ===== updates =====
        top = dot(masked_X, Y.T)
        bottom = (dot((mask * dot(A, Y)), Y.T)) + eps
        A *= top / bottom

        A = np.maximum(A, eps)
        # print 'A',  np.round(A, 2)

        # Matlab: Y=Y.*((A'*(W.*X))./(A'*(W.*(A*Y))));
        top = dot(A.T, masked_X)
        bottom = dot(A.T, mask * dot(A, Y)) + eps
        Y *= top / bottom
        Y = np.maximum(Y, eps)
        # print 'Y', np.round(Y, 2)


        # ==== evaluation ====
        if i % 5 == 0 or i == 1 or i == max_iter:
            X_est = dot(A, Y)
            err = mask * (X_est_prev - X_est)
            fit_residual = np.sqrt(np.sum(err ** 2))
            X_est_prev = X_est

            curRes = linalg.norm(mask * (X - X_est), ord='fro')
            if curRes < error_limit or fit_residual < fit_error_limit:
                break

    return dot(A, Y)
"""