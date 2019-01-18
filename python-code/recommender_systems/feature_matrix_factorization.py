from recommender_systems.modules import helpers
import scipy.sparse as sparse
import numpy as np
import implicit

default_params = {
    "mpd_square_100": {
        "alpha": 0.1,
        "beta": 1,
        "latent_features": 30,
        "steps": 50,
        "c": 100
    },
    "mpd_square_1000": {
        "alpha": 1,
        "beta": 10,
        "latent_features": 30,
        "steps": 200,
        "c": 1
    }
}

def get_factorized_matrix(mongo_collection, track_playlist_matrix, feature_matrix, params=None):
    if params is None:
        params = default_params[mongo_collection]

    model = implicit.als.AlternatingLeastSquares(factors=params['latent_features'] + 3,
                                                 regularization=params['beta'],
                                                 iterations=1)
    for iteration in range(params['steps'] - 1):
        model.fit(sparse.csr_matrix(track_playlist_matrix) * params['alpha'], show_progress=False)
        for track_index in range(model.item_factors.shape[0]):
            model.item_factors[track_index][model.item_factors.shape[1] - 3] = feature_matrix[track_index][0] * params["c"]
            model.item_factors[track_index][model.item_factors.shape[1] - 2] = feature_matrix[track_index][1] * params["c"]
            model.item_factors[track_index][model.item_factors.shape[1] - 1] = feature_matrix[track_index][2] * params["c"]

    model.fit(sparse.csr_matrix(track_playlist_matrix) * params['alpha'], show_progress=False)
    return np.dot(model.user_factors, model.item_factors.T).T.T.tolist()

def get_ranked_tracks(factorized_matrix, input_playlist_index, indexed_tids):
    ranked_tracks = []
    for track_index, prediction in enumerate(factorized_matrix[input_playlist_index]):
        ranked_tracks.append((indexed_tids[track_index], prediction))
    ranked_tracks.sort(reverse=True, key=helpers.sort_by_second_tuple)
    return ranked_tracks