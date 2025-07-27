# hive-caller

**Voice-Shortcut zu GPT-Systemen – minimal, schnell, auditiv.**

## Ziel
Mit einem Tastendruck oder Klick sprichst du direkt ins Mikrofon, dein Text wird sofort an GPT geschickt und die Antwort als Sprachausgabe zurückgegeben. Kein Tippen, kein Lesen – nur sprechen und hören.

## Komponenten

- **electron-ui/**  
  Minimalistisches Electron-Frontend (Button, Status, REST-Call an Python-Backend)

- **main.py**  
  Python-Server (Flask), steuert Status und Listener, REST-API `/trigger` und `/status`

- **whisper_listener.py**  
  Lauscht auf Audiodateien (SuperWhisper/Mikrofon), schickt Text an Responder

- **connector/responder.py**  
  Übergibt Text an GPT (OpenAI/Claude), gibt Antwort als Audiodatei zurück (Text-to-Speech)

- **config.yaml**  
  Lokale Einstellungen (API-Keys, Hotkey, Pfade)

## Quickstart (Skizze)

```bash
# Python-Server starten
python main.py

# Electron-App starten
cd electron-ui
npm install && npm start
