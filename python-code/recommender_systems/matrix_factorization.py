from recommender_systems.modules import helpers
import numpy as np
from scipy import linalg
from numpy import dot


default_params = {
    "mpd_square_100": {
        "alpha": 10000,
        "regularization": 1,
        "latent_features": 100,
        "steps": 500,
        "error_limit": 1e-6,
        "fit_error_limit": 1e-5,
        "learning_rate": 1e-7
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

    # initial matrices. item_features is random [0,1] and user_features is item_features\X.
    items, users = track_playlist_matrix.shape
    item_features = np.random.rand(items, params['latent_features'])
    user_features = np.random.rand(users, params['latent_features'])

    # Alternating least squares
    for i in range(1, params['steps'] + 1):
        # Fix item factors
        error = track_playlist_matrix - dot(item_features, user_features.T)
        for item in range(items):
            gradient = dot(error[item], user_features) - params["regularization"] * item_features[item]
            item_features[item] = item_features[item] + params["learning_rate"] * gradient

        # Fix user factors
        error = (track_playlist_matrix - dot(item_features, user_features.T)).T
        for user in range(users):
            gradient = dot(error[user], item_features) - params["regularization"] * user_features[user]
            user_features[user] = user_features[user] + params["learning_rate"] * gradient

    return dot(item_features, user_features.T).T.tolist()


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