[![ruff](https://github.com/LeskoIam/kronoterm_cloud_relay/actions/workflows/ruff.yml/badge.svg?branch=master)](https://github.com/LeskoIam/kronoterm_cloud_relay/actions/workflows/ruff.yml)
# Kronoterm cloud relay

Relay server for [Kronoterm](https://kronoterm.com//) cloud. It gets data from cloud and exposes it through REST API to local network. 

## Install and run relay
> **_NOTE:_**  Change `python` to `python3` if necessary. Change PORT if needed, assuming 8555 here.
### Debian (Ubuntu, mint, ...)
1. Clone or download the [repo](https://github.com/LeskoIam/kronoterm_cloud_relay),
2. `git clone https://github.com/LeskoIam/kronoterm_cloud_relay.git` *or* download and extract,
3. `cd kronoterm_cloud_relay` to change directory to cloned/extracted,
4. Create `.env` file in `kronoterm_cloud_relay` directory with cloud user and password,
   ```shell
   touch .env
   ```
   Open file in your favorite text editor and add the following content
   ```dotenv
   KRONOTERM_CLOUD_USER="your-user"
   KRONOTERM_CLOUD_PASSWORD="your-password"
   ```
5. [optional] Create and activate python venv,
   ```shell
   python -m venv .venv
   source .venv/bin/activate
   ```
6. Install dependencies (install `requirements.txt` if you want development packages also),
   ```shell
   python -m pip install -r prod_requirements.txt
   ```
7. Run REST API server in the background.
   ```shell
   cd src
   nohup python -m flask --app kronoterm_cloud_relay run --host=0.0.0.0 --port=8555 &
   ```
   Command breakdown
   - `nohup` - no hang-up - don't exit process if shell session ends
   - `--host=0.0.0.0` - run app on all addresses (to be available on local network)
   - `--port=8555` - port on which to run, like in http://192.168.1.111:8555
   - `&` - run process in the background
   
   Running in the foreground (with output to console) can be enabled by running flask server without `nohup` and `&`
   ```shell
   python -m flask --app kronoterm_cloud_relay run --host=0.0.0.0 --port=8555
   ```


## Try it out
With your favorite browser navigate to 

`ip-or-host-address:8555/version`

return should be the current version of kronoterm-cloud-relay
```python
{"version": "0.0.6"}
```
or

`ip-or-host-address:8555/relay/echo/is_it_working`

return should be whatever the last argument is, in this case `is_it_working`
```python
{"message": "relay - echo 'is_it_working' - OK"}
```

#### Home Assistant uses this one to avoid multiple API calls
- `http://ip-or-host-address:8555/hp_info/info_summary`

### Some currently supported endpoints
#### Get data from heat pump (cloud)
Method: `GET`
- `http://ip-or-host-address:8555/hp_info/initial_data`
- `http://ip-or-host-address:8555/hp_info/basic_data`
- `http://ip-or-host-address:8555/hp_info/system_review`
- `http://ip-or-host-address:8555/hp_info/heating_loop/<heating_loop_number>`
  - `<heating_loop_number>`
    - heating loop 1: `1`
    - heating loop 2: `2`
    - sanitary water (heating loop 5): `5`
- `http://ip-or-host-address:8555/hp_info/alarms`
#### Set heat pump configuration
Method: `POST`
- http://ip-or-host-address:8555/hp_control/set_target_temperature
  - payload = `{"temperature": "24.5", "heating_loop": 1}`
  - payload = `{"temperature": "24.5", "heating_loop": 2}`
  - payload = `{"temperature": "24.5", "heating_loop": 5}`
- http://ip-or-host-address:8555/hp_control/set_heating_loop_mode
  - payload = `{"mode": "AUTO", "heating_loop" : 1}`
  - payload = `{"mode": "ON", "heating_loop" : 1}`
  - payload = `{"mode": "OFF", "heating_loop" : 1}`


## Usage with [Home Assistant](https://www.home-assistant.io/)
Home Assistant has [REST](https://www.home-assistant.io/integrations/rest) integration which can request and post data from `relay`.

Refer to [Home Assistant Readme](./docs/home_assistant.md) for details.


## Debugging

   Because we started the `relay` app in the background there is no output to `stdout`. It has been redirected into
   `nohup.out`,
   ```shell
   tail nohup.out
   # or
   tail -f nohup.out  # CTRL-C to exit
   ```
   to kill the process (app), first find the PID (process ID) of `relay` server,
   ```shell
   ps aux | grep python
   ```
   it should output a few lines, we are looking for the one similar to this,
   ```shell
   user      <<8764>> 96.3  4.9  29384 21800 pts/0    R    17:39   0:04 /home/***/***/kronoterm_cloud_relay/.venv/bin/python /home/***/***/kronoterm_cloud_relay/.venv/bin/flask --app kronoterm_cloud_relay --debug run --host=0.0.0.0 --port=8555
   ```
   number in \<\<<number\>\> is PID, kill the process
   ```shell
   kill 8764
   ```
