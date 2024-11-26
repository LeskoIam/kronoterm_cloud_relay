[![ruff](https://github.com/LeskoIam/kronoterm_cloud_relay/actions/workflows/ruff.yml/badge.svg?branch=master)](https://github.com/LeskoIam/kronoterm_cloud_relay/actions/workflows/ruff.yml)
# Kronoterm cloud relay

Relay server for [Kronoterm](https://kronoterm.com//) cloud. It gets data from cloud and exposes it through REST API to local network. 

## Install and run relay
### Docker
On your host system that has [Docker](https://www.docker.com/) installed create `docker-compose.yml` 
file with following content. 
> Update file with your username and password!
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
    environment:
      # Add your kronoterm cloud username and password
      - KRONOTERM_CLOUD_USER="your-user"
      - KRONOTERM_CLOUD_PASSWORD="your-password"
      - TZ=Europe/Paris   # set to your own timezone https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
```
Spin up the image
```shell
docker compose up -d
```

## Try it out
Navigate to

http://ip-or-host-address:8555/docs

for list of supported API endpoints

## Usage with [Home Assistant](https://www.home-assistant.io/)
Home Assistant has [REST](https://www.home-assistant.io/integrations/rest) integration which can request and post data from `relay`.

Refer to [Home Assistant Readme](./docs/home_assistant.md) for details.

## Debugging
Tail container logs:
```shell
docker logs -f kronoterm_cloud_relay
```
Shut down container:
```shell
docker compose down kronoterm_cloud_relay
```

