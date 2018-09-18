import requests
from Functions import authorization
import json

playlist_dict = {} # key = playlist_id, value = playlist
unique_track_dict = {}  # key = track_id, value = track

def make_playlist_and_track_dict(playlist_ids):
    total_tracks = 0
    for playlist_id in playlist_ids:
        spotify_playlist_response = requests.get('https://api.spotify.com/v1/playlists/{0}'.format(playlist_id),
                                                 headers=authorization.auth_header)
        playlist_dict[playlist_id] = {
            'name': json.loads(spotify_playlist_response.text)['name'],
            'playlist_id': playlist_id,
            'tracks': get_tracks_of_playlist_url('https://api.spotify.com/v1/playlists/{0}/tracks'.format(playlist_id))
        }
        total_tracks += len(playlist_dict[playlist_id]['tracks'])

    print("Total Playlists: " + str(len(playlist_dict)))
    print("Total Tracks: " + str(total_tracks))
    print("Distinct Tracks: " + str(len(unique_track_dict)))
    print("\n\n")

    return playlist_dict, unique_track_dict

def get_tracks_of_playlist_url(url):
    # Run through the playlist's tracks recursively and return a list of all of it's tracks
    tracks = []
    spotify_playlist_tracks_response = requests.get(url, headers=authorization.auth_header)
    playlist_tracks = json.loads(spotify_playlist_tracks_response.text)
    for item in playlist_tracks['items']:
        if not item['is_local']:
            track_id = item['track']['id']
            tracks.append(track_id)
            if track_id not in unique_track_dict.keys():
                unique_track_dict[track_id] = {
                    'track_id': item['track']['id'],
                    'name': item['track']['name'].encode('ascii', errors='ignore').decode(),
                    'artist': item['track']['artists'][0]['name'].encode('ascii', errors='ignore').decode(),
                    'popularity': item['track']['popularity']
                }
    if playlist_tracks['next'] is not None:
        tracks.extend(get_tracks_of_playlist_url(playlist_tracks['next']))
    return tracks

