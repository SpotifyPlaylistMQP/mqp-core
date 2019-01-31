from recommender_systems.modules import helpers
import scipy.sparse as sparse
import numpy as np
import implicit
from scipy import linalg
from numpy import dot


default_params = {
    "mpd_square_100": {
        "alpha": 0.01,
        "beta": 1,
        "latent_features": 30,
        "steps": 50,
    },
    "mpd_square_1000": {
        "alpha": 1,
        "beta": 10,
        "latent_features": 30,
        "steps": 200,
    }
}

def get_factorized_matrix(mongo_collection, track_playlist_matrix, params=None):
    # if params is None:
    #     params = default_params[mongo_collection]
    #
    # model = implicit.als.AlternatingLeastSquares(factors=params['latent_features'],
    #                                              regularization=params['beta'],
    #                                              iterations=params['steps'])
    # model.fit(sparse.csr_matrix(track_playlist_matrix) * params['alpha'], show_progress=False)
    # return np.dot(model.user_factors, model.item_factors.T).T.T.tolist()


    # if params is None:
    #     params = default_params[mongo_collection]
    #
    # track_playlist_matrix = np.asarray(track_playlist_matrix)
    #
    # num_factors = params['latent_features']
    #
    # item_factors = np.zeros(len(track_playlist_matrix), num_factors)
    # user_factors = np.zeros(len(track_playlist_matrix[0]), num_factors)
    #
    # num_steps = params['steps']
    #
    # for step in range(num_steps):
    #     for row in range(len(track_playlist_matrix[0])):
    #         for col in range(len(track_playlist_matrix[1]):
    #             rating =

    if params is None:
        params = default_params[mongo_collection]

    eps = 1e-7
    track_playlist_matrix = np.array(track_playlist_matrix) * params["alpha"]

    latent_features = params['latent_features']
    steps = params['steps']
    error_limit = 0.000001
    fit_error_limit = 0.0001

    # initial matrices. U is random [0,1] and V is U\X.
    rows, columns = track_playlist_matrix.shape

    U = np.random.rand(rows, latent_features)
    U = np.maximum(U, eps)

    V = linalg.lstsq(U, track_playlist_matrix)[0]
    V = np.maximum(V, eps)

    matrix_est_prev = dot(U, V)

    for i in range(1, steps + 1):
        # ===== updates =====
        top = dot(track_playlist_matrix, V.T)
        bottom = (dot((dot(U, V)), V.T)) + eps
        U *= top / bottom

        U = np.maximum(U, eps)

        top = dot(U.T, track_playlist_matrix)
        bottom = dot(U.T, dot(U, V)) + eps
        V *= top / bottom
        V = np.maximum(V, eps)

        if i % 5 == 0 or i == 1 or i == steps:
            estimate = dot(U, V)
            loss = np.sqrt(np.sum((matrix_est_prev - estimate)**2))

            matrix_est_prev = estimate

            cur_res = linalg.norm(track_playlist_matrix - estimate, ord='fro')
            if cur_res < error_limit or loss < fit_error_limit:
                break

    return dot(U, V).T.tolist()


def get_ranked_tracks(factorized_matrix, input_playlist_index, indexed_tids):
    ranked_tracks = []
    for track_index, prediction in enumerate(factorized_matrix[input_playlist_index]):
        ranked_tracks.append((indexed_tids[track_index], prediction))
    ranked_tracks.sort(reverse=True, key=helpers.sort_by_second_tuple)
    return ranked_tracks
