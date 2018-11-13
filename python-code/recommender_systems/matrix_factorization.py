from recommender_systems.modules import evaluation, matrix, helpers
import numpy as np
from scipy import linalg
from numpy import dot
import time

def run(playlist_dict, unique_track_dict, N, track_playlist_matrix, indexed_tids, indexed_pids, K, total_iterations):
    print("Matrix factorization...")
    start = time.time()

    number_of_track = len(track_playlist_matrix)
    number_of_playlists = len(track_playlist_matrix[0])

    factorized_matrix = matrix_factorization(track_playlist_matrix, K)

    avg_avg_precision = 0
    for iteration in range(total_iterations):
        avg_precision = 0
        total_results = 0
        for input_playlist_index, input_playlist_row in enumerate(factorized_matrix.T):
            input_pid = indexed_pids[input_playlist_index]
            prediction_tuples = [] # List of tuples: (tid, prediction)
            for track_index, prediction in enumerate(input_playlist_row):
                prediction_tuples.append((indexed_tids[track_index], prediction))
            prediction_tuples.sort(reverse=True, key=helpers.sort_by_second_tuple)

            T, new_playlist_tracks = matrix.split_playlist(input_pid, playlist_dict)
            recommended_tracks = helpers.recommend_n_tracks(N, prediction_tuples, new_playlist_tracks)
            avg_precision += evaluation.dcg_precision(recommended_tracks, T, N, unique_track_dict)
            total_results += 1
        avg_avg_precision += avg_precision / total_results

    final = round(((time.time()) - start),2)
    print("Total time elapsed: " + str(final) + " seconds")
    timing.save_time(final, "Matrix_Factorization")
    return avg_avg_precision / total_iterations

# https://stackoverflow.com/questions/22767695/python-non-negative-matrix-factorization-that-handles-both-zeros-and-missing-dat
def matrix_factorization(track_playlist_matrix, latent_features, steps=100, error_limit=0.000001, fit_error_limit=0.0001):
    eps = 1e-5
    track_playlist_matrix = np.array(track_playlist_matrix)

    # mask
    mask = np.sign(track_playlist_matrix)

    # initial matrices. A is random [0,1] and Y is A\X.
    rows, columns = track_playlist_matrix.shape
    A = np.random.rand(rows, latent_features)
    A = np.maximum(A, eps)

    Y = linalg.lstsq(A, track_playlist_matrix)[0]
    Y = np.maximum(Y, eps)

    masked_matrix = mask * track_playlist_matrix
    matrix_est_prev = dot(A, Y)
    for i in range(1, steps + 1):
        # ===== updates =====
        top = dot(masked_matrix, Y.T)
        bottom = (dot((mask * dot(A, Y)), Y.T)) + eps
        A *= top / bottom

        A = np.maximum(A, eps)

        top = dot(A.T, masked_matrix)
        bottom = dot(A.T, mask * dot(A, Y)) + eps
        Y *= top / bottom
        Y = np.maximum(Y, eps)

        # ==== evaluation ====
        if i % 5 == 0 or i == 1 or i == steps:
            matrix_est = dot(A, Y)
            err = mask * (matrix_est_prev - matrix_est)
            fit_residual = np.sqrt(np.sum(err ** 2))
            matrix_est_prev = matrix_est

            cur_res = linalg.norm(mask * (track_playlist_matrix - matrix_est), ord='fro')
            if cur_res < error_limit or fit_residual < fit_error_limit:
                break

    return dot(A, Y)
