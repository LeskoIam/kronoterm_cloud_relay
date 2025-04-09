## Prometheus
### Prometheus config `prometheus.yml`
```yaml
- job_name: 'heat-pump'
  scrape_interval: 30s
  metrics_path: '/metrics'
  scheme: "http"
  static_configs:
  - targets: ['ip-or-host-address:8555']
```

### Metrics
Exposes **heat pump** metrics, example bellow.

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

#### heat_pump_function gauge value mapping

`heat_pump_function` gauge returns a number as defined in kronoterm_cloud_api - [kronoterm_enums.py](https://github.com/LeskoIam/kronoterm_cloud_api/blob/master/kronoterm_cloud_api/kronoterm_enums.py)

##### working_status - HeatingLoopStatus

| name                   | value |
|------------------------|-------|
| CIRCUIT_STATUS_OFF     | 0     |
| CIRCUIT_STATUS_NORMAL  | 1     |
| CIRCUIT_STATUS_ECO     | 2     |
| CIRCUIT_STATUS_COMFORT | 3     |
| CIRCUIT_STATUS_AUTO    | 4     |

##### working_mode - HeatingLoopMode

| name | value |
|------|-------|
| OFF  | 0     |
| ON   | 1     |
| AUTO | 2     |

##### working_function - WorkingFunction

| name                                   | value |
|----------------------------------------|-------|
| HP_FUNCTION_HEATING                    | 0     |
| HP_FUNCTION_SANITARY_WATER_HEATING     | 1     |
| HP_FUNCTION_COOLING                    | 2     |
| HP_FUNCTION_POOL_HEATING               | 3     |
| HP_FUNCTION_ANTILEGIONELLA             | 4     |
| HP_FUNCTION_SLEEP                      | 5     |
| HP_FUNCTION_STARTUP                    | 6     |
| HP_FUNCTION_REMOTE_DISCONNECT          | 7     |
| HP_FUNCTION_ACTIVE_COMPRESSOR_SECURITY | 8     |

##### operating_mode - HeatPumpOperatingMode

| name    | value |
|---------|-------|
| AUTO    | 0     |
| ECO     | 1     |
| COMFORT | 2     |
