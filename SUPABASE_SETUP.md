# 🗄️ Supabase Datenbank-Integration für Chat Magnus

## 🎯 Warum Supabase?

- **Kostenlos** für kleine Projekte
- **Echte PostgreSQL-Datenbank**
- **Persistente Speicherung** (Benutzer bleiben nach App-Neustart)
- **Einfache Integration** mit Python
- **Automatische Backups**

## 🚀 Supabase Setup-Anleitung

### 1. Supabase Konto erstellen

1. Gehe zu [supabase.com](https://supabase.com)
2. Klicke "Start your project"
3. Melde dich mit GitHub an (empfohlen)
4. Wähle "New Project"

### 2. Neues Projekt erstellen

1. **Project Name**: `chat-magnus`
2. **Database Password**: Wähle ein sicheres Passwort (merke es dir!)
3. **Region**: Wähle eine Region nahe bei dir (z.B. Frankfurt)
4. **Wait for project creation** (dauert 1-2 Minuten)

### 3. Datenbank-Tabelle erstellen

1. Gehe zum Supabase Dashboard → SQL Editor
2. Füge folgendes SQL ein:

```sql
-- Erstelle die Benutzer Tabelle
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Füge den Admin-Benutzer hinzu (Passwort: 5107)
INSERT INTO users (username, password_hash, role)
VALUES ('admin', 'ec2a01611db7fd2f95b5238169442a3d737f3838a7cd90401e1aacf5aff64630', 'admin')
ON CONFLICT (username) DO NOTHING;

-- Erstelle die API Keys Tabelle für persistente API Key Speicherung
CREATE TABLE IF NOT EXISTS api_keys (
    id SERIAL PRIMARY KEY,
    provider VARCHAR(50) UNIQUE NOT NULL,
    api_key TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

3. Klicke "Run"

### 4. API Keys kopieren

1. Gehe zu Project Settings → API
2. Kopiere:
   - **Project URL**: z.B. `https://xyz.supabase.co`
   - **anon public**: z.B. `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

### 5. .env Datei aktualisieren

In deiner `.env` Datei:

```env
OPENAI_API_KEY=dein_openai_key
SUPABASE_URL=https://dein-projekt.supabase.co
SUPABASE_KEY=dein_anon_key
```

### 6. App neustarten

```bash
cd ai-assistant
source venv/bin/activate
streamlit run app.py
```

## 🔧 Für Streamlit Cloud

### Secrets konfigurieren:

1. Gehe zu deiner Streamlit Cloud App
2. Klicke "Settings" → "Secrets"
3. Füge folgende Secrets hinzu:
   - `OPENAI_API_KEY`: Dein OpenAI API Key
   - `SUPABASE_URL`: Deine Supabase Project URL
   - `SUPABASE_KEY`: Dein Supabase anon Key

4. Klicke "Save"
5. App wird automatisch neu deployed

## ✅ Vorteile der Supabase-Integration

### Vorher (Session State):
- ❌ Benutzer gehen bei App-Neustart verloren
- ❌ Keine persistente Speicherung
- ❌ Nur für Entwicklung geeignet

### Nachher (Supabase):
- ✅ Benutzer bleiben persistent
- ✅ Echte Datenbank
- ✅ Skalierbar für Produktion
- ✅ Automatische Backups
- ✅ Zugriff von überall

## 🎉 Fertig!

Deine Chat Magnus App hat jetzt eine echte Datenbank! Benutzer werden persistent gespeichert und gehen auch bei App-Neustarts nicht verloren.

## 🆘 Troubleshooting

### "Supabase Verbindung fehlgeschlagen"
- Überprüfe ob SUPABASE_URL und SUPABASE_KEY korrekt sind
- Prüfe ob dein Supabase Projekt aktiv ist

### "Tabelle existiert nicht"
- Führe das SQL aus Schritt 3 im Supabase Dashboard aus
- Prüfe ob du im richtigen Projekt bist

### "Permission denied"
- Überprüfe ob der anon Key korrekt ist
- Prüfe die RLS Policies in Supabase

## 📊 Benutzerverwaltung

Mit Supabase kannst du Benutzer auch direkt im Dashboard verwalten:
- Gehe zu Table Editor → users
- Sieh, bearbeite oder lösche Benutzer
- SQL Queries für komplexe Operationen