import requests

def get(mongo_collection):
    print("Playlist Statistics:")
    indexed_pids = []
    indexed_tids = []
    playlist_dict = {}
    unique_track_dict = {}
    r = requests.get('http://localhost:8888/mongodb/playlists/' + str(mongo_collection))
    if r.status_code == 200:
        for playlist in r.json():
            indexed_pids.append(playlist['pid'])
            tracks = []
            for track in playlist['tracks']:
                tracks.append(track['tid'])
                if track['tid'] not in unique_track_dict.keys():
                    unique_track_dict[track['tid']] = track
                    indexed_tids.append(track['tid'])
            playlist['tracks'] = tracks
            playlist_dict[playlist['pid']] = playlist

    total_tracks = 0
    for playlist_id in playlist_dict.keys():
        total_tracks += len(playlist_dict[playlist_id]['tracks'])

    print("\tTotal Playlists:", len(playlist_dict))
    print("\tTotal Tracks:", total_tracks)
    print("\tDistinct Tracks:", len(unique_track_dict))

    return playlist_dict, unique_track_dict, indexed_pids, indexed_tids

def post(final_playlists, mongo_collection):
    print("posting")
    chunk_size = 3
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
    print("deleting")
    r = requests.delete('http://localhost:8888/mongodb/playlists/' + str(mongo_collection))
    print(r.status_code)
    if r.status_code == 200:
        print("Deleted mongo collection: " + mongo_collection)