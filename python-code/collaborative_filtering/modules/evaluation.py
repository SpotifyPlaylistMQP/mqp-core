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
