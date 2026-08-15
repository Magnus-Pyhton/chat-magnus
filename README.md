# 🤖 AI Coding Assistant

Eine umfassende KI-Anwendung zum Coden, Chatten und Bildbearbeitung, erstellt mit Streamlit und OpenAI.

## ✨ Funktionen

### 💻 Code Generator
- Generiere qualitativ hochwertigen Code in verschiedenen Programmiersprachen
- Unterstützt: JavaScript, Python, Java, C++, C#, Go, Rust, TypeScript, PHP, Ruby, Swift, Kotlin
- Sauberer, gut dokumentierter Code mit Best Practices

### 💬 Chat mit Internet
- Intelligenter Chatbot mit Internet-Suche
- Automatische Erkennung, wann Web-Suche benötigt wird
- Aktuelle Informationen aus dem Internet für deine Fragen

### 🎨 Bild KI
- **Bild-Generierung**: Erstelle neue Bilder mit DALL-E 3
- **Bild-Bearbeitung**: Bearbeite vorhandene Bilder mit DALL-E 2
- Verschiedene Stile, Größen und Qualitäten

## 🚀 Installation

### Voraussetzungen
- Python 3.8 oder höher
- pip
- OpenAI API Key

### Schritte

1. **Repository klonen oder Projekt erstellen**
```bash
cd ai-assistant
```

2. **Virtuelle Umgebung erstellen**
```bash
python3 -m venv venv
source venv/bin/activate  # Auf Windows: venv\Scripts\activate
```

3. **Abhängigkeiten installieren**
```bash
pip install -r requirements.txt
```

4. **API Key konfigurieren**
```bash
# .env Datei bearbeiten
nano .env  # oder deinen bevorzugten Editor
```

Füge deinen OpenAI API Key ein:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

5. **Anwendung starten**
```bash
streamlit run app.py
```

## 📖 Nutzung

### API Key erhalten
1. Gehe zu [OpenAI Platform](https://platform.openai.com/api-keys)
2. Erstelle ein Konto oder melde dich an
3. Generiere einen neuen API Key
4. Kopiere den Key in die `.env` Datei

### Code Generator
1. Wähle "💻 Code Generator" in der Sidebar
2. Wähle die gewünschte Programmiersprache
3. Beschreibe, was der Code tun soll
4. Klicke auf "Code generieren"

### Chat mit Internet
1. Wähle "💬 Chat mit Internet" in der Sidebar
2. Stelle eine Frage
3. Der Bot sucht automatisch im Internet wenn nötig
4. Erhalte aktuelle, gut recherchierte Antworten

### Bild KI
1. Wähle "🎨 Bild KI" in der Sidebar
2. Wähle zwischen "Generieren" oder "Bearbeiten"
3. Für Generierung: Beschreibe das gewünschte Bild
4. Für Bearbeitung: Lade ein Bild hoch und beschreibe die Änderungen
5. Klicke auf den entsprechenden Button

## 🛠️ Technologie-Stack

- **Frontend**: Streamlit
- **KI-API**: OpenAI (GPT-4, DALL-E 3, DALL-E 2)
- **Web-Scraping**: BeautifulSoup, Requests
- **Bildverarbeitung**: Pillow
- **Umgebungsvariablen**: python-dotenv

## 📁 Projektstruktur

```
ai-assistant/
├── api/
│   ├── __init__.py
│   ├── openai_client.py    # OpenAI API Integration
│   ├── chatbot.py          # Chatbot mit Internet-Suche
│   └── web_scraper.py      # Web-Scraping Funktionen
├── app.py                  # Hauptanwendung (Streamlit)
├── requirements.txt        # Python-Abhängigkeiten
├── .env                    # Umgebungsvariablen (API Key)
└── README.md              # Diese Datei
```

## 🔒 Sicherheit

- Dein API Key wird lokal in der `.env` Datei gespeichert
- Der Key wird niemals an Dritte weitergegeben
- Die Anwendung läuft lokal auf deinem Computer

## 🐛 Fehlerbehebung

### "OPENAI_API_KEY nicht gefunden"
- Stelle sicher, dass die `.env` Datei existiert
- Überprüfe, dass der API Key korrekt eingetragen ist
- Starte die Anwendung neu

### ImportError für Module
- Stelle sicher, dass du die virtuelle Umgebung aktiviert hast
- Installiere alle Abhängigkeiten neu: `pip install -r requirements.txt`

### Bild-Bearbeitung funktioniert nicht
- DALL-E 2 wird für Bild-Bearbeitung verwendet (nicht DALL-E 3)
- Stelle sicher, dass das Bild im PNG/RGBA-Format vorliegt
- Die Bildgröße muss für DALL-E 2 geeignet sein

## 📝 Lizenz

MIT License

## 🤝 Beitrag

Beiträge sind willkommen! Fühle dich frei, Issues zu öffnen oder Pull Requests zu erstellen.

## 📞 Support

Bei Problemen oder Fragen:
- Öffne ein Issue im Repository
- Überprüfe die [OpenAI Dokumentation](https://platform.openai.com/docs)

---

Erstellt mit ❤️ using Streamlit and OpenAI