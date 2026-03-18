Capteurs & Actionneurs avec ESP32
> Simulation sur Wokwi | Langage MicroPython  

---

##  — Capteur HC-SR04 et Buzzer

### Composants
- ESP32 DevKit V1
- Capteur ultrasonique HC-SR04
- Buzzer piézo PWM

### Fonctionnalités
- Mesure de distance par ultrasons (formule : distance = durée × 0.0343 / 2)
- Système d'aide au stationnement avec 5 zones de détection
- Buzzer PWM dont la fréquence de bip augmente à l'approche de l'obstacle

### Zones de détection
| Distance | Zone | Comportement buzzer |
|----------|------|---------------------|
| < 10 cm | STOP ! | Son continu |
| 10 – 20 cm | Très proche | Bips rapides (0.1s) |
| 20 – 40 cm | Proche | Bips moyens (0.3s) |
| 40 – 80 cm | Normal | Bips lents (0.8s) |
| > 80 cm | Loin | Silence |

### Connexions principales
| Composant | Broche | GPIO ESP32 |
|-----------|--------|------------|
| HC-SR04 | TRIG | GPIO 5 |
| HC-SR04 | ECHO | GPIO 18 |
| Buzzer | Signal | GPIO 19 |

---

##— Station IoT Connectée

### Fonctionnalités
- Lecture simultanée DHT22 (T°/Hum) et HC-SR04 (distance)
- Affichage alterné sur OLED toutes les 3 secondes :
  - Page 1 : Température + Humidité + état
  - Page 2 : Distance + Zone de danger
- Gestion des alertes :
  - T° > 35°C → LED clignote
  - Humidité > 75% → LED fixe
  - Distance < 30 cm → Buzzer actif
- Publication JSON dans le terminal série toutes les 5 secondes

### Format JSON série
```json
{"temp": 25.0, "hum": 40.0, "dist": 50.4}
```

### Architecture du code (4 fonctions)
```python
def lire_capteurs()      # Lit DHT22 + HC-SR04, retourne un dict
def afficher_page()      # Affiche Page 1 ou Page 2 sur l'OLED
def gerer_alertes()      # Gère LED et buzzer selon les seuils
def publier_serie()      # Publie les données en JSON
```

---

## Environnement de simulation

| Outil | Description |
|-------|-------------|
| [Wokwi](https://wokwi.com) | Simulateur IoT en ligne |
| MicroPython v1.22 | Langage de programmation |
| ESP32 DevKit V1 | Microcontrôleur cible |

---

## Problèmes rencontrés et solutions

| Problème | Solution |
|----------|----------|
| SyntaxError f-strings MicroPython v1.22 | Remplacé par `str()` + concaténation |
| Buzzer silencieux sur Wokwi | Ajout de l'attribut `"volume": "1"` dans diagram.json |
| DHT22 non détecté | Ajout explicite de `"humidity"` dans les attrs du diagram.json |

---

Réalisé dans le cadre du module **Architecture et Programmation IoT**  
