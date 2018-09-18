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

def visualize_matrix(playlist_dict, unique_track_dict):
    matrix = make_matrix(playlist_dict, unique_track_dict)

    # Prints out the matrix into visual_matrix.txt
    matrix_file = open("matrix.txt", "w")

    # Header
    line = "       "
    for t in range(0, len(unique_track_dict)):
        line += format_cell("t" + str(t)) + " "
    matrix_file.write(line + "\n")

    # Rows
    line = ""
    for p in range(0, len(playlist_dict.keys())):
        line += format_cell("p" + str(p)) + "|"
        for cell in matrix[p]:
            line += format_cell(str(cell)) + "|"
        matrix_file.write(line + "\n")
        line = ""

    # Playlists
    matrix_file.write("\n--------PLAYLISTS\n")
    count=0
    for key in playlist_dict.keys():
        spacer = "\t" if count < 10 else ""
        matrix_file.write("p" + str(count) + ":\t" + spacer + playlist_dict[key]['name'] + "\n")
        count+=1

    # Tracks
    matrix_file.write("\n--------TRACKS\n")
    t = 0
    for track_key in unique_track_dict:
        spacer = "\t" if t < 10 else ""
        matrix_file.write("t" + str(t) + ":\t" + spacer + unique_track_dict[track_key]["name"] + "   by  " + unique_track_dict[track_key]["artist"] + "\n")
        t += 1

    matrix_file.close()

    print("Matrix has been visualized in matrix.txt")

def make_matrix(playlist_dict, unique_track_dict):
    matrix = []
    for key in playlist_dict.keys():
        matrix_row = []
        playlist_track_dict = get_playlsit_track_dict(playlist_dict[key])
        playlist_track_ids = playlist_track_dict.keys()
        for track_id in unique_track_dict.keys():
            if track_id in playlist_track_ids:
                matrix_row.append(playlist_track_dict[track_id]['value'])
            else:
                matrix_row.append("--")
        matrix.append(matrix_row)
    return matrix

def get_playlsit_track_dict(playlist):
    track_dict = {}
    for track in playlist['tracks']:
        track_dict[track['track_id']] = track
    return track_dict