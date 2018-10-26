import numpy as np

# Returns a list of tracks in both recommended_tracks and original_20_percent, and their R-Precision value
def r_precision(recommended_tracks, T, N, track_dict):
    matches = 0
    for recommendation in recommended_tracks:
        if recommendation in T:
            matches += 1
            # print(track_dict[recommendation]['name'])
    return matches / N


def avg_precision(r_precision_results):
    r_precision_sums = 0.0
    for result in r_precision_results:
        r_precision_sums += result

    return r_precision_sums / len(r_precision_results)


def dcg_score(recommended_tracks, N):
    # N is number of tracks to recommend
    print(recommended_tracks)
    r = np.asfarray(recommended_tracks)[:N]
    print(r)
    return recommended_tracks[0] + np.sum(recommended_tracks[1:] / np.log2(np.arange(2, recommended_tracks.size + 1)))

