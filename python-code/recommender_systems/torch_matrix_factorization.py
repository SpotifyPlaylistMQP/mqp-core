
import scipy.sparse as sparse
import numpy as np
import implicit
from scipy.sparse import rand as sprand
import torch
from torch.autograd import Variable
from recommender_systems.modules import helpers
import random

params = {
    "mpd_square_100": {
        "alpha": 100000000,
        "latent_features": 15,
        "learning_rate": 1e-12
    },
    "mpd_square_1000": {
        "alpha": 10,
        "latent_features": 5,
        "learning_rate": 1e-9
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

# https://www.ethanrosenthal.com/2017/06/20/matrix-factorization-in-pytorch/
def get_ranked_tracks(input_playlist_index, indexed_tids, indexed_pids, track_playlist_matrix, feature_matrix, mongo_collection):
    # Create the embeddings and "model"
    model = MatrixFactorization(len(indexed_pids), len(indexed_tids), params[mongo_collection]['latent_features'])
    track_playlist_matrix = np.asarray(track_playlist_matrix).T * params[mongo_collection]["alpha"]
    loss_func = torch.nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=params[mongo_collection]["learning_rate"])

    # Train data
    # indices of rows and cols for training data
    # random sample of 0s and take all 1s


    # All of the 1s
    rows, cols = track_playlist_matrix.nonzero()

    # Put half as many zeros as 1s in the sample
    num_zeroes = round(len(rows)/2)

    # All indices of zeros
    x, y = np.where(track_playlist_matrix == 0)

    # Take random sample of zeros
    zeros = np.random.randint(low=0, high=len(x), size=num_zeroes)

    # Append random sample of 0s
    #if index out of bounds, change this order
    for i in zeros:
        np.append(rows, x[i])
        np.append(cols, y[i])

    # shuffle the indices to mix up 1s and 0s
    indices = np.arange(rows.shape[0])
    np.random.shuffle(indices)

    rows = rows[indices]
    cols = cols[indices]

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
