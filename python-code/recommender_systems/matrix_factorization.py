from recommender_systems.modules import evaluation, matrix, helpers
import numpy

def run(playlist_dict, unique_track_dict, N, track_playlist_matrix, indexed_tids, indexed_pids, steps):
    print("Matrix factorization...")
    number_of_track = len(track_playlist_matrix)
    number_of_playlists = len(track_playlist_matrix[0])
    K = 3

    P = numpy.random.rand(number_of_track, K)
    Q = numpy.random.rand(number_of_playlists, K)

    factorized_matrix = matrix_factorization(track_playlist_matrix, P, Q, K, steps, alpha=0.0002, beta=0.02)

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

"""
@INPUT:
    R     : a matrix to be factorized, dimension N x M
    P     : an initial matrix of dimension N x K
    Q     : an initial matrix of dimension M x K
    K     : the number of latent features
    steps : the maximum number of steps to perform the optimisation
    alpha : the learning rate
    beta  : the regularization parameter
@OUTPUT:
    the final matrices P and Q
http://www.quuxlabs.com/blog/2010/09/matrix-factorization-a-simple-tutorial-and-implementation-in-python/
"""
def matrix_factorization(track_playlist_matrix, P, Q, K, steps, alpha, beta):
    Q = Q.T
    for step in range(steps):
        for row in range(len(track_playlist_matrix)):
            for col in range(len(track_playlist_matrix[row])):
                if track_playlist_matrix[row][col] > 0:
                    eij = track_playlist_matrix[row][col] - numpy.dot(P[row, :], Q[:, col])
                    for k in range(K):
                        P[row][k] = P[row][k] + alpha * (2 * eij * Q[k][col] - beta * P[row][k])
                        Q[k][col] = Q[k][col] + alpha * (2 * eij * P[row][k] - beta * Q[k][col])
        e = 0
        for row in range(len(track_playlist_matrix)):
            for col in range(len(track_playlist_matrix[row])):
                if track_playlist_matrix[row][col] > 0:
                    e = e + pow(track_playlist_matrix[row][col] - numpy.dot(P[row, :], Q[:, col]), 2)
                    for k in range(K):
                        e = e + (beta/2) * ( pow(P[row][k],2) + pow(Q[k][col],2) )
        if e < 0.001:
            break
    return numpy.dot(P, Q)