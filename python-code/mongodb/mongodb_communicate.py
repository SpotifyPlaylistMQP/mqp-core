import requests
import numpy as np
import time
def get_data(mongo_collection):
    print("Getting playlist statistics")
    start = time.time()
    pids = []
    tids = []
    r = requests.get('http://localhost:8888/mongodb/playlists/' + str(mongo_collection))
    if r.status_code == 200:
        playlists = np.asarray(r.json())
        for playlist in playlists:
            pids.append(playlist['pid'])
            for track in playlist['tracks']:
                if track['tid'] not in tids:
                    tids.append(track['tid'])
        print("\t# Unique playlists:", len(pids))
        print("\t# Unique tracks:", len(tids))
        print("-Seconds elapsed:", time.time() - start)

        print("Making matrix...")
        start = time.time()
        playlist_matrix = np.zeros((len(pids), len(tids)))
        tids = np.asarray(tids)
        for row, playlist in np.ndenumerate(playlists):
            playlist_tids = []
            for track in np.asarray(playlist['tracks']):
                playlist_tids.append(track['tid'])
            for col, tid in np.ndenumerate(tids):
                if tid in playlist_tids:
                    playlist_matrix[row][col] = 1
        print("-Seconds elapsed:", time.time() - start)
        return playlist_matrix, pids, tids
    else:
        print("Failed to get database collection from server")
        exit()

def post(final_playlists, mongo_collection):
    print("posting")
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
    print("deleting")
    r = requests.delete('http://localhost:8888/mongodb/playlists/' + str(mongo_collection))
    print(r.status_code)
    if r.status_code == 200:
        print("Deleted mongo collection: " + mongo_collection)