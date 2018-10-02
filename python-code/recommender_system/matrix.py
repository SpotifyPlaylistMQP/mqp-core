
# Returns the playlist X track matrix
def create(playlist_dict, unique_track_dict):
    matrix = [] # rows = tracks, columns = playlists, cells = 1 if track in playlist else 0
    for track_id in unique_track_dict.keys():
        row = []
        for playlist_id in playlist_dict.keys():
            if track_id in playlist_dict[playlist_id]['tracks']:
                row.append(1)
            else:
                row.append(0)
        matrix.append(row)
    return matrix

# Returns the sparsity value of the matrix
def sparsity(playlist_track_matrix):
    playlist_track_matches = 0
    total_cells = 0
    for row in playlist_track_matrix:
        for cell in row:
            total_cells += 1
            if cell == 1:
                playlist_track_matches += 1
    return round(playlist_track_matches / total_cells, 5)

# Updates the tracks of the input_playlist
def update_input_playlist_tracks(input_playlist_index, new_playlist_tracks, matrix, unique_track_dict):
    for index, track_id in enumerate(unique_track_dict.keys()):
        if track_id in new_playlist_tracks:
            matrix[index][input_playlist_index] = 1
        else:
            matrix[index][input_playlist_index] = 0
    return matrix
