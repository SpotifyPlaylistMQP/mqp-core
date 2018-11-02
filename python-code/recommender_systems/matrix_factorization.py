from recommender_systems.modules import evaluation, matrix, helpers
import numpy

def run(playlist_dict, unique_track_dict, N, track_playlist_matrix, indexed_tids, indexed_pids):
    number_of_track = len(track_playlist_matrix)
    number_of_playlists = len(track_playlist_matrix[0])
    K = 2

    P = numpy.random.rand(number_of_track, K)
    Q = numpy.random.rand(number_of_playlists, K)
    print(P)
    print(Q)
    steps = 20
    factorized_matrix = matrix_factorization(track_playlist_matrix, P, Q, K, steps, alpha=0.0002, beta=0.02)

    for input_playlist_index, input_playlist_row in enumerate(factorized_matrix.T):
        input_pid = indexed_pids[input_playlist_index]
        prediction_tuples = [] # List of tuples: (tid, prediction)
        for track_index, prediction in enumerate(input_playlist_row):
            prediction_tuples.append((indexed_tids[track_index], prediction))
        prediction_tuples.sort(reverse=True, key=helpers.sort_by_second_tuple)

        T, new_playlist_tracks = matrix.split_playlist(input_pid, playlist_dict)
        recommended_tracks = helpers.recommend_n_tracks(N, prediction_tuples, new_playlist_tracks)
        print(evaluation.r_precision(recommended_tracks, T, N, unique_track_dict))

    return factorized_matrix

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
"""
def matrix_factorization(R, P, Q, K, steps, alpha, beta):
    Q = Q.T
    for step in range(steps):
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    eij = R[i][j] - numpy.dot(P[i,:],Q[:,j])
                    for k in range(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        e = 0
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - numpy.dot(P[i,:],Q[:,j]), 2)
                    for k in range(K):
                        e = e + (beta/2) * ( pow(P[i][k],2) + pow(Q[k][j],2) )
        if e < 0.001:
            break
    return numpy.dot(P, Q)