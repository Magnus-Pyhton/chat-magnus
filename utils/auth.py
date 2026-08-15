import hashlib
import streamlit as st

class AuthManager:
    def __init__(self):
        # Vorprogrammierte Benutzer (in einer echten App würde dies in einer Datenbank sein)
        self.users = {
            "admin": {
                "password": self._hash_password("5107"),
                "role": "admin"
            }
        }
    
    def _hash_password(self, password):
        """Hash ein Passwort mit SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
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
        if username in self.users:
            return False
        
        self.users[username] = {
            "password": self._hash_password(password),
            "role": role
        }
        return True
    
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