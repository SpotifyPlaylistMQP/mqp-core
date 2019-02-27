import numpy as np
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

def ndcg_precision(recommended_tracks, T):
    def dcg_at_n(r):
        r = np.asfarray(r)
        return r[0] + np.sum(r[1:] / np.log2(np.arange(2, r.size + 1)))

    ideal = []
    for i in range(len(T)):
        ideal.append(1)

    actual = []
    for recommended_track in recommended_tracks:
        if recommended_track[0] in T:
            actual.append(1)
        else: actual.append(0)

    return dcg_at_n(actual) / dcg_at_n(ideal)



# T = [10, 9, 8, 7, 6, 11]
# rec = [12, 13, 10, 9, 8, 7, 6, 5, 4, 3, 2, 11]
# print(ndcg_precision(rec, T))