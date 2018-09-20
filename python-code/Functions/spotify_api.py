import requests
import json

def authorize():
    # Connect to the node server and return the auth token.
    #  -If there is no auth token on the server, you need to login to the spotify API through the react-app
    #  -If there is an error connecting to the node server, make sure it is running
    global auth_token, auth_header
    with open('../config/config.json') as json_file:
        config = json.load(json_file)
        port = config['node-server']['port']
    try:
        node_server_response = requests.get('http://localhost:{}/spotifyAuth/tokens'.format(port))
        try:
            auth_token = json.loads(node_server_response.text)['authToken']
            auth_header = {'Authorization': 'Bearer {0}'.format(auth_token)}
        except KeyError:
            print("There is no auth token on server, you need to login to the Spotify API through the react-app")
            exit()
    except requests.exceptions.RequestException:
        print("Error connecting to node server")
        exit()


# Returns the playlist_dict and unique_track_dict created from spotify's API
def make_playlist_and_track_dict(playlist_ids):
    playlist_dict = {}  # key = playlist_id, value = playlist
    unique_track_dict = {}  # key = track_id, value = track

    # Helper function to recursively return all of a playlist's tracks
    def get_tracks_of_playlist_url(url):
        tracks = []
        spotify_playlist_tracks_response = requests.get(url, headers=auth_header)
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

    for playlist_id in playlist_ids:
        spotify_playlist_response = requests.get('https://api.spotify.com/v1/playlists/{0}'.format(playlist_id),
                                                 headers=auth_header)
        playlist_dict[playlist_id] = {
            'name': json.loads(spotify_playlist_response.text)['name'],
            'playlist_id': playlist_id,
            'tracks': get_tracks_of_playlist_url('https://api.spotify.com/v1/playlists/{0}/tracks'.format(playlist_id))
        }

    return playlist_dict, unique_track_dict

def print_statistics(playlist_dict, unique_track_dict):
    total_tracks = 0
    for playlist_id in playlist_dict.keys():
        total_tracks += len(playlist_dict[playlist_id]['tracks'])
    print("Playlist Statistics:")
    print("\tTotal Playlists:", len(playlist_dict))
    print("\tTotal Tracks:", total_tracks)
    print("\tDistinct Tracks:", len(unique_track_dict))
    print("\n")




