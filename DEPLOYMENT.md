# 🚀 Chat Magnus Deployment auf Streamlit Cloud

## 📋 Voraussetzungen

- GitHub-Konto (kostenlos)
- Streamlit Cloud-Konto (kostenlos)
- OpenAI API Key

## 🛠️ Deployment-Schritte

### 1. GitHub Repository erstellen

1. Gehe zu [GitHub.com](https://github.com) und erstelle ein neues Repository
2. Nenne es `chat-magnus` oder ähnlich
3. Mache es Public (damit Streamlit Cloud kostenlos zugreifen kann)

### 2. Projekt hochladen

Führe diese Befehle im Terminal aus:

```bash
cd ai-assistant

# Git initialisieren (bereits erledigt)
# git init

# Alle Dateien hinzufügen
git add .

# Commit erstellen
git commit -m "Initial commit - Chat Magnus AI Assistant"

# GitHub Repository hinzufügen
git remote add origin https://github.com/DEIN_BENUTZERNAME/chat-magnus.git

# Hochladen
git push -u origin master
```

### 3. Streamlit Cloud deployen

1. Gehe zu [share.streamlit.io](https://share.streamlit.io)
2. Melde dich mit deinem GitHub-Konto an
3. Klicke auf "New app"
4. Wähle dein GitHub Repository aus
5. Wähle die `app.py` Datei als Hauptdatei
6. Klicke auf "Deploy"

### 4. OpenAI API Key konfigurieren

In Streamlit Cloud:

1. Gehe zu deiner App in Streamlit Cloud
2. Klicke auf "Settings" → "Secrets"
3. Füge folgendes Secret hinzu:
   - Name: `OPENAI_API_KEY`
   - Wert: Dein OpenAI API Key

### 5. App testen

Sobald deployt, erhältst du eine öffentliche URL wie:
`https://chat-magnus.streamlit.app`

Diese URL funktioniert von überall!

## 🔧 Konfiguration

### Streamlit Cloud Secrets

In der `.streamlit/config.toml` Datei ist das Theme bereits konfiguriert.

### Umgebungsvariablen

Die App liest den API Key automatisch aus:
1. Zuerst aus Umgebungsvariablen
2. Dann aus Streamlit Cloud Secrets

## 📱 Externe URL

Nach dem Deployment erhältst du:
- Eine permanente öffentliche URL
- Automatische HTTPS-Verschlüsselung
- Globale Verfügbarkeit
- Kostenlos bis zu 3 Apps

## 🔄 Updates

Um Updates zu deployen:

```bash
git add .
git commit -m "Update Beschreibung"
git push
```

Streamlit Cloud deployt automatisch neu!

## 📊 Monitoring

In Streamlit Cloud kannst du:
- Nutzung statistiken sehen
- Logs überprüfen
- App neu starten
- Einstellungen ändern

## 🆘 Troubleshooting

### Deployment schlägt fehl
- Überprüfe die `requirements.txt`
- Stelle sicher, dass alle Abhängigkeiten korrekt sind
- Überprüfe die Logs in Streamlit Cloud

### API Key Probleme
- Stelle sicher, dass das Secret korrekt gesetzt ist
- Überprüfe, ob der API Key gültig ist

### Authentifizierung
- Admin Login: `admin` / `5107`
- Nur Admin kann API Key konfigurieren

## 💡 Tipps

- Repository sollte Public sein für kostenlosen Streamlit Cloud Zugriff
- API Key wird sicher in Secrets gespeichert
- App läuft 24/7 kostenlos
- Bis zu 3 Apps kostenlos auf Streamlit Cloud

## 🎉 Fertig!

Deine Chat Magnus App ist jetzt von überall unter deiner Streamlit Cloud URL erreichbar!