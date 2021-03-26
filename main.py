from boot import do_connect, wlan
import machine
import time
from umqttsimple import MQTTClient
import ubinascii
from secrets import MQTT_SERVER


client_id = ubinascii.hexlify(machine.unique_id())

servo_pin = machine.Pin(14)
servo = machine.PWM(servo_pin, freq=50)
servo.duty(115)

button_pin = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)

servo_on = False
servo_state = True


def sub_cb(topic, msg):
    global servo, servo_on
    print((topic, msg))
    if topic == b'servo':
        print('ESP received hello message')
        servo_on = not servo_on


def connect_and_subscribe():
    client = MQTTClient(client_id, MQTT_SERVER)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe('servo')

    print('Connected to MQTT')
    client.publish('esp32', 'connected!')

    return client


try:
    client = connect_and_subscribe()
except OSError as e:
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()


while True:
    if not wlan.isconnected():
        do_connect()

    client.check_msg()

    if servo_state != servo_on:
        print('Servo toggle')
        servo.duty(115 if servo_state else 40)
        servo_state = servo_on
        time.sleep(1)
