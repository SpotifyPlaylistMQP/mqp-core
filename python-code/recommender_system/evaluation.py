# Returns a list of tracks in both recommended_tracks and original_20_percent, and their R-Precision value
def r_precision(recommended_tracks, T, N, track_dict):
    matches = 0
    print("---------------------------------------------------------------")
    print("TRACKS FROM 20%")
    for tid in T:
        print(track_dict[tid]["name"])

    print("---------------------------------------------------------------")
    print("REC TRACKS BOI")
    for recommendation in recommended_tracks:
        print(track_dict[recommendation]["name"])
        if recommendation in T:
            matches += 1
    return matches, matches / N
