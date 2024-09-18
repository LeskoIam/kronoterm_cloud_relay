## Home Assistant Configuration

Assuming you have kronoterm-cloud-relay running and reachable following needs to be added to your home assistant:

### `configuration.yaml` file.

If you are using hostnames for addressing you network devices I would advise to still **use IPs here**.
I found out the hard way if using hostnames sensors go to `unknown` or `unavailable` state. 

```yaml
# Main sensor with all the data
- platform: rest
  name: Kronoterm heat pump
  unique_id: kronoterm_heat_pump
  scan_interval: 60
  resource: http://ip-or-host:8555/hp_info/info_summary
  value_template: "{{ value_json.data.system_info.working_function }}"
  json_attributes_path: '$.data'
  json_attributes:
    - hp_id
    - location_name
    - user_level
    - heating_loop_names
    - alarms
    - system_info
    - heating_loop_1
    - heating_loop_2
```

#### Creating template sensors from `Heat pump low temperature loop` attribute data
```yaml
- sensor:
  # System info
  - name: "Heat pump id"
    unique_id: heat_pump_id
    state: "{{ state_attr('sensor.kronoterm_heat_pump', 'hp_id') }}"
   
  - name: "Heat pump location name"
    unique_id: heat_pump_location_name
    state: "{{ state_attr('sensor.kronoterm_heat_pump', 'location_name') }}"
    
  - name: "Heat pump room temperature"
    unique_id: heat_pump_room_temperature
    state: "{{ state_attr('sensor.kronoterm_heat_pump', 'system_info').room_temperature }}"
    unit_of_measurement: °C
    device_class: temperature
    state_class: measurement

  - name: "Heat pump outlet temperature"
    unique_id: heat_pump_outlet_temperature
    state: "{{ state_attr('sensor.kronoterm_heat_pump', 'system_info').outlet_temperature }}"
    unit_of_measurement: °C
    device_class: temperature
    state_class: measurement

  - name: "Heat pump outside temperature"
    unique_id: heat_pump_outside_temperature
    state: "{{ state_attr('sensor.kronoterm_heat_pump', 'system_info').outside_temperature }}"
    unit_of_measurement: °C
    device_class: temperature
    state_class: measurement
    
  - name: "Sanitary water temperature"
    unique_id: sanitary_water_temperature
    state: "{{ state_attr('sensor.kronoterm_heat_pump', 'system_info').sanitary_water_temperature }}"
    unit_of_measurement: °C
    device_class: temperature
    state_class: measurement
  
  - name: "Heating system pressure"
    unique_id: heat_pump_heating_system_pressure
    state: "{{ state_attr('sensor.kronoterm_heat_pump', 'system_info').heating_system_pressure }}"
    unit_of_measurement: bar
    device_class: pressure
    state_class: measurement

  - name: "Heat pump working function"
    unique_id: heat_pump_working_function
    state: "{{ state_attr('sensor.kronoterm_heat_pump', 'system_info').working_function }}"
  
  # Heating loop 1 (radiators)
  - name: "Heat pump loop 1 current temperature"
    unique_id: heating_loop_1_current_temperature
    state: "{{ state_attr('sensor.kronoterm_heat_pump', 'heating_loop_1').current_temp }}"
    unit_of_measurement: °C
    device_class: temperature
    state_class: measurement
  
  - name: "Heat pump loop 1 target temperature"
    unique_id: heating_loop_1_target_temperature
    state: "{{ state_attr('sensor.kronoterm_heat_pump', 'heating_loop_1').target_temp }}"
    unit_of_measurement: °C
    device_class: temperature
    state_class: measurement
  
  - name: "Heat pump loop 1 calculated target temperature"
    unique_id: heating_loop_1_calculated_target_temperature
    state: "{{ state_attr('sensor.kronoterm_heat_pump', 'heating_loop_1').calc_target_temp }}"
    unit_of_measurement: °C
    device_class: temperature
    state_class: measurement

  - name: "Heat pump loop 1 working status"
    unique_id: heating_loop_1_working_status
    state: "{{ state_attr('sensor.kronoterm_heat_pump', 'heating_loop_1').working_status }}"
  
  - name: "Heat pump loop 1 working mode"
    unique_id: heating_loop_1_working_mode
    state: "{{ state_attr('sensor.kronoterm_heat_pump', 'heating_loop_1').working_mode }}"
  
  # Heating loop 2 (radiators)
  - name: "Heat pump loop 2 target temperature"
    unique_id: heating_loop_2_target_temperature
    state: "{{ state_attr('sensor.kronoterm_heat_pump', 'heating_loop_2').target_temp }}"
    unit_of_measurement: °C
    device_class: temperature
    state_class: measurement
  
  - name: "Heat pump loop 2 calculated target temperature"
    unique_id: heating_loop_2_calculated_target_temperature
    state: "{{ state_attr('sensor.kronoterm_heat_pump', 'heating_loop_2').calc_target_temp }}"
    unit_of_measurement: °C
    device_class: temperature
    state_class: measurement

  - name: "Heat pump loop 2 working status"
    unique_id: heating_loop_2_working_status
    state: "{{ state_attr('sensor.kronoterm_heat_pump', 'heating_loop_2').working_status }}"
  
  - name: "Heat pump loop 2 working mode"
    unique_id: heating_loop_2_working_mode
    state: "{{ state_attr('sensor.kronoterm_heat_pump', 'heating_loop_2').working_mode }}"
```
### REST commands for heat pump configuration
```yaml
rest_command:
  hp_set_mode_loop_1_on:
    url: http://ip-or-host:8555/hp_control/set_heating_loop_mode
    method: POST
    payload: '{"mode": "ON", "heating_loop": 1}'
    content_type: 'application/json'
  hp_set_mode_loop_1_off:
    url: http://ip-or-host:8555/hp_control/set_heating_loop_mode
    method: POST
    payload: '{"mode": "OFF", "heating_loop": 1}'
    content_type: 'application/json'
  hp_set_mode_loop_1_auto:
    url: http://ip-or-host:8555/hp_control/set_heating_loop_mode
    method: POST
    payload: '{"mode": "AUTO", "heating_loop": 1}'
    content_type: 'application/json'
    
  hp_set_mode_loop_2_on:
    url: http://ip-or-host:8555/hp_control/set_heating_loop_mode
    method: POST
    payload: '{"mode": "ON", "heating_loop": 2}'
    content_type: 'application/json'
  hp_set_mode_loop_2_off:
    url: http://ip-or-host:8555/hp_control/set_heating_loop_mode
    method: POST
    payload: '{"mode": "OFF", "heating_loop": 2}'
    content_type: 'application/json'
  hp_set_mode_loop_2_auto:
    url: http://ip-or-host:8555/hp_control/set_heating_loop_mode
    method: POST
    payload: '{"mode": "AUTO", "heating_loop": 2}'
    content_type: 'application/json'
  
  hp_set_temperature:
    url: http://ip-or-host:8555/hp_control/set_target_temperature
    method: POST
    payload: '{"temperature": "{{ set_temp }}", "heating_loop": 2}'
    content_type: 'application/json'
```

### Automation to sync it to `input_number` helper

You must have a helper `input_number.heat_pump_set_temperature` defined.
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