import requests
from Functions import authorization
import json

def make_playlist_dictionary(playlist_ids):
    playlist_dict = {}
    unique_track_dict = {}
    total_track_num = 0
    for playlist_id in playlist_ids:
        spotify_playlist = get_playlist(playlist_id)
        playlist_dict[playlist_id] = spotify_playlist
        for track in spotify_playlist['tracks']:
            total_track_num += 1
            if track['track_id'] not in unique_track_dict.keys():
                unique_track_dict[track['track_id']] = track

    print("Total Playlists: " + str(len(playlist_dict)))
    print("Total Tracks: " + str(total_track_num))
    print("Distinct Tracks: " + str(len(unique_track_dict)))
    print("\n\n")

    return playlist_dict, unique_track_dict

def get_playlist(playlist_id):
    # Returns a playlist built from the data of 2 different Spotify api calls
    playlist_url = 'https://api.spotify.com/v1/playlists/{0}'.format(playlist_id)
    playlist_response = requests.get(playlist_url, headers=authorization.auth_header)
    return {
        'name': json.loads(playlist_response.text)['name'],
        'playlist_id': playlist_id,
        'tracks': get_tracks_of_playlist_url('https://api.spotify.com/v1/playlists/{0}/tracks'.format(playlist_id))
    }

def get_tracks_of_playlist_url(url):
    # Run through the playlist's tracks recursively and return a list of all of it's tracks
    tracks = []
    playlist_tracks_response = requests.get(url, headers=authorization.auth_header)
    playlist_tracks = json.loads(playlist_tracks_response.text)
    for item in playlist_tracks['items']:
        if not item['is_local']:
            tracks.append({
                'track_id': item['track']['id'],
                'name': item['track']['name'].encode('ascii', errors='ignore').decode(),
                'artist': item['track']['artists'][0]['name'].encode('ascii', errors='ignore').decode(),
                'popularity': item['track']['popularity'],
                'value': item['track']['popularity']
            })
    if playlist_tracks['next'] is not None:
        tracks.extend(get_tracks_of_playlist_url(playlist_tracks['next']))
    return tracks
