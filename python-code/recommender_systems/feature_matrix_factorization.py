from recommender_systems.modules import evaluation, matrix, helpers
import scipy.sparse as sparse
import numpy as np
import time
import implicit
from scipy.sparse.linalg import spsolve

params = {
    "mpd_square_100": {
        "alpha": 0.1,
        "beta": 1,
        "latent_features": 90,
        "steps": 150,
        "c": 3,
        "number_of_runs": 10,
        "sample_size_for_avg": 100
    },
    "mpd_square_1000": {
        "alpha": 1e-06,
        "beta": 0.001,
        "latent_features": 70,
        "steps": 200,
        "c": 1,
        "number_of_runs": 5,
        "sample_size_for_avg": 100
    }
}

def make_feature_matrix(unique_track_dict):
    feature_matrix = []
    for tid in unique_track_dict.keys():
        feature_matrix.append([
            unique_track_dict[tid]["danceability"],
            unique_track_dict[tid]["energy"],
            unique_track_dict[tid]["valence"]
        ])
    return feature_matrix

def get_ranked_tracks(input_playlist_index, unique_track_dict, indexed_tids, track_playlist_matrix, mongo_collection):
    num_spotify_features = 3
    feature_matrix = make_feature_matrix(unique_track_dict)
    c_feature_matrix = (np.array(feature_matrix) * params[mongo_collection]["c"]).tolist()
    model = implicit.als.AlternatingLeastSquares(factors=params[mongo_collection]['latent_features'] + num_spotify_features,
                                                 regularization=params[mongo_collection]['beta'],
                                                 iterations=1)
    for iteration in range(params[mongo_collection]['steps']):
        model.fit(sparse.csr_matrix(track_playlist_matrix) * params[mongo_collection]['alpha'])
        for track_index in range(model.item_factors.shape[0]):
            model.item_factors[track_index][model.item_factors.shape[1] - 3] = c_feature_matrix[track_index][0]
            model.item_factors[track_index][model.item_factors.shape[1] - 2] = c_feature_matrix[track_index][1]
            model.item_factors[track_index][model.item_factors.shape[1] - 1] = c_feature_matrix[track_index][2]

    factorized_matrix = np.dot(model.user_factors, model.item_factors.T).T.T.tolist()

    ranked_tracks = []
    for track_index, prediction in enumerate(factorized_matrix[input_playlist_index]):
        ranked_tracks.append((indexed_tids[track_index], prediction))
    ranked_tracks.sort(reverse=True, key=helpers.sort_by_second_tuple)

    return ranked_tracks

    """
    feature_matrix = make_feature_matrix(unique_track_dict)
    c_feature_matrix = (np.array(feature_matrix) * params[mongo_collection]["c"]).tolist()
    factorized_matrix = matrix_factorization(track_playlist_matrix,
                                             params[mongo_collection]['alpha'],
                                             params[mongo_collection]['beta'],
                                             params[mongo_collection]['latent_features'],
                                             params[mongo_collection]['steps'],
                                             c_feature_matrix)

    prediction_tuples = []
    for track_index, prediction in enumerate(factorized_matrix[input_playlist_index]):
        prediction_tuples.append((indexed_tids[track_index], prediction))
    prediction_tuples.sort(reverse=True, key=helpers.sort_by_second_tuple)

    return prediction_tuples
    """

# https://jessesw.com/Rec-System/
def matrix_factorization(track_playlist_matrix, alpha, beta, latent_features, iterations, feature_matrix, seed=0):
    num_spotify_features = 3
    total_features = latent_features + num_spotify_features

    conf = (alpha * sparse.csr_matrix(track_playlist_matrix)).T

    num_user = conf.shape[0]
    num_item = conf.shape[1]

    rstate = np.random.RandomState(seed)

    X = sparse.csr_matrix(rstate.normal(size=(num_user, total_features)))
    Y = sparse.csr_matrix(rstate.normal(size=(num_item, latent_features)))

    Y = sparse.csr_matrix(sparse.hstack((Y, feature_matrix)))

    X_eye = sparse.eye(num_user)
    Y_eye = sparse.eye(num_item)
    lambda_eye = beta * sparse.eye(total_features)

    for iter_step in range(iterations):
        yTy = Y.T.dot(Y) #item
        xTx = X.T.dot(X) #user

        for u in range(num_user):
            conf_samp = conf[u, :].toarray()  # Grab user row from confidence matrix and convert to dense
            pref = conf_samp.copy()
            pref[pref != 0] = 1  # Create binarized preference vector
            CuI = sparse.diags(conf_samp, [0])  # Get Cu - I term, don't need to subtract 1 since we never added it
            yTCuIY = Y.T.dot(CuI).dot(Y)  # This is the yT(Cu-I)Y term
            yTCupu = Y.T.dot(CuI + Y_eye).dot(pref.T)  # This is the yTCuPu term, where we add the eye back in
            # Cu - I + I = Cu
            X[u] = spsolve(yTy + yTCuIY + lambda_eye, yTCupu)

        for i in range(num_item):
            conf_samp = conf[:, i].T.toarray()  # transpose to get it in row format and convert to dense
            pref = conf_samp.copy()
            pref[pref != 0] = 1  # Create binarized preference vector
            CiI = sparse.diags(conf_samp, [0])  # Get Ci - I term, don't need to subtract 1 since we never added it
            xTCiIX = X.T.dot(CiI).dot(X)  # This is the xT(Cu-I)X term
            xTCiPi = X.T.dot(CiI + X_eye).dot(pref.T)  # This is the xTCiPi term
            new_yi = list(np.array(spsolve(xTx + xTCiIX + lambda_eye, xTCiPi)))
            new_yi[total_features-3] = feature_matrix[i][0]
            new_yi[total_features-2] = feature_matrix[i][1]
            new_yi[total_features-1] = feature_matrix[i][2]
            Y[i] = sparse.csr_matrix(new_yi)

    return np.dot(X.toarray(), Y.toarray().T).tolist()
