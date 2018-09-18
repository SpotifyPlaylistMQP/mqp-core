def calculate_sparsity(matrix):
    playlist_track_matches = 0
    total_cells = 0
    for row in matrix:
        for cell in row:
            total_cells += 1
            if cell == 1:
                playlist_track_matches += 1
    return round(playlist_track_matches / total_cells, 5)
