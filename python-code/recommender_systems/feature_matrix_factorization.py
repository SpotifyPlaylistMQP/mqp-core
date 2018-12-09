from recommender_systems.modules import evaluation, matrix, helpers
import scipy.sparse as sparse
import numpy as np
import time
from scipy.sparse.linalg import spsolve

import pandas as pd

import collections
import os

import numpy as np
from sklearn.metrics import roc_auc_score
import torch
import torch.autograd
from torch.autograd import Variable
from torch import nn
import torch.multiprocessing as mp
import torch.utils.data as data
from tqdm import tqdm

import metric

def train(playlist_dict, unique_track_dict, feature_matrix, N, track_playlist_matrix, indexed_tids, indexed_pids, params):
    filename = str(len(playlist_dict.keys())) + "feature_mf_training" + time.strftime("_%m-%d-%Y__%Hh%Mm") + ".txt"
    output = open(filename, "a")
    output.write("Alpha, Beta, c, Latent Features, Steps, NDCG, R-Precision\n")
    runs_for_avg = 5
    input_playlist_index = 0

    T, new_playlist_tracks = matrix.split_playlist_not_random(indexed_pids[input_playlist_index], playlist_dict)
    matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks, track_playlist_matrix,
                                        unique_track_dict)

    for alpha in params["alpha_set"]:
        for beta in params["beta_set"]:
            for latent_features in params["latent_features_set"]:
                for steps in params["steps_set"]:
                    for c in params["c_set"]:
                        c_feature_matrix = (np.array(feature_matrix) * c).tolist()
                        sum_ndcg = 0
                        sum_r = 0
                        for run in range(runs_for_avg):
                            factorized_matrix = matrix_factorization(track_playlist_matrix, alpha, beta, latent_features, steps, c_feature_matrix)

                            prediction_tuples = []
                            for track_index, prediction in enumerate(factorized_matrix[input_playlist_index]):
                                prediction_tuples.append((indexed_tids[track_index], prediction))
                            prediction_tuples.sort(reverse=True, key=helpers.sort_by_second_tuple)

                            recommended_tracks = helpers.recommend_n_tracks(N, prediction_tuples, new_playlist_tracks)

                            sum_ndcg += evaluation.ndcg_precision(recommended_tracks, T, N, unique_track_dict)
                            sum_r += evaluation.r_precision(recommended_tracks, T)
                        print("Alpha:{}, Beta:{}, C:{}, Latent_Features:{}, steps:{},  NDCG:{}, R:{}".format(alpha, beta, c, latent_features, steps, sum_ndcg / runs_for_avg, sum_r / runs_for_avg))
                        output.write("{}, {}, {}, {}, {}, {}, {}\n".format(alpha, beta, c, latent_features, steps, sum_ndcg / runs_for_avg, sum_r / runs_for_avg))
    print("Wrote results to " + filename)

def run(playlist_dict, unique_track_dict, feature_matrix, N, track_playlist_matrix, indexed_tids, indexed_pids, params):
    print("Feature matrix factorization...")
    start = time.time()

    sum_iteration_ndcg = 0
    sum_iteration_r = 0
    for test_iteration in range(params['number_of_runs']):
        print("Run #", test_iteration)
        sum_ndcg = 0
        sum_r = 0
        for input_playlist_index in helpers.get_random_input_playlist_indexes(params['sample_size_for_avg'], len(indexed_pids)):
            T, new_playlist_tracks = matrix.split_playlist(indexed_pids[input_playlist_index], playlist_dict)
            matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks, track_playlist_matrix, unique_track_dict)

            factorized_matrix = matrix_factorization(track_playlist_matrix, params['alpha'], params['beta'], params['latent_features'], params['steps'], feature_matrix)

            prediction_tuples = []
            for track_index, prediction in enumerate(factorized_matrix[input_playlist_index]):
                prediction_tuples.append((indexed_tids[track_index], prediction))
            prediction_tuples.sort(reverse=True, key=helpers.sort_by_second_tuple)

            recommended_tracks = helpers.recommend_n_tracks(N, prediction_tuples, new_playlist_tracks)
            matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks + T, track_playlist_matrix, unique_track_dict)
            sum_ndcg += evaluation.ndcg_precision(recommended_tracks, T, N, unique_track_dict)
            sum_r += evaluation.r_precision(recommended_tracks, T)
        sum_iteration_ndcg += sum_ndcg / params['sample_size_for_avg']
        sum_iteration_r += sum_r / params['sample_size_for_avg']

    print("Final Avg NDCG: {}      R: {}".format(sum_iteration_ndcg / params['number_of_runs'], sum_iteration_r / params['number_of_runs']))
    final = round(((time.time()) - start),2)
    print("Total time elapsed: " + str(final) + " seconds")
    # timing.save_time(final, "Matrix_Factorization")

    return sum_iteration_ndcg / params['number_of_runs'], sum_iteration_r / params['number_of_runs']

