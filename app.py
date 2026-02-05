import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import random
import math
from datetime import datetime, timedelta
import streamlit.components.v1 as components
import qrcode
from io import BytesIO
import base64
from supabase import create_client, Client
import json

# ==========================================
# 0. SUPABASE CONFIGURATION
# ==========================================
SUPABASE_URL = "https://skycmsmjgfqsphasilba.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNreWNtc21qZ2Zxc3BoYXNpbGJhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAyMjU0ODksImV4cCI6MjA4NTgwMTQ4OX0.zks6TXbA3LLYuOBuNSnj2UU46stlpfnz4BZd3u1U95o"

@st.cache_resource
def init_supabase():
    """Initialize and cache the Supabase client connection."""
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        return None

supabase: Client = init_supabase()

# ==========================================
# 1. TRANSLATION MATRIX (ENGLISH / HINDI / PUNJABI)
# ==========================================
TRANSLATIONS = {
    "English": {
        "app_name": "NabhaSeva AI",
        "tagline": "Clinical OS v7.2 + Intelligent Ops",
        "role_patient": "PATIENT",
        "role_patient_desc": "Triage & Booking",
        "role_staff": "STAFF",
        "role_staff_desc": "Roster & Queue",
        "role_volunteer": "VOLUNTEER",
        "role_volunteer_desc": "Join the Mission",
        "btn_login": "Login",
        "btn_apply": "Apply / Login",
        "login_header": "Login Portal",
        "username": "Username / ID",
        "password": "Password",
        "auth_btn": "Authenticate System",
        "return_btn": "← Return",
        "dash_triage": "🩺 AI Triage",
        "dash_book": "Book Appointment",
        "dash_mobile": "🚚 Mobile Clinic Tracker",
        "symptoms_label": "Select Symptoms",
        "analyze_btn": "Analyze Condition",
        "emergency_alert": "CRITICAL EMERGENCY DETECTED",
        "urgent_alert": "URGENT ATTENTION NEEDED",
        "stable_alert": "STABLE / LOW SEVERITY",
        "roster_control": "Roster Control",
        "queue_monitor": "Patient Queue",
        "admin_ops": "Hospital Ops",
        "admin_analytics": "Analytics",
        "admin_logistics": "Fleet & Routes",
        "stock_alert": "CRITICAL STOCK ALERT",
        "vol_pending": "Pending Applications",
        "vol_approve": "Approve & Assign",
        "vol_reject": "Reject",
        "lang_select": "Select Language / भाषा चुनें / ਭਾਸ਼ਾ ਚੁਣੋ",
        "route_plan_btn": "Generate Optimal Route",
        "village_select": "Select Target Villages",
        "eta_label": "Estimated Arrival",
        "distance_label": "Total Distance",
        "unit_status": "Unit Status",
        "add_unit_header": "Commission New Mobile Unit",
        "add_unit_btn": "Add to Fleet",
        "history_tab": "My Medical Records"
    },
    "Hindi": {
        "app_name": "नाभा सेवा एआई",
        "tagline": "क्लिनिकल ओएस v7.2 + इंटेलिजेंट ऑप्स",
        "role_patient": "रोगी",
        "role_patient_desc": "जांच और बुकिंग",
        "role_staff": "कर्मचारी",
        "role_staff_desc": "रोस्टर और कतार",
        "role_volunteer": "स्वयंसेवक",
        "role_volunteer_desc": "मिशन में शामिल हों",
        "btn_login": "लॉग इन करें",
        "btn_apply": "आवेदन / लॉग इन",
        "login_header": "लॉगिन पोर्टल",
        "username": "उपयोगकर्ता नाम / आईडी",
        "password": "पासवर्ड",
        "auth_btn": "सिस्टम प्रमाणित करें",
        "return_btn": "← वापस",
        "dash_triage": "🩺 एआई जांच",
        "dash_book": "नियुक्ति बुक करें",
        "dash_mobile": "🚚 मोबाइल क्लिनिक ट्रैकर",
        "symptoms_label": "लक्षण चुनें",
        "analyze_btn": "स्थिति का विश्लेषण करें",
        "emergency_alert": "गंभीर आपातकाल का पता चला",
        "urgent_alert": "तत्काल ध्यान देने की आवश्यकता",
        "stable_alert": "स्थिर / कम गंभीरता",
        "roster_control": "रोस्टर नियंत्रण",
        "queue_monitor": "रोगी कतार",
        "admin_ops": "अस्पताल संचालन",
        "admin_analytics": "एनालिटिक्स",
        "admin_logistics": "बेड़े और मार्ग",
        "stock_alert": "महत्वपूर्ण स्टॉक चेतावनी",
        "vol_pending": "लंबित आवेदन",
        "vol_approve": "स्वीकार और असाइन करें",
        "vol_reject": "अस्वीकार",
        "lang_select": "भाषा चुनें",
        "route_plan_btn": "इष्टतम मार्ग उत्पन्न करें",
        "village_select": "लक्षित गांव चुनें",
        "eta_label": "अनुमानित आगमन",
        "distance_label": "कुल दूरी",
        "unit_status": "यूनिट स्थिति",
        "add_unit_header": "नई मोबाइल यूनिट जोड़ें",
        "add_unit_btn": "बेड़े में जोड़ें",
        "history_tab": "मेरे मेडिकल रिकॉर्ड"
    },
    "Punjabi": {
        "app_name": "ਨਾਭਾ ਸੇਵਾ ਏ.ਆਈ",
        "tagline": "ਕਲੀਨਿਕਲ ਓਪਰੇਟਿੰਗ ਸਿਸਟਮ v7.2",
        "role_patient": "ਮਰੀਜ਼",
        "role_patient_desc": "ਜਾਂਚ ਅਤੇ ਬੁਕਿੰਗ",
        "role_staff": "ਸਟਾਫ",
        "role_staff_desc": "ਰੋਸਟਰ ਅਤੇ ਕਤਾਰ",
        "role_volunteer": "ਵਲੰਟੀਅਰ",
        "role_volunteer_desc": "ਮਿਸ਼ਨ ਵਿੱਚ ਸ਼ਾਮਲ ਹੋਵੋ",
        "btn_login": "ਲੌਗ ਇਨ ਕਰੋ",
        "btn_apply": "ਅਪਲਾਈ / ਲੌਗ ਇਨ",
        "login_header": "ਲਾਗਇਨ ਪੋਰਟਲ",
        "username": "ਯੂਜ਼ਰ ਨਾਮ / ਆਈ.ਡੀ",
        "password": "ਪਾਸਵਰਡ",
        "auth_btn": "ਸਿਸਟਮ ਪ੍ਰਮਾਣਿਤ ਕਰੋ",
        "return_btn": "← ਵਾਪਸ",
        "dash_triage": "🩺 ਏ.ਆਈ ਜਾਂਚ",
        "dash_book": "ਮੁਲਾਕਾਤ ਬੁੱਕ ਕਰੋ",
        "dash_mobile": "🚚 ਮੋਬਾਈਲ ਕਲੀਨਿਕ ਟਰੈਕਰ",
        "symptoms_label": "ਲੱਛਣ ਚੁਣੋ",
        "analyze_btn": "ਸਥਿਤੀ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਕਰੋ",
        "emergency_alert": "ਗੰਭੀਰ ਐਮਰਜੈਂਸੀ",
        "urgent_alert": "ਤੁਰੰਤ ਧਿਆਨ ਦੀ ਲੋੜ ਹੈ",
        "stable_alert": "ਸਥਿਰ / ਘੱਟ ਗੰਭੀਰਤਾ",
        "roster_control": "ਰੋਸਟਰ ਕੰਟਰੋਲ",
        "queue_monitor": "ਮਰੀਜ਼ ਕਤਾਰ",
        "admin_ops": "ਹਸਪਤਾਲ ਓਪਰੇਸ਼ਨ",
        "admin_analytics": "ਵਿਸ਼ਲੇਸ਼ਣ",
        "admin_logistics": "ਰੂਟ ਪਲੈਨਿੰਗ",
        "stock_alert": "ਨਾਜ਼ੁਕ ਸਟਾਕ ਚੇਤਾਵਨੀ",
        "vol_pending": "ਬਕਾਇਆ ਅਰਜ਼ੀਆਂ",
        "vol_approve": "ਮਨਜ਼ੂਰ ਅਤੇ ਨਿਯੁਕਤ ਕਰੋ",
        "vol_reject": "ਰੱਦ ਕਰੋ",
        "lang_select": "ਭਾਸ਼ਾ ਚੁਣੋ",
        "route_plan_btn": "ਰੂਟ ਤਿਆਰ ਕਰੋ",
        "village_select": "ਪਿੰਡ ਚੁਣੋ",
        "eta_label": "ਪਹੁੰਚਣ ਦਾ ਸਮਾਂ",
        "distance_label": "ਕੁੱਲ ਦੂਰੀ",
        "unit_status": "ਯੂਨਿਟ ਸਥਿਤੀ",
        "add_unit_header": "ਨਵੀਂ ਮੋਬਾਈਲ ਯੂਨਿਟ ਸ਼ਾਮਲ ਕਰੋ",
        "add_unit_btn": "ਸ਼ਾਮਲ ਕਰੋ",
        "history_tab": "ਮੇਰੇ ਮੈਡੀਕਲ ਰਿਕਾਰਡ"
    }
}

