# Exercice 03 : Station IoT Connectee
# ESP32 / MicroPython

import dht
import machine
import ssd1306
import time
import json

# ── Initialisation ──
capteur_dht = dht.DHT22(machine.Pin(4))
i2c = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
led = machine.Pin(2, machine.Pin.OUT)
buzzer = machine.PWM(machine.Pin(19), freq=1000, duty=0)
TRIG = machine.Pin(5, machine.Pin.OUT)
ECHO = machine.Pin(18, machine.Pin.IN)

# Seuils
SEUIL_TEMP = 35.0
SEUIL_HUM  = 75.0
SEUIL_DIST = 30.0

# ── Fonction 1 : Lire tous les capteurs ──
def lire_capteurs():
    donnees = {"temp": None, "hum": None, "dist": -1}
    try:
        capteur_dht.measure()
        donnees["temp"] = capteur_dht.temperature()
        donnees["hum"]  = capteur_dht.humidity()
    except OSError:
        pass
    try:
        TRIG.value(0)
        time.sleep_us(2)
        TRIG.value(1)
        time.sleep_us(10)
        TRIG.value(0)
        duree = machine.time_pulse_us(ECHO, 1, 30000)
        if duree > 0:
            donnees["dist"] = (duree * 0.0343) / 2
    except OSError:
        pass
    return donnees

# ── Fonction 2 : Afficher une page sur l'OLED ──
def afficher_page(page_num, donnees):
    oled.fill(0)
    if page_num == 0:
        oled.text("-- Page 1/2 --", 0, 0)
        oled.hline(0, 10, 128, 1)
        if donnees["temp"] is not None:
            oled.text("Temp: " + str(round(donnees["temp"], 1)) + " C", 0, 18)
            oled.text("Hum : " + str(round(donnees["hum"], 1)) + " %", 0, 32)
            if donnees["temp"] > SEUIL_TEMP:
                oled.text("!! T HAUTE !!", 10, 50)
            elif donnees["hum"] > SEUIL_HUM:
                oled.text("!! HUM HAUTE !!", 0, 50)
            else:
                oled.text("Etat : OK", 0, 50)
        else:
            oled.text("Erreur DHT22", 0, 18)
    else:
        oled.text("-- Page 2/2 --", 0, 0)
        oled.hline(0, 10, 128, 1)
        if donnees["dist"] > 0:
            oled.text("Dist: " + str(round(donnees["dist"], 1)) + " cm", 0, 18)
            if donnees["dist"] < 10:
                oled.text("Zone : STOP !", 0, 32)
            elif donnees["dist"] < 20:
                oled.text("Zone : Tres proche", 0, 32)
            elif donnees["dist"] < 40:
                oled.text("Zone : Proche", 0, 32)
            elif donnees["dist"] < 80:
                oled.text("Zone : Normal", 0, 32)
            else:
                oled.text("Zone : Loin", 0, 32)
        else:
            oled.text("Erreur HC-SR04", 0, 18)
    oled.show()

# ── Fonction 3 : Gérer les alertes ──
def gerer_alertes(donnees):
    alerte_led = False
    # Alerte température : LED clignote
    if donnees["temp"] is not None and donnees["temp"] > SEUIL_TEMP:
        led.value(1)
        time.sleep(0.1)
        led.value(0)
        alerte_led = True
    # Alerte humidité : LED fixe
    elif donnees["hum"] is not None and donnees["hum"] > SEUIL_HUM:
        led.value(1)
        alerte_led = True
    else:
        led.value(0)
    # Alerte proximité : Buzzer
    if donnees["dist"] > 0 and donnees["dist"] < SEUIL_DIST:
        buzzer.duty(512)
        time.sleep(0.1)
        buzzer.duty(0)
    else:
        buzzer.duty(0)

# ── Fonction 4 : Publier en JSON ──
def publier_serie(donnees):
    sortie = {
        "temp": donnees["temp"],
        "hum": donnees["hum"],
        "dist": round(donnees["dist"], 1) if donnees["dist"] > 0 else -1
    }
    print(json.dumps(sortie))

# ── Boucle principale ──
print("Station IoT demarree")
print("-----------------------------------")

compteur = 0
page = 0

while True:
    donnees = lire_capteurs()
    afficher_page(page, donnees)
    gerer_alertes(donnees)
    if compteur % 5 == 0:
        publier_serie(donnees)
    if compteur % 3 == 0:
        page = (page + 1) % 2
    compteur += 1
    time.sleep(1)