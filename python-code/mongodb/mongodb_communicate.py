import requests

def get(mongo_collection):
    playlist_ids = []
    playlist_dict = {}
    unique_track_dict = {}
    r = requests.get('http://localhost:8888/mongodb/playlists/' + str(mongo_collection))
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

def post(final_playlists, mongo_collection):
    chunk_size = 5
    chunk = []
    num_chunks_sent = 0
    for i in range(len(final_playlists)):
        chunk.append(final_playlists[i])
        if len(chunk) == chunk_size or i == len(final_playlists) - 1:
            num_chunks_sent += 1
            r = requests.post('http://localhost:8888/mongodb/playlists/' + str(mongo_collection), json=chunk)
            print("Chunk #" + str(num_chunks_sent) + " sent with status code:", r.status_code)
            chunk = []

def delete(mongo_collection):
    r = requests.delete('http://localhost:8888/mongodb/playlists/' + str(mongo_collection))
    if r.status_code == 200:
        print("Deleted mongo collection: " + mongo_collection)