from recommender_systems.modules import helpers
import scipy.sparse as sparse
import numpy as np
import implicit
from scipy import linalg
from numpy import dot


default_params = {
    "mpd_square_100": {
        "alpha": 0.01,
        "regularization": 1e-8,
        "latent_features": 3,
        "steps": 950,
        "error_limit": 1e-6,
        "learning_rate": 1e-6,
        "fit_error_limit": 1e-5
    },
    "mpd_square_1000": {
        "alpha": 0.01,
        "regularization": 1e-8,
        "latent_features": 3,
        "steps": 750,
        "error_limit": 1e-6,
        "fit_error_limit": 1e-5
    }
}

def get_factorized_matrix(mongo_collection, track_playlist_matrix, params=None):
    if params is None:
        params = default_params[mongo_collection]
    track_playlist_matrix = np.array(track_playlist_matrix) * params["alpha"]

    # initial matrices. U is random [0,1] and V is U\X.
    rows, columns = track_playlist_matrix.shape
    U = np.random.rand(rows, params['latent_features'])
    V = linalg.lstsq(U, track_playlist_matrix)[0]

    length = params["regularization"] * ((len(U) ** 2) + (len(V) ** 2))
    ratings = dot(U, V)

    for i in range(1, params['steps'] + 1):
        # Gradient Descent from stack, not sure what it is?
        # top = dot(track_playlist_matrix, V.T)
        # bottom = (dot((dot(U, V)), V.T)) + length
        # U *= top / bottom
        # U = np.maximum(U, length)
        #
        # top = dot(U.T, track_playlist_matrix)
        # bottom = dot(U.T, dot(U, V)) + length
        # V *= top / bottom
        # V = np.maximum(V, length)

        # SGD
        U = U + (params["learning_rate"] * (dot(dot(U, V), V.T) - (params["regularization"] * U)))
        V = V + (params["learning_rate"] * (dot(U.T, dot(U, V)) - (params["regularization"] * V)))

        # Check if it's good enough
        if i % 5 == 0 or i == 1 or i == params['steps']:
            estimated_ratings = dot(U, V)
            error = np.sqrt(np.sum((ratings - estimated_ratings)**2) + length)
            ratings = estimated_ratings

            cur_res = linalg.norm(track_playlist_matrix - estimated_ratings, ord='fro')

            if cur_res < params["error_limit"] or error < params["fit_error_limit"]:
                break

    return dot(U, V).T.tolist()


def get_ranked_tracks(factorized_matrix, input_playlist_index, indexed_tids):
    ranked_tracks = []
    for track_index, prediction in enumerate(factorized_matrix[input_playlist_index]):
        ranked_tracks.append((indexed_tids[track_index], prediction))
    ranked_tracks.sort(reverse=True, key=helpers.sort_by_second_tuple)
    return ranked_tracks


### OLD IMPLICIT USING MF
# def get_factorized_matrix(mongo_collection, track_playlist_matrix, params=None):
#     if params is None:
#         params = default_params[mongo_collection]
#
#     model = implicit.als.AlternatingLeastSquares(factors=params['latent_features'],
#                                                  regularization=params['beta'],
#                                                  iterations=params['steps'])
#     model.fit(sparse.csr_matrix(track_playlist_matrix) * params['alpha'], show_progress=False)
#     return np.dot(model.user_factors, model.item_factors.T).T.T.tolist()