def evaluate(playlist_dict, unique_track_dict, feature_matrix, max_N, track_playlist_matrix, indexed_tids, indexed_pids, params):
    print("Feature matrix factorization...")

    ndcg_N_dict = {}
    r_N_dict = {}
    for N in range(1, max_N + 1):
        ndcg_N_dict[N] = 0
        r_N_dict[N] = 0

    for run in range(params['number_of_runs']):
        print("Run #", run)
        for input_playlist_index in helpers.get_random_input_playlist_indexes(params['sample_size_for_avg'], len(indexed_pids)):
            T, new_playlist_tracks = matrix.split_playlist(indexed_pids[input_playlist_index], playlist_dict)
            matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks, track_playlist_matrix, unique_track_dict)

            make_df(track_playlist_matrix)
            c_feature_matrix = (np.array(feature_matrix) * params["c"]).tolist()
            factorized_matrix = matrix_factorization(track_playlist_matrix, params['alpha'], params['beta'], params['latent_features'], params['steps'], c_feature_matrix)

            prediction_tuples = []
            for track_index, prediction in enumerate(factorized_matrix[input_playlist_index]):
                prediction_tuples.append((indexed_tids[track_index], prediction))
            prediction_tuples.sort(reverse=True, key=helpers.sort_by_second_tuple)

            for N in range(1, max_N + 1):
                recommended_tracks = helpers.recommend_n_tracks(N, prediction_tuples, new_playlist_tracks)
                ndcg_N_dict[N] += evaluation.ndcg_precision(recommended_tracks, T, N, unique_track_dict)
                r_N_dict[N] += evaluation.r_precision(recommended_tracks, T)

            matrix.update_input_playlist_tracks(input_playlist_index, new_playlist_tracks + T, track_playlist_matrix, unique_track_dict)

    for N in range(1, max_N + 1):
        ndcg_N_dict[N] = ndcg_N_dict[N] / (params['number_of_runs'] * params['sample_size_for_avg'])
        r_N_dict[N] = r_N_dict[N] / (params['number_of_runs'] * params['sample_size_for_avg'])
    print("\tAvg NDCG:", ndcg_N_dict)
    print("\tAvg R-Precision:", r_N_dict)

    return ndcg_N_dict, r_N_dict

def make_df(matrixx):
    df = pd.DataFrame(matrixx)
    print(df)

# https://jessesw.com/Rec-System/
def matrix_factorization(track_playlist_matrix, alpha, beta, latent_features, iterations, feature_matrix, seed=0):
    interactions = make_df(track_playlist_matrix)
    interactions = (interactions >= 4).astype(np.float32)
    train, test = train_test_split(interactions)
    train = sp.coo_matrix(train)
    test = sp.coo_matrix(test)
    return train, test

    pipeline = BasePipeline(train, test=test, verbose=True,
                            batch_size=1024, num_workers=4,
                            n_factors=20, weight_decay=0,
                            dropout_p=0., lr=.2, sparse=True,
                            optimizer=torch.optim.SGD, n_epochs=40,
                            random_seed=2017, loss_function=bpr_loss,
                            model=BPRModule,
                            interaction_class=PairwiseInteractions,
                            eval_metrics=('auc', 'patk'))
    pipeline.fit()

