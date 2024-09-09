## Home Assistant Configuration

Assuming you have kronoterm-cloud-relay running and reachable following needs to be added to your home assistant:

### `configuration.yaml` file.

```yaml
sensor:
  - platform: rest
    name: "Heat pump room temperature"
    unique_id: generate-your-own-unique-id
    resource: http://your-relay-host:8555/hp-info/room_temperature
    method: GET
    value_template: "{{ value_json.data }}"
    unit_of_measurement: '°C'
    device_class: temperature
    state_class: measurement
    timeout: 20
    scan_interval: 60
    
  - platform: rest
    name: "Heat pump outlet temperature"
    unique_id: generate-your-own-unique-id
    resource: http://your-relay-host:8555/hp-info/outlet_temperature
    method: GET
    value_template: "{{ value_json.data }}"
    unit_of_measurement: '°C'
    device_class: temperature
    state_class: measurement
    timeout: 20
    scan_interval: 60
    
  - platform: rest
    name: "Heat pump set room temperature"
    unique_id: generate-your-own-unique-id
    resource: http://your-relay-host:8555/hp-info/set_temperature
    method: GET
    value_template: "{{ value_json.data }}"
    unit_of_measurement: '°C'
    device_class: temperature
    state_class: measurement
    timeout: 20
    scan_interval: 60
    
  - platform: rest
    name: "Heat pump outside temperature"
    unique_id: generate-your-own-unique-id
    resource: http://your-relay-host:8555/hp-info/outside_temperature
    method: GET
    value_template: "{{ value_json.data }}"
    unit_of_measurement: '°C'
    device_class: temperature
    state_class: measurement
    timeout: 20
    scan_interval: 60
    
  - platform: rest
    name: "Sanitary water temperature"
    unique_id: generate-your-own-unique-id
    resource: http://your-relay-host:8555/hp-info/water_temperature
    method: GET
    value_template: "{{ value_json.data }}"
    unit_of_measurement: '°C'
    device_class: temperature
    state_class: measurement
    timeout: 20
    scan_interval: 60
    
  - platform: rest
    name: "Heat pump working function"
    unique_id: generate-your-own-unique-id
    resource: http://your-relay-host:8555/hp-info/working_function
    method: GET
    value_template: "{{ value_json.data }}"
    timeout: 20
    scan_interval: 60
    
  - platform: rest
    name: "Heat pump working status"
    unique_id: generate-your-own-unique-id
    resource: http://your-relay-host:8555/hp-info/working_status
    method: GET
    value_template: "{{ value_json.data }}"
    timeout: 20
    scan_interval: 60
    
  - platform: rest
    name: "Heat pump working mode"
    unique_id: generate-your-own-unique-id
    resource: http://your-relay-host:8555/hp-info/working_mode
    method: GET
    value_template: "{{ value_json.data }}"
    timeout: 20
    scan_interval: 60
  
  - platform: rest
    name: Heat pump low temperature loop
    unique_id: generate-your-own-unique-id
    scan_interval: 60
    resource: http://your-relay-host:8555/hp-info/info_summary
    value_template: "{{ value_json.working_status }}"
    json_attributes:
      - room_temperature
      - outside_temperature
      - sanitary_water_temperature
      - outlet_temperature
      - low_temp_target_temp
      - working_function
      - working_status
      - working_mode

rest_command:
  hp_set_mode_on:
    url: http://your-relay-host:8555/hp-control/set_heating_loop_mode
    method: POST
    payload: '{"mode": "ON"}'
    content_type: 'application/json'
  hp_set_mode_off:
    url: http://your-relay-host:8555/hp-control/set_heating_loop_mode
    method: POST
    payload: '{"mode": "OFF"}'
    content_type: 'application/json'
  hp_set_mode_auto:
    url: http://your-relay-host:8555/hp-control/set_heating_loop_mode
    method: POST
    payload: '{"mode": "AUTO"}'
    content_type: 'application/json'
  hp_set_temperature:
    url: http://your-relay-host:8555/hp-control/set_temperature
    method: POST
    payload: '{"temperature": "{{ set_temp }}" }'
    content_type: 'application/json'
```
#### Creating template sensors from `Heat pump low temperature loop` attribute data
```yaml
###############
## HEAT PUMP ##
###############
- sensor:
  - name: "Heat pump room temperature"
    unique_id: 6e2d97a6-f2be-43dd-a389-91daf602fa20
    state: "{{ state_attr('sensor.heat_pump_low_temperature_loop', 'room_temperature') }}"
    unit_of_measurement: °C
    device_class: temperature
    state_class: measurement
  - name: "Heat pump outlet temperature"
    unique_id: 19451526-f813-43a3-88bd-823b1ea464fb
    state: "{{ state_attr('sensor.heat_pump_low_temperature_loop', 'outlet_temperature') }}"
    unit_of_measurement: °C
    device_class: temperature
    state_class: measurement
  - name: "Heat pump configured room temperature"
    unique_id: 479e8ee1-5dce-4ffb-9339-57c65211634c
    state: "{{ state_attr('sensor.heat_pump_low_temperature_loop', 'low_temp_target_temp') }}"
    unit_of_measurement: °C
    device_class: temperature
    state_class: measurement
  - name: "Heat pump outside temperature"
    unique_id: 3316cf5a-6ecf-4c18-8821-69a58fd57ac7
    state: "{{ state_attr('sensor.heat_pump_low_temperature_loop', 'outside_temperature') }}"
    unit_of_measurement: °C
    device_class: temperature
    state_class: measurement
  - name: "Sanitary water temperature"
    unique_id: 12fa0800-577f-4230-a9f9-f5fad8f6b26a
    state: "{{ state_attr('sensor.heat_pump_low_temperature_loop', 'sanitary_water_temperature') }}"
    unit_of_measurement: °C
    device_class: temperature
    state_class: measurement
  - name: "Heat pump working function"
    unique_id: 4997f71d-eb60-43d9-a3c0-e1df2e721f24
    state: "{{ state_attr('sensor.heat_pump_low_temperature_loop', 'working_function') }}"
  - name: "Heat pump working status"
    unique_id: 9f725bb6-6be6-407f-8cb0-e755f7c1797c
    state: "{{ state_attr('sensor.heat_pump_low_temperature_loop', 'working_status') }}"
  - name: "Heat pump working mode"
    unique_id: 26b86176-853e-4829-aa9e-c1f0aaa86905
    state: "{{ state_attr('sensor.heat_pump_low_temperature_loop', 'working_mode') }}"
```
### Automation to sync it to `input_number` helper

```yaml
alias: HP_set_room_temperature
description: >-
  Set room temperature every time 'input_number.heat_pump_set_temperature' is
  changed
trigger:
  - platform: state
    entity_id:
      - input_number.heat_pump_set_temperature
    from: null
    to: null
condition: []
action:
  - action: rest_command.hp_set_temperature
    metadata: {}
    data:
      set_temp: "{{ states('input_number.heat_pump_set_temperature') }}"
mode: single
```