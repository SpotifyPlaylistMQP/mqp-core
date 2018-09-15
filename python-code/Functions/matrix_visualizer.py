def format_cell(data):
    if data == "0":
        data = "00"
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

def visualize_matrix(matrix, playlists, tracks):
    # Prints out the matrix into visual_matrix.txt
    matrix_file = open("matrix.txt", "w")

    # Header
    line = "       "
    for t in range(0, len(tracks)):
        line += format_cell("t" + str(t)) + " "
    matrix_file.write(line + "\n")

    # Rows
    line = ""
    for p in range(0, len(playlists)):
        line += format_cell("p" + str(p)) + "|"
        for cell in matrix[p]:
            line += format_cell(str(cell)) + "|"
        matrix_file.write(line + "\n")
        line = ""

    # Playlists
    matrix_file.write("\n--------PLAYLISTS\n")
    count=0
    for key in playlists.keys():
        count+=1
        spacer = "\t" if count < 10 else ""
        matrix_file.write("count" + str(count) + ":\t" + spacer + playlists[key]['name'] + "\n")

    # Tracks
    matrix_file.write("\n--------TRACKS\n")
    for t in range(0, len(tracks)):
        spacer = "\t" if t < 10 else ""
        matrix_file.write("t" + str(t) + ":\t" + spacer + tracks[t]["name"] + "   by  " + tracks[t]["artist"] + "\n")
    matrix_file.close()

    print("Matrix has been visualized in matrix.txt")