def train_test_split(interactions, n=10):
    """
    Split an interactions matrix into training and test sets.
    Parameters
    ----------
    interactions : np.ndarray
    n : int (default=10)
        Number of items to select / row to place into test.
    Returns
    -------
    train : np.ndarray
    test : np.ndarray
    """
    test = np.zeros(interactions.shape)
    train = interactions.copy()
    for user in range(interactions.shape[0]):
        if interactions[user, :].nonzero()[0].shape[0] > n:
            test_interactions = np.random.choice(interactions[user, :].nonzero()[0],
                                                 size=n,
                                                 replace=False)
            train[user, test_interactions] = 0.
            test[user, test_interactions] = interactions[user, test_interactions]

    # Test and training are truly disjoint
    assert(np.all((train * test) == 0))
    return train, test

class Interactions(data.Dataset):
    """
    Hold data in the form of an interactions matrix.
    Typical use-case is like a ratings matrix:
    - Users are the rows
    - Items are the columns
    - Elements of the matrix are the ratings given by a user for an item.
    """

    def __init__(self, mat):
        self.mat = mat.astype(np.float32).tocoo()
        self.n_users = self.mat.shape[0]
        self.n_items = self.mat.shape[1]

    def __getitem__(self, index):
        row = self.mat.row[index]
        col = self.mat.col[index]
        val = self.mat.data[index]
        return (row, col), val

    def __len__(self):
        return self.mat.nnz


class PairwiseInteractions(data.Dataset):
    """
    Sample data from an interactions matrix in a pairwise fashion. The row is
    treated as the main dimension, and the columns are sampled pairwise.
    """

    def __init__(self, mat):
        self.mat = mat.astype(np.float32).tocoo()

        self.n_users = self.mat.shape[0]
        self.n_items = self.mat.shape[1]

        self.mat_csr = self.mat.tocsr()
        if not self.mat_csr.has_sorted_indices:
            self.mat_csr.sort_indices()

    def __getitem__(self, index):
        row = self.mat.row[index]
        found = False

        while not found:
            neg_col = np.random.randint(self.n_items)
            if self.not_rated(row, neg_col, self.mat_csr.indptr,
                              self.mat_csr.indices):
                found = True

        pos_col = self.mat.col[index]
        val = self.mat.data[index]

        return (row, (pos_col, neg_col)), val

    def __len__(self):
        return self.mat.nnz

    @staticmethod
    def not_rated(row, col, indptr, indices):
        # similar to use of bsearch in lightfm
        start = indptr[row]
        end = indptr[row + 1]
        searched = np.searchsorted(indices[start:end], col, 'right')
        if searched >= (end - start):
            # After the array
            return False
        return col != indices[searched]  # Not found

    def get_row_indices(self, row):
        start = self.mat_csr.indptr[row]
        end = self.mat_csr.indptr[row + 1]
        return self.mat_csr.indices[start:end]


