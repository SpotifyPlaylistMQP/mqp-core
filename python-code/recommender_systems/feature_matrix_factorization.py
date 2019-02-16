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

    # initial matrices. item_features is random [0,1] and user_features is item_features\X.
    items, users = track_playlist_matrix.shape
    item_features = np.random.rand(items, params['latent_features'])
    user_features = np.random.rand(users, params['latent_features'])

    # Alternating least squares
    for i in range(1, params['steps'] + 1):
        # Fix item factors
        loss = track_playlist_matrix - dot(item_features, user_features.T)
        for item in range(items):
            item_features[item] += 2 * params["learning_rate"] * dot(loss[item], user_features)
            item_features[item][params["latent_features"] - 3] = feature_matrix[item][0] * params["spotify_feature_weight"]
            item_features[item][params["latent_features"] - 2] = feature_matrix[item][1] * params["spotify_feature_weight"]
            item_features[item][params["latent_features"] - 1] = feature_matrix[item][2] * params["spotify_feature_weight"]

        # Fix user factors
        loss = (track_playlist_matrix - dot(item_features, user_features.T)).T
        for user in range(users):
            user_features[user] += 2 * params["learning_rate"] * dot(loss[user], item_features)

    return dot(item_features, user_features.T).T.tolist()

def get_ranked_tracks(factorized_matrix, input_playlist_index, indexed_tids):
    ranked_tracks = []
    for track_index, prediction in enumerate(factorized_matrix[input_playlist_index]):
        ranked_tracks.append((indexed_tids[track_index], prediction))
    ranked_tracks.sort(reverse=True, key=helpers.sort_by_second_tuple)
    return ranked_tracks