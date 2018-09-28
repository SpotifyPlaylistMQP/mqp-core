import json
import os.path
import requests

def json_reader():
    all_playlists = {}
    #Open 10 json files, loop and add each playlist to a dictionary
    path_to_json = "./dataset_creator/mpd_json/"

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
                    "name": track["track_name"].encode('ascii', errors='ignore').decode(),
                    "artist": track["artist_name"]
                })
            all_playlists[playlist["pid"]] = {
                "pid": str(playlist["pid"]),
                "name": playlist["name"].encode('ascii', errors='ignore').decode(),
                "tracks": tracks
            }
    print("Number of playlists:", len(all_playlists.keys()))
    return all_playlists

def master_count(all_playlists, track_relevancy_threshold, min_playlist_len):
    # Gets dictionary of all unique tracks and total count of ocurrence
    unique_track_scores = {}
    for playlist_id in all_playlists.keys():
        for track in all_playlists[playlist_id]["tracks"]:
            if track["tid"] not in unique_track_scores:
                unique_track_scores[track['tid']] = 1
            else:
                unique_track_scores[track['tid']] += 1
    print("Number of unique tracks:", len(unique_track_scores.keys()))

    top_tracks = []
    for tid in unique_track_scores.keys():
        if unique_track_scores[tid] > track_relevancy_threshold:
            top_tracks.append(tid)
    print("Number of relevant tracks:", len(top_tracks))

    playlist_scores = {}
    avg_relevancy = 0
    for playlist_id in all_playlists.keys():
        if len(all_playlists[playlist_id]["tracks"]) > min_playlist_len:
            score = 0
            for track in all_playlists[playlist_id]["tracks"]:
                if track["tid"] in top_tracks:
                    score = score + 1
            playlist_scores[playlist_id] = score
            avg_relevancy += score
    return playlist_scores, all_playlists

def get_final_playlists(playlist_scores, all_playlists, playlist_relevancy_threshold):
    final_playlists = []
    for pid in playlist_scores.keys():
        if playlist_scores[pid] / len(all_playlists[pid]['tracks']) > playlist_relevancy_threshold:
            final_playlists.append(all_playlists[pid])
    print("Number of relevant playlists:", len(final_playlists))
    return final_playlists

def send_to_server(final_playlists, track_relevancy_threshold, playlist_relevancy_threshold):
    chunk_size = 5
    chunk = []
    num_chunks_sent = 0
    for i in range(len(final_playlists)):
        chunk.append(final_playlists[i])
        if len(chunk) == chunk_size or i == len(final_playlists) - 1:
            num_chunks_sent += 1
            r = requests.post('http://localhost:8888/mongodb/playlists/mpd_' + str(track_relevancy_threshold) + "_" + str(playlist_relevancy_threshold), json=chunk)
            print("Chunk #" + str(num_chunks_sent) + " sent with status code:", r.status_code)
            chunk = []