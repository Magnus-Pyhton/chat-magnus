import hashlib
import json
import os
from supabase import create_client, Client

def safe_text(obj):
    """Konvertiert zu String mit Encoding-Fallback"""
    if isinstance(obj, bytes):
        try:
            return obj.decode('utf-8', errors='ignore')
        except:
            return obj.decode('latin-1', errors='ignore')
    elif isinstance(obj, str):
        return obj.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
    else:
        return str(obj)

def safe_print(text):
    """Encoding-sichere Print-Funktion"""
    if text is None:
        return
    text = safe_text(text)
    try:
        print(text)
    except Exception as e:
        pass

class SupabaseAuthManager:
    def __init__(self):
        # Supabase Credentials direkt im Code gespeichert
        self.supabase_url = "https://ctvaifbsemdvsaffmalk.supabase.co"
        self.supabase_key = "sb_publishable_GNTVXI_9_-rokKHs_iAIEg_L2ZO0RHA"
        
        try:
            self.client: Client = create_client(self.supabase_url, self.supabase_key)
            self._initialize_database()
        except Exception as e:
            print(f"Supabase Client Initialisierung fehlgeschlagen: {e}")
            raise
    
    def _initialize_database(self):
        """Initialisiert die Datenbanktabelle für Benutzer"""
        # In Produktion würde dies durch SQL Migrationen erfolgen
        # Hier versuchen wir die Tabelle zu nutzen, Fehler werden abgefangen
        try:
            # Test ob users Tabelle existiert
            self.client.table('users').select('*').limit(1).execute()
        except:
            # Tabelle existiert nicht oder anderer Fehler
            # Wir ignoriere es für jetzt und versuchen bei add_user
            pass
        
        # Versuche auch api_keys Tabelle zu initialisieren
        try:
            self.client.table('api_keys').select('*').limit(1).execute()
        except:
            # api_keys Tabelle existiert nicht, ignoriere für jetzt
            pass
    
    def _hash_password(self, password):
        """Hash ein Passwort mit SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _validate_username(self, username):
        """Validiert Benutzernamen"""
        if not username or len(username) < 3:
            return False, "Benutzername muss mindestens 3 Zeichen lang sein"
        if not username.isalnum() and "_" not in username and "-" not in username:
            return False, "Benutzername darf nur Buchstaben, Zahlen, _ und - enthalten"
        return True, ""
    
    def _validate_password(self, password):
        """Validiert Passwort"""
        if not password or len(password) < 4:
            return False, "Passwort muss mindestens 4 Zeichen lang sein"
        return True, ""
    
    def add_user(self, username, password, role="user"):
        """Fügt einen neuen Benutzer hinzu"""
        # Encoding-sichere Validierung
        username = safe_text(username)
        
        # Validierung
        valid, error = self._validate_username(username)
        if not valid:
            return False, error
        
        valid, error = self._validate_password(password)
        if not valid:
            return False, error
        
        try:
            # Prüfe ob Benutzer bereits existiert
            existing = self.client.table('users').select('*').eq('username', username).execute()
            if existing.data:
                return False, "Benutzername existiert bereits"
            
            # Füge neuen Benutzer hinzu
            self.client.table('users').insert({
                'username': username,
                'password_hash': self._hash_password(password),
                'role': role
            }).execute()
            
            return True, "Benutzer erfolgreich erstellt"
        except Exception as e:
            # Wenn Tabelle nicht existiert, versuche sie zu erstellen
            if "does not exist" in str(e) or "relation" in str(e):
                if self._create_users_table():
                    # Versuche erneut nach Tabellenerstellung
                    try:
                        self.client.table('users').insert({
                            'username': username,
                            'password_hash': self._hash_password(password),
                            'role': role
                        }).execute()
                        return True, "Benutzer erfolgreich erstellt (Tabelle wurde erstellt)"
                    except Exception as e2:
                        return False, safe_text(f"Fehler nach Tabellenerstellung: {str(e2)}")
            return False, safe_text(f"Datenbankfehler: {str(e)}")
    
    def _create_users_table(self):
        """Erstellt die Benutzer Tabelle via Supabase SQL"""
        try:
            # Wir verwenden Supabase SQL über die client library
            # Da direkte SQL-Execution über client library limitiert ist,
            # erstellen wir die Tabelle manuell über Supabase Dashboard
            # Für jetzt geben wir eine Anleitung zurück
            return False
        except Exception as e:
            print(f"Fehler beim Erstellen der Tabelle: {e}")
            return False
    
    def verify_password(self, username, password):
        """Überprüft Benutzername und Passwort"""
        try:
            result = self.client.table('users').select('*').eq('username', username).execute()
            
            if not result.data:
                return False
            
            user = result.data[0]
            hashed_password = self._hash_password(password)
            return user['password_hash'] == hashed_password
        except Exception as e:
            print(f"Fehler bei Passwort-Verifizierung: {e}")
            return False
    
    def get_user_role(self, username):
        """Gibt die Rolle des Benutzers zurück"""
        try:
            result = self.client.table('users').select('*').eq('username', username).execute()
            
            if not result.data:
                return None
            
            return result.data[0]['role']
        except Exception as e:
            print(f"Fehler beim Abrufen der Benutzerrolle: {e}")
            return None
    
    def is_admin(self, username):
        """Überprüft ob der Benutzer Admin ist"""
        return self.get_user_role(username) == "admin"
    
    def get_all_users(self):
        """Gibt alle Benutzernamen zurück (außer Passwörter)"""
        try:
            result = self.client.table('users').select('username', 'role').execute()
            return {user['username']: {"role": user['role']} for user in result.data}
        except Exception as e:
            print(f"Fehler beim Abrufen aller Benutzer: {e}")
            return {}
    
    def delete_user(self, username):
        """Löscht einen Benutzer"""
        try:
            self.client.table('users').delete().eq('username', username).execute()
            return True, "Benutzer erfolgreich gelöscht"
        except Exception as e:
            return False, f"Fehler beim Löschen: {str(e)}"
    
    def login(self, username, password):
        """Login-Funktion"""
        if self.verify_password(username, password):
            import streamlit as st
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = self.get_user_role(username)
            return True
        return False
    
    def logout(self):
        """Logout-Funktion"""
        import streamlit as st
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.role = None
    
    def is_authenticated(self):
        """Überprüft ob der Benutzer authentifiziert ist"""
        import streamlit as st
        return st.session_state.get('authenticated', False)
    
    def get_current_user(self):
        """Gibt den aktuellen Benutzernamen zurück"""
        import streamlit as st
        return st.session_state.get('username', None)
    
    def get_current_role(self):
        """Gibt die aktuelle Rolle zurück"""
        import streamlit as st
        return st.session_state.get('role', None)
    
    def save_api_key(self, provider, api_key):
        """Speichert API Key in der Datenbank mit Fallback zu Session State"""
        import streamlit as st
        
        try:
            # Prüfe ob api_keys Tabelle existiert
            self.client.table('api_keys').select('*').limit(1).execute()
            
            # Prüfe ob API Key bereits existiert
            existing = self.client.table('api_keys').select('*').eq('provider', provider).execute()
            
            if existing.data:
                # Update
                self.client.table('api_keys').update({'api_key': api_key}).eq('provider', provider).execute()
            else:
                # Insert
                self.client.table('api_keys').insert({'provider': provider, 'api_key': api_key}).execute()
            
            # Speichere auch in Session State als Backup
            st.session_state[f'api_key_{provider}'] = api_key
            
            return True, "API Key erfolgreich gespeichert (Datenbank + Session State)"
        except Exception as e:
            print(f"Fehler beim Speichern des API Keys: {e}")
            
            # Fallback zu Session State
            st.session_state[f'api_key_{provider}'] = api_key
            return False, f"Datenbankfehler, in Session State gespeichert: {str(e)}"
    
    def get_api_key(self, provider):
        """Ruft API Key aus der Datenbank oder Session State ab"""
        import streamlit as st
        
        # Versuche zuerst Session State
        session_key = st.session_state.get(f'api_key_{provider}')
        if session_key:
            return session_key
        
        # Versuche dann Datenbank
        try:
            result = self.client.table('api_keys').select('*').eq('provider', provider).execute()
            
            if result.data:
                return result.data[0]['api_key']
            return None
        except Exception as e:
            print(f"Fehler beim Abrufen des API Keys: {e}")
            return None