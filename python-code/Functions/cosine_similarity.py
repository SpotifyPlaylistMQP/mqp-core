from math import *

# Returns cosine_sim_dict, the cosine_sim of each playlist_id compared to the playlist_id_of_interest
def create(playlist_ids, playlist_id_of_interest, playlist_track_matrix):
    def calculate(col1, col2):
        numerator = sum(a * b for a, b in zip(col1, col2))
        denominator = sqrt(sum(a * a for a in col1)) * sqrt(sum(b * b for b in col2))
        return round(numerator / denominator, 5)

    cosine_sim_dict = {} # key = playlist_id, value = cosine_sim
    index_of_interest = playlist_ids.index(playlist_id_of_interest)
    for playlist_id in playlist_ids:
        if playlist_id != playlist_id_of_interest:
            column_of_interest = []
            column_being_compared = []
            for t in range(len(playlist_track_matrix)):
                column_of_interest.append(playlist_track_matrix[t][index_of_interest])
                column_being_compared.append(playlist_track_matrix[t][playlist_ids.index(playlist_id)])
            cosine_sim_dict[playlist_id] = calculate(column_of_interest, column_being_compared)

    return cosine_sim_dict

# Pretty prints the cosine_sim_dict
def pretty_print(cosine_sim_dict, playlist_dict):
    print("Cosine Similarity:")
    for playlist_id in cosine_sim_dict.keys():
        print("\t", playlist_dict[playlist_id]['name'], ":", cosine_sim_dict[playlist_id])
    print("\n")

# Returns the playlist_id of the most similar playlist in cosine_sim_dict
def most_similar(cosine_sim_dict):
    most_similar_tuple = ("init", 0)
    for playlist_id in cosine_sim_dict.keys():
        if cosine_sim_dict[playlist_id] > most_similar_tuple[1]:
            most_similar_tuple = (playlist_id, cosine_sim_dict[playlist_id])

    return most_similar_tuple[0]
