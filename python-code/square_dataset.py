from dataset_creator import master_count
from mongodb import mongodb_communicate
import sys, time, requests

start = time.time()

# How to run program
#   py square_dataset.py {square_size}
square_size = int(float(sys.argv[1]))


def sort_by_second_tuple(input):
    return input[1]


# Load the databases from all the JSON files
all_playlists = master_count.json_reader("mpd_json") # Key = pid, Value = playlist object

# Count how many times each track appears
print("Counting tracks_and_appearances...")
tracks_and_appearances = {} # Key = tid     Value = number of appearances
for pid in all_playlists.keys():
    for track in all_playlists[pid]['tracks']:
        if track['tid'] not in tracks_and_appearances.keys():
            tracks_and_appearances[track['tid']] = 1
        else:
            tracks_and_appearances[track['tid']] += 1

# Make a list of tracks that is sorted by how many times they appear
print("Turning tracks_and_appearances into a sorted tuple list...")
sortable_track_list = [] # List of tuples where [0] = tid, [1] = number of appearances
for tid in tracks_and_appearances.keys():
    sortable_track_list.append((tid, tracks_and_appearances[tid]))
sortable_track_list.sort(reverse=True, key=sort_by_second_tuple)
print("\tMax number of appearances:", sortable_track_list[0][1])
print("\tMin number of appearances:", sortable_track_list[-1:][0][1])

# Get the tracks of interest for the square
print("Making tracks_and_appearances back into a dictionary...")
tracks_of_interest = {} # Key = tid     Value = number of appearances
for tid_and_appearances_tuple in sortable_track_list[:square_size]:
    tracks_of_interest[tid_and_appearances_tuple[0]] = tid_and_appearances_tuple[1]
tids_of_interest = tracks_of_interest.keys()

# Remove all tracks that are not in tracks_of_interest from every playlist,
#  and calculate each playlists score based on how many tracks_of_interest they have
print("Making playlists_and_scores...")
playlists_and_scores = [] # List of tuples where [0] = pid, [1] = score
for pid in all_playlists.keys():
    score = 0
    tracks_to_keep = [] # List of track objects
    for track in all_playlists[pid]['tracks']:
        if track['tid'] in tids_of_interest:
            tracks_to_keep.append(track)
            score += tracks_of_interest[track['tid']]
    playlists_and_scores.append((pid, score))
    all_playlists[pid]['tracks'] = tracks_to_keep
playlists_and_scores.sort(reverse=True, key=sort_by_second_tuple)
print("\tMax playlist score:", playlists_and_scores[0][1])
print("\tMin playlist score:", playlists_and_scores[-1:][0][1])

# Get the final playlists for the square
print("Finding the final playlists...")
final_playlists = []
for playlist_and_score in playlists_and_scores[:square_size]:
    final_playlists.append(all_playlists[playlist_and_score[0]])

# Fetch audio-features to each track
print("Fetching audio-features for each track of interest...")
audio_features = {}
tid_chunk = []
for tid_index, tid in enumerate(tids_of_interest):
    tid_chunk.append(tid)
    if len(tid_chunk) == 100 or tid_index + 1 == len(tids_of_interest):
        r = requests.get('http://localhost:8888/spotify/audio-features?tids=' + ','.join(map(str, tid_chunk)))
        if r.status_code == 200:
           for track_features in r.json()['audio_features']:
               audio_features[track_features['id']] = {
                   'danceability': track_features['danceability'],
                   'energy': track_features['energy'],
                   'tempo': track_features['tempo'],
                   'valence': track_features['valence']
               }
        else:
            print("\tError connecting to spotify/audio-features", r)
        tid_chunk = []
        time.sleep(5)

# Attach each audio-feature to each track
print("Saving each audio-feature to each track...")
for playlist_index, playlist in enumerate(final_playlists):
    updated_tracks = []
    for track in playlist['tracks']:
        updated_tracks.append({**track, **audio_features[track['tid']]})
    playlist['tracks'] = updated_tracks
    final_playlists[playlist_index] = playlist

# Send the final playlists to mongo
mongo_collection = "mpd_square_" + str(square_size)
print("Deleting the mongo collection " + mongo_collection)
mongodb_communicate.delete(mongo_collection)
print("Writing final_playlists to mongo")
mongodb_communicate.post(final_playlists, mongo_collection)

print("Total execution time in seconds: ", time.time() - start)