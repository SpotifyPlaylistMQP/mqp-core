import requests
import random

def make_playlist_and_track_dict():
    playlist_ids = []
    playlist_dict = {}
    unique_track_dict = {}
    r = requests.get('http://localhost:8888/mongodb/playlists/mpd')
    if r.status_code == 200:
        for playlist in r.json():
            playlist_ids.append(playlist['pid'])
            tracks = []
            for track in playlist['tracks']:
                tracks.append(track['tid'])
                if track['tid'] not in unique_track_dict.keys():
                    unique_track_dict[track['tid']] = track
            playlist['tracks'] = tracks
            playlist_dict[playlist['pid']] = playlist
    return playlist_dict, unique_track_dict, playlist_ids

def find_random_playlist_id_of_interest(playlist_dict):
    all_playlist_ids = list(playlist_dict.keys())
    return all_playlist_ids[random.randint(0, len(all_playlist_ids) - 1)]