
import scipy.sparse as sparse
import numpy as np
import implicit
from scipy.sparse import rand as sprand
import torch
from torch.autograd import Variable
from recommender_systems.modules import helpers

params = {
    "mpd_square_100": {
        "alpha": .1,
        "latent_features": 20,
        "learning_rate": 1e-6,
    },
    "mpd_square_1000": {
    }
}


class MatrixFactorization(torch.nn.Module):

    def __init__(self, n_users, n_items, n_factors):
        super().__init__()
        self.user_factors = torch.nn.Embedding(n_users,
                                               n_factors,
                                               sparse=True)
        self.item_factors = torch.nn.Embedding(n_items,
                                               n_factors,
                                               sparse=True)

    def forward(self, user, item):
        return (self.user_factors(user) * self.item_factors(item)).sum(1)

def get_ranked_tracks(input_playlist_index, indexed_tids, indexed_pids, track_playlist_matrix, feature_matrix, mongo_collection):

    # Create the embeddings and "model"
    model = MatrixFactorization(len(indexed_pids), len(indexed_tids), params[mongo_collection]['latent_features'])

    # print(track_playlist_matrix)
    # print(type(track_playlist_matrix))

    # change to numpy array
    track_playlist_matrix = np.asarray(track_playlist_matrix).T * params[mongo_collection]["alpha"]

    # Sort our data
    rows, cols = track_playlist_matrix.nonzero()
    p = np.random.permutation(len(rows))
    rows, cols = rows[p], cols[p]

    # loss function
    loss_func = torch.nn.MSELoss()

    # optimizer
    optimizer = torch.optim.SGD(model.parameters(), lr=params[mongo_collection]["learning_rate"]) # learning rate

    for row, col in zip(*(rows, cols)):
        # Turn data into variables
        rating = Variable(torch.FloatTensor([track_playlist_matrix[row, col]]))

        row = Variable(torch.LongTensor([np.long(row)]))
        col = Variable(torch.LongTensor([np.long(col)]))

        # Predict and calculate loss
        prediction = model(row, col)

        # print(prediction)
        loss = loss_func(prediction, rating)
        # print(loss)

        # Backpropagate
        loss.backward()

        # Update the parameters
        optimizer.step()

        # print("done")
        # print(matrix)



    # input = torch.LongTensor([[0]])
    items = np.asarray(model.item_factors.weight.data)
    users = np.asarray(model.user_factors.weight.data)
    # print(items)

    factorized_matrix = np.dot(users, items.T).T.T.tolist()

    ranked_tracks = []
    for track_index, prediction in enumerate(factorized_matrix[input_playlist_index]):
        ranked_tracks.append((indexed_tids[track_index], prediction))
    ranked_tracks.sort(reverse=True, key=helpers.sort_by_second_tuple)

    return ranked_tracks




def train_run(input_playlist_index, indexed_tids, indexed_pids, track_playlist_matrix, train_params):

    # Create the embeddings and "model"
    model = MatrixFactorization(len(indexed_pids), len(indexed_tids), train_params['latent_features'])

    # change to numpy array
    track_playlist_matrix = np.asarray(track_playlist_matrix).T * train_params["alpha"]

    # Sort our data
    rows, cols = track_playlist_matrix.nonzero()
    p = np.random.permutation(len(rows))
    rows, cols = rows[p], cols[p]

    # loss function
    loss_func = torch.nn.MSELoss()

    # optimizer
    optimizer = torch.optim.SGD(model.parameters(), lr=train_params["learning_rate"])

    for row, col in zip(*(rows, cols)):
        # Turn data into variables
        rating = Variable(torch.FloatTensor([track_playlist_matrix[row, col]]))

        row = Variable(torch.LongTensor([np.long(row)]))
        col = Variable(torch.LongTensor([np.long(col)]))

        # Predict and calculate loss
        prediction = model(row, col)

        # print(prediction)
        loss = loss_func(prediction, rating)
        # print(loss)

        # Backpropagate
        loss.backward()

        # Update the parameters
        optimizer.step()

        # print("done")
        # print(matrix)



    # input = torch.LongTensor([[0]])
    items = np.asarray(model.item_factors.weight.data)
    users = np.asarray(model.user_factors.weight.data)
    # print(items)

    factorized_matrix = np.dot(users, items.T).T.T.tolist()

    ranked_tracks = []
    for track_index, prediction in enumerate(factorized_matrix[input_playlist_index]):
        ranked_tracks.append((indexed_tids[track_index], prediction))
    ranked_tracks.sort(reverse=True, key=helpers.sort_by_second_tuple)

    return ranked_tracks
