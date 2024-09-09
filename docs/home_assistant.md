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
    # json_attributes_path: "$"
    json_attributes:
      - room_temperature
      - outside_temperature
      - sanitary_water_temperature
      - outlet_temperature
      - low_temp_target_temp
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