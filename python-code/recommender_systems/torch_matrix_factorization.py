import numpy as np
import torch
from torch.autograd import Variable
from recommender_systems.modules import helpers
import scipy.sparse as sparse
import numpy as np
from scipy import linalg
from numpy import dot

# default_params = {
#     "mpd_square_100": {
#         "alpha": 1000000,
#         "beta": 100,
#         "steps": 50,
#         "latent_features": 200,
#         "learning_rate": 1e-10,
#         "percent_zeros": 0.5,
#         "optimizer": "SGD",
#         "embeddings": 0
#     },
#     "mpd_square_1000": {
#         "alpha": 10,
#         "latent_features": 5,
#         "learning_rate": 1e-9,
#         "percent_zeros": 0.5,
#         "optimizer": "SGD",
#         "embeddings": 0
#     }
# }

default_params = {
    "mpd_square_100": {
        "alpha": 0.01,
        "regularization": 1e-7,
        "latent_features": 30,
        "steps": 50,
        "error_limit": 0.000001,
        "fit_error_limit": 0.0001

    },
    "mpd_square_1000": {
        "alpha": 1,
        "beta": 10,
        "latent_features": 30,
        "steps": 200,
    }
}


# class MatrixFactorization(torch.Tensor):
#     def __init__(self, n_users, n_items, n_factors, n_embeddings):
#         super().__init__()
#         # self.user_factors = torch.Tensor.new_ones(n_users, n_factors)
#         self.user_factors = Variable(torch.LongTensor(n_users, n_factors))
#         print(self.user_factors)
#         self.item_factors = Variable(torch.LongTensor(n_items, n_factors))
#
#     def forward(self, user, item):
#         print("users ", self.user_factors[user])
#         return torch.mm(self.user_factors[user], torch.t(self.item_factors[item]))

# https://www.ethanrosenthal.com/2017/06/20/matrix-factorization-in-pytorch/
def get_factorized_matrix(mongo_collection, track_playlist_matrix, params=None):
    # if params is None:
    #     params = default_params[mongo_collection]
    #
    # # Create the embeddings and "model"
    # model = MatrixFactorization(len(track_playlist_matrix[0]), len(track_playlist_matrix), params['latent_features'], params['embeddings'])
    # track_playlist_matrix = np.asarray(track_playlist_matrix).T * params["alpha"]
    # # loss_func = torch.nn.MSELoss()
    # optimizer = torch.optim.SGD([model.user_factors, model.item_factors], lr=params["learning_rate"], weight_decay=params["beta"])
    #
    # # Train data
    # # indices of rows and cols for training data
    # # random sample of 0s and take all 1s
    #
    # # All of the 1s
    # rows, cols = track_playlist_matrix.nonzero()
    #
    # # Put half as many zeros    as 1s in the sample
    # num_zeroes = round(len(rows) * params["percent_zeros"])
    #
    # # All indices of zeros
    # x, y = np.where(track_playlist_matrix == 0)
    #
    # # Take random sample of zeros
    # zeros = np.random.randint(low=0, high=len(x), size=num_zeroes)
    #
    # # Append random sample of 0s
    # # if index out of bounds, change this order
    # for i in zeros:
    #     np.append(rows, x[i])
    #     np.append(cols, y[i])
    #
    # p = np.random.permutation(len(rows))
    # rows, cols = rows[p], cols[p]
    #
    # for row, col in zip(*(rows, cols)):
    #     # Turn data into variables
    #     rating = Variable(torch.FloatTensor([track_playlist_matrix[row, col]]))
    #     row = Variable(torch.LongTensor([np.long(row)]))
    #     col = Variable(torch.LongTensor([np.long(col)]))
    #
    #     # Predict and calculate loss
    #     prediction = model.forward(row, col)
    #     print("pred ", prediction)
    #     # loss = loss_func(prediction, rating)
    #     l = torch.norm(rating - prediction)
    #     print("loss before ", l)
    #     loss = Variable(l, requires_grad=True)
    #     print("loss after ", loss)
    #
    #     # Backpropagate
    #     loss.backward()
    #
    #     # Update the parameters
    #     optimizer.step()
    #
    # items = model.item_factors.numpy()
    # users = model.user_factors.numpy()
    # return np.dot(users, items.T).T.T.tolist()

    if params is None:
        params = default_params[mongo_collection]
    track_playlist_matrix = torch.Tensor(track_playlist_matrix) * params["alpha"]

    # initial matrices. U is random [0,1] and V is U\X.
    rows, columns = track_playlist_matrix.shape
    U = torch.rand(rows, params['latent_features'])
    V = torch.Tensor(linalg.lstsq(U, track_playlist_matrix)[0])

    length = params["regularization"] * ((len(U) ** 2) + (len(V) ** 2))
    ratings = torch.mm(U, V)

    for i in range(1, params['steps'] + 1):
        # Gradient Descent
        top = torch.mm(track_playlist_matrix, torch.t(V))
        bottom = (torch.mm((torch.mm(U, V)), torch.t(V))) + length
        U *= top / bottom
        U = np.maximum(U, length)

        top = torch.mm(torch.t(U), track_playlist_matrix)
        bottom = torch.mm(torch.t(U), torch.mm(U, V)) + length
        V *= top / bottom
        V = np.maximum(V, length)

        # Check if it's good enough
        if i % 5 == 0 or i == 1 or i == params['steps']:
            estimated_ratings = torch.mm(U, V)
            error = torch.sqrt(torch.sum((ratings - estimated_ratings)**2) + length)
            ratings = estimated_ratings

            cur_res = linalg.norm(track_playlist_matrix - estimated_ratings, ord='fro')

            if cur_res < params["error_limit"] or error < params["fit_error_limit"]:
                break

    return torch.t(torch.mm(U, V)).tolist()

def get_ranked_tracks(factorized_matrix, input_playlist_index, indexed_tids):
    ranked_tracks = []
    for track_index, prediction in enumerate(factorized_matrix[input_playlist_index]):
        ranked_tracks.append((indexed_tids[track_index], prediction))
    ranked_tracks.sort(reverse=True, key=helpers.sort_by_second_tuple)
    return ranked_tracks
