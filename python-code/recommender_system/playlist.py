import random

# Removes 20% of input_playlist_id's tracks and returns a list of those original 20%
def split(input_playlist_id, playlist_dict):
    random_indexes_to_split = []
    for i in range(round(len(playlist_dict[input_playlist_id]['tracks']) / 5)):
        random_index = random.randint(0, len(playlist_dict[input_playlist_id]['tracks']) - 1)
        if random_index not in random_indexes_to_split:
            random_indexes_to_split.append(random_index)

    split_20_percent = []
    split_80_percent = []
    for i in range(len(playlist_dict[input_playlist_id]['tracks'])):
        if i in random_indexes_to_split:
            split_20_percent.append(playlist_dict[input_playlist_id]['tracks'][i])
        else:
            split_80_percent.append(playlist_dict[input_playlist_id]['tracks'][i])
    return split_20_percent, split_80_percent

def pretty_print(playlist_dict, unique_track_dict):
    total_tracks = 0
    for playlist_id in playlist_dict.keys():
        total_tracks += len(playlist_dict[playlist_id]['tracks'])
    print("Playlist Statistics:")
    print("  Total Playlists:", len(playlist_dict))
    print("  Total Tracks:", total_tracks)
    print("  Distinct Tracks:", len(unique_track_dict))