[![ruff](https://github.com/LeskoIam/kronoterm_cloud_relay/actions/workflows/ruff.yml/badge.svg?branch=master)](https://github.com/LeskoIam/kronoterm_cloud_relay/actions/workflows/ruff.yml)
[![tests](https://github.com/LeskoIam/kronoterm_cloud_relay/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/LeskoIam/kronoterm_cloud_relay/actions/workflows/tests.yml)
# Kronoterm cloud relay

Relay server for [Kronoterm](https://kronoterm.com//) cloud. It gets data from cloud and exposes it through REST API to local network.

Also has [prometheus](#usage-with-prometheus) endpoint for heat pump data.

## Install and run relay
### Docker
Host system must have [Docker](https://www.docker.com/) installed!

Put both files (`docker-compose.yml` and `.env`) in the same directory and make sure they are named accordingly! 

####  docker-compose.yml file
Get example here: [docker-compose.yml](./docker-compose.yml)

```yaml
services:
  kronoterm_cloud_relay:
    image: leskoiam/kronoterm_cloud_relay:latest
    container_name: kronoterm_cloud_relay
    restart: unless-stopped
    ports:
      - "8555:8555"  # Adjust the port mappings as needed
    ## If you are having problems with slow connection uncomment lines bellow.
    ## GitHub issue reference [#26](https://github.com/LeskoIam/kronoterm_cloud_relay/issues/26)
    # extra_hosts:
    #   - "cloud.kronoterm.com=145.14.48.71"  # TODO: don't forget to periodically check the validity of IP
    env_file: .env
```

####  .env file
Sets environment variables.

Get example here: [.env](./.env_example)
> Set your Kronoterm cloud **username** and **password** here! File name **must** be `.env`!
```dotenv
# Kronoterm cloud user details
KRONOTERM_CLOUD_USER=your-user
KRONOTERM_CLOUD_PASSWORD=your-password

# Set to your own timezone https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
TZ=Europe/Paris

# Prometheus metrics update interval in seconds (if empty or missing defaults to 30, minimum is 10)
PROMETHEUS_UPDATE_INTERVAL=30
```

#### Spin up container
```shell
docker compose up -d
```

## Try it out
Navigate to http://ip-or-host-address:8555/docs for list of supported API endpoints

## Usage with [Home Assistant](https://www.home-assistant.io/)
Home Assistant has [REST](https://www.home-assistant.io/integrations/rest) integration which can request and post data from `relay`.

Refer to [Home Assistant Readme](./docs/home_assistant.md) for details.

## Usage with [prometheus](https://prometheus.io/)
`kronoterm_cloud_api` offers prometheus metrics endpoint at `/metrics` e.g.: http://ip-or-host-address:8555/metrics.

More on prometheus configuration can be found in [Prometheus Readme](./docs/prometheus.md).

## Debugging
Tail container logs:
```shell
docker logs -f kronoterm_cloud_relay
```
Shut down container:
```shell
docker compose down kronoterm_cloud_relay
```

