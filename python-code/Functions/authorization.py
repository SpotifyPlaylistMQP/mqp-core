import requests
import json

def get_auth_token_from_node_server():
    # Connect to the node server and return the auth token.
    #  -If there is no auth token on the server, you need to login to the spotify API through the react-app
    #  -If there is an error connecting to the node server, make sure it is running
    global auth_token, auth_header
    with open('../config/config.json') as json_file:
        config = json.load(json_file)
        port = config['node-server']['port']
    try:
        node_server_response = requests.get('http://localhost:{}/spotifyAuth/tokens'.format(port))
        try:
            auth_token = json.loads(node_server_response.text)['authToken']
            auth_header = {'Authorization': 'Bearer {0}'.format(auth_token)}
        except KeyError:
            print("There is no auth token on server, you need to login to the Spotify API through the react-app")
            exit()
    except requests.exceptions.RequestException:
        print("Error connecting to node server")
        exit()
