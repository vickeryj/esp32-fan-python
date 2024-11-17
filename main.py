import asyncio
from machine import Pin, reset, PWM

import home_assistant_mqtt
import show as lcd

pwm_pin = Pin(17)
pwm = PWM(pwm_pin)
pwm.freq(25000)

relay_pin = Pin(18, Pin.OUT)

show = lcd.Show()
show.line("hi!")

home_ass_mqtt = home_assistant_mqtt.HomeAssistantMQTT(pwm, relay_pin, show)

try:
    asyncio.run(home_ass_mqtt.start())
except:
    reset()