# Returns a list of tracks in both recommended_tracks and original_20_percent, and their R-Precision value
def r_precision(recommended_tracks, original_20_percent):
    matches = []
    for recommendation in recommended_tracks:
        if recommendation in original_20_percent:
            matches.append(recommendation)
    return matches, len(matches) / len(original_20_percent)

# Pretty prints the matching_tracks list
def pretty_print(matching_tracks, unique_track_dict, r_precision):
    print("Matching Tracks:")
    if len(matching_tracks) == 0:
        print("\tThere are no matching tracks")
    else:
        for track_id in matching_tracks:
            print("\t", unique_track_dict[track_id]['name'], "by", unique_track_dict[track_id]['artist'])
    print("R-Precision:\n\t", r_precision)
    print("\n")