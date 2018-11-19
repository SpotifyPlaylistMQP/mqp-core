import numpy as np

# Returns a list of tracks in both recommended_tracks and original_20_percent, and their R-Precision value
def ndcg_precision(recommended_tracks, T, N, track_dict):
    matches = 0
    matches_list = []
    ideal_list = []

    for recommendation in recommended_tracks:
        ideal_list.append(recommendation[1])
        if recommendation[0] in T:

            matches_list.append(recommendation[1])

            matches += 1
        else:
            matches_list.append(0.0)
            # print(track_dict[recommendation]['name'])

    #Sort from greatest to least
    sorted_matches = np.sort(matches_list)
    reverse_matches = sorted_matches[::-1]

    sorted_ideal = np.sort(ideal_list)
    reverse_ideal = sorted_ideal[::-1]
    # print("Scores array: ", reverse_array)

    # return matches / N
    
    return dcg_at_n(reverse_matches, N, 0) / dcg_at_n(reverse_ideal, N, 0)

def r_precision(recommended_tracks, T):
    matches = 0
    for recommendation in recommended_tracks:
        if recommendation[0] in T:
            matches += 1
    return matches / len(T)

def avg_precision(r_precision_results):
    r_precision_sums = 0.0
    for result in r_precision_results:
        r_precision_sums += result

    return r_precision_sums / len(r_precision_results)



def dcg_at_n(r, n, method=0):
    """Score is discounted cumulative gain (dcg)
    Relevance is positive real values.  Can use binary
    as the previous methods.
    Example from
    http://www.stanford.edu/class/cs276/handouts/EvaluationNew-handout-6-per.pdf
    Args:
        r: Relevance scores (list or numpy) in rank order
            (first element is the first item)
        n: Number of results to consider
        method: If 0 then weights are [1.0, 1.0, 0.6309, 0.5, 0.4307, ...]
                If 1 then weights are [1.0, 0.6309, 0.5, 0.4307, ...]
    Returns:
        Discounted cumulative gain
    """
    r = np.asfarray(r)[:n]
    if r.size:
        if method == 0:
            return r[0] + np.sum(r[1:] / np.log2(np.arange(2, r.size + 1)))
        elif method == 1:
            return np.sum(r / np.log2(np.arange(2, r.size + 2)))
        else:
            raise ValueError('method must be 0 or 1.')
    return 0.


def ndcg_at_n(r, n, method=0):
    """Score is normalized discounted cumulative gain (ndcg)
    Relevance is positive real values.  Can use binary
    as the previous methods.
    Example from
    http://www.stanford.edu/class/cs276/handouts/EvaluationNew-handout-6-per.pdf
    Args:
        r: Relevance scores (list or numpy) in rank order
            (first element is the first item)
        n: Number of results to consider
        method: If 0 then weights are [1.0, 1.0, 0.6309, 0.5, 0.4307, ...]
                If 1 then weights are [1.0, 0.6309, 0.5, 0.4307, ...]
    Returns:
        Normalized discounted cumulative gain
    """
    dcg_max = dcg_at_n(sorted(r, reverse=True), n, method)
    if not dcg_max:
        return 0.

    print("DCG: ", dcg_at_n(r, n, method) / dcg_max)
    return dcg_at_n(r, n, method) / dcg_max
