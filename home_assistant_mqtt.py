import asyncio
from mqtt_as import MQTTClient, config
import machine

import dont_commit

class HomeAssistantMQTT:

    def __init__(self, pwm):
        self.pwm = pwm
        config['server'] = '192.168.1.82'
        config['ssid'] = '4101'
        config['wifi_pw'] = dont_commit.secrets['wifi_pw']
        config["queue_len"] = 1
        MQTTClient.DEBUG = True

        self.device_name = 'esp32_fan_python_3'

        self.discover_payload = \
        f'{{"name" :null, \
        "unique_id":"{self.device_name}", \
        "object_id":"{self.device_name}", \
        "~":"{self.device_name}", \
        "icon":"mdi:fan", \
        "command_topic":"~/cmnd/MODE", \
        "state_topic":"~/stat/MODE", \
        "payload_on": "fan_only", \
        "payload_off": "off", \
        "percentage_state_topic": "~/stat/FANPWM", \
        "percentage_command_topic": "~/cmnd/FANPWM", \
        "speed_range_min": 1, \
        "speed_range_max": 1023, \
        "availability_topic":"~/stat/STATUS", \
        "dev": {{"name":"{self.device_name}", \
        "model":"{self.device_name}", \
        "identifiers":["{self.device_name}"], \
        "manufacturer":"me" \
        }}}}'


    async def listen(self):
        while True:
            await self.client.up.wait()
            self.client.up.clear()
            await self.client.subscribe('homeassistant/status', 1)
            await self.client.subscribe(f'{self.device_name}/cmnd/FANPWM', 1)
            await self.client.publish(f'homeassistant/fan/{self.device_name}/config', self.discover_payload)
    
    async def process(self):
        async for topic, msg, retained in self.client.queue:
            decoded_topic = topic.decode()
            decoded_message = msg.decode()
            if decoded_topic == f'{self.device_name}/cmnd/FANPWM':
                self.pwm.duty(int(decoded_message))
            print(decoded_topic, decoded_message, retained)

    async def start(self):
        self.client = MQTTClient(config)
        await self.client.connect()
        asyncio.create_task(self.listen())
        asyncio.create_task(self.process())
        while True:
            await asyncio.sleep(5)
            pwm_value = f'{self.pwm.duty()}'
            print(f'publish: {pwm_value}')
            await self.client.publish(f'{self.device_name}/stat/STATUS', "online")
            await self.client.publish(f'{self.device_name}/stat/MODE', "fan_only")
            await self.client.publish(f'{self.device_name}/stat/FANPWM', pwm_value, qos = 1)

    def close(self):
        self.client.close()