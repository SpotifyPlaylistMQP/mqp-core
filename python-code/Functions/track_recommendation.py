
def find_most_similar_metric(similarity_metrics):
    most_similar_metric = ('start', 0)
    for metric in similarity_metrics:
        if metric[1] > most_similar_metric[1]:
            most_similar_metric = metric
    print(most_similar_metric)
    return most_similar_metric

# Takes in playlistID of most similar playlist to the input, along with the 80% and 20% splits of the original playlist
# returns list of recommended songs that total 20% of original playlist
def recommend_tracks(similarity_metrics, playlist_dict, split_dict, playlist_to_split):
    most_similar_metric = find_most_similar_metric(similarity_metrics)
    most_similar_playlist = playlist_dict[most_similar_metric[0]]
    print("Most similar playlist to Rap Caviar:" + most_similar_playlist['name'])

    count = 0
    recommend_songs_list = []
    tracks = []

    for track in most_similar_playlist['tracks']:
        tracks.append(track)

    set_80 = set(split_dict[(playlist_to_split, '80')])
    set_20 = set(split_dict[(playlist_to_split, '20')])
    set_spotify_playlist = set(tracks)

    length_of_20 = len(set_20)

    # symmetric difference
    symmetric_difference = (set_spotify_playlist ^ set_80)

    # set difference
    possible_songs_to_recommend = (symmetric_difference - set_80)

    for i in symmetric_difference:
        if (count < length_of_20):
            recommend_songs_list.append(i)
            count = count + 1
        else:
            break

    return recommend_songs_list


# Takes in 20% split from original playlist and compares it to the 20% equivalent of recommended songs
# returns the R-precision metric between the omitted songs and the recommended songs
def r_precision(split20, recommended_songs):
    size_of_20_split = len(split20)
    matches = set(split20).intersection(recommended_songs)

    eval_metric = len(matches) / size_of_20_split

    return (eval_metric)