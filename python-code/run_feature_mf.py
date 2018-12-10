from recommender_systems import feature_matrix_factorization
"""
start = time.time()
mongo_collection = sys.argv[1]
N = 10

playlist_dict, unique_track_dict, indexed_pids, indexed_tids = mongodb_communicate.get(mongo_collection)
track_playlist_matrix = matrix.create(playlist_dict, unique_track_dict)
print("\tSparsity: ", matrix.sparsity(track_playlist_matrix))
"""
def run(mongo_collection, playlist_dict, unique_track_dict, track_playlist_matrix, indexed_tids, indexed_pids, max_N):
    mf_params = {
        "mpd_square_100": {
            "alpha": 1e-5,
            "beta": 1,
            "latent_features": 70,
            "steps": 10,
            "number_of_runs": 10,
            "sample_size_for_avg": 100
        },
        "mpd_square_1000": {
            "alpha": 1e-06,
            "beta": 0.001,
            "latent_features": 70,
            "steps": 200,
            "number_of_runs": 5,
            "sample_size_for_avg": 100
        }
    }
    print("Params:")
    print(mf_params[mongo_collection])

    #Get features
    feature_matrix = []

    for tid in unique_track_dict.keys():
        feature_matrix.append([
            unique_track_dict[tid]["danceability"],
            unique_track_dict[tid]["energy"],
            unique_track_dict[tid]["valence"]
        ])

    # feature_matrix = np.array(feature_matrix).transpose()

    ndcg_dict, r_dict = feature_matrix_factorization.evaluate(playlist_dict, unique_track_dict, feature_matrix, max_N, track_playlist_matrix, indexed_tids, indexed_pids, mf_params[mongo_collection])

    return ndcg_dict, r_dict
