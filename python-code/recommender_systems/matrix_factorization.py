from recommender_systems.modules import helpers
import numpy as np
from scipy import linalg
from numpy import dot


default_params = {
    "mpd_square_100": {
        "alpha": 0.01,
        "regularization": 1e-8,
        "latent_features": 3,
        "steps": 600,
        "error_limit": 1e-6,
        "fit_error_limit": 1e-5,
        "learning_rate": 1e-6
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

    # initial matrices. item_factors is random [0,1] and user_factors is item_factors\X.
    items, users = track_playlist_matrix.shape
    item_factors = np.random.rand(items, params['latent_features'])
    user_factors = np.random.rand(users, params['latent_features'])

    length = params["regularization"] * ((len(item_factors) ** 2) + (len(user_factors) ** 2))

    for i in range(1, params['steps'] + 1):
        # Gradient Descent from stack, not sure what it is?
        # top = dot(track_playlist_matrix, user_factors.T)
        # bottom = (dot((dot(item_factors, user_factors)), user_factors.T)) + length
        # item_factors *= top / bottom
        # item_factors = np.maximum(item_factors, length)
        #
        # top = dot(item_factors.T, track_playlist_matrix)
        # bottom = dot(item_factors.T, dot(item_factors, user_factors)) + length
        # user_factors *= top / bottom
        # user_factors = np.maximum(user_factors, length)

        e = track_playlist_matrix - dot(item_factors, user_factors.T)
        for item in range(items):
            a = params["regularization"] * item_factors[item]
            b = dot(e[item], user_factors)
            c = b - a
            d = params["learning_rate"] * c
            item_factors[item] = item_factors[item] + d

        e = e.T
        for user in range(users):
            a = params["regularization"] * user_factors[user]
            b = dot(e[user], item_factors)
            c = b - a
            d = params["learning_rate"] * c
            user_factors[user] = user_factors[user] + d

        # Check if it's good enough
        if i % 5 == 0 or i == 1 or i == params['steps']:
            estimated_ratings = dot(item_factors, user_factors.T)
            error = np.sqrt(np.sum((track_playlist_matrix - estimated_ratings)**2) + length)

            cur_res = linalg.norm(track_playlist_matrix - estimated_ratings, ord='fro')

            if cur_res < params["error_limit"] or error < params["fit_error_limit"]:
                break

    return dot(item_factors, user_factors.T).T.tolist()


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