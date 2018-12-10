from recommender_systems.modules import helpers
import scipy.sparse as sparse
import numpy as np
import implicit

params = {
    "mpd_square_100": {
        "alpha": 0.1,
        "beta": 1,
        "latent_features": 90,
        "steps": 150,
    },
    "mpd_square_1000": {
        "alpha": 1,
        "beta": 1e-4,
        "latent_features": 10,
        "steps": 100,
    }
}

def get_ranked_tracks(input_playlist_index, indexed_tids, track_playlist_matrix, mongo_collection):
    model = implicit.als.AlternatingLeastSquares(factors=params[mongo_collection]['latent_features'],
                                                 regularization=params[mongo_collection]['beta'],
                                                 iterations=params[mongo_collection]['steps'])
    model.fit(sparse.csr_matrix(track_playlist_matrix) * params[mongo_collection]['alpha'], show_progress=False)
    factorized_matrix = np.dot(model.user_factors, model.item_factors.T).T.T.tolist()

    ranked_tracks = []
    for track_index, prediction in enumerate(factorized_matrix[input_playlist_index]):
        ranked_tracks.append((indexed_tids[track_index], prediction))
    ranked_tracks.sort(reverse=True, key=helpers.sort_by_second_tuple)

    return ranked_tracks


