import json
from glob import glob
import os.path


def json_reader():
    all_playlists = {}
    #Open 10 json files, loop and add each playlist to a dictionary
    path_to_json = "C:/Users/s7sal/Documents/MQP/mqp-core/python-code/mongodb/JSONs/"

    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

    for file in json_files:
        file_path = path_to_json + file
        with open(file_path) as f:
            data = json.load(f)["playlists"]
        for playlist in data:
            tracks = []
            for track in playlist["tracks"]:
                tracks.append({
                    "tid": track["track_uri"].replace('spotify:track:', ''),
                    "name": track["track_name"],
                    "artist": track["artist_name"]
                })
            all_playlists[playlist["pid"]] = {
                "pid": playlist["pid"],
                "name": playlist["name"],
                "tracks": tracks
            }

    masterCount(all_playlists)


def masterCount(all_playlists):
    # Gets dictionary of all unique tracks and total count of ocurrence
    unique_track_scores = {}
    for playlist_id in all_playlists.keys():
        for track in all_playlists[playlist_id]["tracks"]:
            if track["tid"] not in unique_track_scores:
                unique_track_scores[track['tid']] = 1
            else:
                unique_track_scores[track['tid']] += 1


    unique_track_threshold = 25

    top_tracks = []
    for tid in unique_track_scores.keys():
        if unique_track_scores[tid] > unique_track_threshold:
            #print(unique_track_scores[tid])
            top_tracks.append(tid)
    print("Length of top tracks: ", len(top_tracks))

    playlist_scores = {}
    for playlist_id in all_playlists.keys():
        score = 0
        for track in all_playlists[playlist_id]["tracks"]:
            if track["tid"] in top_tracks:
                score = score + 1
        playlist_scores[playlist_id] = score


    get_final_playlists(playlist_scores, all_playlists)

playlist_threshold = 100
def get_final_playlists(playlist_scores, all_playlists):
    final_playlists = []
    for pid in playlist_scores.keys():
        if playlist_scores[pid] > playlist_threshold:
            print(playlist_scores[pid])
            final_playlists.append(all_playlists[pid])

    print("Number of playlists above threshold:", len(final_playlists))
    return final_playlists




#test running it
json_reader()
