from recommender_systems.modules import helpers
import scipy.sparse as sparse
import numpy as np
import implicit

params = {
    "mpd_square_100": {
        "alpha": 1,
        "beta": 1,
        "latent_features": 10,
        "steps": 100,
        "c": 0.01,
    },
    "mpd_square_1000": {
        "alpha": 1,
        "beta": 1e-4,
        "latent_features": 10,
        "steps": 100,
        "c": 10
    }
}

def get_ranked_tracks(input_playlist_index, indexed_tids, track_playlist_matrix, feature_matrix, mongo_collection):
    model = implicit.als.AlternatingLeastSquares(factors=params[mongo_collection]['latent_features'],
                                                 regularization=params[mongo_collection]['beta'],
                                                 iterations=1)
    for iteration in range(params[mongo_collection]['steps'] - 1):
        model.fit(sparse.csr_matrix(track_playlist_matrix) * params[mongo_collection]['alpha'], show_progress=False)
        for track_index in range(model.item_factors.shape[0]):
            model.item_factors[track_index][model.item_factors.shape[1] - 3] = feature_matrix[track_index][0] * params[mongo_collection]["c"]
            model.item_factors[track_index][model.item_factors.shape[1] - 2] = feature_matrix[track_index][1] * params[mongo_collection]["c"]
            model.item_factors[track_index][model.item_factors.shape[1] - 1] = feature_matrix[track_index][2] * params[mongo_collection]["c"]

    model.fit(sparse.csr_matrix(track_playlist_matrix) * params[mongo_collection]['alpha'], show_progress=False)
    factorized_matrix = np.dot(model.user_factors, model.item_factors.T).T.T.tolist()

    ranked_tracks = []
    for track_index, prediction in enumerate(factorized_matrix[input_playlist_index]):
        ranked_tracks.append((indexed_tids[track_index], prediction))
    ranked_tracks.sort(reverse=True, key=helpers.sort_by_second_tuple)

    return ranked_tracks

def train_run(input_playlist_index, indexed_tids, track_playlist_matrix, feature_matrix, train_params):
    model = implicit.als.AlternatingLeastSquares(factors=train_params['latent_features'],
                                                 regularization=train_params['beta'],
                                                 iterations=1)
    for iteration in range(train_params['steps']):
        model.fit(sparse.csr_matrix(track_playlist_matrix) * train_params['alpha'], show_progress=False)
        for track_index in range(model.item_factors.shape[0]):
            model.item_factors[track_index][model.item_factors.shape[1] - 3] = feature_matrix[track_index][0] * train_params["c"]
            model.item_factors[track_index][model.item_factors.shape[1] - 2] = feature_matrix[track_index][1] * train_params["c"]
            model.item_factors[track_index][model.item_factors.shape[1] - 1] = feature_matrix[track_index][2] * train_params["c"]

    factorized_matrix = np.dot(model.user_factors, model.item_factors.T).T.T.tolist()

    ranked_tracks = []
    for track_index, prediction in enumerate(factorized_matrix[input_playlist_index]):
        ranked_tracks.append((indexed_tids[track_index], prediction))
    ranked_tracks.sort(reverse=True, key=helpers.sort_by_second_tuple)

    return ranked_tracks