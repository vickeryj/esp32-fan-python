import asyncio
from mqtt_as import MQTTClient, config
import machine

import dont_commit

pwm_pin = machine.Pin(17)
pwm = machine.PWM(pwm_pin)
pwm.freq(25000)


config['server'] = '192.168.1.82'
config['ssid'] = '4101'
config['wifi_pw'] = dont_commit.secrets['wifi_pw']

device_name = 'esp32_fan_python_3'
discover_payload = \
f'{{"name" :null, \
"unique_id":"{device_name}", \
"object_id":"{device_name}", \
"~":"{device_name}", \
"icon":"mdi:fan", \
"command_topic":"~/cmnd/MODE", \
"state_topic":"~/stat/MODE", \
"payload_on": "fan_only", \
"payload_off": "off", \
"percentage_state_topic": "~/stat/FANPWM", \
"percentage_command_topic": "~/cmnd/FANPWM", \
"speed_range_min": 1, \
"speed_range_max": 65535, \
"availability_topic":"~/stat/STATUS", \
"dev": {{"name":"{device_name}", \
"model":"{device_name}", \
"identifiers":["{device_name}"], \
"manufacturer":"me" \
}}}}'

async def messages(client):  # Respond to incoming messages
    # If MQTT V5is used this would read
    # async for topic, msg, retained, properties in client.queue:
    async for topic, msg, retained in client.queue:
        print(topic.decode(), msg.decode(), retained)

async def up(client):  # Respond to connectivity being (re)established
    while True:
        await client.up.wait()  # Wait on an Event
        client.up.clear()
        await client.subscribe('homeassistant/status', 1)
        await client.subscribe(f'{device_name}/cmnd/FANPWM', 1)
        await client.publish(f'homeassistant/fan/{device_name}/config', discover_payload)
        await client.publish(f'{device_name}/stat/STATUS', "online")

async def main(client):
    await client.connect()
    for coroutine in (up, messages):
        asyncio.create_task(coroutine(client))
    while True:
        await asyncio.sleep(5)
        pwm_value = f'{pwm.duty()}'
        print(f'publish: {pwm_value}')
        await client.publish(f'{device_name}/stat/FANPWM', pwm_value, qos = 1)
       

config["queue_len"] = 1  # Use event interface with default queue size
MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)
try:
    asyncio.run(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors