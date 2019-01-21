import numpy as np
import torch
from torch.autograd import Variable
from recommender_systems.modules import helpers

default_params = {
    "mpd_square_100": {
        "alpha": 1000000,
        "latent_features": 200,
        "learning_rate": 1e-10,
        "percent_zeros": 0.5,
        "optimizer": "SGD",
        "embeddings": 0
    },
    "mpd_square_1000": {
        "alpha": 10,
        "latent_features": 5,
        "learning_rate": 1e-9,
        "percent_zeros": 0.5,
        "optimizer": "SGD",
        "embeddings": 0
    }
}


class MatrixFactorization(torch.nn.Module):
    def __init__(self, n_users, n_items, n_factors, n_embeddings):
        super().__init__()
        self.user_factors = torch.nn.Embedding(n_users, n_factors, sparse=True)
        self.item_factors = torch.nn.Embedding(n_items, n_factors, sparse=True)
        if n_embeddings != 0:
            self.user_biases = torch.nn.Embedding(n_users, n_embeddings, sparse=True)
            self.item_biases = torch.nn.Embedding(n_items, n_embeddings, sparse=True)

    def forward(self, user, item):
        try:
            pred = self.user_biases(user) + self.item_biases(item)
            pred += (self.user_factors(user) * self.item_factors(item)).sum(1)
            return (self.user_factors(user) * self.item_factors(item)).sum(1)
        except AttributeError:
            return (self.user_factors(user) * self.item_factors(item)).sum(1)

# https://www.ethanrosenthal.com/2017/06/20/matrix-factorization-in-pytorch/
def get_factorized_matrix(mongo_collection, track_playlist_matrix, params=None):
    if params is None:
        params = default_params[mongo_collection]

    # Create the embeddings and "model"
    model = MatrixFactorization(len(track_playlist_matrix[0]), len(track_playlist_matrix), params['latent_features'], params['embeddings'])
    track_playlist_matrix = np.asarray(track_playlist_matrix).T * params["alpha"]
    loss_func = torch.nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=params["learning_rate"]) if params["optimizer"] == "SGD"\
        else torch.optim.SparseAdam(model.parameters(), lr=params["learning_rate"])

    # Train data
    # indices of rows and cols for training data
    # random sample of 0s and take all 1s

    # All of the 1s
    rows, cols = track_playlist_matrix.nonzero()

    # Put half as many zeros    as 1s in the sample
    num_zeroes = round(len(rows) * params["percent_zeros"])

    # All indices of zeros
    x, y = np.where(track_playlist_matrix == 0)

    # Take random sample of zeros
    zeros = np.random.randint(low=0, high=len(x), size=num_zeroes)

    # Append random sample of 0s
    # if index out of bounds, change this order
    for i in zeros:
        np.append(rows, x[i])
        np.append(cols, y[i])

    p = np.random.permutation(len(rows))
    rows, cols = rows[p], cols[p]

    for row, col in zip(*(rows, cols)):
        # Turn data into variables
        rating = Variable(torch.FloatTensor([track_playlist_matrix[row, col]]))
        row = Variable(torch.LongTensor([np.long(row)]))
        col = Variable(torch.LongTensor([np.long(col)]))

        # Predict and calculate loss
        prediction = model(row, col)
        loss = loss_func(prediction, rating)

        # Backpropagate
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
