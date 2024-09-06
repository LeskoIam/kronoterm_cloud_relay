# Kronoterm cloud relay

Relay server for kronoterm cloud. It gets data from cloud and exposes it through REST API to local network. 

## Install and run relay

1. Clone or download the [repo](https://github.com/LeskoIam/kronoterm_cloud_relay)
2. Create `.env` file in `kronoterm_cloud_relay` directory with cloud user and password e.g.:
```dotenv
KRONOTERM_CLOUD_USER=your-user
KRONOTERM_CLOUD_PASSWORD=your-password
```
3. [optional] Create and activate python venv
```shell
python -m venv .venv
source .venv/bin/activate
```
4. Install dependencies
```shell
python -m pip install -r requirements.txt
```
5. Run REST API server in the background
```shell
cd src
nohup flask --app kronoterm_cloud_relay run --host=0.0.0.0 --port=8555 &
```

## Usage with Home [Assistant](https://www.home-assistant.io/)
Home Assistant has [REST](https://www.home-assistant.io/integrations/rest) integration which can request data from relay.

Refer to [Home Assistant Readme](./docs/home_assistant.md) for details.