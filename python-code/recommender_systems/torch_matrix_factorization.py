import numpy as np
import torch
from torch.autograd import Variable
from recommender_systems.modules import helpers

default_params = {
    "mpd_square_100": {
        "alpha": 1e4,
        "latent_features": 150,
        "learning_rate": 1e-8,
        "percent_zeros": 2,
    },
    "mpd_square_1000": {
        "alpha": 10,
        "latent_features": 5,
        "learning_rate": 1e-9,
        "percent_zeros": 0.5,
    }
}


class MatrixFactorization(torch.nn.Module):
    def __init__(self, n_users, n_items, n_factors):
        super().__init__()
        self.user_factors = torch.nn.Embedding(n_users, n_factors)
        self.item_factors = torch.nn.Embedding(n_items, n_factors)

    def forward(self, user, item):
        # Dot product of two feature vectors
        return (self.user_factors(user) * self.item_factors(item)).sum(1)

# https://www.ethanrosenthal.com/2017/06/20/matrix-factorization-in-pytorch/
def get_factorized_matrix(mongo_collection, track_playlist_matrix, params=None):
    if params is None:
        params = default_params[mongo_collection]

    # Create the embeddings and "model"
    model = MatrixFactorization(len(track_playlist_matrix[0]), len(track_playlist_matrix), params['latent_features'])
    track_playlist_matrix = np.asarray(track_playlist_matrix).T * params["alpha"]
    loss_func = torch.nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=params["learning_rate"])

    # All of the 1s
    rows, cols = track_playlist_matrix.nonzero()

    # Add a random sample of zeroes
    x, y = np.where(track_playlist_matrix == 0)
    zeros = np.random.randint(low=0, high=len(x), size=round(len(rows) * params["percent_zeros"]))
    for i in zeros:
        np.append(rows, x[i])
        np.append(cols, y[i])

    # Shuffle the list of 1s and 0s
    p = np.random.permutation(len(rows))
    rows, cols = rows[p], cols[p]

    for row, col in zip(*(rows, cols)):
        # Turn data into variables
        rating = Variable(torch.FloatTensor([track_playlist_matrix[row, col]]))
        row = Variable(torch.LongTensor([np.long(row)]))
        col = Variable(torch.LongTensor([np.long(col)]))

        # Predict and calculate loss
        prediction = model.forward(row, col)
        loss = loss_func(prediction, rating)
        loss.backward()

        # Update the parameters
        optimizer.step()

    items = np.asarray(model.item_factors.weight.data)
    users = np.asarray(model.user_factors.weight.data)
    return np.dot(users, items.T).T.T.tolist()

def get_ranked_tracks(factorized_matrix, input_playlist_index, indexed_tids):
    ranked_tracks = []
    for track_index, prediction in enumerate(factorized_matrix[input_playlist_index]):
        ranked_tracks.append((indexed_tids[track_index], prediction))
    ranked_tracks.sort(reverse=True, key=helpers.sort_by_second_tuple)
    return ranked_tracks
