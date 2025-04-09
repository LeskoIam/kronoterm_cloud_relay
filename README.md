[![ruff](https://github.com/LeskoIam/kronoterm_cloud_relay/actions/workflows/ruff.yml/badge.svg?branch=master)](https://github.com/LeskoIam/kronoterm_cloud_relay/actions/workflows/ruff.yml)
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

Spin up container
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

It exposes **heat pump** data, example bellow.

```
# HELP heat_pump_basic_info Heat pump information
# TYPE heat_pump_basic_info gauge
heat_pump_basic_info{hp_id="FFFFFF",location_name="MyHome",user_level="4"} 1.0
# HELP heat_pump_temperature_c Heat pump temperatures [°C]
# TYPE heat_pump_temperature_c gauge
heat_pump_temperature_c{heating_loop="system",name="room_temperature"} 22.1
heat_pump_temperature_c{heating_loop="system",name="outlet_temperature"} 38.5
heat_pump_temperature_c{heating_loop="system",name="outside_temperature"} 9.0
heat_pump_temperature_c{heating_loop="system",name="sanitary_water_temperature"} 54.3
heat_pump_temperature_c{heating_loop="loop_1",name="current_temp"} 35.6
heat_pump_temperature_c{heating_loop="loop_1",name="target_temp"} 50.0
heat_pump_temperature_c{heating_loop="loop_1",name="calc_target_temp"} 36.8
heat_pump_temperature_c{heating_loop="loop_2",name="target_temp"} 22.0
heat_pump_temperature_c{heating_loop="loop_2",name="calc_target_temp"} 22.0
heat_pump_temperature_c{heating_loop="loop_5",name="target_temp"} 55.0
heat_pump_temperature_c{heating_loop="loop_5",name="calc_target_temp"} 0.0
# HELP heat_pump_power_consumption_kwh Heat pump power consumption [kWh]
# TYPE heat_pump_power_consumption_kwh gauge
heat_pump_power_consumption_kwh{function="heating"} 6.556233333333337
heat_pump_power_consumption_kwh{function="cooling"} 0.0
heat_pump_power_consumption_kwh{function="tap_water"} 2.0836000000000006
heat_pump_power_consumption_kwh{function="pumps"} 0.40832638888888895
heat_pump_power_consumption_kwh{function="total"} 9.048159722222227
# HELP heat_pump_pressure_bar Heat pump system pressure [bar]
# TYPE heat_pump_pressure_bar gauge
heat_pump_pressure_bar 1.9
# HELP heat_pump_function Heat pump function
# TYPE heat_pump_function gauge
heat_pump_function{function="operating_mode",heating_loop="system"} 0.0
heat_pump_function{function="working_function",heating_loop="system"} 0.0
heat_pump_function{function="working_status",heating_loop="loop_1"} 1.0
heat_pump_function{function="working_mode",heating_loop="loop_1"} 2.0
heat_pump_function{function="working_status",heating_loop="loop_2"} 1.0
heat_pump_function{function="working_mode",heating_loop="loop_2"} 2.0
heat_pump_function{function="working_status",heating_loop="loop_5"} 0.0
heat_pump_function{function="working_mode",heating_loop="loop_5"} 0.0
```

> `heat_pump_function` gauge returns a number as defined in kronoterm_cloud_api - [kronoterm_enums.py](https://github.com/LeskoIam/kronoterm_cloud_api/blob/master/kronoterm_cloud_api/kronoterm_enums.py)

## Debugging
Tail container logs:
```shell
docker logs -f kronoterm_cloud_relay
```
Shut down container:
```shell
docker compose down kronoterm_cloud_relay
```

