# Definitions


DEBUG = True

def ld(msg, *args):
	if DEBUG == True:
		logger.info("%s :: %s", ENTITY_ID, msg % args)

logger.info("Start Thermostat reset offset")

# Attributes
# What zwave implementation is working?
# the "Old" one: "zwave"
# the newer OZW implementation beta: "ozw"
#ZWAVE_SERVICE = "zwave"
ZWAVE_SERVICE = "ozw"

PARAM_ENTITY_ID 	= "climate_entity"
PARAM_OFFSET_STORE = "current_offset"

ENTITY_ID = data.get(PARAM_ENTITY_ID, None)
CURRENT_OFFSET_STORE = data.get(PARAM_OFFSET_STORE, None)

ld("ID: %s - Store: %s", ENTITY_ID, CURRENT_OFFSET_STORE)

SERVICE_SET_CONFIG_PARAMETER = "set_config_parameter"
ZWAVE_PARAMETER = 8
ATTR_NODE_ID = "node_id"

ACTUAL_STATES = hass.states.get(ENTITY_ID)
NODE_ID = ACTUAL_STATES.attributes.get(ATTR_NODE_ID)

SERVICE_DATA = {"node_id": NODE_ID, "parameter": 8, "value": 0}

try:
	hass.services.call(ZWAVE_SERVICE, SERVICE_SET_CONFIG_PARAMETER, SERVICE_DATA, False)
	
	INPUT_NUMBER = {"entity_id": CURRENT_OFFSET_STORE, "value": 0}
	hass.services.call("input_number", "set_value", INPUT_NUMBER, False)
	
except:
		logger.info("%s - Reset OFFSET fails", ENTITY_ID)
