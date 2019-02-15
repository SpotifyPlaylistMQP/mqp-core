import torch
from recommender_systems.modules import helpers
from torch.autograd import Variable


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
        "alpha": 10000,
        "regularization": 100,
        "latent_features": 100,
        "steps": 300,
        "error_limit": 1e-6,
        "fit_error_limit": 1e-5,
        "learning_rate": 1e-7
    }
}

def get_factorized_matrix(mongo_collection, track_playlist_matrix, params=None):
    if params is None:
        params = default_params[mongo_collection]
    track_playlist_matrix = torch.Tensor(track_playlist_matrix) * params["alpha"]

    # initial matrices. item_features is random [0,1] and user_features is item_features\X.
    items, users = track_playlist_matrix.shape
    item_features = Variable(torch.rand(items, params['latent_features']), requires_grad=True)
    user_features = Variable(torch.rand(users, params['latent_features']), requires_grad=True)

    # Alternating Least Squares
    for i in range(1, params['steps'] + 1):
        # Fix item features
        loss = (track_playlist_matrix - torch.mm(item_features, torch.t(user_features))).pow(2).sum()
        loss.backward()
        print(item_features.grad)
        item_features = Variable(item_features - params["learning_rate"] * item_features.grad, requires_grad=True)
        user_features = user_features - params["learning_rate"] * user_features.grad
        print(item_features.grad)
        item_features.grad.zero_()
        user_features.grad.zero_()

    return torch.t(torch.mm(item_features, torch.t(user_features))).tolist()

def get_ranked_tracks(factorized_matrix, input_playlist_index, indexed_tids):
    ranked_tracks = []
    for track_index, prediction in enumerate(factorized_matrix[input_playlist_index]):
        ranked_tracks.append((indexed_tids[track_index], prediction))
    ranked_tracks.sort(reverse=True, key=helpers.sort_by_second_tuple)
    return ranked_tracks