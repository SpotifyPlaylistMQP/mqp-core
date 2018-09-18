
# Function to get a list of unique song names in a playlist
# string -> list
def get_unique_songs(playlist):
    tracks = []
    for track in playlist['tracks']:
        if track not in tracks:
            tracks.append(track)
    return tracks


# split_playlist(array)
#   Takes the entered playlist by the user and removes a randomly selected 20%
#   for comparison. Stores the 20% and 80% split in two arrays locally accessible.
# input_playlist = the playlist for comparison
#   the format of {key: playlist_id, value: [track_list]}
#   each elements is {playlist_id: tracklist[]}
# array -> array, array
def split_playlist(input_playlist_id, playlist_dict):
    split_dictionary = {}
    all_tracks = get_unique_songs(playlist_dict[input_playlist_id]) #local lists for playlist tracks
    list_80split = [] #80% of the songs
    list_20split = [] #20% of the songs (for removal, non-inclusive)

    #shuffled_array = np.random.shuffle(all_tracks) ##Randomly shuffle the array
    all_tracks_length = len(all_tracks)/5
    count = 0
    for song in all_tracks: #Takes the first 20 (0 to 1/5 of the array)
        count += 1
        if count <= all_tracks_length:
            list_20split.append(song)
            all_tracks.pop(count) #Removes the song from the shuffled_array after adding it to the 20% split array

    for remaining_song in all_tracks: #Adds the remaining songs to the comparison array
        list_80split.append(remaining_song)

    split_dictionary[(input_playlist_id, '80')] = list_80split
    split_dictionary[(input_playlist_id, '20')] = list_20split

    return split_dictionary
