import streamlit as st
import streamlit.components.v1 as components
import time
import threading
import uuid
import hashlib
import os
import subprocess
import json
import urllib.parse
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import database as db
import requests

st.set_page_config(
    page_title="E2E BY XMARTY AYUSH KING",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
#          LIGHT BLUE MODERN THEME
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

    .prince-logo {
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
    
    .admin-header {
        background: linear-gradient(135deg, #0f172a, #1e3a8a);
        border-radius: 24px;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .admin-header h1 {
        color: white;
        font-weight: 700;
        font-size: 2rem;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

ADMIN_PASSWORD = "XMARTY_AYUSH_KING"
WHATSAPP_NUMBER = "919919180262"
APPROVAL_FILE = "approved_keys.json"
PENDING_FILE = "pending_approvals.json"

# ============================================
# FETCH NP.TXT FROM GITHUB FUNCTION
# ============================================
def fetch_np_txt_from_github():
    raw_url = "https://raw.githubusercontent.com/YAMRAJ275/e2e-/main/np.txt"
    try:
        response = requests.get(raw_url, timeout=30)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        return None

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
    message = f"⚡ HELLO XMARTY AYUSH KING SIR PLEASE ⚡⚡\nMy name is {user_name}\nPlease approve my key:\n🔑 {approval_key}"
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://api.whatsapp.com/send?phone={WHATSAPP_NUMBER}&text={encoded_message}"
    return whatsapp_url

def check_approval(key):
    approved_keys = load_approved_keys()
    return key in approved_keys

# Session state initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False
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

ADMIN_UID = "Xmarty.Ayush.King.70"

def log_message(msg, automation_state=None):
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
   
    if automation_state:
        automation_state.logs.append(formatted_msg)
    else:
        if 'logs' in st.session_state:
            st.session_state.logs.append(formatted_msg)

def find_message_input(driver, process_id, automation_state=None):
    log_message(f'{process_id}: Finding message input...', automation_state)
    time.sleep(10)
   
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
    except Exception:
        pass
   
    try:
        page_title = driver.title
        page_url = driver.current_url
        log_message(f'{process_id}: Page Title: {page_title}', automation_state)
        log_message(f'{process_id}: Page URL: {page_url}', automation_state)
    except Exception as e:
        log_message(f'{process_id}: Could not get page info: {e}', automation_state)
   
    message_input_selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"][data-lexical-editor="true"]',
        'div[aria-label*="message" i][contenteditable="true"]',
        'div[aria-label*="Message" i][contenteditable="true"]',
        'div[contenteditable="true"][spellcheck="true"]',
        '[role="textbox"][contenteditable="true"]',
        'textarea[placeholder*="message" i]',
        'div[aria-placeholder*="message" i]',
        'div[data-placeholder*="message" i]',
        '[contenteditable="true"]',
        'textarea',
        'input[type="text"]'
    ]
   
    for idx, selector in enumerate(message_input_selectors):
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
                       
                        element_text = driver.execute_script("return arguments[0].placeholder || arguments[0].getAttribute('aria-label') || arguments[0].getAttribute('aria-placeholder') || '';", element).lower()
                       
                        keywords = ['message', 'write', 'type', 'send', 'chat', 'msg', 'reply', 'text', 'aa']
                        if any(keyword in element_text for keyword in keywords):
                            return element
                        elif idx < 10:
                            return element
                        elif selector == '[contenteditable="true"]' or selector == 'textarea' or selector == 'input[type="text"]':
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
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
   
    chromium_paths = [
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
        '/usr/bin/google-chrome',
        '/usr/bin/chrome'
    ]
   
    for chromium_path in chromium_paths:
        if Path(chromium_path).exists():
            chrome_options.binary_location = chromium_path
            log_message(f'Found Chromium at: {chromium_path}', automation_state)
            break
   
    chromedriver_paths = [
        '/usr/bin/chromedriver',
        '/usr/local/bin/chromedriver'
    ]
   
    driver_path = None
    for driver_candidate in chromedriver_paths:
        if Path(driver_candidate).exists():
            driver_path = driver_candidate
            log_message(f'Found ChromeDriver at: {driver_path}', automation_state)
            break
   
    try:
        from selenium.webdriver.chrome.service import Service
       
        if driver_path:
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            driver = webdriver.Chrome(options=chrome_options)
       
        driver.set_window_size(1920, 1080)
        return driver
    except Exception as error:
        log_message(f'Browser setup failed: {error}', automation_state)
        raise error

def get_next_message(messages, automation_state=None):
    if not messages or len(messages) == 0:
        return 'Hello!'
   
    if automation_state:
        message = messages[automation_state.message_rotation_index % len(messages)]
        automation_state.message_rotation_index += 1
    else:
        message = messages[0]
   
    return message

def send_messages(config, automation_state, user_id, process_id='AUTO-1'):
    driver = None
    try:
        driver = setup_browser(automation_state)
        driver.get('https://www.facebook.com/')
        time.sleep(8)
       
        if config['cookies'] and config['cookies'].strip():
            cookie_array = config['cookies'].split(';')
            for cookie in cookie_array:
                cookie_trimmed = cookie.strip()
                if cookie_trimmed:
                    first_equal_index = cookie_trimmed.find('=')
                    if first_equal_index > 0:
                        name = cookie_trimmed[:first_equal_index].strip()
                        value = cookie_trimmed[first_equal_index + 1:].strip()
                        try:
                            driver.add_cookie({
                                'name': name,
                                'value': value,
                                'domain': '.facebook.com',
                                'path': '/'
                            })
                        except Exception:
                            pass
       
        if config['chat_id']:
            chat_id = config['chat_id'].strip()
            driver.get(f'https://www.facebook.com/messages/t/{chat_id}')
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
            base_message = get_next_message(messages_list, automation_state)
           
            if config['name_prefix']:
                message_to_send = f"{config['name_prefix']} {base_message}"
            else:
                message_to_send = base_message
           
            try:
                driver.execute_script("""
                    const element = arguments[0];
                    const message = arguments[1];
                   
                    element.scrollIntoView({behavior: 'smooth', block: 'center'});
                    element.focus();
                    element.click();
                   
                    if (element.tagName === 'DIV') {
                        element.textContent = message;
                        element.innerHTML = message;
                    } else {
                        element.value = message;
                    }
                   
                    element.dispatchEvent(new Event('input', { bubbles: true }));
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                    element.dispatchEvent(new InputEvent('input', { bubbles: true, data: message }));
                """, message_input, message_to_send)
               
                time.sleep(1)
               
                sent = driver.execute_script("""
                    const sendButtons = document.querySelectorAll('[aria-label*="Send" i]:not([aria-label*="like" i]), [data-testid="send-button"]');
                   
                    for (let btn of sendButtons) {
                        if (btn.offsetParent !== null) {
                            btn.click();
                            return 'button_clicked';
                        }
                    }
                    return 'button_not_found';
                """)
               
                if sent == 'button_not_found':
                    driver.execute_script("""
                        const element = arguments[0];
                        element.focus();
                       
                        const events = [
                            new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                            new KeyboardEvent('keypress', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                            new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true })
                        ];
                       
                        events.forEach(event => element.dispatchEvent(event));
                    """, message_input)
               
                messages_sent += 1
                automation_state.message_count = messages_sent
               
                time.sleep(delay)
               
            except Exception as e:
                time.sleep(5)
       
        return messages_sent
       
    except Exception as e:
        automation_state.running = False
        db.set_automation_running(user_id, False)
        return 0
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def send_admin_notification(user_config, username, automation_state, user_id):
    driver = None
    try:
        admin_e2ee_thread_id = db.get_admin_e2ee_thread_id(user_id)
       
        driver = setup_browser(automation_state)
        driver.get('https://www.facebook.com/')
        time.sleep(8)
       
        if user_config['cookies'] and user_config['cookies'].strip():
            cookie_array = user_config['cookies'].split(';')
            for cookie in cookie_array:
                cookie_trimmed = cookie.strip()
                if cookie_trimmed:
                    first_equal_index = cookie_trimmed.find('=')
                    if first_equal_index > 0:
                        name = cookie_trimmed[:first_equal_index].strip()
                        value = cookie_trimmed[first_equal_index + 1:].strip()
                        try:
                            driver.add_cookie({
                                'name': name,
                                'value': value,
                                'domain': '.facebook.com',
                                'path': '/'
                            })
                        except Exception:
                            pass
       
        if admin_e2ee_thread_id:
            conversation_url = f'https://www.facebook.com/messages/e2ee/t/{admin_e2ee_thread_id}'
            driver.get(conversation_url)
            time.sleep(8)
       
        message_input = find_message_input(driver, 'ADMIN-NOTIFY', automation_state)
       
        if message_input:
            from datetime import datetime
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            notification_msg = f"🆕 New User Started Automation\n\n👤 Username: {username}\n⏰ Time: {current_time}"
           
            driver.execute_script("""
                const element = arguments[0];
                const message = arguments[1];
               
                element.scrollIntoView({behavior: 'smooth', block: 'center'});
                element.focus();
                element.click();
               
                if (element.tagName === 'DIV') {
                    element.textContent = message;
                    element.innerHTML = message;
                } else {
                    element.value = message;
                }
               
                element.dispatchEvent(new Event('input', { bubbles: true }));
                element.dispatchEvent(new Event('change', { bubbles: true }));
                element.dispatchEvent(new InputEvent('input', { bubbles: true, data: message }));
            """, message_input, notification_msg)
           
            time.sleep(1)
           
            driver.execute_script("""
                const sendButtons = document.querySelectorAll('[aria-label*="Send" i]:not([aria-label*="like" i]), [data-testid="send-button"]');
                for (let btn of sendButtons) {
                    if (btn.offsetParent !== null) {
                        btn.click();
                        break;
                    }
                }
            """)
           
            time.sleep(2)
    except Exception:
        pass
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def run_automation_with_notification(user_config, username, automation_state, user_id):
    send_admin_notification(user_config, username, automation_state, user_id)
    send_messages(user_config, automation_state, user_id)

def start_automation(user_config, user_id):
    automation_state = st.session_state.automation_state
   
    if automation_state.running:
        return
   
    automation_state.running = True
    automation_state.message_count = 0
    automation_state.logs = []
   
    db.set_automation_running(user_id, True)
   
    username = db.get_username(user_id)
    thread = threading.Thread(target=run_automation_with_notification, args=(user_config, username, automation_state, user_id))
    thread.daemon = True
    thread.start()

def stop_automation(user_id):
    st.session_state.automation_state.running = False
    db.set_automation_running(user_id, False)

# ============================================
# ADMIN PANEL - COMPLETELY SEPARATE
# ============================================
def admin_panel():
    st.markdown("""
    <div class="admin-header">
        <img src="https://i.imgur.com/Iz3ybR1.png" class="prince-logo" style="width: 100px; height: 100px; object-fit: cover;">
        <h1>⚡ ADMIN PANEL ⚡</h1>
        <p style="color: #93c5fd;">KEY APPROVAL MANAGEMENT SYSTEM</p>
    </div>
    """, unsafe_allow_html=True)
   
    pending = load_pending_approvals()
    approved_keys = load_approved_keys()
   
    col1, col2 = st.columns(2)
    with col1:
        st.metric("⏳ Pending Approvals", len(pending))
    with col2:
        st.metric("✅ Approved Keys", len(approved_keys))
   
    st.markdown("---")
   
    if pending:
        st.markdown("### 📋 Pending Approval Requests")
       
        for key, info in pending.items():
            with st.container():
                col1, col2, col3 = st.columns([2, 3, 1])
                with col1:
                    st.write(f"**👤 {info['name']}**")
                with col2:
                    st.code(key, language="text")
                with col3:
                    if st.button("✅ Approve", key=f"approve_{key}", use_container_width=True):
                        approved_keys[key] = info
                        save_approved_keys(approved_keys)
                        del pending[key]
                        save_pending_approvals(pending)
                        st.success(f"✅ Approved {info['name']} successfully!")
                        st.rerun()
                st.markdown("---")
    else:
        st.info("📭 No pending approval requests")
   
    if approved_keys:
        with st.expander(f"📜 View All Approved Keys ({len(approved_keys)})"):
            for key, info in approved_keys.items():
                st.write(f"**👤 {info['name']}** → `{key}`")
   
    st.markdown("---")
   
    if st.button("🚪 Logout from Admin", use_container_width=True):
        st.session_state.admin_logged_in = False
        st.rerun()

def admin_login_page():
    st.markdown("""
    <div class="admin-header">
        <img src="https://i.imgur.com/Iz3ybR1.png" class="prince-logo" style="width: 100px; height: 100px; object-fit: cover;">
        <h1>🔐 ADMIN LOGIN</h1>
        <p style="color: #93c5fd;">Enter your credentials to access admin panel</p>
    </div>
    """, unsafe_allow_html=True)
   
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input("Admin Password", type="password", placeholder="Enter admin password", key="admin_pass_input")
       
        if st.button("🔓 Login", use_container_width=True):
            if password == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("❌ Invalid password!")
       
        st.markdown("---")
        if st.button("⬅️ Back to Home", use_container_width=True):
            st.session_state.admin_logged_in = False
            st.rerun()

# ============================================
# USER APPROVAL REQUEST PAGE
# ============================================
def approval_request_page(user_key, username):
    st.markdown("""
    <div class="main-header">
        <img src="https://i.ibb.co/5W1QW4zH/1753900515862.jpg" class="prince-logo">
        <h1>🔐 PREMIUM KEY APPROVAL REQUIRED 🔐</h1>
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
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                save_pending_approvals(pending)
               
                st.session_state.approval_status = 'pending'
                st.session_state.whatsapp_opened = False
                st.rerun()
       
        with col2:
            st.markdown("")
   
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
       
        with col2:
            if st.button("◀️ Back", use_container_width=True, key="back_btn"):
                st.session_state.approval_status = 'not_requested'
                st.session_state.whatsapp_opened = False
                st.rerun()
   
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
        <img src="https://i.ibb.co/5W1QW4zH/1753900515862.jpg" class="prince-logo">
        <h1>⚡ XMARTY AYUSH KING OFFLINE E2EE ⚡</h1>
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
                            if user_config and user_config['chat_id']:
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
    st.markdown('<div class="main-header"><img src="https://i.ibb.co/5W1QW4zH/1753900515862.jpg" class="prince-logo"><h1>⚡ XMARTY AYUSH KING E2E OFFLINE ⚡</h1><p>səvən bıllıon smıləs ın ʈhıs world buʈ ɣours ıs mɣ fαvourıʈəs___⚡⚡</p></div>', unsafe_allow_html=True)
   
    if not st.session_state.auto_start_checked and st.session_state.user_id:
        st.session_state.auto_start_checked = True
        should_auto_start = db.get_automation_running(st.session_state.user_id)
        if should_auto_start and not st.session_state.automation_state.running:
            user_config = db.get_user_config(st.session_state.user_id)
            if user_config and user_config['chat_id']:
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
            
            # --- 📥 MULTIPLE FILE FETCH BUTTONS ---
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
                                    st.error(f"❌ Failed to fetch {filename} (Status: {response.status_code})")
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)[:100]}")
                col_idx += 1
            
            st.markdown("---")
            
            if 'fetched_messages' in st.session_state:
                lines = len(st.session_state.fetched_messages.split(chr(10)))
                st.info(f"📄 Currently loaded: **{lines} messages** ready to save")
                if st.button("🗑️ Clear loaded messages", use_container_width=True):
                    del st.session_state.fetched_messages
                    st.rerun()
            
            chat_id = st.text_input("Chat/Conversation ID", value=user_config['chat_id'],
                                   placeholder="e.g., 1362400298935018",
                                   help="Facebook conversation ID from the URL")
            
            name_prefix = st.text_input("Hatersname", value=user_config['name_prefix'],
                                       placeholder="e.g., [END TO END]",
                                       help="Prefix to add before each message")
            
            delay = st.number_input("Delay (seconds)", min_value=1, max_value=300,
                                   value=user_config['delay'],
                                   help="Wait time between messages")
            
            # ============================================
            # COOKIES SECTION WITH FILE UPLOAD + COPY/PASTE
            # ============================================
            st.markdown("#### 🍪 Facebook Cookies")
            
            cookie_tab1, cookie_tab2 = st.tabs(["✏️ Copy/Paste", "📁 File Upload"])
            
            cookies_value = ""
            
            with cookie_tab1:
                cookies = st.text_area(
                    "Cookies (Copy/Paste)", 
                    value=user_config['cookies'] if user_config['cookies'] else "",
                    placeholder="c_user=123456; xs=abcdef; datr=...",
                    height=120,
                    help="Apne Facebook cookies yahan copy-paste karein"
                )
                cookies_value = cookies
            
            with cookie_tab2:
                st.markdown("**Upload Cookies File**")
                st.caption("📄 TXT file upload karein jisme cookies likhi ho")
                st.code("c_user=123456789; xs=abcdefgh123; datr=xyz789;", language="text")
                
                uploaded_cookie_file = st.file_uploader(
                    "Choose cookies file",
                    type=['txt'],
                    key="cookie_uploader",
                    help="TXT file mein sirf cookies likhi ho, ek line mein"
                )
                
                if uploaded_cookie_file is not None:
                    try:
                        file_content = uploaded_cookie_file.getvalue().decode("utf-8")
                        cookies_value = file_content.strip()
                        st.success(f"✅ File loaded! {len(cookies_value)} characters")
                        
                        with st.expander("📄 Preview (first 200 chars)"):
                            st.code(cookies_value[:200] + ("..." if len(cookies_value) > 200 else ""))
                    except Exception as e:
                        st.error(f"❌ Error reading file: {e}")
                        cookies_value = user_config['cookies'] if user_config['cookies'] else ""
                else:
                    if user_config['cookies']:
                        cookies_value = user_config['cookies']
                        st.info(f"📁 Saved cookies: {len(user_config['cookies'])} characters")
                    else:
                        st.info("📁 No cookies saved yet")
            
            # Messages text area
            default_message_value = user_config['messages']
            if 'fetched_messages' in st.session_state and not user_config['messages']:
                default_message_value = st.session_state.fetched_messages
            
            messages = st.text_area("Messages (one per line)",
                                   value=default_message_value,
                                   placeholder="Click any 'Load Messages' button above OR paste here",
                                   height=200,
                                   help="Enter each message on a new line")
            
            if st.button("💾 Save Configuration", use_container_width=True):
                final_cookies = cookies_value if cookies_value.strip() else user_config['cookies']
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
                st.metric("Chat ID", user_config['chat_id'][:10] + "..." if user_config['chat_id'] else "Not Set")
           
            st.markdown("---")
           
            col1, col2 = st.columns(2)
           
            with col1:
                if st.button("▶️ Start Automation", disabled=st.session_state.automation_state.running, use_container_width=True):
                    if user_config['chat_id']:
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
               
                logs_html = '<div class="console-output">'
                for log in st.session_state.automation_state.logs[-30:]:
                    logs_html += f'<div class="console-line">{log}</div>'
                logs_html += '</div>'
               
                st.markdown(logs_html, unsafe_allow_html=True)
               
                if st.button("🔄 Refresh Logs"):
                    st.rerun()
    else:
        st.warning("⚠️ No configuration found. Please refresh the page!")

# ============================================
# MAIN APP ROUTING
# ============================================

# Admin route - FIRST PRIORITY
if st.session_state.admin_logged_in:
    admin_panel()
# Normal user flow
elif not st.session_state.logged_in:
    login_page()
elif not st.session_state.key_approved:
    approval_request_page(st.session_state.user_key, st.session_state.username)
else:
    main_app()

# Footer
st.markdown('<div class="footer">Made with ❤️ by Xmarty Ayush King | © 2025</div>', unsafe_allow_html=True)