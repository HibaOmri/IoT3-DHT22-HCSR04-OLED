# Exercice 02 : HC-SR04 + Buzzer
# ESP32 / MicroPython

import machine
import time

# Initialisation
TRIG = machine.Pin(5, machine.Pin.OUT)
ECHO = machine.Pin(18, machine.Pin.IN)
buzzer = machine.PWM(machine.Pin(19), freq=1000, duty=0)

def mesurer_distance_cm():
    TRIG.value(0)
    time.sleep_us(2)
    TRIG.value(1)
    time.sleep_us(10)
    TRIG.value(0)
    try:
        duree = machine.time_pulse_us(ECHO, 1, 30000)
        if duree < 0:
            return -1
        return (duree * 0.0343) / 2
    except OSError:
        return -1

def biper(dist):
    if dist < 0:
        buzzer.duty(0)
        return
    if dist < 10:
        # Son continu
        buzzer.duty(512)
        time.sleep(0.05)
    elif dist < 20:
        # Bips très rapides
        buzzer.duty(512)
        time.sleep(0.1)
        buzzer.duty(0)
        time.sleep(0.1)
    elif dist < 40:
        # Bips moyens
        buzzer.duty(512)
        time.sleep(0.1)
        buzzer.duty(0)
        time.sleep(0.3)
    elif dist < 80:
        # Bips lents
        buzzer.duty(512)
        time.sleep(0.1)
        buzzer.duty(0)
        time.sleep(0.8)
    else:
        # Silence
        buzzer.duty(0)

print("Aide au stationnement demarree")
print("-----------------------------------")

while True:
    distance = mesurer_distance_cm()
    if distance < 0:
        print("Erreur capteur")
        buzzer.duty(0)
    else:
        if distance < 10:
            zone = "STOP !"
        elif distance < 20:
            zone = "Tres proche"
        elif distance < 40:
            zone = "Proche"
        elif distance < 80:
            zone = "Normal"
        else:
            zone = "Loin"
        print("Distance : " + str(round(distance, 1)) + " cm | Zone : " + zone)
        biper(distance)
    time.sleep(0.1)