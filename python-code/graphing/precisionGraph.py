# x: K
# y: R precision
# z: N?


def create_graph(graph_data, playlist_name):
    # Jaccard
    uj = graph_data["uj"]
    ij = graph_data["ij"]
    # Cosine
    uc = graph_data["uc"]
    ic = graph_data["ic"]
