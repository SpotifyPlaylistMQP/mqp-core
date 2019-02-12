from recommender_systems.modules import helpers
import scipy.sparse as sparse
import numpy as np
import implicit
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
        "learning_rate": 1e-7,
        "c": 1e-13
    },
    "mpd_square_1000": {
        "alpha": 10000,
        "regularization": 100,
        "latent_features": 100,
        "steps": 300,
        "error_limit": 1e-6,
        "fit_error_limit": 1e-5,
        "learning_rate": 1e-7,
        "c": 1e-5
    }
}

def get_factorized_matrix(mongo_collection, track_playlist_matrix, feature_matrix, params=None):
    if params is None:
        params = default_params[mongo_collection]
    track_playlist_matrix = np.array(track_playlist_matrix) * params["alpha"]

    # initial matrices. item_factors is random [0,1] and user_factors is item_factors\X.
    items, users = track_playlist_matrix.shape
    item_factors = np.random.rand(items, params['latent_features'])
    user_factors = np.random.rand(users, params['latent_features'])

    # Alternating least squares
    for i in range(1, params['steps'] + 1):
        # Fix item factors
        error = track_playlist_matrix - dot(item_factors, user_factors.T)
        for item in range(items):
            gradient = dot(error[item], user_factors) - params["regularization"] * item_factors[item]
            item_factors[item] = item_factors[item] + params["learning_rate"] * gradient
            item_factors[item][params["latent_features"] - 3] = feature_matrix[item][0] * params["c"]
            item_factors[item][params["latent_features"] - 2] = feature_matrix[item][1] * params["c"]
            item_factors[item][params["latent_features"] - 1] = feature_matrix[item][2] * params["c"]

        # Fix user factors
        error = (track_playlist_matrix - dot(item_factors, user_factors.T)).T
        for user in range(users):
            gradient = dot(error[user], item_factors) - params["regularization"] * user_factors[user]
            user_factors[user] = user_factors[user] + params["learning_rate"] * gradient

    return dot(item_factors, user_factors.T).T.tolist()

def get_ranked_tracks(factorized_matrix, input_playlist_index, indexed_tids):
    ranked_tracks = []
    for track_index, prediction in enumerate(factorized_matrix[input_playlist_index]):
        ranked_tracks.append((indexed_tids[track_index], prediction))
    ranked_tracks.sort(reverse=True, key=helpers.sort_by_second_tuple)
    return ranked_tracks