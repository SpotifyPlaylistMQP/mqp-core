def make_matrix(playlist_dict, unique_track_dict):
    # Matrix: rows = tracks, columns = playlists, cells = 1 if track in playlist else 0
    matrix = []
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

def visualize(matrix, playlist_dict, unique_track_dict):
    # Prints out the matrix into visual_matrix.txt
    matrix_file = open("matrix.txt", "w")

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

    print("Matrix has been visualized in matrix.txt")

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
