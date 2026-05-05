import streamlit as st
import streamlit.components.v1 as components
import time
import threading
import hashlib
import os
import json
import urllib.parse
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import database as db
import requests
from datetime import datetime

# ============================================
# PAGE CONFIG - RISHU XROS
# ============================================
st.set_page_config(
    page_title="RISHU XROS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
#          CUSTOM CSS THEME
# ============================================
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 50%, #7dd3fc 100%);
        background-attachment: fixed;
    }

    .main .block-container {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 28px;
        padding: 32px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06);
    }

    .main-header {
        background: linear-gradient(135deg, #0f172a, #1e3a8a);
        border-radius: 24px;
        padding: 1.8rem;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    }

    .main-header h1 {
        background: linear-gradient(90deg, #93c5fd, #60a5fa, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 2.5rem;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .main-header p {
        color: #bfdbfe;
        font-size: 1rem;
        margin-top: 0.5rem;
        opacity: 0.9;
    }

    .rishi-logo {
        width: 90px;
        height: 90px;
        border-radius: 50%;
        margin-bottom: 15px;
        border: 3px solid #3b82f6;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.4);
        object-fit: cover;
    }

    .stButton>button {
        background: linear-gradient(45deg, #2563eb, #3b82f6);
        color: white;
        border: none;
        border-radius: 40px;
        padding: 0.7rem 1.8rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25);
        width: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35);
        background: linear-gradient(45deg, #1d4ed8, #2563eb);
    }

    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stNumberInput>div>div>input {
        background: white;
        border: 1px solid #cbd5e1;
        border-radius: 16px;
        color: #1e293b;
        padding: 0.7rem 1rem;
        font-size: 0.9rem;
    }

    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
    }

    label {
        color: #1e293b !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        margin-bottom: 4px !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: #f1f5f9;
        border-radius: 40px;
        padding: 5px;
        gap: 6px;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #475569;
        border-radius: 32px;
        padding: 8px 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #2563eb, #3b82f6);
        color: white;
    }

    [data-testid="stMetricValue"] {
        color: #1e3a8a;
        font-size: 1.8rem;
        font-weight: 700;
    }

    [data-testid="stMetricLabel"] {
        color: #475569;
        font-weight: 500;
        font-size: 0.85rem;
    }

    .console-output {
        background: #0f172a;
        border-radius: 20px;
        padding: 18px;
        color: #a5f3fc;
        font-family: 'Courier New', monospace;
        font-size: 11px;
        max-height: 400px;
        overflow-y: auto;
        border: 1px solid #334155;
    }

    .console-line {
        background: rgba(51, 65, 85, 0.3);
        border-left: 3px solid #3b82f6;
        padding: 6px 12px;
        margin: 5px 0;
        color: #cbd5e1;
        border-radius: 8px;
        font-size: 11px;
    }

    .whatsapp-btn {
        background: linear-gradient(45deg, #059669, #10b981);
        border: none;
        color: white;
        font-weight: 600;
        border-radius: 40px;
        padding: 10px 24px;
        text-decoration: none;
        display: inline-block;
        font-size: 0.9rem;
    }

    .whatsapp-btn:hover {
        background: linear-gradient(45deg, #047857, #059669);
        transform: translateY(-2px);
    }

    .footer {
        background: rgba(255, 255, 255, 0.7);
        border-top: 2px solid #3b82f6;
        color: #1e293b;
        text-align: center;
        padding: 1.5rem;
        font-size: 0.8rem;
        border-radius: 20px;
        margin-top: 2rem;
    }
    
    .stAlert {
        border-radius: 16px !important;
    }
    
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(10px);
        border-right: 1px solid #3b82f6;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #1e293b;
    }
    
    .admin-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #3b82f6;
    }
    
    .admin-card h4 {
        color: #60a5fa;
        margin-bottom: 0.5rem;
    }
    
    .admin-badge {
        background: #3b82f6;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.7rem;
        display: inline-block;
        margin-bottom: 10px;
    }
    
    .request-item {
        background: white;
        border-radius: 12px;
        padding: 0.8rem;
        margin-bottom: 0.8rem;
        border-left: 4px solid #f59e0b;
    }
    
    .key-code {
        background: #f1f5f9;
        padding: 4px 8px;
        border-radius: 8px;
        font-family: monospace;
        font-size: 0.8rem;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# ============================================
# CONSTANTS
# ============================================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Rishi@Xros@2025"
WHATSAPP_NUMBER = "919919180262"
APPROVAL_FILE = "approved_keys.json"
PENDING_FILE = "pending_approvals.json"

# ============================================
# FILE HANDLING FUNCTIONS
# ============================================
def generate_user_key(username, password):
    combined = f"{username}:{password}"
    key_hash = hashlib.sha256(combined.encode()).hexdigest()[:8].upper()
    return f"KEY-{key_hash}"

def load_approved_keys():
    if os.path.exists(APPROVAL_FILE):
        try:
            with open(APPROVAL_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_approved_keys(keys):
    with open(APPROVAL_FILE, 'w') as f:
        json.dump(keys, f, indent=2)

def load_pending_approvals():
    if os.path.exists(PENDING_FILE):
        try:
            with open(PENDING_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_pending_approvals(pending):
    with open(PENDING_FILE, 'w') as f:
        json.dump(pending, f, indent=2)

def send_whatsapp_message(user_name, approval_key):
    message = f"⚡ HELLO RISHU XROS SIR PLEASE ⚡⚡\nMy name is {user_name}\nPlease approve my key:\n🔑 {approval_key}"
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://api.whatsapp.com/send?phone={WHATSAPP_NUMBER}&text={encoded_message}"
    return whatsapp_url

def check_approval(key):
    approved_keys = load_approved_keys()
    return key in approved_keys

# ============================================
# SESSION STATE INITIALIZATION
# ============================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'admin_mode' not in st.session_state:
    st.session_state.admin_mode = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_key' not in st.session_state:
    st.session_state.user_key = None
if 'key_approved' not in st.session_state:
    st.session_state.key_approved = False
if 'approval_status' not in st.session_state:
    st.session_state.approval_status = 'not_requested'
if 'automation_running' not in st.session_state:
    st.session_state.automation_running = False
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0
if 'whatsapp_opened' not in st.session_state:
    st.session_state.whatsapp_opened = False

class AutomationState:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.logs = []
        self.message_rotation_index = 0

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

if 'auto_start_checked' not in st.session_state:
    st.session_state.auto_start_checked = False

# ============================================
# LOGGING FUNCTION
# ============================================
def log_message(msg, automation_state=None):
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
   
    if automation_state:
        automation_state.logs.append(formatted_msg)
    else:
        if 'logs' in st.session_state:
            st.session_state.logs.append(formatted_msg)

# ============================================
# SELENIUM FUNCTIONS (Simplified)
# ============================================
def find_message_input(driver, process_id, automation_state=None):
    log_message(f'{process_id}: Finding message input...', automation_state)
    time.sleep(10)
   
    message_input_selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"][data-lexical-editor="true"]',
        'div[aria-label*="message" i][contenteditable="true"]',
        'textarea[placeholder*="message" i]',
        '[contenteditable="true"]',
        'textarea',
    ]
   
    for selector in message_input_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                try:
                    is_editable = driver.execute_script("""
                        return arguments[0].contentEditable === 'true' ||
                               arguments[0].tagName === 'TEXTAREA' ||
                               arguments[0].tagName === 'INPUT';
                    """, element)
                   
                    if is_editable:
                        try:
                            element.click()
                            time.sleep(0.5)
                        except:
                            pass
                        return element
                except Exception:
                    continue
        except Exception:
            continue
   
    return None

def setup_browser(automation_state=None):
    log_message('Setting up Chrome browser...', automation_state)
   
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
   
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(1920, 1080)
        return driver
    except Exception as error:
        log_message(f'Browser setup failed: {error}', automation_state)
        raise error

def send_messages(config, automation_state, user_id, process_id='AUTO-1'):
    driver = None
    try:
        driver = setup_browser(automation_state)
        driver.get('https://www.facebook.com/')
        time.sleep(8)
       
        if config.get('cookies') and config['cookies'].strip():
            cookie_array = config['cookies'].split(';')
            for cookie in cookie_array:
                cookie_trimmed = cookie.strip()
                if cookie_trimmed and '=' in cookie_trimmed:
                    name, value = cookie_trimmed.split('=', 1)
                    try:
                        driver.add_cookie({'name': name, 'value': value, 'domain': '.facebook.com', 'path': '/'})
                    except Exception:
                        pass
       
        if config.get('chat_id'):
            driver.get(f"https://www.facebook.com/messages/t/{config['chat_id'].strip()}")
        else:
            driver.get('https://www.facebook.com/messages')
       
        time.sleep(15)
        message_input = find_message_input(driver, process_id, automation_state)
       
        if not message_input:
            automation_state.running = False
            db.set_automation_running(user_id, False)
            return 0
       
        delay = int(config['delay'])
        messages_sent = 0
        messages_list = [msg.strip() for msg in config['messages'].split('\n') if msg.strip()]
       
        if not messages_list:
            messages_list = ['Hello!']
       
        while automation_state.running:
            message_to_send = messages_list[messages_sent % len(messages_list)]
            if config.get('name_prefix'):
                message_to_send = f"{config['name_prefix']} {message_to_send}"
           
            try:
                driver.execute_script("""
                    arguments[0].focus();
                    arguments[0].click();
                    arguments[0].textContent = arguments[1];
                    arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                """, message_input, message_to_send)
               
                time.sleep(1)
               
                driver.execute_script("""
                    const btn = document.querySelector('[aria-label*="Send" i], [data-testid="send-button"]');
                    if(btn) btn.click();
                """)
               
                messages_sent += 1
                automation_state.message_count = messages_sent
                time.sleep(delay)
            except Exception:
                time.sleep(5)
       
        return messages_sent
    except Exception:
        automation_state.running = False
        db.set_automation_running(user_id, False)
        return 0
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def start_automation(user_config, user_id):
    automation_state = st.session_state.automation_state
   
    if automation_state.running:
        return
   
    automation_state.running = True
    automation_state.message_count = 0
    automation_state.logs = []
   
    db.set_automation_running(user_id, True)
   
    username = db.get_username(user_id)
    thread = threading.Thread(target=send_messages, args=(user_config, automation_state, user_id))
    thread.daemon = True
    thread.start()

def stop_automation(user_id):
    st.session_state.automation_state.running = False
    db.set_automation_running(user_id, False)

# ============================================
# SIDEBAR ADMIN PANEL - DIRECT APPROVAL
# ============================================
def sidebar_admin_panel():
    """Sidebar mein admin panel - direct approval system"""
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👑 ADMIN PANEL")
    
    # Admin login section
    if not st.session_state.admin_mode:
        with st.sidebar.expander("🔐 Admin Login", expanded=True):
            admin_user = st.text_input("Username", key="admin_user", placeholder="admin")
            admin_pass = st.text_input("Password", type="password", key="admin_pass", placeholder="Password")
            
            if st.button("🔓 Login as Admin", key="admin_login_btn", use_container_width=True):
                if admin_user == ADMIN_USERNAME and admin_pass == ADMIN_PASSWORD:
                    st.session_state.admin_mode = True
                    st.success("✅ Admin logged in!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials!")
    else:
        # Admin is logged in - show admin controls
        st.sidebar.success("✅ Admin Mode Active")
        
        if st.sidebar.button("🚪 Logout from Admin", key="admin_logout_btn", use_container_width=True):
            st.session_state.admin_mode = False
            st.rerun()
        
        st.sidebar.markdown("---")
        
        # Load data
        pending = load_pending_approvals()
        approved_keys = load_approved_keys()
        
        # Stats
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.sidebar.metric("⏳ Pending", len(pending))
        with col2:
            st.sidebar.metric("✅ Approved", len(approved_keys))
        
        st.sidebar.markdown("---")
        
        # Pending Approvals Section
        st.sidebar.markdown("#### ⏳ Pending Approvals")
        
        if pending:
            # Approve All button
            if st.sidebar.button("✅ Approve All", key="approve_all_btn", use_container_width=True):
                for key, info in pending.items():
                    approved_keys[key] = info
                save_approved_keys(approved_keys)
                save_pending_approvals({})
                st.sidebar.success(f"✅ Approved all {len(pending)} requests!")
                st.rerun()
            
            st.sidebar.markdown("---")
            
            # Individual requests
            for key, info in list(pending.items()):
                with st.sidebar.container():
                    st.sidebar.markdown(f"""
                    <div class="request-item">
                        <b>👤 {info['name']}</b><br>
                        <span class="key-code">{key}</span><br>
                        <small>📅 {info.get('timestamp', 'Unknown')}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.sidebar.columns(2)
                    with col1:
                        if st.button(f"✅ Approve", key=f"approve_{key}", use_container_width=True):
                            approved_keys[key] = info
                            save_approved_keys(approved_keys)
                            del pending[key]
                            save_pending_approvals(pending)
                            st.sidebar.success(f"✅ Approved {info['name']}!")
                            st.rerun()
                    with col2:
                        if st.button(f"❌ Reject", key=f"reject_{key}", use_container_width=True):
                            del pending[key]
                            save_pending_approvals(pending)
                            st.sidebar.warning(f"❌ Rejected {info['name']}")
                            st.rerun()
                    st.sidebar.markdown("---")
        else:
            st.sidebar.info("No pending approvals")
        
        st.sidebar.markdown("---")
        
        # Approved Keys Section (Collapsible)
        with st.sidebar.expander(f"✅ Approved Keys ({len(approved_keys)})"):
            if approved_keys:
                for key, info in list(approved_keys.items()):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{info['name']}**")
                        st.caption(key[:20] + "...")
                    with col2:
                        if st.button(f"🗑️", key=f"revoke_{key}", help="Revoke this key"):
                            del approved_keys[key]
                            save_approved_keys(approved_keys)
                            st.rerun()
                    st.markdown("---")
            else:
                st.info("No approved keys")

# ============================================
# USER APPROVAL REQUEST PAGE
# ============================================
def approval_request_page(user_key, username):
    st.markdown("""
    <div class="main-header">
        <img src="https://i.ibb.co/5W1QW4zH/1753900515862.jpg" class="rishi-logo">
        <h1>🔐 RISHU XROS - PREMIUM KEY REQUIRED 🔐</h1>
        <p>ONE MONTH 500 RS PAID</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.approval_status == 'not_requested':
        st.markdown("### 📝 Request Access")
        st.info(f"**Your Unique Key:** `{user_key}`")
        st.info(f"**Username:** {username}")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("📤 Request Approval", use_container_width=True, key="request_approval_btn"):
                pending = load_pending_approvals()
                pending[user_key] = {
                    "name": username,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                save_pending_approvals(pending)
                
                st.session_state.approval_status = 'pending'
                st.session_state.whatsapp_opened = False
                st.rerun()
    
    elif st.session_state.approval_status == 'pending':
        st.warning("⏳ Approval Pending...")
        st.info(f"**Your Key:** `{user_key}`")
        
        whatsapp_url = send_whatsapp_message(username, user_key)
        
        if not st.session_state.whatsapp_opened:
            whatsapp_js = f"""
            <script>
                setTimeout(function() {{
                    window.open('{whatsapp_url}', '_blank');
                }}, 500);
            </script>
            """
            components.html(whatsapp_js, height=0)
            st.session_state.whatsapp_opened = True
        
        st.success(f"📱 WhatsApp opening automatically for: **{username}**")
        st.markdown(f"""
        <div style="text-align: center; margin: 20px 0;">
            <a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">
                💬 Click Here to Open WhatsApp
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Check Approval Status", use_container_width=True, key="check_approval_btn"):
                if check_approval(user_key):
                    st.session_state.key_approved = True
                    st.session_state.approval_status = 'approved'
                    st.success("✅ Approved! Redirecting...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Not approved yet. Please wait!")
    
    elif st.session_state.approval_status == 'approved':
        st.success("✅ Your key has been approved! Redirecting...")
        time.sleep(1)
        st.rerun()

# ============================================
# USER LOGIN & SIGNUP
# ============================================
def login_page():
    st.markdown("""
    <div class="main-header">
        <img src="https://i.ibb.co/5W1QW4zH/1753900515862.jpg" class="rishi-logo">
        <h1>⚡ RISHU XROS - OFFLINE E2EE ⚡</h1>
        <p>səvən bıllıon smılə's ın ʈhıs world buʈ ɣour's ıs mɣ fαvourıʈəs___⚡⚡</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])
    
    with tab1:
        st.markdown("### Welcome Back!")
        username = st.text_input("Username", key="login_username", placeholder="Enter your username")
        password = st.text_input("Password", key="login_password", type="password", placeholder="Enter your password")
        
        if st.button("Login", key="login_btn", use_container_width=True):
            if username and password:
                user_id = db.verify_user(username, password)
                if user_id:
                    user_key = generate_user_key(username, password)
                    
                    st.session_state.logged_in = True
                    st.session_state.user_id = user_id
                    st.session_state.username = username
                    st.session_state.user_key = user_key
                    
                    if check_approval(user_key):
                        st.session_state.key_approved = True
                        st.session_state.approval_status = 'approved'
                        
                        should_auto_start = db.get_automation_running(user_id)
                        if should_auto_start:
                            user_config = db.get_user_config(user_id)
                            if user_config and user_config.get('chat_id'):
                                start_automation(user_config, user_id)
                    else:
                        st.session_state.key_approved = False
                        st.session_state.approval_status = 'not_requested'
                    
                    st.success(f"✅ Welcome back, {username}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password!")
            else:
                st.warning("⚠️ Please enter both username and password")
    
    with tab2:
        st.markdown("### Create New Account")
        new_username = st.text_input("Choose Username", key="signup_username", placeholder="Choose a unique username")
        new_password = st.text_input("Choose Password", key="signup_password", type="password", placeholder="Create a strong password")
        confirm_password = st.text_input("Confirm Password", key="confirm_password", type="password", placeholder="Re-enter your password")
        
        if st.button("Create Account", key="signup_btn", use_container_width=True):
            if new_username and new_password and confirm_password:
                if new_password == confirm_password:
                    success, message = db.create_user(new_username, new_password)
                    if success:
                        st.success(f"✅ {message} Please login now!")
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error("❌ Passwords do not match!")
            else:
                st.warning("⚠️ Please fill all fields")

# ============================================
# MAIN USER APP (After Login & Approval)
# ============================================
def main_app():
    st.markdown('<div class="main-header"><img src="https://i.ibb.co/5W1QW4zH/1753900515862.jpg" class="rishi-logo"><h1>⚡ RISHU XROS - E2E OFFLINE ⚡</h1><p>səvən bıllıon smıləs ın ʈhıs world buʈ ɣours ıs mɣ fαvourıʈəs___⚡⚡</p></div>', unsafe_allow_html=True)
    
    if not st.session_state.auto_start_checked and st.session_state.user_id:
        st.session_state.auto_start_checked = True
        should_auto_start = db.get_automation_running(st.session_state.user_id)
        if should_auto_start and not st.session_state.automation_state.running:
            user_config = db.get_user_config(st.session_state.user_id)
            if user_config and user_config.get('chat_id'):
                start_automation(user_config, st.session_state.user_id)
    
    st.sidebar.markdown(f"### ⚡ {st.session_state.username}")
    st.sidebar.markdown(f"**User ID:** {st.session_state.user_id}")
    st.sidebar.markdown(f"**Key:** `{st.session_state.user_key}`")
    st.sidebar.success("✅ Key Approved")
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        if st.session_state.automation_state.running:
            stop_automation(st.session_state.user_id)
        
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.user_key = None
        st.session_state.key_approved = False
        st.session_state.automation_running = False
        st.session_state.auto_start_checked = False
        st.session_state.approval_status = 'not_requested'
        st.rerun()
    
    user_config = db.get_user_config(st.session_state.user_id)
    
    if user_config:
        tab1, tab2 = st.tabs(["⚙️ Configuration", "🤖 Automation"])
        
        with tab1:
            st.markdown("### Your Configuration")
            
            # Message file buttons
            st.markdown("#### 📥 Load Messages from GitHub")
            
            message_files = {
                "bot_response_text.txt": "🤖 Bot Response Messages",
                "RISHI NP 30xl.txt": "📝 RISHI NP 30xl (Large)",
                "File.txt": "📄 File.txt Messages",
                "45K RISHI BRAND GAALI.txt": "🔥 45K RISHI BRAND GAALI"
            }
            
            cols = st.columns(2)
            col_idx = 0
            
            for filename, display_name in message_files.items():
                with cols[col_idx % 2]:
                    raw_url = f"https://raw.githubusercontent.com/JOHNSEENA1/e2e-/main/{filename.replace(' ', '%20')}"
                    if st.button(f"📥 {display_name}", key=f"fetch_{filename.replace(' ', '_')}", use_container_width=True):
                        with st.spinner(f"Fetching {filename}..."):
                            try:
                                response = requests.get(raw_url, timeout=60)
                                if response.status_code == 200:
                                    content = response.text
                                    if content:
                                        st.session_state.fetched_messages = content
                                        line_count = len(content.split('\n'))
                                        st.success(f"✅ Loaded {line_count} messages from {filename}!")
                                        st.rerun()
                                    else:
                                        st.error(f"❌ {filename} is empty!")
                                else:
                                    st.error(f"❌ Failed to fetch {filename}")
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)[:100]}")
                col_idx += 1
            
            st.markdown("---")
            
            if 'fetched_messages' in st.session_state:
                lines = len(st.session_state.fetched_messages.split('\n'))
                st.info(f"📄 Currently loaded: **{lines} messages** ready to save")
                if st.button("🗑️ Clear loaded messages", use_container_width=True):
                    del st.session_state.fetched_messages
                    st.rerun()
            
            chat_id = st.text_input("Chat/Conversation ID", value=user_config.get('chat_id', ''),
                                   placeholder="e.g., 1362400298935018")
            
            name_prefix = st.text_input("Hatersname", value=user_config.get('name_prefix', ''),
                                       placeholder="e.g., [END TO END]")
            
            delay = st.number_input("Delay (seconds)", min_value=1, max_value=300,
                                   value=user_config.get('delay', 10))
            
            # Cookies section with file upload
            st.markdown("#### 🍪 Facebook Cookies")
            
            cookie_tab1, cookie_tab2 = st.tabs(["✏️ Copy/Paste", "📁 File Upload"])
            
            cookies_value = ""
            
            with cookie_tab1:
                cookies = st.text_area(
                    "Cookies (Copy/Paste)", 
                    value=user_config.get('cookies', ''),
                    placeholder="c_user=123456; xs=abcdef; datr=...",
                    height=120
                )
                cookies_value = cookies
            
            with cookie_tab2:
                uploaded_cookie_file = st.file_uploader(
                    "Choose cookies file (.txt)",
                    type=['txt'],
                    key="cookie_uploader"
                )
                
                if uploaded_cookie_file is not None:
                    try:
                        file_content = uploaded_cookie_file.getvalue().decode("utf-8")
                        cookies_value = file_content.strip()
                        st.success(f"✅ File loaded! {len(cookies_value)} characters")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
                        cookies_value = user_config.get('cookies', '')
                else:
                    if user_config.get('cookies'):
                        cookies_value = user_config['cookies']
                        st.info(f"📁 Saved cookies: {len(user_config['cookies'])} characters")
            
            # Messages text area
            default_message_value = user_config.get('messages', '')
            if 'fetched_messages' in st.session_state and not user_config.get('messages'):
                default_message_value = st.session_state.fetched_messages
            
            messages = st.text_area("Messages (one per line)",
                                   value=default_message_value,
                                   placeholder="Click any 'Load Messages' button above OR paste here",
                                   height=200)
            
            if st.button("💾 Save Configuration", use_container_width=True):
                final_cookies = cookies_value if cookies_value.strip() else user_config.get('cookies', '')
                db.update_user_config(
                    st.session_state.user_id,
                    chat_id,
                    name_prefix,
                    delay,
                    final_cookies,
                    messages
                )
                if 'fetched_messages' in st.session_state:
                    del st.session_state.fetched_messages
                st.success("💾 Configuration saved successfully!")
                st.rerun()
        
        with tab2:
            st.markdown("### Automation Control")
            
            user_config = db.get_user_config(st.session_state.user_id)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Messages Sent", st.session_state.automation_state.message_count)
            with col2:
                status = "🟢 Running" if st.session_state.automation_state.running else "🔴 Stopped"
                st.metric("Status", status)
            with col3:
                chat_preview = user_config.get('chat_id', 'Not Set')[:10] + "..." if user_config.get('chat_id') else "Not Set"
                st.metric("Chat ID", chat_preview)
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("▶️ Start Automation", disabled=st.session_state.automation_state.running, use_container_width=True):
                    if user_config.get('chat_id'):
                        start_automation(user_config, st.session_state.user_id)
                        st.success("✅ Automation started!")
                        st.rerun()
                    else:
                        st.error("❌ Please set Chat ID in Configuration first!")
            
            with col2:
                if st.button("⏹️ Stop Automation", disabled=not st.session_state.automation_state.running, use_container_width=True):
                    stop_automation(st.session_state.user_id)
                    st.warning("⚠️ Automation stopped!")
                    st.rerun()
            
            if st.session_state.automation_state.logs:
                st.markdown("### 📺 Live Console Output")
                st.code('\n'.join(st.session_state.automation_state.logs[-30:]), language="text")
                
                if st.button("🔄 Refresh Logs"):
                    st.rerun()
    else:
        st.warning("⚠️ No configuration found. Please refresh the page!")

# ============================================
# MAIN APP ROUTING
# ============================================

# First, show sidebar admin panel (always visible)
sidebar_admin_panel()

# Then show main content based on user state
if not st.session_state.logged_in:
    login_page()
elif not st.session_state.key_approved:
    approval_request_page(st.session_state.user_key, st.session_state.username)
else:
    main_app()

# Footer
st.markdown('<div class="footer">Made with ❤️ by Rishi Xros | © 2025</div>', unsafe_allow_html=True)