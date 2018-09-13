# mqp-core
Core repository for MQP needs

## how?
1. Install yarn if you haven't already: `npm install -g yarn`
2. Install project dependencies if you haven't already: `yarn install`
3. Add the `config.json` file to to the config directory
3. Run project: `yarn dev`

### config.json
This file contains an object like so:
```
{
  "spotify": {
    "client_id": "",
    "client_secret": "",
    "redirect_uri": "",
    "scope": ""
  },
  "node-server": {
    "port": 8888
  }
}
```
