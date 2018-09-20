import random

# Removes 20% of input_playlist_id's tracks and returns a list of those original 20%
def split(input_playlist_id, playlist_dict):
    original_20_percent = []
    num_of_tracks_in_20_percent = round(len(playlist_dict[input_playlist_id]['tracks']) / 5)
    for i in range(num_of_tracks_in_20_percent):
        random_index_to_remove = random.randint(0, len(playlist_dict[input_playlist_id]['tracks']) - 1)
        original_20_percent.append(playlist_dict[input_playlist_id]['tracks'][random_index_to_remove])
        playlist_dict[input_playlist_id]['tracks'].pop(random_index_to_remove)
    return original_20_percent

# Returns a list of of recommended tracks for playlist_id_of_interest based on most_similar_playlist_id's tracks
def recommend_tracks(playlist_dict, playlist_id_of_interest, most_similar_playlist_id, num_of_songs_to_recommend):
    recommended_tracks = []
    tracks_of_playlist_of_interest = playlist_dict[playlist_id_of_interest]
    tracks_of_most_similar_playlist = playlist_dict[most_similar_playlist_id]['tracks']
    for i in range(num_of_songs_to_recommend):
        suggested_track_id = tracks_of_most_similar_playlist[random.randint(0, len(tracks_of_most_similar_playlist) - 1)]
        if suggested_track_id not in tracks_of_playlist_of_interest and suggested_track_id not in recommended_tracks:
            recommended_tracks.append(suggested_track_id)
    return recommended_tracks