class BaseModule(nn.Module):
    """
    Base module for explicit matrix factorization.
    """

    def __init__(self,
                 n_users,
                 n_items,
                 n_factors=40,
                 dropout_p=0,
                 sparse=False):
        """
        Parameters
        ----------
        n_users : int
            Number of users
        n_items : int
            Number of items
        n_factors : int
            Number of latent factors (or embeddings or whatever you want to
            call it).
        dropout_p : float
            p in nn.Dropout module. Probability of dropout.
        sparse : bool
            Whether or not to treat embeddings as sparse. NOTE: cannot use
            weight decay on the optimizer if sparse=True. Also, can only use
            Adagrad.
        """
        super(BaseModule, self).__init__()
        self.n_users = n_users
        self.n_items = n_items
        self.n_factors = n_factors
        self.user_biases = nn.Embedding(n_users, 1, sparse=sparse)
        self.item_biases = nn.Embedding(n_items, 1, sparse=sparse)
        self.user_embeddings = nn.Embedding(n_users, n_factors, sparse=sparse)
        self.item_embeddings = nn.Embedding(n_items, n_factors, sparse=sparse)

        self.dropout_p = dropout_p
        self.dropout = nn.Dropout(p=self.dropout_p)

        self.sparse = sparse

    def forward(self, users, items):
        """
        Forward pass through the model. For a single user and item, this
        looks like:
        user_bias + item_bias + user_embeddings.dot(item_embeddings)
        Parameters
        ----------
        users : np.ndarray
            Array of user indices
        items : np.ndarray
            Array of item indices
        Returns
        -------
        preds : np.ndarray
            Predicted ratings.
        """
        ues = self.user_embeddings(users)
        uis = self.item_embeddings(items)

        preds = self.user_biases(users)
        preds += self.item_biases(items)
        preds += (self.dropout(ues) * self.dropout(uis)).sum(1)

        return preds

    def __call__(self, *args):
        return self.forward(*args)

    def predict(self, users, items):
        return self.forward(users, items)


def bpr_loss(preds, vals):
    sig = nn.Sigmoid()
    return (1.0 - sig(preds)).pow(2).sum()


class BPRModule(nn.Module):

    def __init__(self,
                 n_users,
                 n_items,
                 n_factors=40,
                 dropout_p=0,
                 sparse=False,
                 model=BaseModule):
        super(BPRModule, self).__init__()

        self.n_users = n_users
        self.n_items = n_items
        self.n_factors = n_factors
        self.dropout_p = dropout_p
        self.sparse = sparse
        self.pred_model = model(
            self.n_users,
            self.n_items,
            n_factors=n_factors,
            dropout_p=dropout_p,
            sparse=sparse
        )

    def forward(self, users, items):
        assert isinstance(items, tuple), \
            'Must pass in items as (pos_items, neg_items)'
        # Unpack
        (pos_items, neg_items) = items
        pos_preds = self.pred_model(users, pos_items)
        neg_preds = self.pred_model(users, neg_items)
        return pos_preds - neg_preds

    def predict(self, users, items):
        return self.pred_model(users, items)


