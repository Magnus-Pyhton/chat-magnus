import hashlib
import json
import os
import streamlit as st

class AuthManager:
    def __init__(self):
        # Verschiedene mögliche Speicherorte für persistente Speicherung
        self.storage_locations = [
            "/mount/data/users.json",  # Streamlit Cloud persistent
            "/home/admin/.streamlit/users.json",  # Alternative Cloud-Verzeichnis
            "users.json",  # Lokales Verzeichnis
            os.path.expanduser("~/.streamlit/users.json")  # Home-Verzeichnis
        ]
        
        # Finde den ersten beschreibbaren Speicherort
        self.users_file = self._find_writable_storage()
        
        # Lade Benutzer oder erstelle Standard
        self.users = self._load_users()
    
    def _find_writable_storage(self):
        """Findet den ersten beschreibbaren Speicherort"""
        for location in self.storage_locations:
            try:
                # Versuche das Verzeichnis zu erstellen wenn nötig
                dir_path = os.path.dirname(location)
                if dir_path and not os.path.exists(dir_path):
                    os.makedirs(dir_path, exist_ok=True)
                
                # Test-Schreiben
                test_file = location + ".test"
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                
                return location
            except Exception as e:
                print(f"Speicherort {location} nicht beschreibbar: {e}")
                continue
        
        # Fallback zu Session State
        return None
    
    def _load_users(self):
        """Lädt Benutzer aus persistenter JSON-Datei oder Session State"""
        # Versuche zuerst aus Datei zu laden
        if self.users_file and os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Fehler beim Laden der Benutzer: {e}")
        
        # Versuche Session State
        if 'users' in st.session_state:
            return st.session_state.users
        
        # Standard-Benutzer wenn nichts funktioniert
        return {
            "admin": {
                "password": self._hash_password("5107"),
                "role": "admin"
            }
        }
    
    def _save_users(self):
        """Speichert Benutzer mit verschiedenen Methoden"""
        # Versuche zuerst in Datei zu schreiben
        if self.users_file:
            try:
                with open(self.users_file, 'w') as f:
                    json.dump(self.users, f)
                return True
            except Exception as e:
                print(f"Fehler beim Speichern in Datei: {e}")
        
        # Fallback zu Session State
        st.session_state.users = self.users
        return False
    
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
    
    def verify_password(self, username, password):
        """Überprüft Benutzername und Passwort"""
        if username not in self.users:
            return False
        
        hashed_password = self._hash_password(password)
        return self.users[username]["password"] == hashed_password
    
    def get_user_role(self, username):
        """Gibt die Rolle des Benutzers zurück"""
        if username in self.users:
            return self.users[username]["role"]
        return None
    
    def is_admin(self, username):
        """Überprüft ob der Benutzer Admin ist"""
        return self.get_user_role(username) == "admin"
    
    def add_user(self, username, password, role="user"):
        """Fügt einen neuen Benutzer hinzu"""
        # Validierung
        valid, error = self._validate_username(username)
        if not valid:
            return False, error
        
        valid, error = self._validate_password(password)
        if not valid:
            return False, error
        
        if username in self.users:
            return False, "Benutzername existiert bereits"
        
        self.users[username] = {
            "password": self._hash_password(password),
            "role": role
        }
        self._save_users()
        return True, "Benutzer erfolgreich erstellt"
    
    def get_all_users(self):
        """Gibt alle Benutzernamen zurück (außer Passwörter)"""
        return {username: {"role": user["role"]} for username, user in self.users.items()}
    
    def login(self, username, password):
        """Login-Funktion"""
        if self.verify_password(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = self.get_user_role(username)
            return True
        return False
    
    def logout(self):
        """Logout-Funktion"""
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.role = None
    
    def is_authenticated(self):
        """Überprüft ob der Benutzer authentifiziert ist"""
        return st.session_state.get('authenticated', False)
    
    def get_current_user(self):
        """Gibt den aktuellen Benutzernamen zurück"""
        return st.session_state.get('username', None)
    
    def get_current_role(self):
        """Gibt die aktuelle Rolle zurück"""
        return st.session_state.get('role', None)
    
    def get_storage_info(self):
        """Gibt Informationen über den Speicherort zurück"""
        if self.users_file:
            return f"Datei: {self.users_file}"
        else:
            return "Session State"