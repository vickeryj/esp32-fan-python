import asyncio
from machine import Pin, reset

import home_assistant_mqtt


from mqtt_as import MQTTClient, config
import machine

import dont_commit

pwm_pin = machine.Pin(17)
pwm = machine.PWM(pwm_pin)
pwm.freq(25000)
mqtt = home_assistant_mqtt.HomeAssistantMQTT(pwm)
try:
    asyncio.run(mqtt.start())
except KeyboardInterrupt:
    reset()
finally:
    mqtt.close()
