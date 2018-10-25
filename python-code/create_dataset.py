from dataset_creator import master_count
from mongodb import mongodb_communicate
import sys

if len(sys.argv) <= 3 or not isinstance(int(float(sys.argv[1])), int) or not 0 <= float(sys.argv[2]) <= 1:
    print("Incorrect arguments!")
    print("Execute the program like so:")
    print("   py create_dataset.py {track_relevancy_threshold} {playlist_relevancy_threshold} {save}")
    print("Where:")
    print("   -track_relevancy_threshold is a number")
    print("   -playlist_relevancy_threshold is a decimal from 0 to 1")
    print("   -save indicates if the results should persist to mongo or not")
    print("       Put a value here if you want it to persist, or leave it blank if not")
    exit()

track_relevancy_threshold = int(float(sys.argv[1]))
playlist_relevancy_threshold = float(sys.argv[2])
min_playlist_len = 60

all_playlists = master_count.json_reader()
playlist_scores, all_playlists = master_count.master_count(all_playlists, track_relevancy_threshold, min_playlist_len)
final_playlists = master_count.get_final_playlists(playlist_scores, all_playlists, playlist_relevancy_threshold)

# If the save flag was set, persist the playlists into mongo
if len(sys.argv) == 4:
    mongo_collection = 'mpd_' + str(track_relevancy_threshold) + "_" + str(playlist_relevancy_threshold)
    mongodb_communicate.delete(mongo_collection)
    mongodb_communicate.post(final_playlists, mongo_collection)