# ==========================================
# 2. SYSTEM CONFIGURATION & STATE
# ==========================================
st.set_page_config(
    page_title="NabhaSeva AI | Clinical OS v7.2",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if 'language' not in st.session_state: st.session_state.language = "English"
if 'page' not in st.session_state: st.session_state.page = "landing"
if 'selected_role' not in st.session_state: st.session_state.selected_role = None
if 'user' not in st.session_state: st.session_state.user = None
if 'chat_log' not in st.session_state: st.session_state.chat_log = []
if 'last_booking_qr' not in st.session_state: st.session_state.last_booking_qr = None
if 'analysis_done' not in st.session_state: st.session_state.analysis_done = False
if 'active_route' not in st.session_state: st.session_state.active_route = None

def T(key):
    """Translation Helper Function"""
    lang = st.session_state.language
    return TRANSLATIONS.get(lang, TRANSLATIONS["English"]).get(key, key)

# ==========================================
# 3. CSS ENGINE (GLASSMORPHISM UI)
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Gurmukhi:wght@400;700&display=swap');
    
    /* Global Reset */
    header, footer { visibility: hidden; height: 0; }
    [data-testid="stHeader"] { background-color: transparent; z-index: 1; }
    .block-container { padding-top: 2rem !important; }
    
    /* Typography & Background */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Noto Sans Devanagari', 'Noto Sans Gurmukhi', sans-serif;
        background-color: #020408;
        color: #ffffff;
    }

    .stApp {
        background: 
            linear-gradient(135deg, rgba(2, 4, 8, 0.95) 0%, rgba(10, 25, 47, 0.9) 100%),
            url('https://images.unsplash.com/photo-1516549655169-df83a0674503?auto=format&fit=crop&q=80&w=2000');
        background-size: cover;
        background-attachment: fixed;
    }

    /* Cards & Glass Panels */
    .role-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2.5rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: 100%;
        cursor: pointer;
    }
    .role-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0, 242, 254, 0.2);
        border-color: #00f2fe;
        background: rgba(255, 255, 255, 0.07);
    }

    .glass-panel {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 2rem;
        border-radius: 24px;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* Bed Management Grid */
    .bed-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
        gap: 10px;
        margin-top: 15px;
    }
    .bed-box {
        padding: 15px;
        text-align: center;
        border-radius: 12px;
        font-weight: bold;
        cursor: pointer;
        transition: 0.2s;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .bed-avail { background-color: rgba(0, 255, 127, 0.2); color: #00ff7f; }
    .bed-occ { background-color: rgba(255, 75, 75, 0.2); color: #ff4b4b; }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%) !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        padding: 0.8rem 1.5rem !important;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        box-shadow: 0 0 25px rgba(0, 242, 254, 0.6);
        transform: translateY(-2px);
        color: #fff !important;
    }
    
    /* Emergency Alert Styles */
    .emergency-alert {
        background: rgba(220, 38, 38, 0.9);
        color: white;
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #ff0000;
        animation: pulse 2s infinite;
        text-align: center;
        margin-bottom: 15px;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .priority-high { color: #ff4b4b; font-weight: bold; }
    .priority-med { color: #ffa500; font-weight: bold; }
    .priority-low { color: #00ff7f; font-weight: bold; }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(255, 0, 0, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0); }
    }

    /* Titles */
    .hero-title {
        font-size: 4.5rem;
        background: linear-gradient(to right, #ffffff, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 40px rgba(0, 242, 254, 0.3);
    }
    .sub-hero { color: #94a3b8; font-size: 1.3rem; letter-spacing: 2px; }

    /* Chat Interface */
    .chat-user { 
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.2), rgba(0, 242, 254, 0.2)); 
        padding: 15px; 
        border-radius: 20px 20px 0 20px; 
        margin: 10px 0; 
        text-align: right; 
        border: 1px solid rgba(0, 242, 254, 0.3);
    }
    .chat-ai { 
        background: rgba(255, 255, 255, 0.05); 
        padding: 15px; 
        border-radius: 20px 20px 20px 0; 
        margin: 10px 0; 
        text-align: left; 
        border: 1px solid rgba(255,255,255,0.1); 
    }

    /* Language Footer Styling */
    .lang-footer {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: rgba(0,0,0,0.8);
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #333;
        z-index: 9999;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 4. ACCESSIBILITY ENGINE
# ==========================================
def inject_accessibility():
    """
    Injects a floating Accessibility Menu into the main Streamlit app.
    Features: TTS on Hover & UI Magnification.
    """
    components.html("""
    <script>
        const doc = window.parent.document;
        
        // 1. Create the Menu Container
        if (!doc.getElementById('acc-menu')) {
            const menu = doc.createElement('div');
            menu.id = 'acc-menu';
            menu.style.cssText = `
                position: fixed;
                bottom: 20px;
                left: 20px;
                z-index: 999999;
                display: flex;
                flex-direction: column;
                gap: 10px;
                font-family: 'Plus Jakarta Sans', sans-serif;
            `;
            doc.body.appendChild(menu);

            // 2. Main Toggle Button
            const btn = doc.createElement('button');
            btn.innerText = '♿';
            btn.style.cssText = `
                width: 50px;
                height: 50px;
                border-radius: 50%;
                background: linear-gradient(135deg, #00f2fe, #4facfe);
                border: none;
                color: #000;
                font-size: 24px;
                cursor: pointer;
                box-shadow: 0 0 15px rgba(0, 242, 254, 0.5);
                transition: transform 0.2s;
            `;
            btn.onclick = () => {
                const panel = doc.getElementById('acc-panel');
                panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
            };
            menu.appendChild(btn);

            // 3. The Options Panel
            const panel = doc.createElement('div');
            panel.id = 'acc-panel';
            panel.style.cssText = `
                display: none;
                background: rgba(15, 23, 42, 0.95);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 15px;
                border-radius: 15px;
                margin-bottom: 10px;
                color: white;
                width: 200px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            `;
            
            // --- Feature A: Text-to-Speech (TTS) ---
            let ttsEnabled = false;
            const ttsBtn = doc.createElement('button');
            ttsBtn.innerText = '🔊 TTS: OFF';
            ttsBtn.style.cssText = 'width: 100%; padding: 8px; margin-bottom: 8px; background: #334155; color: white; border: none; border-radius: 8px; cursor: pointer;';
            
            const speakHandler = (e) => {
                if (!ttsEnabled) return;
                const text = e.target.innerText || e.target.alt;
                if (text && text.length > 2) {
                    window.parent.speechSynthesis.cancel();
                    const utterance = new SpeechSynthesisUtterance(text);
                    // Attempt to detect language broadly (Hindi/English mix usually works on auto)
                    utterance.rate = 1.0; 
                    window.parent.speechSynthesis.speak(utterance);
                    e.target.style.outline = "2px solid #00f2fe"; // Highlight
                }
            };

            const leaveHandler = (e) => {
                if (!ttsEnabled) return;
                window.parent.speechSynthesis.cancel();
                e.target.style.outline = "none";
            };

            ttsBtn.onclick = () => {
                ttsEnabled = !ttsEnabled;
                ttsBtn.innerText = ttsEnabled ? '🔊 TTS: ON' : '🔊 TTS: OFF';
                ttsBtn.style.background = ttsEnabled ? '#00f2fe' : '#334155';
                ttsBtn.style.color = ttsEnabled ? '#000' : '#fff';
                
                const targets = doc.querySelectorAll('p, h1, h2, h3, span, button, div.stMarkdown, a');
                if (ttsEnabled) {
                    targets.forEach(el => {
                        el.addEventListener('mouseenter', speakHandler);
                        el.addEventListener('mouseleave', leaveHandler);
                    });
                } else {
                    targets.forEach(el => {
                        el.removeEventListener('mouseenter', speakHandler);
                        el.removeEventListener('mouseleave', leaveHandler);
                        el.style.outline = "none";
                    });
                    window.parent.speechSynthesis.cancel();
                }
            };
            panel.appendChild(ttsBtn);

            // --- Feature B: Magnification (Zoom) ---
            let zoomLevel = 1.0;
            const zoomBtn = doc.createElement('button');
            zoomBtn.innerText = '🔍 Zoom: 100%';
            zoomBtn.style.cssText = 'width: 100%; padding: 8px; background: #334155; color: white; border: none; border-radius: 8px; cursor: pointer;';
            
            zoomBtn.onclick = () => {
                if (zoomLevel === 1.0) zoomLevel = 1.1;
                else if (zoomLevel === 1.1) zoomLevel = 1.25;
                else zoomLevel = 1.0;
                
                doc.body.style.zoom = zoomLevel; // Works best in Chrome/Edge
                doc.body.style.transformOrigin = "0 0"; // Fallback for some browsers
                
                zoomBtn.innerText = `🔍 Zoom: ${Math.round(zoomLevel * 100)}%`;
                zoomBtn.style.background = zoomLevel > 1.0 ? '#00f2fe' : '#334155';
                zoomBtn.style.color = zoomLevel > 1.0 ? '#000' : '#fff';
            };
            panel.appendChild(zoomBtn);

            // Assemble
            menu.insertBefore(panel, btn);
        }
    </script>
    """, height=0)

# ==========================================
# 5. DATABASE ENGINE (ROBUST & SAFE)
# ==========================================

# --- SIMULATED GEOSPATIAL DATA ---
# Since we don't have real Google Maps, we simulate a coordinate grid around Nabha.
VILLAGES_DB = {
    "V-01": {"name": "Rohti Chhanna", "lat": 30.38, "lon": 76.12, "pop": 1200, "risk_score": 8},
    "V-02": {"name": "Bhojo Majra", "lat": 30.39, "lon": 76.16, "pop": 800, "risk_score": 3},
    "V-03": {"name": "Thuhi", "lat": 30.35, "lon": 76.10, "pop": 1500, "risk_score": 7},
    "V-04": {"name": "Dhingi", "lat": 30.40, "lon": 76.18, "pop": 950, "risk_score": 4},
    "V-05": {"name": "Sakrali", "lat": 30.34, "lon": 76.19, "pop": 600, "risk_score": 2},
    "V-06": {"name": "Sauja", "lat": 30.36, "lon": 76.20, "pop": 1100, "risk_score": 6},
    "V-07": {"name": "Ageti", "lat": 30.41, "lon": 76.13, "pop": 1300, "risk_score": 9},
    "V-08": {"name": "Borewal", "lat": 30.33, "lon": 76.11, "pop": 700, "risk_score": 5},
    "V-09": {"name": "Kakrala", "lat": 30.37, "lon": 76.08, "pop": 2000, "risk_score": 8},
    "V-10": {"name": "Dhangera", "lat": 30.42, "lon": 76.17, "pop": 500, "risk_score": 1}
}
HOSPITAL_LOC = {"name": "Nabha Civil Hospital", "lat": 30.37, "lon": 76.15}

def db_init():
    """Initializes tables if empty. Handles first-run setup."""
    if not supabase: return
    try:
        # Check Users
        res = supabase.table("users").select("uid").limit(1).execute()
        if not res.data:
            seed_users = [
                {"uid": "admin", "pwd": "123", "role": "Admin", "name": "System Admin"},
                {"uid": "staff", "pwd": "123", "role": "Staff", "name": "Head Nurse"},
                {"uid": "pat", "pwd": "123", "role": "Patient", "name": "Rahul Sharma"}
            ]
            supabase.table("users").insert(seed_users).execute()

        # Check Docs
        res = supabase.table("doctors").select("name").limit(1).execute()
        if not res.data:
            seed_docs = [
                {"name": "Dr. Amrit Pal", "spec": "Cardiologist", "status": "Available", "room": "101", "tokens": 10, "last_token_num": 0, "last_date": ""},
                {"name": "Dr. Simran Kaur", "spec": "Pediatrician", "status": "Available", "room": "202", "tokens": 12, "last_token_num": 0, "last_date": ""},
                {"name": "Dr. Vikas Goyal", "spec": "General Physician", "status": "Available", "room": "204", "tokens": 15, "last_token_num": 0, "last_date": ""},
                {"name": "Dr. Harpreet Singh", "spec": "Orthopedic", "status": "Away", "room": "105", "tokens": 8, "last_token_num": 0, "last_date": ""},
                {"name": "Dr. Anjali Rao", "spec": "Neurologist", "status": "Available", "room": "301", "tokens": 6, "last_token_num": 0, "last_date": ""},
                {"name": "Dr. Sanjay Mehta", "spec": "Dermatologist", "status": "Available", "room": "205", "tokens": 20, "last_token_num": 0, "last_date": ""},
                {"name": "Dr. K. Das", "spec": "ENT Specialist", "status": "Available", "room": "206", "tokens": 15, "last_token_num": 0, "last_date": ""},
                {"name": "Dr. Priya Sharma", "spec": "Gynecologist", "status": "Surgery", "room": "305", "tokens": 10, "last_token_num": 0, "last_date": ""},
                {"name": "Dr. M. Khan", "spec": "Psychiatrist", "status": "Available", "room": "401", "tokens": 8, "last_token_num": 0, "last_date": ""},
                {"name": "Dr. R. Verma", "spec": "Ophthalmologist", "status": "Available", "room": "208", "tokens": 12, "last_token_num": 0, "last_date": ""},
                {"name": "Dr. John Joseph", "spec": "Dentist", "status": "Available", "room": "G02", "tokens": 15, "last_token_num": 0, "last_date": ""}
            ]
            supabase.table("doctors").insert(seed_docs).execute()

        # Check Inventory
        res = supabase.table("inventory").select("item").limit(1).execute()
        if not res.data:
            seed_inv = [
                {"item": "Oxygen Cylinders", "quantity": 45},
                {"item": "Paracetamol", "quantity": 500},
                {"item": "Insulin", "quantity": 20},
                {"item": "Bandages", "quantity": 150},
                {"item": "Syringes", "quantity": 1000}
            ]
            supabase.table("inventory").insert(seed_inv).execute()
        
        # Check Beds
        res = supabase.table("beds").select("bed_id").limit(1).execute()
        if not res.data:
            seed_beds = []
            bed_map = {
                "ICU-01": "Available", "ICU-02": "Occupied", "ICU-03": "Available",
                "W-101": "Occupied", "W-102": "Available", "W-103": "Occupied", "W-104": "Available",
                "W-201": "Occupied", "W-202": "Available", "W-203": "Available"
            }
            for k, v in bed_map.items():
                seed_beds.append({"bed_id": k, "status": v})
            supabase.table("beds").insert(seed_beds).execute()

        # Check Mobile Units
        # Table Schema: unit_name (text), driver (text), status (text), current_route (jsonb)
        try:
            res = supabase.table("mobile_units").select("unit_name").limit(1).execute()
            if not res.data:
                seed_units = [
                    {"unit_name": "MHU-Alpha", "driver": "Ram Singh", "status": "Idle", "current_route": {}},
                    {"unit_name": "MHU-Beta", "driver": "Karan Kumar", "status": "Idle", "current_route": {}}
                ]
                supabase.table("mobile_units").insert(seed_units).execute()
        except: pass

    except Exception as e:
        pass

def db_io(key, data=None, action="read"):
    """
    Robust Database Handler.
    """
    if not supabase: return {} if action == "read" else None
    
    try:
        # ------------------ READ OPERATIONS ------------------
        if action == "read":
            if key == "users":
                res = supabase.table("users").select("*").execute()
                return {row['uid']: row for row in res.data} if res.data else {}
            
            elif key == "docs":
                res = supabase.table("doctors").select("*").execute()
                return {row['name']: row for row in res.data} if res.data else {}
            
            elif key == "inv":
                res = supabase.table("inventory").select("*").execute()
                return {row['item']: row['quantity'] for row in res.data} if res.data else {}
            
            elif key == "beds":
                res = supabase.table("beds").select("*").execute()
                return {row['bed_id']: row['status'] for row in res.data} if res.data else {}
            
            elif key == "hist":
                try:
                    res = supabase.table("history").select("*").execute()
                    if not res.data: return []
                    formatted = []
                    for r in res.data:
                        formatted.append({
                            "Date": r.get('date', ''), 
                            "Time": r.get('time', ''), 
                            "Patient": r.get('patient', ''), 
                            "Doctor": r.get('doctor', ''), 
                            "Token": r.get('token', ''), 
                            "Specialty": r.get('specialty', ''),
                            "Priority": r.get('priority', 'Low')
                        })
                    return formatted
                except:
                    return []
            
            elif key == "vols":
                try:
                    res = supabase.table("volunteers").select("*").execute()
                    return res.data if res.data else []
                except: return []

            elif key == "mobile_units":
                try:
                    res = supabase.table("mobile_units").select("*").execute()
                    return res.data if res.data else []
                except: return []

        # ------------------ WRITE OPERATIONS ------------------
        elif action == "write":
            if key == "users":
                rows = [{"uid": k, **v} for k, v in data.items()]
                supabase.table("users").upsert(rows).execute()
                
            elif key == "docs":
                rows = [{"name": k, **v} for k, v in data.items()]
                supabase.table("doctors").upsert(rows).execute()
                
            elif key == "inv":
                rows = [{"item": k, "quantity": v} for k, v in data.items()]
                supabase.table("inventory").upsert(rows).execute()
            
            elif key == "beds":
                rows = [{"bed_id": k, "status": v} for k, v in data.items()]
                supabase.table("beds").upsert(rows).execute()

            elif key == "hist":
                if data and isinstance(data, dict):
                    row = {
                        "date": data.get("Date"), "time": data.get("Time"), "patient": data.get("Patient"),
                        "doctor": data.get("Doctor"), "token": data.get("Token"), "specialty": data.get("Specialty"),
                        "priority": data.get("Priority", "Low")
                    }
                    supabase.table("history").insert(row).execute()

            elif key == "vols":
                if data: supabase.table("volunteers").insert(data).execute()

            elif key == "vols_update":
                if data: supabase.table("volunteers").update({"status": data['status']}).eq("id", data['id']).execute()

            # --- UPDATE MOBILE UNITS ---
            elif key == "units_update":
                if data: supabase.table("mobile_units").update({"current_route": data['current_route'], "status": data['status']}).eq("id", data['id']).execute()
            
            # --- NEW: ADD NEW MOBILE UNIT ---
            elif key == "units_add":
                if data: supabase.table("mobile_units").insert(data).execute()

    except Exception as e:
        print(f"DB Error ({key}): {e}")
        return {} if action == "read" else None

# Initialize DB on load
db_init()

# ==========================================
# 6. INTELLIGENT LOGIC MODULES
# ==========================================

def get_qr_code(data_str):
    """Generate QR Code as Base64 string"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data_str)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def get_smart_response(user_input, docs_data=None):
    """
    Enhanced Context-Aware Smart AI.
    Now connects to LIVE DB for beds, mobile units, and inventory.
    """
    q = user_input.lower().strip()
    
    # --- REAL-TIME DATA FETCH ---
    beds = db_io("beds")
    inv = db_io("inv")
    units = db_io("mobile_units")
    
    # 1. BED AVAILABILITY
    if any(x in q for x in ['bed', 'icu', 'ward', 'vacant']):
        avail_icu = sum(1 for k, v in beds.items() if 'ICU' in k and v == 'Available')
        avail_ward = sum(1 for k, v in beds.items() if 'W' in k and v == 'Available')
        return f"🏥 **Bed Status:**\n- ICU Beds Free: **{avail_icu}**\n- General Ward Beds Free: **{avail_ward}**\nPlease proceed to reception for admission."

    # 2. MOBILE CLINIC STATUS
    if any(x in q for x in ['mobile', 'clinic', 'van', 'vehicle', 'mhu']):
        active = [u for u in units if u.get('status') == 'En Route']
        if not active:
            return "🚚 No Mobile Clinics are currently active on routes. They are stationed at the Hospital."
        msg = "🚚 **Active Mobile Units:**\n"
        for u in active:
            route_name = "Unknown Route"
            # Try to get first stop name
            try:
                if u['current_route'] and u['current_route']['path']:
                    route_name = f"Towards {u['current_route']['path'][1]['name']}" 
            except: pass
            msg += f"- **{u['unit_name']}**: {route_name}\n"
        return msg

    # 3. DOCTOR AVAILABILITY
    if any(x in q for x in ['doctor', 'dr.', 'available', 'cardiologist', 'specialist']):
        if not docs_data: docs_data = db_io("docs")
        found_docs = []
        for name, info in docs_data.items():
            if name.lower().split()[-1] in q or name.lower() in q or info['spec'].lower() in q:
                found_docs.append((name, info))
        
        if found_docs:
            resp = ""
            for name, info in found_docs:
                status_icon = "🟢" if info['status'] == "Available" else "🔴"
                resp += f"{status_icon} **{name}** ({info['spec']}) is **{info['status']}** (Room {info['room']})\n"
            return resp
        elif 'list' in q or 'who' in q:
             resp = "Current Medical Roster:\n\n"
             for name, info in docs_data.items():
                icon = "🟢" if info['status'] == "Available" else "🔴"
                resp += f"{icon} **{name}** ({info['spec']})\n"
             return resp

    # 4. GREETINGS
    if any(x in q for x in ['hi', 'hello', 'hey', 'start']):
        return "Hello! I am the NabhaSeva Intelligent Assistant. I can check **ICU beds**, **locate mobile clinics**, or find **doctors** for you. What do you need?"
    
    return "I can help with Hospital Logistics. Try asking: 'Are ICU beds available?', 'Where is the mobile van?', or 'Is the Cardiologist in?'"

def triage_logic(symptoms):
    """Advanced Triage Logic."""
    if not symptoms: return "General Physician", "Low", "No symptoms selected."
    
    critical_sx = ["Chest Pain", "Breathlessness", "Uncontrolled Bleeding", "Seizures", "Severe Head Trauma", "Sudden Vision Loss"]
    if any(x in symptoms for x in critical_sx):
        if "Chest Pain" in symptoms or "Breathlessness" in symptoms: 
            return "Cardiologist", "High", "Suspected Cardiac Event. IMMEDIATE attention required."
        if "Seizures" in symptoms or "Severe Head Trauma" in symptoms: 
            return "Neurologist", "High", "Critical Neurological Event. IMMEDIATE attention required."
        return "Emergency Unit", "High", "Critical Condition. Proceed to ER immediately."

    urgent_sx = ["High Fever (>103)", "Fracture", "Deep Cut", "Severe Headache", "Eye Pain", "Blurred Vision", "Ear Pain"]
    if any(x in symptoms for x in urgent_sx):
        if "Fracture" in symptoms: return "Orthopedic", "Med", "Possible fracture. X-Ray required."
        if "Eye Pain" in symptoms or "Blurred Vision" in symptoms: return "Ophthalmologist", "Med", "Eye injury requires urgent check."
        if "Severe Headache" in symptoms: return "Neurologist", "Med", "Migraine or Neuro issue."
        return "General Physician", "Med", "Urgent consultation recommended."

    mapping = {
        "Skin Rash": "Dermatologist", "Itching": "Dermatologist", "Acne": "Dermatologist",
        "Bone Pain": "Orthopedic", "Back Pain": "Orthopedic",
        "Dizziness": "Neurologist", "Sore Throat": "ENT Specialist",
        "Toothache": "Dentist", "Gum Bleeding": "Dentist",
        "Pregnancy Checkup": "Gynecologist", "Period Pain": "Gynecologist",
        "Anxiety": "Psychiatrist", "Depression": "Psychiatrist", "Insomnia": "Psychiatrist",
        "Child Fever": "Pediatrician", "Child Cough": "Pediatrician",
        "Mild Fever": "General Physician", "Cough": "General Physician"
    }
    
    found_spec = "General Physician"
    for s, doc in mapping.items():
        if s in symptoms: 
            found_spec = doc
            break 
            
    return found_spec, "Low", "Condition appears stable. Consider Home Care or booking a later slot."

# ==========================================
# 7. ROUTE PLANNING & LOGISTICS ENGINE
# ==========================================

def calculate_distance(p1, p2):
    return math.sqrt((p1['lat'] - p2['lat'])**2 + (p1['lon'] - p2['lon'])**2)

def generate_optimal_route(target_villages_keys):
    if not target_villages_keys: return None
    route_path = []
    current_node = HOSPITAL_LOC
    unvisited = [v_key for v_key in target_villages_keys]
    total_dist = 0
    route_path.append({"name": "Hospital (Start)", "lat": HOSPITAL_LOC['lat'], "lon": HOSPITAL_LOC['lon'], "type": "Hub"})
    
    while unvisited:
        nearest_v = None
        min_dist = float('inf')
        for v_key in unvisited:
            v_data = VILLAGES_DB[v_key]
            dist = calculate_distance(current_node, v_data)
            if dist < min_dist:
                min_dist = dist
                nearest_v = v_key
        if nearest_v:
            v_data = VILLAGES_DB[nearest_v]
            route_path.append({"name": v_data['name'], "lat": v_data['lat'], "lon": v_data['lon'], "type": "Stop"})
            total_dist += min_dist
            current_node = v_data
            unvisited.remove(nearest_v)
            
    dist_back = calculate_distance(current_node, HOSPITAL_LOC)
    total_dist += dist_back
    route_path.append({"name": "Hospital (End)", "lat": HOSPITAL_LOC['lat'], "lon": HOSPITAL_LOC['lon'], "type": "Hub"})
    return route_path, round(total_dist * 111, 2)

def render_route_map(route_data):
    lats = [p['lat'] for p in route_data]
    lons = [p['lon'] for p in route_data]
    names = [p['name'] for p in route_data]
    fig = go.Figure()
    fig.add_trace(go.Scattermapbox(mode="markers+lines", lon=lons, lat=lats, marker={'size': 12, 'color': '#00f2fe'}, line={'width': 3, 'color': '#00f2fe'}, text=names, name="Route"))
    fig.add_trace(go.Scattermapbox(mode="markers", lon=[lons[0]], lat=[lats[0]], marker={'size': 15, 'color': 'white', 'symbol': 'hospital'}, text=["Hospital"], name="Base"))
    fig.update_layout(margin ={'l':0,'t':0,'b':0,'r':0}, mapbox = {'center': {'lon': 76.15, 'lat': 30.37}, 'style': "carto-darkmatter", 'zoom': 11}, height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

# --- NEW: VOLUNTEER ASSIGNMENT ALGORITHM ---
def find_doctor_needing_help():
    """
    Finds the doctor with the highest patient load today.
    Returns: Name of Doctor (str), Load Count (int)
    """
    docs = db_io("docs")
    if not docs: return None, 0
    
    # Check patient load via 'last_token_num' which represents patients served/booked today
    # Convert dict to list of (name, tokens_served)
    load_list = []
    for d_name, info in docs.items():
        load = info.get('last_token_num', 0)
        load_list.append((d_name, load))
    
    if not load_list: return None, 0
    
    # Sort by load descending
    load_list.sort(key=lambda x: x[1], reverse=True)
    
    # Logic: Get max load value
    max_load = load_list[0][1]
    
    # Find all doctors with this max load (handle ties)
    candidates = [d for d in load_list if d[1] == max_load]
    
    # Pick random if tie
    chosen = random.choice(candidates)
    return chosen[0], chosen[1]

# ==========================================
# 8. SESSION & STATE MANAGEMENT
# ==========================================

def perform_logout():
    st.session_state.user = None
    st.session_state.page = "landing"
    st.session_state.selected_role = None
    st.session_state.chat_log = []
    st.session_state.last_booking_qr = None
    st.session_state.analysis_done = False
    st.session_state.active_route = None
    st.rerun()

def render_language_selector():
    st.markdown("---")
    c_spacer, c_lang = st.columns([8, 2])
    with c_lang:
        new_lang = st.selectbox(
            T("lang_select"), 
            ["English", "Hindi", "Punjabi"], 
            key="global_lang_selector",
            index=["English", "Hindi", "Punjabi"].index(st.session_state.language)
        )
        if new_lang != st.session_state.language:
            st.session_state.language = new_lang
            st.rerun()

# ==========================================
# 9. VIEWS & COMPONENTS
# ==========================================

def render_landing():
    inject_accessibility()
    c_top, c_admin = st.columns([10, 1.5])
    with c_admin:
        st.markdown('<div class="admin-btn">', unsafe_allow_html=True)
        if st.button("🔐 Admin HQ", key="admin_entry"):
            st.session_state.selected_role = "Admin"
            st.session_state.page = "auth"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 10vh'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown(
            f"<div style='text-align:center'>"
            f"<h1 class='hero-title'>{T('app_name')}</h1>"
            f"<p class='sub-hero'>{T('tagline')}</p>"
            f"</div>", 
            unsafe_allow_html=True
        )
    
    st.markdown("<div style='height: 8vh'></div>", unsafe_allow_html=True)
    _, col_pat, col_staff, col_vol, _ = st.columns([0.5, 2, 2, 2, 0.5])
    
    with col_pat:
        st.markdown(
            f"<div class='role-card'>"
            f"<div style='font-size:3.5rem; margin-bottom:10px'>🧬</div>"
            f"<h3>{T('role_patient')}</h3>"
            f"<p style='color:#aaa'>{T('role_patient_desc')}</p>"
            f"</div>", unsafe_allow_html=True
        )
        if st.button(f"{T('role_patient')} {T('btn_login')}", use_container_width=True):
            st.session_state.selected_role = "Patient"
            st.session_state.page = "auth"
            st.rerun()

    with col_staff:
        st.markdown(
            f"<div class='role-card'>"
            f"<div style='font-size:3.5rem; margin-bottom:10px'>🩺</div>"
            f"<h3>{T('role_staff')}</h3>"
            f"<p style='color:#aaa'>{T('role_staff_desc')}</p>"
            f"</div>", unsafe_allow_html=True
        )
        if st.button(f"{T('role_staff')} {T('btn_login')}", use_container_width=True):
            st.session_state.selected_role = "Staff"
            st.session_state.page = "auth"
            st.rerun()

    with col_vol:
        st.markdown(
            f"<div class='role-card' style='border-color: #00ff7f;'>"
            f"<div style='font-size:3.5rem; margin-bottom:10px'>🤝</div>"
            f"<h3>{T('role_volunteer')}</h3>"
            f"<p style='color:#aaa'>{T('role_volunteer_desc')}</p>"
            f"</div>", unsafe_allow_html=True
        )
        if st.button(T('btn_apply'), use_container_width=True):
            st.session_state.selected_role = "Volunteer"
            st.session_state.page = "auth"
            st.rerun()
    
    render_language_selector()

def render_auth():
    inject_accessibility()
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<div style='height:10vh'></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='glass-panel'><h2 style='text-align:center; color:#00f2fe'>{T('login_header')}: {st.session_state.selected_role}</h2>", unsafe_allow_html=True)
        
        if st.session_state.selected_role == "Volunteer":
            v_tabs = st.tabs(["📝 Apply Now", "🔐 Existing Login"])
            
            with v_tabs[0]:
                st.info("Help us solve the staff shortage. Join NabhaSeva.")
                with st.form("vol_app_form"):
                    v_name = st.text_input("Full Name")
                    v_role = st.selectbox("Preferred Role", ["Visiting Doctor", "Nurse Assistant", "Data Entry", "Pharmacist Helper"])
                    v_exp = st.text_area("Experience / Qualifications")
                    v_contact = st.text_input("Phone / Email")
                    v_reason = st.text_area("Why do you want to join?")
                    
                    if st.form_submit_button("Submit Application"):
                        if v_name and v_contact:
                            payload = {
                                "full_name": v_name, "role": v_role, "experience": v_exp,
                                "contact": v_contact, "why_join": v_reason, "status": "Pending"
                            }
                            db_io("vols", payload, "write")
                            st.success("Application Submitted! Admin will review shortly.")
                        else:
                            st.error("Name and Contact are required.")
            
            with v_tabs[1]:
                uid = st.text_input("Volunteer ID", key="vl_uid")
                pwd = st.text_input(T("password"), type="password", key="vl_pwd")
                if st.button(T("btn_login"), use_container_width=True):
                    users = db_io("users")
                    if uid in users and users[uid]['pwd'] == pwd:
                        st.session_state.user = users[uid]['name']
                        st.session_state.page = "dashboard"
                        st.session_state.selected_role = "Staff" 
                        st.rerun()
                    else:
                        st.error("Invalid or Not Approved yet.")

        elif st.session_state.selected_role in ["Admin", "Staff"]:
            tabs = st.tabs(["🔐 Secure Login"])
            active_tab = tabs[0]
            show_register = False
            
            with active_tab:
                uid = st.text_input(T("username"), key="l_uid")
                pwd = st.text_input(T("password"), type="password", key="l_pwd")
                if st.button(T("auth_btn"), use_container_width=True):
                    users = db_io("users")
                    if uid in users and users[uid]['pwd'] == pwd:
                        user_role = users[uid].get('role', 'Patient')
                        if users[uid]['role'] == "Admin" or user_role == st.session_state.selected_role:
                            st.session_state.user = users[uid]['name']
                            st.session_state.page = "dashboard"
                            st.rerun()
                        else: st.error(f"Access Denied: Not a {st.session_state.selected_role}.")
                    else: st.error("Invalid Credentials or Database Connection Failed.")

        else: # PATIENT LOGIN
            tabs = st.tabs(["🔐 Login Credentials", "📝 New Registration"])
            
            with tabs[0]:
                uid = st.text_input(T("username"), key="l_uid")
                pwd = st.text_input(T("password"), type="password", key="l_pwd")
                if st.button(T("auth_btn"), use_container_width=True):
                    users = db_io("users")
                    if uid in users and users[uid]['pwd'] == pwd:
                        st.session_state.user = users[uid]['name']
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else: st.error("Invalid.")

            with tabs[1]:
                new_uid = st.text_input("Choose ID", key="r_uid")
                new_name = st.text_input("Full Name", key="r_name")
                new_pwd = st.text_input("Set Password", type="password", key="r_pwd")
                if st.button("Create Digital ID", use_container_width=True):
                    users = db_io("users")
                    if new_uid in users: st.error("ID taken.")
                    else:
                        users[new_uid] = {"pwd": new_pwd, "name": new_name, "role": "Patient"}
                        db_io("users", users, "write")
                        st.success("Identity Created.")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(T("return_btn")):
            st.session_state.page = "landing"
            st.session_state.selected_role = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    render_language_selector()

def render_dashboard():
    inject_accessibility()
    
    with st.sidebar:
        st.title("NS·AI")
        st.markdown(f"User: <br><b style='font-size:1.5rem; color:#00f2fe'>{st.session_state.user}</b>", unsafe_allow_html=True)
        st.caption(f"Role: {st.session_state.selected_role}")
        st.divider()
        st.caption(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
        st.markdown("<div style='height:40vh'></div>", unsafe_allow_html=True)
        if st.button("🛑 LOGOUT", use_container_width=True): perform_logout()

    col_head_1, col_head_2 = st.columns([6, 1])
    with col_head_1:
        st.markdown(f"<h1 style='margin-top:-2rem'>Dashboard <span style='font-size:1.5rem; color:#888'>// {st.session_state.selected_role}</span></h1>", unsafe_allow_html=True)
    with col_head_2:
        if st.button("Log Out ⏻"): perform_logout()
    st.divider()
    
    # ==========================
    # PATIENT PORTAL
    # ==========================
    if st.session_state.selected_role == "Patient":
        p_tabs = st.tabs([f"🩺 {T('dash_triage')}", f"🚚 {T('dash_mobile')}", f"📂 {T('history_tab')}"])
        
        with p_tabs[0]:
            c1, c2 = st.columns([1.5, 1])
            with c1:
                st.markdown(f"<div class='glass-panel'><h3>{T('dash_triage')} & {T('dash_book')}</h3>", unsafe_allow_html=True)
                
                symptoms_list = sorted([
                    "Chest Pain", "Breathlessness", "High Fever (>103)", "Mild Fever", "Cough", 
                    "Bone Pain", "Fracture", "Child Fever", "Child Cough", "Skin Rash", "Acne", "Itching",
                    "Severe Headache", "Seizures", "Dizziness", "Eye Pain", "Blurred Vision",
                    "Toothache", "Gum Bleeding", "Ear Pain", "Sore Throat", "Pregnancy Checkup", "Period Pain",
                    "Anxiety", "Depression", "Insomnia", "Uncontrolled Bleeding", "Severe Head Trauma", "Sudden Vision Loss"
                ])
                
                symptoms = st.multiselect(T("symptoms_label"), symptoms_list)
                
                if st.button(T("analyze_btn")):
                    rec, severity, advice = triage_logic(symptoms)
                    st.session_state.last_rec = rec
                    st.session_state.last_sev = severity
                    st.session_state.last_adv = advice
                    st.session_state.analysis_done = True
                
                if st.session_state.analysis_done:
                    sev = st.session_state.last_sev
                    rec = st.session_state.last_rec
                    adv = st.session_state.last_adv
                    
                    if sev == "High":
                        st.markdown(f"""<div class='emergency-alert' style='background: #dc2626; border-color: #ef4444;'>⚠️ <b>{T('emergency_alert')}</b><br>{adv}<br>Recommended: {rec} (Proceed to ER)</div>""", unsafe_allow_html=True)
                    elif sev == "Med":
                        st.markdown(f"""<div class='emergency-alert' style='background: #d97706; border-color: #f59e0b;'>⚠️ <b>{T('urgent_alert')}</b><br>{adv}<br>Recommended: {rec} (Book Next Slot)</div>""", unsafe_allow_html=True)
                    else: # LOW
                        st.markdown(f"""<div class='emergency-alert' style='background: #166534; border-color: #22c55e;'>✅ <b>{T('stable_alert')}</b><br>{adv}<br><b>Recommendation: Stay at Home / Rest.</b><br>Book appointment only if necessary.</div>""", unsafe_allow_html=True)

                    st.markdown("---")
                    
                    docs = db_io("docs")
                    found = False
                    for d, info in docs.items():
                        if info['spec'] == rec or (rec == "Emergency Unit" and info['spec'] == "General Physician"):
                            found = True
                            with st.container():
                                cc1, cc2 = st.columns([3, 1])
                                with cc1:
                                    st.write(f"**{d}** ({info['spec']})")
                                    st.caption(f"Room: {info['room']} | Tokens: {info['tokens']}")
                                with cc2:
                                    if info['status'] == "Available" and info['tokens'] > 0:
                                        btn_label = T("dash_book")
                                        if sev == "Low": btn_label = "Book Later"
                                        
                                        if st.button(f"{btn_label}", key=d):
                                            today_str = str(datetime.now().date())
                                            if info.get('last_date') != today_str:
                                                info['last_token_num'] = 0
                                                info['last_date'] = today_str
                                            
                                            new_num = info.get('last_token_num', 0) + 1
                                            info['last_token_num'] = new_num
                                            info['tokens'] -= 1
                                            tkn = f"T-{new_num}"
                                            wait_min = (new_num - 1) * 15
                                            if wait_min < 0: wait_min = 0
                                            wait_str = f"{wait_min} mins"
                                            
                                            hist = db_io("hist")
                                            new_entry = {
                                                "Date": today_str, "Time": datetime.now().strftime("%H:%M:%S"),
                                                "Patient": st.session_state.user, "Doctor": d, 
                                                "Token": tkn, "Specialty": info['spec'], "Priority": sev
                                            }
                                            db_io("hist", new_entry, "write")
                                            db_io("docs", docs, "write")
                                            
                                            qr_data = f"NabhaSeva-TOKEN\nPt: {st.session_state.user}\nDoc: {d}\nTok: {tkn}\nWait: ~{wait_str}\nPri: {sev}"
                                            st.session_state.last_booking_qr = (get_qr_code(qr_data), tkn, d, sev, wait_str)
                                            st.rerun()
                                    else:
                                        st.error("Full / Unavail.")
                    if not found and rec != "Emergency Unit": 
                        st.warning("No specific specialist available today. Try General Physician.")

                if st.session_state.last_booking_qr:
                    b64_img, tkn, doc_name, p_sev, w_time = st.session_state.last_booking_qr
                    h_color = "white"
                    if p_sev == "High": h_color = "#ff4b4b"
                    elif p_sev == "Med": h_color = "#ffa500"
                    elif p_sev == "Low": h_color = "#00ff7f"

                    st.markdown(f"""
                        <div style="background:rgba(255,255,255,0.1); padding:20px; border-radius:10px; text-align:center; border: 2px solid {h_color}">
                            <h3>Booking Confirmed!</h3>
                            <p>Doctor: {doc_name}</p>
                            <h1 style="color:{h_color}">{tkn}</h1>
                            <p style="color:{h_color}">Priority: {p_sev}</p>
                            <div style="background: rgba(0,0,0,0.5); padding: 5px; border-radius: 5px; margin-bottom: 10px;">
                                ⏱️ <b>Est. Wait: {w_time}</b>
                            </div>
                            <img src="data:image/png;base64,{b64_img}" width="200" />
                            <p>Scan for Digital Entry</p>
                        </div>
                        """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with c2:
                st.markdown("<div class='glass-panel'><h3>🤖 Smart Assistant</h3>", unsafe_allow_html=True)
                chat_container = st.container()
                with chat_container:
                    for c in st.session_state.chat_log:
                        if c['role'] == "You":
                            st.markdown(f"<div class='chat-user'><b>You:</b> {c['msg']}</div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div class='chat-ai'><b>AI:</b> {c['msg']}</div>", unsafe_allow_html=True)
                
                with st.form(key='chat_form', clear_on_submit=True):
                    u_in = st.text_input("Ask about doctors, departments, or help...", key="chat_in_widget")
                    if st.form_submit_button("Send") and u_in:
                        st.session_state.chat_log.append({"role": "You", "msg": u_in})
                        docs_snapshot = db_io("docs")
                        # --- PASSING DOCS DATA to SMART ASSISTANT ---
                        ans = get_smart_response(u_in, docs_snapshot)
                        st.session_state.chat_log.append({"role": "AI", "msg": ans})
                        st.rerun()
                st.caption("Tip: Ask 'How many beds are free?' or 'Where is the mobile clinic?'.")
                st.markdown("</div>", unsafe_allow_html=True)
        
        with p_tabs[1]:
            st.markdown(f"<div class='glass-panel'>", unsafe_allow_html=True)
            st.markdown("<h3>🚚 Live Mobile Clinics (MHU)</h3>", unsafe_allow_html=True)
            st.info("Check when the Mobile Health Unit (MHU) is visiting your village.")
            
            # --- NEW: VILLAGE STATUS CHECK ---
            st.markdown("<h4>🔍 Check My Village</h4>", unsafe_allow_html=True)
            village_names = [v['name'] for v in VILLAGES_DB.values()]
            my_village = st.selectbox("Select Your Village", village_names)
            
            units = db_io("mobile_units")
            active_units = [u for u in units if u.get('status') == 'En Route' and u.get('current_route')]
            
            mhu_coming = False
            if st.button("Check Schedule"):
                if active_units:
                    for u in active_units:
                        route = u['current_route'].get('path', [])
                        for idx, stop in enumerate(route):
                            if stop['type'] == 'Stop' and stop['name'] == my_village:
                                eta = (datetime.now() + timedelta(minutes=30*(idx))).strftime("%I:%M %p")
                                st.success(f"✅ GOOD NEWS! {u['unit_name']} is scheduled to visit {my_village} today at approx {eta}.")
                                mhu_coming = True
                if not mhu_coming:
                    st.error(f"No Mobile Unit is currently scheduled for {my_village} today.")

            st.divider()
            
            if active_units:
                for u in active_units:
                    route = u['current_route'].get('path', [])
                    if route:
                        st.subheader(f"{u['unit_name']} - Active Route")
                        st.plotly_chart(render_route_map(route), use_container_width=True)
                        st.write("🛑 **Stop Schedule:**")
                        for idx, stop in enumerate(route):
                            if stop['type'] == 'Stop':
                                eta = (datetime.now() + timedelta(minutes=30*(idx))).strftime("%I:%M %p")
                                st.write(f"📍 **{stop['name']}** - ETA: {eta}")
            else:
                st.warning("No Mobile Clinics are currently active. Check back later.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with p_tabs[2]:
            st.markdown(f"<div class='glass-panel'><h3>📂 {T('history_tab')}</h3>", unsafe_allow_html=True)
            hist_data = db_io("hist")
            if hist_data:
                # Filter by current logged in user name
                my_hist = [h for h in hist_data if h['Patient'] == st.session_state.user]
                if my_hist:
                    df = pd.DataFrame(my_hist)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No past medical records found for your account.")
            else:
                st.info("No records found.")
            st.markdown("</div>", unsafe_allow_html=True)

    # ==========================
    # STAFF PORTAL
    # ==========================
    elif st.session_state.selected_role == "Staff":
        st.info("Welcome, Staff Member / Volunteer. View your assignments below.")
        
        # --- NEW: VOLUNTEER ASSIGNMENT CARD ---
        users = db_io("users")
        current_user_data = users.get(next((u for u, d in users.items() if d['name'] == st.session_state.user), None), {})
        assigned_doc_name = current_user_data.get('assigned_doc', None)
        
        if assigned_doc_name:
            st.markdown(f"""
            <div class='emergency-alert' style='background: #0f172a; border-color: #00f2fe; text-align:left;'>
                <h3 style='margin:0; color:#00f2fe'>📋 My Assignment</h3>
                <p style='font-size:1.2rem'>You are assigned to assist: <b>{assigned_doc_name}</b></p>
                <p>Please report to their cabin immediately.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show live status of that doctor
            docs = db_io("docs")
            if assigned_doc_name in docs:
                doc_info = docs[assigned_doc_name]
                st.markdown(f"**Doctor Status:** {doc_info['status']} | **Room:** {doc_info['room']} | **Patients Served:** {doc_info['last_token_num']}")

        tab_roster, tab_logs = st.tabs([f"👨‍⚕️ {T('roster_control')}", f"📂 {T('queue_monitor')}"])
        
        with tab_roster:
            st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
            docs = db_io("docs")
            cols = st.columns(3) 
            for i, (name, info) in enumerate(docs.items()):
                with cols[i % 3]:
                    with st.expander(f"{name} ({info['spec']})", expanded=True):
                        st.write(f"Room: **{info['room']}**")
                        st.write(f"Tokens Served: **{info.get('last_token_num', 0)}**")
                        c_a, c_b = st.columns(2)
                        new_status = c_a.selectbox("Status", ["Available", "Away", "Surgery"], index=["Available", "Away", "Surgery"].index(info['status']), key=f"s_{name}")
                        new_tokens = c_b.number_input("Max T", value=info['tokens'], key=f"t_{name}")
                        if st.button(f"Update", key=f"btn_{name}"):
                            docs[name]['status'] = new_status
                            docs[name]['tokens'] = new_tokens
                            db_io("docs", docs, "write")
                            st.success("✓")
                            time.sleep(0.5); st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
        with tab_logs:
            st.markdown("<div class='glass-panel'><h3>🔍 Live Patient Queue</h3>", unsafe_allow_html=True)
            hist_data = db_io("hist")
            if hist_data and len(hist_data) > 0:
                df = pd.DataFrame(hist_data)
                df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='coerce')
                df = df.dropna(subset=['DateTime'])
                priority_map = {"High": 0, "Med": 1, "Low": 2}
                df['SortKey'] = df['Priority'].map(priority_map).fillna(2)
                df = df.sort_values(by=['SortKey', 'DateTime'], ascending=[True, False])
                def highlight_priority(val):
                    color = ''
                    if val == 'High': color = 'background-color: #7f1d1d; color: white; font-weight: bold;'
                    elif val == 'Med': color = 'background-color: #7c2d12; color: white;'
                    elif val == 'Low': color = 'color: #aaa;'
                    return color
                display_cols = ['Priority', 'Token', 'Patient', 'Doctor', 'Specialty', 'Date', 'Time']
                st.dataframe(df[display_cols].style.map(highlight_priority, subset=['Priority']), use_container_width=True, hide_index=True, height=500)
            else:
                st.info("No patient history found.")
            st.markdown("</div>", unsafe_allow_html=True)

    # ==========================
    # ADMIN PORTAL
    # ==========================
    elif st.session_state.selected_role == "Admin":
        inv = db_io("inv")
        low_stock_items = [k for k, v in inv.items() if v < 50]
        if low_stock_items:
            st.error(f"⚠️ {T('stock_alert')}: {', '.join(low_stock_items)} below threshold!")

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            f"📊 {T('admin_analytics')}", 
            f"🛏️ {T('admin_ops')}", 
            "⚙️ Manage Staff", 
            "🤝 Volunteer Mgmt",
            f"🚚 {T('admin_logistics')}"
        ])
        
        with tab1:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("<div class='glass-panel'><h3>Live Traffic</h3>", unsafe_allow_html=True)
                m1, m2, m3 = st.columns(3)
                m1.metric("Sanctioned Posts", "23", delta="Full Capacity")
                m2.metric("Active Doctors", f"{len(db_io('docs'))}", delta="On Roster")
                m3.metric("Avg Wait Time", "12 min", delta="-2 min")
                df = pd.DataFrame({"Hour": ["8am", "9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm"], "Patients": [12, 28, 45, 50, 80, 65, 60, 40, 25]})
                fig = px.area(df, x="Hour", y="Patients", title="Daily Footfall", template="plotly_dark")
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_family="Plus Jakarta Sans")
                fig.update_traces(line_color='#00f2fe', fillcolor='rgba(0, 242, 254, 0.2)')
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            with col2:
                st.markdown("<div class='glass-panel'><h3>Inventory</h3>", unsafe_allow_html=True)
                for item, qty in inv.items():
                    c_i1, c_i2 = st.columns([2, 1])
                    c_i1.metric(item, f"{qty}")
                    if qty < 50:
                        if c_i2.button("Restock", key=f"rs_{item}"):
                            inv[item] += 50
                            db_io("inv", inv, "write")
                            st.rerun()
                    st.divider()
                st.markdown("</div>", unsafe_allow_html=True)

        with tab2:
            st.markdown("<div class='glass-panel'><h3>Real-Time Bed Management</h3>", unsafe_allow_html=True)
            beds = db_io("beds")
            cols = st.columns(5)
            keys = list(beds.keys())
            for i, k in enumerate(keys):
                status = beds[k]
                color_class = "bed-avail" if status == "Available" else "bed-occ"
                with cols[i % 5]:
                    st.markdown(f"<div class='bed-box {color_class}'>{k}<br><small>{status}</small></div>", unsafe_allow_html=True)
                    if st.button("Toggle", key=f"bed_{k}"):
                        beds[k] = "Occupied" if status == "Available" else "Available"
                        db_io("beds", beds, "write")
                        st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        with tab3:
            st.markdown("<div class='glass-panel'><h3>Add New Doctor</h3>", unsafe_allow_html=True)
            with st.form("add_doc_form"):
                d_name = st.text_input("Doctor Name (e.g. Dr. John Doe)")
                d_spec = st.selectbox("Specialization", ["General Physician", "Cardiologist", "Neurologist", "Pediatrician", "Orthopedic", "Dermatologist", "ENT Specialist", "Gynecologist", "Psychiatrist", "Ophthalmologist", "Dentist"])
                d_room = st.text_input("Room Number")
                d_tok = st.number_input("Daily Token Limit", value=20)
                if st.form_submit_button("Onboard Doctor"):
                    if d_name and d_room:
                        docs = db_io("docs")
                        docs[d_name] = {"spec": d_spec, "status": "Available", "room": d_room, "tokens": d_tok, "last_token_num": 0, "last_date": ""}
                        db_io("docs", docs, "write")
                        st.success(f"{d_name} added to system.")
                    else:
                        st.error("Missing details.")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tab4:
            st.markdown(f"<div class='glass-panel'><h3>{T('vol_pending')}</h3>", unsafe_allow_html=True)
            vols = db_io("vols")
            pending_vols = [v for v in vols if v['status'] == 'Pending']
            all_docs = db_io("docs")
            doc_names = list(all_docs.keys())

            if not pending_vols:
                st.success("No pending applications.")
            else:
                for v in pending_vols:
                    with st.expander(f"Applicant: {v['full_name']} ({v['role']})", expanded=True):
                        c_a, c_b = st.columns([3, 1])
                        with c_a:
                            st.write(f"**Experience:** {v['experience']}")
                            st.write(f"**Reason:** {v['why_join']}")
                            st.write(f"**Contact:** {v['contact']}")
                            st.caption(f"Applied: {v['created_at']}")
                        with c_b:
                            # --- MANUAL ASSIGNMENT UI ---
                            target_doc = st.selectbox("Assign to (Optional)", ["Auto-Assign"] + doc_names, key=f"sel_{v['id']}")
                            
                            if st.button(f"✅ {T('vol_approve')}", key=f"app_{v['id']}"):
                                # Determine Assignment
                                final_doc = None
                                load = 0
                                if target_doc == "Auto-Assign":
                                    final_doc, load = find_doctor_needing_help()
                                else:
                                    final_doc = target_doc
                                    load = all_docs[final_doc].get('last_token_num', 0)

                                if final_doc:
                                    assign_msg = f"Assigned to {final_doc} (Load: {load} patients)"
                                    # Update Volunteer Status
                                    db_io("vols_update", {"id": v['id'], "status": "Approved"}, "write")
                                    
                                    # Create Login
                                    new_uid = v['full_name'].split()[0].lower() + str(random.randint(10,99))
                                    users = db_io("users")
                                    users[new_uid] = {
                                        "pwd": "123", 
                                        "name": v['full_name'], 
                                        "role": "Staff",
                                        "assigned_doc": final_doc # Store assignment in user profile
                                    }
                                    db_io("users", users, "write")
                                    
                                    st.success(f"Approved! User ID: {new_uid} | {assign_msg}")
                                    time.sleep(2)
                                    st.rerun()
                                else:
                                    st.warning("No doctors available.")

                            if st.button(f"❌ {T('vol_reject')}", key=f"rej_{v['id']}"):
                                db_io("vols_update", {"id": v['id'], "status": "Rejected"}, "write")
                                st.error("Application Rejected.")
                                time.sleep(1)
                                st.rerun()
            
            st.markdown("---")
            st.markdown("<h3>Active Volunteers & Reassignment</h3>", unsafe_allow_html=True)
            approved_vols = [v for v in vols if v['status'] == 'Approved']
            users = db_io("users")
            
            if approved_vols:
                for v in approved_vols:
                    # Find user record
                    user_id = None
                    user_data = None
                    for uid, udata in users.items():
                        if udata['name'] == v['full_name']:
                            user_id = uid
                            user_data = udata
                            break
                    
                    current_assign = user_data.get('assigned_doc', 'Unassigned') if user_data else 'Unknown'
                    
                    with st.expander(f"✅ {v['full_name']} (Assigned: {current_assign})"):
                        c_r1, c_r2 = st.columns([3, 1])
                        with c_r1:
                            new_assign = st.selectbox("Reassign to:", doc_names, index=doc_names.index(current_assign) if current_assign in doc_names else 0, key=f"re_{v['id']}")
                        with c_r2:
                            if st.button("Update", key=f"upd_{v['id']}"):
                                if user_id:
                                    users[user_id]['assigned_doc'] = new_assign
                                    db_io("users", users, "write")
                                    st.success(f"Reassigned to {new_assign}")
                                    time.sleep(1)
                                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tab5:
            st.markdown(f"<div class='glass-panel'><h3>{T('admin_logistics')}</h3>", unsafe_allow_html=True)
            
            # --- NEW: ADD MOBILE UNIT FORM ---
            st.markdown(f"<h4>{T('add_unit_header')}</h4>", unsafe_allow_html=True)
            with st.form("add_unit_form"):
                u_c1, u_c2 = st.columns(2)
                new_u_name = u_c1.text_input("Unit Name (e.g. MHU-Charlie)")
                new_u_driver = u_c2.text_input("Driver Name")
                if st.form_submit_button(T("add_unit_btn")):
                    if new_u_name and new_u_driver:
                        db_io("units_add", {
                            "unit_name": new_u_name,
                            "driver": new_u_driver,
                            "status": "Idle",
                            "current_route": {}
                        }, "write")
                        st.success(f"Unit {new_u_name} commissioned successfully.")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Name and Driver required.")

            st.markdown("---")
            st.caption("Select high-risk villages to generate an optimal route.")
            
            villages_list = [f"{k}: {v['name']} (Risk: {v['risk_score']})" for k, v in VILLAGES_DB.items()]
            selected_v_raw = st.multiselect(T("village_select"), villages_list)
            selected_keys = [s.split(":")[0] for s in selected_v_raw]
            
            if st.button(T("route_plan_btn")):
                if selected_keys:
                    route, dist = generate_optimal_route(selected_keys)
                    st.session_state.active_route = {"path": route, "dist": dist}
                    st.success(f"Route Generated! Total Distance: {dist} km")
                else:
                    st.error("Select villages first.")
            
            if st.session_state.active_route:
                route_data = st.session_state.active_route
                st.plotly_chart(render_route_map(route_data['path']), use_container_width=True)
                c_d1, c_d2 = st.columns(2)
                c_d1.metric(T("distance_label"), f"{route_data['dist']} km")
                c_d2.metric("Stops", len(route_data['path']) - 2)
                
                with st.form("assign_route_form"):
                    units = db_io("mobile_units")
                    if not units:
                        st.warning("⚠️ No Mobile Units found in fleet. Please commission a new unit above to enable deployment.")
                    else:
                        unit_names = [u['unit_name'] for u in units]
                        target_unit = st.selectbox("Assign to Unit", unit_names)
                        if st.form_submit_button("Deploy Unit"):
                            u_id = next((u['id'] for u in units if u['unit_name'] == target_unit), None)
                            if u_id:
                                # IMPORTANT: Pass route_data as a proper dictionary/JSON for Supabase
                                db_io("units_update", {"id": u_id, "status": "En Route", "current_route": route_data}, "write")
                                st.success(f"{target_unit} is now En Route!")
                                time.sleep(1)
                                st.rerun()

            st.markdown("---")
            st.markdown("<h4>Fleet Status</h4>", unsafe_allow_html=True)
            units = db_io("mobile_units")
            if units:
                for u in units:
                    status_color = "#00ff7f" if u['status'] == "En Route" else "#aaa"
                    with st.container():
                        col_u1, col_u2 = st.columns([3,1])
                        with col_u1:
                            st.markdown(f"""<div style="border:1px solid {status_color}; padding:10px; border-radius:10px; margin-bottom:10px"><b>{u['unit_name']}</b> | Driver: {u['driver']}<br>Status: <span style="color:{status_color}">{u['status']}</span></div>""", unsafe_allow_html=True)
                        with col_u2:
                            if u['status'] == "En Route":
                                if st.button("Return", key=f"ret_{u['id']}"):
                                    db_io("units_update", {"id": u['id'], "status": "Idle", "current_route": {}}, "write")
                                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    render_language_selector()

# ==========================================
# 10. MAIN EXECUTION
# ==========================================
if st.session_state.page == "landing": render_landing()
elif st.session_state.page == "auth": render_auth()
elif st.session_state.page == "dashboard": render_dashboard()