import torch
from recommender_systems.modules import helpers


default_params = {
    "mpd_square_100": {
        "alpha": 1,
        "latent_features": 700,
        "steps": 105,
        "learning_rate": 0.9
    },
    "mpd_square_1000": {
        "alpha": 1,
        "latent_features": 25,
        "steps": 50,
        "learning_rate": 1
    }
}

def get_factorized_matrix(mongo_collection, track_playlist_matrix, params=None):
    if params is None:
        params = default_params[mongo_collection]

    sig_fn = torch.nn.Sigmoid()

    def sigmoid(x):
        # return 1 / (1 + torch.exp(-10 * x + 5))
        return sig_fn(10*torch.nn.functional.normalize(x) - 5)
        # return sig_fn(x)

    def normalize(x):
        # max = torch.unsqueeze(torch.max(x, 1)[0], 1)
        # min = torch.unsqueeze(torch.min(x, 1)[0], 1)
        # return (x - min) / (max - min)
        return torch.nn.functional.normalize(x)
        # return (x - torch.min(x).item())/(torch.max(x).item() - torch.min(x).item())

    track_playlist_matrix = torch.t(torch.Tensor(track_playlist_matrix))
    item_features = torch.rand(len(track_playlist_matrix[0]), params['latent_features'], requires_grad=True)
    user_features = torch.rand(len(track_playlist_matrix), params['latent_features'], requires_grad=True)
    loss_fn = torch.nn.BCELoss()

    for i in range(1, params['steps'] + 1):
        predictions = sigmoid(torch.mm(user_features, torch.t(item_features)))
        loss = loss_fn(predictions, track_playlist_matrix)
        loss.backward()
        with torch.no_grad():
            item_features -= params["learning_rate"] * item_features.grad
            user_features -= params["learning_rate"] * user_features.grad
            item_features.grad.zero_()
            user_features.grad.zero_()

    return sigmoid(torch.mm(user_features, torch.t(item_features))).tolist()

def get_ranked_tracks(factorized_matrix, input_playlist_index, indexed_tids):
    ranked_tracks = []
    for track_index, prediction in enumerate(factorized_matrix[input_playlist_index]):
        ranked_tracks.append((indexed_tids[track_index], prediction))
    ranked_tracks.sort(reverse=True, key=helpers.sort_by_second_tuple)
    return ranked_tracks