# Gets dictionary of all unique tracks and total count of occurence
unique_track_scores = {}
for playlist in all_playlists:
    for track in playlist:
        if track not in unique_track_scores:
            unique_track_scores[track] = 1
        else:
            unique_track_scores[track] = ++unique_track_scores[track]

unique_track_threshhold = 1
top_tracks = []
for key in unique_track_scores.keys():
    if key.value() > unique_track_threshhold:
        top_tracks.append(key)
    else
        continue

playlist_scores = {}
for playlist in all_playlists:
    score = 0
    for track in playlist:
        if track in top_tracks:
            ++score
    playlist_scores[playlist] = score