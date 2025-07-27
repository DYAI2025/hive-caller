# hive-caller

**Voice-Shortcut zu GPT-Systemen – minimal, schnell, auditiv.**

Ein lokales Gateway, um via Hotkey oder Klick mit einem GPT-System zu sprechen
und die Antwort als Sprache zu erhalten. Die Anwendung besteht aus einer
Electron-Oberfläche und einem kleinen Python-Server.

## Komponenten

- **electron-ui/** – Minimalistische Electron-App mit Start/Stopp-Button und
  Statusanzeige. Kommuniziert per REST mit dem Python-Server und registriert
  einen globalen Hotkey (standardmäßig `CommandOrControl+Shift+H`).
- **main.py** – Flask-Server mit den Routen `/trigger` (startet das Recording)
  und `/status` (liefert aktuellen Zustand). Lädt Einstellungen aus
  `config.yaml`.
- **whisper_listener.py** – Nimmt Audio vom Mikrofon auf und leitet den Text an
  den Responder weiter.
- **connector/responder.py** – Sendet Text an GPT (z. B. OpenAI) und gibt die
  Antwort per Text‑to‑Speech wieder aus.
- **config.yaml** – Beispielkonfiguration für API-Keys und Aufnahmedauer.

## Installation

```bash
# Python-Abhängigkeiten
pip install -r requirements.txt

# Electron-Abhängigkeiten
cd electron-ui
npm install
```

## Nutzung

```bash
# Python-Server starten
python main.py

# Electron-App starten
cd electron-ui
npm start
```

Mit dem Hotkey (Standard: `CommandOrControl+Shift+H`) oder dem Button wird die
Aufnahme gestartet. Nach wenigen Sekunden antwortet das GPT-Modell und gibt die
Sprachausgabe wieder.

## Docker

Optional lässt sich der Python-Teil per Docker starten:

```bash
docker build -t hive-caller .
docker run -p 8723:8723 hive-caller
```
