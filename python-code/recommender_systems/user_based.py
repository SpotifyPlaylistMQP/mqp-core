from recommender_systems.modules import similarities, helpers

params = {
    "mpd_square_100": {
        "K": 50
    },
    "mpd_square_1000": {
        "K": 40
    }
}

def create_similarity_dictionaries(input_playlist_index, input_pid, playlist_dict, track_playlist_matrix):
    # For each input playlist, get the list of the other playlists ordered by similarity
    cosine_similarity_tuples = []  # List of tuples where tuple[0] = pid, tuple[1] = cosine_similarity_value
    for comparison_playlist_index, comparison_pid in enumerate(playlist_dict.keys()):
        if input_pid != comparison_pid:
            input_playlist_column, comparison_playlist_column = helpers.get_two_playlist_column(input_playlist_index, comparison_playlist_index, track_playlist_matrix)
            cosine_similarity_tuples.append((comparison_pid, similarities.cosine(input_playlist_column, comparison_playlist_column)))
    cosine_similarity_tuples.sort(reverse=True, key=helpers.sort_by_second_tuple)

    return cosine_similarity_tuples

def get_ranked_tracks(input_pid, input_playlist_index, playlist_dict, unique_track_dict, track_playlist_matrix, mongo_collection):
    similar_track_dict = {}  # Key = potential tid to recommend, Value = Sum total of cosine_similarities
    cosine_similarity_tuples = create_similarity_dictionaries(input_playlist_index, input_pid, playlist_dict, track_playlist_matrix)
    for cosine_sim_playlist_tuple in cosine_similarity_tuples[:params[mongo_collection]['K']]:
        for tid in playlist_dict[cosine_sim_playlist_tuple[0]]['tracks']:
            if tid not in similar_track_dict.keys():
                similar_track_dict[tid] = 0
            similar_track_dict[tid] += cosine_sim_playlist_tuple[1]

    # Transform those sum similarity scores into an ordered list of tuples
    ranked_tracks = []  # List of tuples where tuple[0] = tid, tuple[1] = sum total cosine similarity score
    for cosine_similar_tid in similar_track_dict.keys():
        ranked_tracks.append((cosine_similar_tid, similar_track_dict[cosine_similar_tid]))
    ranked_tracks.sort(reverse=True, key=helpers.sort_by_second_tuple)

    return ranked_tracks