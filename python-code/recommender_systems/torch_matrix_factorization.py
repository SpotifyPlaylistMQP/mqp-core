import torch
from recommender_systems.modules import helpers


default_params = {
    "mpd_square_100": {
        "alpha": 1,
        "latent_features": 300,
        "steps": 250,
        "learning_rate": 1e-3
    },
    "mpd_square_1000": {
        "alpha": 10000,
        "latent_features": 100,
        "steps": 500,
        "learning_rate": 1e-7
    }
}

def sigmoid(x):
    return 1 / (1 + torch.exp(-x))

def get_factorized_matrix(mongo_collection, track_playlist_matrix, params=None):
    if params is None:
        params = default_params[mongo_collection]

    # initial matrices. item_features is random [0,1] and user_features is item_features\X.
    track_playlist_matrix = torch.Tensor(track_playlist_matrix) * params["alpha"]
    item_features = torch.rand(len(track_playlist_matrix), params['latent_features'], requires_grad=True)
    user_features = torch.rand(len(track_playlist_matrix[0]), params['latent_features'], requires_grad=True)

    # Alternating Least Squares
    for i in range(1, params['steps'] + 1):
        # predictions = sigmoid(torch.mm(item_features, torch.t(user_features))) * params["alpha"]
        predictions = torch.mm(item_features, torch.t(user_features))
        loss = (track_playlist_matrix - predictions).pow(2).sum()
        loss.backward()
        with torch.no_grad():
            item_features -= params["learning_rate"] * item_features.grad
            user_features -= params["learning_rate"] * user_features.grad
            item_features.grad.zero_()
            user_features.grad.zero_()

    return torch.t(torch.mm(item_features, torch.t(user_features))).tolist()

def get_ranked_tracks(factorized_matrix, input_playlist_index, indexed_tids):
    ranked_tracks = []
    for track_index, prediction in enumerate(factorized_matrix[input_playlist_index]):
        ranked_tracks.append((indexed_tids[track_index], prediction))
    ranked_tracks.sort(reverse=True, key=helpers.sort_by_second_tuple)
    return ranked_tracks