class BasePipeline:
    """
    Class defining a training pipeline. Instantiates data loaders, model,
    and optimizer. Handles training for multiple epochs and keeping track of
    train and test loss.
    """

    def __init__(self,
                 train,
                 test=None,
                 model=BaseModule,
                 n_factors=40,
                 batch_size=32,
                 dropout_p=0.02,
                 sparse=False,
                 lr=0.01,
                 weight_decay=0.,
                 optimizer=torch.optim.Adam,
                 loss_function=nn.MSELoss(size_average=False),
                 n_epochs=10,
                 verbose=False,
                 random_seed=None,
                 interaction_class=Interactions,
                 hogwild=False,
                 num_workers=0,
                 eval_metrics=None,
                 k=5):
        self.train = train
        self.test = test

        if hogwild:
            num_loader_workers = 0
        else:
            num_loader_workers = num_workers
        self.train_loader = data.DataLoader(
            interaction_class(train), batch_size=batch_size, shuffle=True,
            num_workers=num_loader_workers)
        if self.test is not None:
            self.test_loader = data.DataLoader(
                interaction_class(test), batch_size=batch_size, shuffle=True,
                num_workers=num_loader_workers)
        self.num_workers = num_workers
        self.n_users = self.train.shape[0]
        self.n_items = self.train.shape[1]
        self.n_factors = n_factors
        self.batch_size = batch_size
        self.dropout_p = dropout_p
        self.lr = lr
        self.weight_decay = weight_decay
        self.loss_function = loss_function
        self.n_epochs = n_epochs
        if sparse:
            assert weight_decay == 0.0
        self.model = model(self.n_users,
                           self.n_items,
                           n_factors=self.n_factors,
                           dropout_p=self.dropout_p,
                           sparse=sparse)
        self.optimizer = optimizer(self.model.parameters(),
                                   lr=self.lr,
                                   weight_decay=self.weight_decay)
        self.warm_start = False
        self.losses = collections.defaultdict(list)
        self.verbose = verbose
        self.hogwild = hogwild
        if random_seed is not None:
            if self.hogwild:
                random_seed += os.getpid()
            torch.manual_seed(random_seed)
            np.random.seed(random_seed)

        if eval_metrics is None:
            eval_metrics = []
        self.eval_metrics = eval_metrics
        self.k = k

    def break_grads(self):
        for param in self.model.parameters():
            # Break gradient sharing
            if param.grad is not None:
                param.grad.data = param.grad.data.clone()

    def fit(self):
        for epoch in range(1, self.n_epochs + 1):

            if self.hogwild:
                self.model.share_memory()
                processes = []
                train_losses = []
                queue = mp.Queue()
                for rank in range(self.num_workers):
                    p = mp.Process(target=self._fit_epoch,
                                   kwargs={'epoch': epoch,
                                           'queue': queue})
                    p.start()
                    processes.append(p)
                for p in processes:
                    p.join()

                while True:
                    is_alive = False
                    for p in processes:
                        if p.is_alive():
                            is_alive = True
                            break
                    if not is_alive and queue.empty():
                        break

                    while not queue.empty():
                        train_losses.append(queue.get())
                queue.close()
                train_loss = np.mean(train_losses)
            else:
                train_loss = self._fit_epoch(epoch)

            self.losses['train'].append(train_loss)
            row = 'Epoch: {0:^3}  train: {1:^10.5f}'.format(epoch, self.losses['train'][-1])
            if self.test is not None:
                self.losses['test'].append(self._validation_loss())
                row += 'val: {0:^10.5f}'.format(self.losses['test'][-1])
                for metric in self.eval_metrics:
                    func = getattr(metrics, metric)
                    res = func(self.model, self.test_loader.dataset.mat_csr,
                               num_workers=self.num_workers)
                    self.losses['eval-{}'.format(metric)].append(res)
                    row += 'eval-{0}: {1:^10.5f}'.format(metric, res)
            self.losses['epoch'].append(epoch)
            if self.verbose:
                print(row)

    def _fit_epoch(self, epoch=1, queue=None):
        if self.hogwild:
            self.break_grads()

        self.model.train()
        total_loss = torch.Tensor([0])
        pbar = tqdm(enumerate(self.train_loader),
                    total=len(self.train_loader),
                    desc='({0:^3})'.format(epoch))
        for batch_idx, ((row, col), val) in pbar:
            self.optimizer.zero_grad()

            row = Variable(row.long())
            # TODO: turn this into a collate_fn like the data_loader
            if isinstance(col, list):
                col = tuple(Variable(c.long()) for c in col)
            else:
                col = Variable(col.long())
            val = Variable(val).float()

            preds = self.model(row, col)
            loss = self.loss_function(preds, val)
            loss.backward()

            self.optimizer.step()

            total_loss += loss.data[0]
            batch_loss = loss.data[0] / row.size()[0]
            pbar.set_postfix(train_loss=batch_loss)
        total_loss /= self.train.nnz
        if queue is not None:
            queue.put(total_loss[0])
        else:
            return total_loss[0]

    def _validation_loss(self):
        self.model.eval()
        total_loss = torch.Tensor([0])
        for batch_idx, ((row, col), val) in enumerate(self.test_loader):
            row = Variable(row.long())
            if isinstance(col, list):
                col = tuple(Variable(c.long()) for c in col)
            else:
                col = Variable(col.long())
            val = Variable(val).float()

            preds = self.model(row, col)
            loss = self.loss_function(preds, val)
            total_loss += loss.data[0]

        total_loss /= self.test.nnz
        return total_loss[0]