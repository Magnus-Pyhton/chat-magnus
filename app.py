import streamlit as st
import os
from dotenv import load_dotenv
from api.openai_client import OpenAIClient
from api.chatbot import ChatBot
from api.web_scraper import scrape_web
from utils.auth import AuthManager

load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="Chat Magnus",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Auth Manager mit Supabase
try:
    from utils.supabase_auth import SupabaseAuthManager
    auth_manager = SupabaseAuthManager()
    st.sidebar.success("✅ Supabase Datenbank verbunden")
except Exception as e:
    # Fallback zu lokaler Auth bei Fehlern
    auth_manager = AuthManager()
    st.sidebar.warning(f"⚠️ Supabase Verbindung fehlgeschlagen, nutze lokale Auth: {e}")

# Fallback zu AuthManager wenn Supabase Manager fehlgeschlagen ist
if not hasattr(auth_manager, 'is_authenticated'):
    auth_manager = AuthManager()
    st.sidebar.warning("⚠️ Fallback zu lokaler Auth")

# Initialize session state for auth
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'role' not in st.session_state:
    st.session_state.role = None

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .code-block {
        background-color: #1e1e1e;
        color: #d4d4d4;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    .user-message {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 2rem;
    }
    
    .assistant-message {
        background-color: #f0f0f0;
        color: #333;
        margin-right: 2rem;
    }
    
    .system-message {
        background-color: #fff3cd;
        color: #856404;
        border-left: 4px solid #ffc107;
    }
    
    .login-container {
        max-width: 400px;
        margin: 100px auto;
        padding: 2rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .welcome-text {
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .login-header {
        font-size: 2rem;
        font-weight: bold;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid rgba(255, 255, 255, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Login Page
if not auth_manager.is_authenticated():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    st.markdown('<div class="login-header">🤖 Chat Magnus</div>', unsafe_allow_html=True)
    
    # Tab für Login/Register
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Registrieren"])
    
    with tab1:
        st.markdown('<div class="welcome-text">', unsafe_allow_html=True)
        st.markdown('<h2>🔐 Login</h2>', unsafe_allow_html=True)
        st.markdown('<p>Melde dich an, um auf Chat Magnus Funktionen zuzugreifen</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        username = st.text_input("Benutzername", placeholder="z.B. admin", key="login_username")
        password = st.text_input("Passwort", type="password", placeholder="Dein Passwort", key="login_password")
        
        if st.button("🔑 Einloggen", use_container_width=True):
            if auth_manager.login(username, password):
                st.success("✅ Erfolgreich eingeloggt!")
                st.rerun()
            else:
                st.error("❌ Falscher Benutzername oder Passwort")
    
    with tab2:
        st.markdown('<div class="welcome-text">', unsafe_allow_html=True)
        st.markdown('<h2>📝 Registrieren</h2>', unsafe_allow_html=True)
        st.markdown('<p>Erstelle einen neuen Account für Chat Magnus</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        new_username = st.text_input("Benutzername", placeholder="Mindestens 3 Zeichen", key="reg_username")
        new_password = st.text_input("Passwort", type="password", placeholder="Mindestens 4 Zeichen", key="reg_password")
        confirm_password = st.text_input("Passwort bestätigen", type="password", placeholder="Passwort wiederholen", key="reg_confirm")
        
        if st.button("📝 Account erstellen", use_container_width=True):
            if not new_username or not new_password:
                st.error("❌ Bitte alle Felder ausfüllen")
            elif new_password != confirm_password:
                st.error("❌ Passwörter stimmen nicht überein")
            else:
                success, message = auth_manager.add_user(new_username, new_password, "user")
                if success:
                    st.success(f"✅ {message}")
                    st.info("👤 Du kannst dich jetzt einloggen!")
                else:
                    st.error(f"❌ {message}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.stop()  # Stop execution if not authenticated

# Initialize session state
if 'api_key' not in st.session_state:
    # Versuche zuerst Umgebungsvariable, dann Secrets
    st.session_state.api_key = os.getenv('OPENAI_API_KEY', '')
    if not st.session_state.api_key:
        try:
            st.session_state.api_key = st.secrets['OPENAI_API_KEY']
        except:
            pass

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'generated_images' not in st.session_state:
    st.session_state.generated_images = []

# Sidebar
with st.sidebar:
    st.markdown('<div class="main-header">🤖 Chat Magnus</div>', unsafe_allow_html=True)
    
    # User Info
    st.subheader("👤 Benutzerinfo")
    current_user = auth_manager.get_current_user()
    current_role = auth_manager.get_current_role()
    
    st.markdown(f"""
    <div style='padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; color: white;'>
        <strong>👤 Benutzer:</strong> {current_user}<br>
        <strong>⭐ Rolle:</strong> {current_role}
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚪 Logout", use_container_width=True):
        auth_manager.logout()
        st.rerun()
    
    st.markdown("---")
    
    # API Key Configuration (nur für Admin)
    if auth_manager.is_admin(current_user):
        st.subheader("⚙️ API Konfiguration")
        api_key = st.text_input("OpenAI API Key", type="password", value=st.session_state.api_key)
        st.session_state.api_key = api_key
        
        if api_key:
            os.environ['OPENAI_API_KEY'] = api_key
            st.success("✅ API Key gespeichert")
        else:
            st.warning("⚠️ Bitte API Key eingeben")
        
        st.markdown("---")
    else:
        st.info("ℹ️ API Key Konfiguration ist nur für Admins verfügbar")
        st.markdown("---")
    
    # Navigation
    st.subheader("📱 Navigation")
    page = st.radio(
        "Wähle eine Funktion:",
        ["💻 Code Generator", "💬 Chat mit Internet", "🎨 Bild KI", "👥 Benutzer verwalten"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # About
    st.subheader("ℹ️ Über")
    st.markdown("""
    **Chat Magnus** v1.0.0
    
    Eine umfassende KI-Anwendung zum:
    - Coden in verschiedenen Sprachen
    - Chatten mit Internet-Suche
    - Bild-Generierung und -Bearbeitung
    
    Erstellt mit Streamlit & OpenAI
    """)

# Main Content
if page == "💻 Code Generator":
    st.markdown('<div class="main-header">💻 Code Generator</div>', unsafe_allow_html=True)
    st.markdown("Generiere qualitativ hochwertigen Code in verschiedenen Programmiersprachen")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        language = st.selectbox(
            "Programmiersprache:",
            ["JavaScript", "Python", "Java", "C++", "C#", "Go", "Rust", "TypeScript", "PHP", "Ruby", "Swift", "Kotlin", "Auto-detect"]
        )
        
        prompt = st.text_area(
            "Beschreibe, was der Code tun soll:",
            placeholder="z.B. Erstelle eine Funktion, die eine Fibonacci-Folge berechnet und die ersten n Zahlen zurückgibt...",
            height=150
        )
        
        if st.button("⚡ Code generieren", use_container_width=True):
            if not st.session_state.api_key:
                st.error("❌ Kein API Key konfiguriert. Bitte wende dich an den Admin.")
            elif not prompt.strip():
                st.error("❌ Bitte eine Beschreibung eingeben")
            else:
                with st.spinner("Generiere Code..."):
                    try:
                        client = OpenAIClient()
                        result = client.generate_code(prompt, language.lower())
                        
                        if result["success"]:
                            st.success("✅ Code erfolgreich generiert!")
                            st.markdown(f"**{result['language']} Code:**")
                            st.markdown(f'<div class="code-block">{result["code"]}</div>', unsafe_allow_html=True)
                            
                            # Copy button
                            if st.button("📋 Code kopieren"):
                                st.code(result["code"], language=language.lower())
                        else:
                            st.error(f"❌ Fehler: {result['error']}")
                    except Exception as e:
                        st.error(f"❌ Fehler: {str(e)}")

elif page == "💬 Chat mit Internet":
    st.markdown('<div class="main-header">💬 Chat mit Internet-Suche</div>', unsafe_allow_html=True)
    st.markdown("Stelle Fragen und erhalte Antworten mit aktuellen Informationen aus dem Internet")
    
    # Chat interface
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user-message">👤 {message["content"]}</div>', unsafe_allow_html=True)
            elif message["role"] == "assistant":
                st.markdown(f'<div class="chat-message assistant-message">🤖 {message["content"]}</div>', unsafe_allow_html=True)
            elif message["role"] == "system":
                st.markdown(f'<div class="chat-message system-message">🔍 {message["content"]}</div>', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.text_input(
        "Stelle eine Frage:",
        placeholder="z.B. Was sind die neuesten Entwicklungen in der KI-Forschung?",
        key="chat_input"
    )
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("📤 Senden", use_container_width=True):
            if not st.session_state.api_key:
                st.error("❌ Kein API Key konfiguriert. Bitte wende dich an den Admin.")
            elif not user_input.strip():
                st.error("❌ Bitte eine Frage eingeben")
            else:
                # Add user message to history
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                
                with st.spinner("Denke nach..."):
                    try:
                        chatbot = ChatBot()
                        result = chatbot.chat_with_internet(user_input)
                        
                        if result["success"]:
                            # Add assistant response to history
                            st.session_state.chat_history.append({"role": "assistant", "content": result["response"]})
                            
                            if result.get("used_web_search"):
                                st.session_state.chat_history.append({"role": "system", "content": "🔍 Internet-Suche wurde verwendet"})
                            
                            st.rerun()
                        else:
                            st.error(f"❌ Fehler: {result['error']}")
                    except Exception as e:
                        st.error(f"❌ Fehler: {str(e)}")
    
    with col2:
        if st.button("🗑️ Chat löschen", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

elif page == "🎨 Bild KI":
    st.markdown('<div class="main-header">🎨 Bild KI</div>', unsafe_allow_html=True)
    st.markdown("Generiere neue Bilder oder bearbeite vorhandene mit KI")
    
    mode = st.radio(
        "Modus wählen:",
        ["🎨 Generieren", "✏️ Bearbeiten"],
        horizontal=True
    )
    
    if mode == "🎨 Generieren":
        st.subheader("Bild generieren")
        
        prompt = st.text_area(
            "Bildbeschreibung:",
            placeholder="z.B. Ein futuristisches Stadtbild bei Sonnenuntergang mit fliegenden Autos...",
            height=100
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            size = st.selectbox("Größe:", ["1024x1024", "1792x1024", "1024x1792"])
        with col2:
            style = st.selectbox("Stil:", ["vivid", "natural"])
        with col3:
            quality = st.selectbox("Qualität:", ["standard", "hd"])
        
        if st.button("🎨 Bild generieren", use_container_width=True):
            if not st.session_state.api_key:
                st.error("❌ Kein API Key konfiguriert. Bitte wende dich an den Admin.")
            elif not prompt.strip():
                st.error("❌ Bitte eine Bildbeschreibung eingeben")
            else:
                with st.spinner("Generiere Bild..."):
                    try:
                        client = OpenAIClient()
                        result = client.generate_image(prompt, size, quality, style)
                        
                        if result["success"]:
                            st.success("✅ Bild erfolgreich generiert!")
                            
                            for i, img in enumerate(result["images"]):
                                st.image(img["url"], caption=f"Generiertes Bild {i+1}")
                                st.markdown(f"**Revised Prompt:** {img['revised_prompt']}")
                                
                                # Add to session state
                                st.session_state.generated_images.append(img["url"])
                        else:
                            st.error(f"❌ Fehler: {result['error']}")
                    except Exception as e:
                        st.error(f"❌ Fehler: {str(e)}")
    
    else:  # Bearbeiten
        st.subheader("Bild bearbeiten")
        
        uploaded_file = st.file_uploader(
            "Bild hochladen:",
            type=["png", "jpg", "jpeg", "webp"]
        )
        
        if uploaded_file:
            st.image(uploaded_file, caption="Hochgeladenes Bild", use_column_width=True)
            
            edit_prompt = st.text_area(
                "Bearbeitungsbeschreibung:",
                placeholder="z.B. Füge einen Sonnenuntergang hinzu, ändere die Farbe des Himmels...",
                height=100
            )
            
            if st.button("✏️ Bild bearbeiten", use_container_width=True):
                if not st.session_state.api_key:
                    st.error("❌ Kein API Key konfiguriert. Bitte wende dich an den Admin.")
                elif not edit_prompt.strip():
                    st.error("❌ Bitte eine Bearbeitungsbeschreibung eingeben")
                else:
                    with st.spinner("Bearbeite Bild..."):
                        try:
                            client = OpenAIClient()
                            image_data = uploaded_file.getvalue()
                            result = client.edit_image(image_data, edit_prompt)
                            
                            if result["success"]:
                                st.success("✅ Bild erfolgreich bearbeitet!")
                                
                                for i, img in enumerate(result["images"]):
                                    st.image(img["url"], caption=f"Bearbeitetes Bild {i+1}")
                                    
                                    # Add to session state
                                    st.session_state.generated_images.append(img["url"])
                            else:
                                st.error(f"❌ Fehler: {result['error']}")
                        except Exception as e:
                            st.error(f"❌ Fehler: {str(e)}")
    
    # Display generated images gallery
    if st.session_state.generated_images:
        st.markdown("---")
        st.subheader("🖼️ Generierte Bilder Galerie")
        
        cols = st.columns(min(3, len(st.session_state.generated_images)))
        for i, img_url in enumerate(st.session_state.generated_images):
            with cols[i % 3]:
                st.image(img_url, use_column_width=True)
        
        if st.button("🗑️ Galerie leeren"):
            st.session_state.generated_images = []
            st.rerun()

elif page == "👥 Benutzer verwalten":
    st.markdown('<div class="main-header">👥 Benutzer verwalten</div>', unsafe_allow_html=True)
    
    # Nur Admin darf Benutzer verwalten
    if not auth_manager.is_admin(current_user):
        st.error("❌ Nur Admins dürfen Benutzer verwalten")
    else:
        st.subheader("Alle Benutzer")
        
        users = auth_manager.get_all_users()
        
        if users:
            # Benutzer in einer Tabelle anzeigen
            user_data = []
            for username, user_info in users.items():
                user_data.append({
                    "Benutzername": username,
                    "Rolle": user_info["role"],
                    "Aktionen": f"{'⭐ Admin' if user_info['role'] == 'admin' else '👤 User'}"
                })
            
            st.dataframe(user_data, use_container_width=True)
            
            # Neuen Benutzer erstellen (Admin-Funktion)
            st.markdown("---")
            st.subheader("Neuen Benutzer erstellen")
            
            admin_username = st.text_input("Benutzername", placeholder="Neuer Benutzername", key="admin_new_username")
            admin_password = st.text_input("Passwort", type="password", placeholder="Passwort", key="admin_new_password")
            admin_role = st.selectbox("Rolle", ["user", "admin"], key="admin_new_role")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("➕ Benutzer erstellen", use_container_width=True):
                    if admin_username and admin_password:
                        success, message = auth_manager.add_user(admin_username, admin_password, admin_role)
                        if success:
                            st.success(f"✅ {message}")
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
                    else:
                        st.error("❌ Bitte Benutzername und Passwort eingeben")
            
            with col2:
                if st.button("🔄 Benutzerliste aktualisieren", use_container_width=True):
                    st.rerun()
        else:
            st.info("ℹ️ Keine Benutzer gefunden (außer Admin)")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>💡 Tipp: Du kannst einen OpenAI API Key von <a href='https://platform.openai.com/api-keys' target='_blank'>OpenAI Platform</a> erhalten</p>
    <p>🔒 Dein API Key wird lokal gespeichert und niemals an Dritte weitergegeben</p>
    <p>🤖 <strong>Chat Magnus</strong> - Dein persönlicher KI-Assistent</p>
</div>
""", unsafe_allow_html=True)