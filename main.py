import asyncio
from machine import Pin, reset, PWM

import home_assistant_mqtt

pwm_pin = Pin(12)
pwm = PWM(pwm_pin)
pwm.freq(25000)

relay_pin = Pin(13, Pin.OUT)

home_ass_mqtt = home_assistant_mqtt.HomeAssistantMQTT(pwm, relay_pin)

try:
    asyncio.run(home_ass_mqtt.start())
except SystemExit:
    reset()
finally:
    home_ass_mqtt.close()
