def print_dataset_statistics(playlist_dict, unique_track_dict):
    total_tracks = 0
    for playlist_id in playlist_dict.keys():
        total_tracks += len(playlist_dict[playlist_id]['tracks'])
    print("Playlist Statistics:")
    print("\tTotal Playlists:", len(playlist_dict))
    print("\tTotal Tracks:", total_tracks)
    print("\tDistinct Tracks:", len(unique_track_dict))
    print("\n")