import random

def split_playlist(input_playlist_id, playlist_dict):
    original_20_percent = []
    num_of_tracks_in_20_percent = round(len(playlist_dict[input_playlist_id]['tracks']) / 5)
    for i in range(num_of_tracks_in_20_percent):
        random_index_to_remove = random.randint(0, len(playlist_dict[input_playlist_id]['tracks']))
        original_20_percent.append(playlist_dict[input_playlist_id]['tracks'][random_index_to_remove])
        playlist_dict[input_playlist_id]['tracks'].pop(random_index_to_remove)

    return original_20_percent
