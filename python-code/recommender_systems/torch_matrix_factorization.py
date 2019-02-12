import torch
from recommender_systems.modules import helpers
from scipy import linalg

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
    if params is None:
        params = default_params[mongo_collection]
    track_playlist_matrix = torch.Tensor(track_playlist_matrix) * params["alpha"]

    # initial matrices. item_features is random [0,1] and user_features is item_features\X.
    items, users = track_playlist_matrix.shape
    item_features = torch.rand(items, params['latent_features'])
    user_features = torch.rand(users, params['latent_features'])

    # Alternating Least Squares
    for i in range(1, params['steps'] + 1):
        # Fix item features
        error = track_playlist_matrix - torch.mm(item_features, torch.t(user_features))
        for item in range(items):
            gradient = torch.mm(torch.unsqueeze(error[item], 0), user_features) - params["regularization"] * item_features[item]
            item_features[item] = item_features[item] + params["learning_rate"] * gradient

        # Fix user features
        error = torch.t(track_playlist_matrix - torch.mm(item_features, torch.t(user_features)))
        for user in range(users):
            gradient = torch.mm(torch.unsqueeze(error[user], 0), item_features) - params["regularization"] * user_features[user]
            user_features[user] = user_features[user] + params["learning_rate"] * gradient

    print(torch.t(torch.mm(item_features, torch.t(user_features))).tolist())
    return torch.t(torch.mm(item_features, torch.t(user_features))).tolist()

def get_ranked_tracks(factorized_matrix, input_playlist_index, indexed_tids):
    ranked_tracks = []
    for track_index, prediction in enumerate(factorized_matrix[input_playlist_index]):
        ranked_tracks.append((indexed_tids[track_index], prediction))
    ranked_tracks.sort(reverse=True, key=helpers.sort_by_second_tuple)
    return ranked_tracks


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