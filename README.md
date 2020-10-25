<a href="https://github.com/amrheing/thermostat_offset/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/amrheing/climate_automation"></a>
<a href="https://github.com/amrheing/thermostat_offset/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/amrheing/climate_automation"></a>
<a href="https://github.com/amrheing/thermostat_offset/blob/master/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/amrheing/thermostat_offset"></a>

This python_script is for use in HomeAssistant

## Features

# thermostat_offset
Set the offset for eurotronics spirit zwave thermostat

the spirit can be use a external sensor. poor, that there is no sensor on market what is working :-(

furthermore i got no information when it should be delivered

Now, with this script i set the offset of the thermostat with the data of an external temperature sensor.

that can be any sensor on the market :-)

The thermostat offset can be only -5 to 5 degrees. If the offset is more -5/5 degrees will be set. 

In my situation the thermostat in living room is placed under the floor and there the offset is not enough when the target tepmeratur is reached. 
Then it is needed to increase the target temperatur

```yaml
- id: 'schlafzimmer_thermostat_offset_rechts'
  alias: Schlafzimmer Thermostat Offset rechts
  description: ''
  trigger:
  # reduce the time for the script as you want. Every control decrease the battery live
  # but also not too long, when heating the differnce increase
  - platform: time_pattern
    hours: /1
  condition: []
  action:
  - service: python_script.thermostat_offset
    data:
      climate_entity: climate.thermostat_schlafzimmer_rechts
      external_sensor: sensor.multisensor_schlafzimmer_temperature
      current_offset: input_number.sz_current_offset_rechts
  mode: single
  ```

In the code you can change the zwave ackend now:

```yaml
# What zwave implementation is working?
# the "Old" one: "zwave"
# the newer OZW implementation beta: "ozw"
#ZWAVE_SERVICE = "zwave"
ZWAVE_SERVICE = "ozw"
```
