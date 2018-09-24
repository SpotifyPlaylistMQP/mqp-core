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
             all_playlists[playlist["pid"]] = playlist["tracks"]

    masterCount(all_playlists)


def masterCount(all_playlists):
    # Gets dictionary of all unique tracks and total count of occurence
    unique_track_scores = {}
    for playlist_id in all_playlists.keys():
        for track in all_playlists[playlist_id]:
            if track['track_uri'] not in unique_track_scores:
                unique_track_scores[track['track_uri']] = 1
            else:

                unique_track_scores[track['track_uri']] += 1

    unique_track_threshhold = 1

    top_tracks = []
    for key in unique_track_scores.keys():
        if unique_track_scores[key] > unique_track_threshhold:
            top_tracks.append(key)

    playlist_scores = {}
    for playlist_id in all_playlists.keys():
        score = 0
        for track in all_playlists[playlist_id]:
            if track in top_tracks:
                score = score + 1
        playlist_scores[playlist_id] = score

    to_final_json(playlist_scores, all_playlists)


def to_final_json(playlist_scores, all_playlists) {
    final_json = {}
    for pid in playlist_scores.keys():
        #test string to see how it looks
        final_json[pid] = all_playlists["tracks"]["name"]
        #janky string to return
        #final_json = {"pid": pid, "tracks":[{"name": all_playlists[pid]["tracks"]["name"], "artist": all_playlists[pid]["tracks"]["artist"], "tid": all_playlists[pid]["tracks"]["track_uri"]}]}

print(final_json)


#test running it
json_reader()
