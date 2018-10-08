# Returns a list of tracks in both recommended_tracks and original_20_percent, and their R-Precision value
def r_precision(recommended_tracks, T, N, track_dict):
    matches = 0
    for recommendation in recommended_tracks:
        if recommendation in T:
            matches += 1
    return matches, matches / N

def avg_precision(r_precision_results):
    r_precision_sums = 0.0
    for result in r_precision_results:
        r_precision_sums += result[1]

    return r_precision_sums / len(r_precision_results)

def avg_data(data):
    avg_data = {
        "x": [],
        "y": []
    }
    for i in range(len(data[0])):
        sum_of_row = 0
        for cosine_ranks in data:
            sum_of_row += cosine_ranks[i]
        avg_data["y"].append(sum_of_row / len(data))
        avg_data["x"].append(i + 1)

    return avg_data