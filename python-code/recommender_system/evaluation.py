# Returns a list of tracks in both recommended_tracks and original_20_percent, and their R-Precision value
def r_precision(recommended_tracks, T, N):
    matches = 0
    for recommendation in recommended_tracks:
        if recommendation in T:
            matches += 1
    return matches, matches / N