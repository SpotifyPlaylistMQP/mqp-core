# Gets dictionary of all unique tracks and total count of occurence
uniqueTrackScores = {}
for playlist in all_playlists:
    for track in playlist:
        if track not in playlist_scores:
            uniqueTrackScores[track] = 1;
        else
            uniqueTrackScores[track] = ++uniqueTrackScores[track];

unique_track_threshhold = 1;
top_tracks = []
for key in uniqueTrackScores.keys():
    if key.value() > unique_track_threshhold:
        top_tracks.append(key);
    else
        continue;

playlist_scores = {}
for playlist in all_playlists:
    score = 0;
    for track in playlist:
        if track in top_tracks:
            ++score;
    playlist_scores[playlist] = score;
