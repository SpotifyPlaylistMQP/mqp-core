from recommender_systems.modules import similarities, evaluation, matrix, helpers

params = {
    "mpd_square_100": {
        "K": 20
    },
    "mpd_square_1000": {
        "K": 40
    }
}

# For each input track, get the list of the other tracks ordered by similarity
def create_similarity_dictionaries(input_tid, indexed_tids, matrix_rows):
    input_track_row = None
    for track_index, track_row in enumerate(matrix_rows):
        if indexed_tids[track_index] == input_tid:
            input_track_row = track_row
            break

    cosine_similarity_tuples = []  # List of tuples where tuple[0] = tid, tuple[1] = cosine_similarity_value
    for comparison_track_index, comparison_track_row in enumerate(matrix_rows):
        comparison_tid = indexed_tids[comparison_track_index]
        if input_tid != comparison_tid:
            cosine_similarity_tuples.append((comparison_tid, similarities.cosine(input_track_row, comparison_track_row)))
    cosine_similarity_tuples.sort(reverse=True, key=helpers.sort_by_second_tuple)

    return cosine_similarity_tuples

def get_ranked_tracks(new_playlist_tracks, indexed_tids, track_playlist_matrix, mongo_collection):
    cosine_similar_track_dict = {}  # Key = similar_tid, Value = Sum total of cosine_similarities for this playlist
    for input_tid in new_playlist_tracks:
        similarity_tuples = create_similarity_dictionaries(input_tid, indexed_tids, track_playlist_matrix)
        for cosine_sim_tuple in similarity_tuples[:params[mongo_collection]['K']]:
            if cosine_sim_tuple[0] not in cosine_similar_track_dict.keys():
                cosine_similar_track_dict[cosine_sim_tuple[0]] = 0
            cosine_similar_track_dict[cosine_sim_tuple[0]] += cosine_sim_tuple[1]

    # Transform those sum similarity scores into an ordered list of tuples
    ranked_tracks = []  # List of tuples: (similar_tid, Sum total of cosine_similarities for this playlist)
    for similar_tid in cosine_similar_track_dict.keys():
        ranked_tracks.append((similar_tid, cosine_similar_track_dict[similar_tid]))
    ranked_tracks.sort(reverse=True, key=helpers.sort_by_second_tuple)

    return ranked_tracks
