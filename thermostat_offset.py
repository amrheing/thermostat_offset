# Definitions


DEBUG = True

def ld(msg, *args):
	if DEBUG == True:
		logger.info("%s :: %s", ENTITY_ID, msg % args)

logger.info("Start Thermostat offset")

# Attributes

PARAM_ENTITY_ID 	= "climate_entity"
PARAM_EXT_SENSOR 	= "external_sensor"
PARAM_OFFSET_STORE = "current_offset"
HVAC_MODE_HEAT = "heat"

ENTITY_ID = data.get(PARAM_ENTITY_ID, None)
EXT_SENSOR = data.get(PARAM_EXT_SENSOR, None)
CURRENT_OFFSET_STORE = data.get(PARAM_OFFSET_STORE, None)

ld("ID: %s - EXT: %s - Store: %s", ENTITY_ID, EXT_SENSOR, CURRENT_OFFSET_STORE)

SERVICE_SET_CONFIG_PARAMETER = "set_config_parameter"
ZWAVE_PARAMETER = 8
ATTR_NODE_ID = "node_id"
ATTR_TEMPERATURE = "current_temperature"
ATTR_HVAC_MODE = "hvac_mode"

ACTUAL_ROOM_TEMPERATURE = hass.states.get(EXT_SENSOR).state
CURRENT_OFFSET = hass.states.get(CURRENT_OFFSET_STORE).state
ld("Current Offset: %s", CURRENT_OFFSET)
ACTUAL_STATES = hass.states.get(ENTITY_ID)
ld("Actual State: %s", ACTUAL_STATES)
NODE_ID = ACTUAL_STATES.attributes.get(ATTR_NODE_ID)
ACTUAL_THERMOSTAT_TEMPERATURE = ACTUAL_STATES.attributes.get(ATTR_TEMPERATURE)
ACTUAL_MODE = ACTUAL_STATES.state

ld("Actual Mode: %s - HVAC Heat: %s", ACTUAL_MODE, HVAC_MODE_HEAT)

if ACTUAL_MODE == HVAC_MODE_HEAT:

	ld("\"%s\" - Actual Thermostat Temperature: %s", ENTITY_ID, ACTUAL_THERMOSTAT_TEMPERATURE)

	ACTUAL_ROOM_TEMPERATURE = float(ACTUAL_ROOM_TEMPERATURE)
	CURRENT_OFFSET = float(CURRENT_OFFSET)



	if CURRENT_OFFSET >= 206:
		CURRENT_OFFSET = (CURRENT_OFFSET - 255) / 10
	elif CURRENT_OFFSET <= 50:
		CURRENT_OFFSET = CURRENT_OFFSET / 10
	else:
		CURRENT_OFFSET = 128
	
	REAL_THERMOSTAT_TEMPERATURE = ACTUAL_THERMOSTAT_TEMPERATURE - CURRENT_OFFSET

	ld("\"%s\" - External Sensor Temperature: %s", ENTITY_ID, ACTUAL_ROOM_TEMPERATURE)
	ld("\"%s\" - Node ID: %s", ENTITY_ID, NODE_ID)
	ld("\"%s\" - Current Offset: %s", ENTITY_ID, CURRENT_OFFSET)


	ld("\"%s\" - Real Thermostat Temperature: %s", ENTITY_ID, REAL_THERMOSTAT_TEMPERATURE)

	temp_offset = round((ACTUAL_ROOM_TEMPERATURE - REAL_THERMOSTAT_TEMPERATURE), 1)

	if temp_offset < -5:
		offset = 206
	elif temp_offset > 5:
		offset = 50
	elif temp_offset < 0:
		offset = 255 + (temp_offset * 10)
	elif temp_offset > 0:
		offset = temp_offset * 10

	ld("\"%s\" - Diffence: %s", ENTITY_ID, temp_offset)

	ld("\"%s\" - New Offset: %s", ENTITY_ID, offset)

	SERVICE_DATA = {"node_id": NODE_ID, "parameter": 8, "value": offset}

	try:
		hass.services.call("zwave", SERVICE_SET_CONFIG_PARAMETER, SERVICE_DATA, False)
	
		INPUT_NUMBER = {"entity_id": CURRENT_OFFSET_STORE, "value": offset}
		hass.services.call("input_number", "set_value", INPUT_NUMBER, False)
	
	except:
			logger.info("%s - Set OFFSET fails", ENTITY_ID)
			
else:
	logger.info("%s - is OFF - nothing to do", ENTITY_ID)
	
