import codecs

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
    visualize(matrix, playlist_dict, unique_track_dict)
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

# Visualizes the matrix to matrix.txt
def visualize(matrix, playlist_dict, unique_track_dict):
    def format_cell(data):
        if len(data) == 1:
            return "   " + data + "  "
        if len(data) == 2:
            return "  " + data + "  "
        if len(data) == 3:
            return "  " + data + " "
        if len(data) == 4:
            return " " + data + " "
        if len(data) == 5:
            return " " + data
        if len(data) == 6:
            return data

    # Prints out the matrix into visual_matrix.txt
    matrix_file = codecs.open("matrix.txt", "w",encoding='utf8')

    # Playlist Header
    line = "       "
    for p in range(len(playlist_dict.keys())):
        line += format_cell("p" + str(p)) + " "
    matrix_file.write(line + "\n")

    # Track Rows
    line = ""
    for t in range(len(unique_track_dict.keys())):
        line += format_cell("t" + str(t)) + "|"
        for cell in matrix[t]:
            line += format_cell(str(cell)) + "|"
        matrix_file.write(line + "\n")
        line = ""

    # Playlist Legend
    matrix_file.write("\n--------PLAYLISTS\n")
    count=0
    for key in playlist_dict.keys():
        spacer = "\t" if count < 10 else ""
        matrix_file.write("p" + str(count) + ":\t" + spacer + playlist_dict[key]['name'] + "\n")
        count+=1

    # Track Legend
    matrix_file.write("\n--------TRACKS\n")
    t = 0
    for track_key in unique_track_dict.keys():
        spacer = "\t" if t < 10 else ""
        matrix_file.write("t" + str(t) + ":\t" + spacer + unique_track_dict[track_key]["name"] + "   by  " + unique_track_dict[track_key]["artist"] + "\n")
        t += 1

    matrix_file.close()