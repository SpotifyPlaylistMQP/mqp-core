# Takes in a set of playlists and returns a dictionary of relevant songs based
# on predefined properties
def masterCount():
    # Creates a dictionary of TrackName:Score, where Score is the number of
    # occurences across all playlists
    unique_track_scores = {} # Dictionary of TrackName:Score
    for playlist in all_playlists:
        for track in playlist:
            if track not in unique_track_scores:
                unique_track_scores[track] = 1
            else:
                unique_track_scores[track] = ++unique_track_scores[track]

    # Takes in the unique_track_scores dictionary
    # Creates a new list of tracks that exceed a predefined threshhold
    unique_track_threshhold = 1 # Number of times a track needs to appear to be considered relevant
    top_tracks = [] # List of tracks that meet the threshhold
    for key in unique_track_scores.keys():
        if key.value() > unique_track_threshhold:
            top_tracks.append(key)
        else
            continue

    # From the set of playlists, creates a dictionary of PlaylistName:Score
    # where score based on the number of top tracks that appear in the playlist.
    playlist_scores = {} # Dictionary of PlaylistName:Score
    for playlist in all_playlists:
        score = 0
        for track in playlist:
            if track in top_tracks:
                ++score
        playlist_scores[playlist] = score

    # Returns a dictionary of PlaylistName:Score
    return playlist_scores
