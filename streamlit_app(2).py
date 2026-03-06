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
import gc
import tempfile
from datetime import datetime

st.set_page_config(
    page_title="E2E YAMRAJ APPROVAL SYSTEM",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 👑 ROYAL / KINGLY THEME CSS
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Great+Vibes&family=Playfair+Display:wght@400;700&display=swap');

    * {
        font-family: 'Playfair Display', serif;
    }

    .stApp {
        background-image: linear-gradient(rgba(20, 0, 40, 0.88), rgba(40, 0, 80, 0.78)),
                          url('https://i.ibb.co/Rkp3VcHy/image.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    .main .block-container {
        background: rgba(30, 10, 60, 0.68);
        backdrop-filter: blur(12px);
        border-radius: 22px;
        padding: 32px;
        border: 2px solid rgba(255, 215, 0, 0.38);
        box-shadow: 0 12px 45px rgba(255, 215, 0, 0.18),
                    inset 0 0 28px rgba(255, 215, 0, 0.10);
    }

    .main-header {
        background: linear-gradient(135deg, #1a0033, #4b0082, #2a0055);
        border: 2px solid #ffd700;
        border-radius: 25px;
        padding: 2.4rem;
        text-align: center;
        margin-bottom: 2.8rem;
        box-shadow: 0 18px 55px rgba(0, 0, 0, 0.75),
                    0 0 35px rgba(255, 215, 0, 0.30);
        position: relative;
        overflow: hidden;
    }

    .main-header::before {
        content: "👑";
        position: absolute;
        top: -40px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 6.5rem;
        opacity: 0.14;
        color: #ffd700;
    }

    .main-header h1 {
        background: linear-gradient(90deg, #ffd700, #ffeb3b, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Cinzel Decorative', cursive;
        font-size: 3.4rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 0 25px rgba(255, 215, 0, 0.7);
    }

    .main-header p {
        color: #d4af37;
        font-family: 'Great Vibes', cursive;
        font-size: 1.8rem;
        margin-top: 0.7rem;
        letter-spacing: 1.8px;
    }

    .prince-logo {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        margin-bottom: 22px;
        border: 4px solid #ffd700;
        box-shadow: 0 0 35px rgba(255, 215, 0, 0.8),
                    inset 0 0 18px rgba(255, 255, 255, 0.35);
    }

    .stButton>button {
        background: linear-gradient(45deg, #b8860b, #ffd700, #daa520);
        color: #1a0033;
        border: 2px solid #b8860b;
        border-radius: 16px;
        padding: 1rem 2.4rem;
        font-family: 'Cinzel Decorative', cursive;
        font-weight: 700;
        font-size: 1.2rem;
        transition: all 0.4s ease;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.45);
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
        width: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-5px) scale(1.04);
        box-shadow: 0 15px 40px rgba(255, 215, 0, 0.75);
        background: linear-gradient(45deg, #ffd700, #ffeb3b, #ffd700);
    }

    /* ALL TASK CLOSE BUTTON */
    div[data-testid="column"]:nth-of-type(3) .stButton>button {
        background: linear-gradient(45deg, #8b0000, #ff4444, #8b0000) !important;
        color: white !important;
        border: 2px solid #ffd700 !important;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.5) !important;
        animation: pulse 2s infinite;
    }
    
    div[data-testid="column"]:nth-of-type(3) .stButton>button:hover {
        background: linear-gradient(45deg, #ff4444, #ff6666, #ff4444) !important;
        transform: scale(1.05) !important;
        box-shadow: 0 0 30px rgba(255, 0, 0, 0.8) !important;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 20px rgba(255, 0, 0, 0.5); }
        50% { box-shadow: 0 0 30px rgba(255, 0, 0, 0.8); }
        100% { box-shadow: 0 0 20px rgba(255, 0, 0, 0.5); }
    }
    
    /* Confirmation Dialog */
    .task-close-confirm {
        background: linear-gradient(135deg, #8b0000, #4b0082);
        border: 2px solid #ffd700;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        margin: 20px 0;
    }
    
    /* File Upload Area */
    .upload-area {
        background: rgba(40, 20, 80, 0.75);
        border: 2px dashed #ffd700;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        background: rgba(60, 30, 100, 0.85);
        border-color: #ffeb3b;
        transform: scale(1.02);
    }

    /* Console Output - Exactly like screenshot */
    .console-output {
        background: #0a0014;
        border: 2px solid #b8860b;
        border-radius: 12px;
        padding: 15px;
        color: #00ff00;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        max-height: 500px;
        overflow-y: auto;
        box-shadow: inset 0 0 20px rgba(255, 215, 0, 0.2);
    }

    .console-line {
        border-bottom: 1px solid #332211;
        padding: 8px 12px;
        margin: 4px 0;
        font-family: 'Courier New', monospace;
        white-space: pre-wrap;
        word-break: break-all;
        font-size: 13px;
    }
    
    .console-line-success {
        border-left: 4px solid #00ff00;
        background: rgba(0, 255, 0, 0.1);
        color: #aaffaa;
    }
    
    .console-line-info {
        border-left: 4px solid #ffd700;
        background: rgba(255, 215, 0, 0.1);
        color: #ffffaa;
    }
    
    .console-line-warning {
        border-left: 4px solid #ff9900;
        background: rgba(255, 153, 0, 0.1);
        color: #ffcc66;
    }
    
    .console-line-error {
        border-left: 4px solid #ff4444;
        background: rgba(255, 0, 0, 0.1);
        color: #ffaaaa;
    }
    
    .console-line-send {
        border-left: 4px solid #00ffff;
        background: rgba(0, 255, 255, 0.1);
        color: #aaffff;
    }
    
    /* Status Box */
    .status-box {
        background: linear-gradient(135deg, #1a0033, #2a0055);
        border: 2px solid #ffd700;
        border-radius: 16px;
        padding: 15px;
        margin: 10px 0;
        text-align: center;
    }
    
    .status-box h3 {
        color: #ffd700;
        font-family: 'Cinzel Decorative', cursive;
        margin: 0;
        font-size: 1.5rem;
    }
    
    .status-box p {
        color: #d4af37;
        font-size: 1.2rem;
        margin: 5px 0;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #ffd700;
        font-size: 2rem;
        font-weight: 700;
        text-shadow: 0 0 18px rgba(255, 215, 0, 0.7);
    }
    
    [data-testid="stMetricLabel"] {
        color: #d4af37;
        font-weight: 500;
        font-size: 1rem;
    }
    
    /* Running animation */
    .running-dot {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #00ff00;
        margin-right: 8px;
        animation: blink 1s infinite;
    }
    
    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0.3; }
        100% { opacity: 1; }
    }

    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stNumberInput>div>div>input {
        background: rgba(40, 20, 80, 0.75);
        border: 2px solid #b8860b;
        border-radius: 14px;
        color: #ffd700;
        padding: 1rem;
        font-size: 1.1rem;
    }

    .stTextInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {
        color: #d4af37aa;
    }

    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #ffd700;
        box-shadow: 0 0 0 4px rgba(255, 215, 0, 0.35);
        background: rgba(50, 30, 90, 0.85);
    }

    label {
        color: #ffd700 !important;
        font-weight: 600 !important;
        font-size: 1.15rem !important;
        text-shadow: 1px 1px 4px #000;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: rgba(30, 10, 60, 0.65);
        border-radius: 16px;
        padding: 10px;
        border: 1px solid #b8860b;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(75, 0, 130, 0.55);
        color: #d4af37;
        border-radius: 12px;
        padding: 14px 26px;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #b8860b, #ffd700);
        color: #1a0033;
    }

    .whatsapp-btn {
        background: linear-gradient(45deg, #006400, #228b22, #006400);
        border: 2px solid #ffd700;
        color: #ffd700;
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        box-shadow: 0 8px 25px rgba(0, 100, 0, 0.55);
        text-decoration: none;
        padding: 12px 24px;
        border-radius: 16px;
        display: inline-block;
        margin: 10px 0;
    }

    .whatsapp-btn:hover {
        background: linear-gradient(45deg, #228b22, #32cd32, #228b22);
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(50, 205, 50, 0.7);
        text-decoration: none;
        color: #ffd700;
    }

    .footer {
        background: rgba(30, 10, 60, 0.75);
        border-top: 3px solid #b8860b;
        color: #d4af37;
        font-family: 'Great Vibes', cursive;
        font-size: 1.5rem;
        padding: 2.8rem;
        text-shadow: 1px 1px 5px #000;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# WhatsApp number for notifications
WHATSAPP_NUMBER = "7654221354"

# Approval System Constants
ADMIN_PASSWORD = "YAMRAJ_ADMIN_2025"
APPROVAL_FILE = "approved_keys.json"
PENDING_FILE = "pending_approvals.json"

def generate_user_key(username, password):
    combined = f"{username}:{password}"
    key_hash = hashlib.sha256(combined.encode()).hexdigest()[:8].upper()
    return f"KEY-{key_hash}"

# Approval System Functions
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
    message = f"👑 HELLO YAMRAJ SIR PLEASE APPROVE 👑\nMy name is {user_name}\nPlease approve my key:\n🔑 {approval_key}"
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://api.whatsapp.com/send?phone={WHATSAPP_NUMBER}&text={encoded_message}"
    return whatsapp_url

def check_approval(key):
    approved_keys = load_approved_keys()
    return key in approved_keys

# Session State Initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
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
if 'show_close_confirmation' not in st.session_state:
    st.session_state.show_close_confirmation = False
if 'last_file_check' not in st.session_state:
    st.session_state.last_file_check = 0
if 'last_file_load' not in st.session_state:
    st.session_state.last_file_load = 0
if 'messages_content' not in st.session_state:
    st.session_state.messages_content = ""
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()

class AutomationState:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.logs = []
        self.message_rotation_index = 0
        self.driver = None
        self.current_chat_id = None
        self.speed = 0
        self.total_messages = 0
        self.start_time = None

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

if 'auto_start_checked' not in st.session_state:
    st.session_state.auto_start_checked = False

ADMIN_UID = "YAMRAJ DEV"

def log_message(msg, msg_type="info", automation_state=None):
    """Enhanced log message with timestamp and type"""
    now = datetime.now()
    timestamp = now.strftime("%I:%M:%S %p")  # 12-hour format with AM/PM
    
    # Create formatted message based on type
    if msg_type == "success":
        formatted_msg = f"[{timestamp}] ✅ {msg}"
    elif msg_type == "error":
        formatted_msg = f"[{timestamp}] ❌ {msg}"
    elif msg_type == "warning":
        formatted_msg = f"[{timestamp}] ⚠️ {msg}"
    elif msg_type == "send":
        formatted_msg = f"[{timestamp}] 📤 {msg}"
    elif msg_type == "load":
        formatted_msg = f"[{timestamp}] 📥 {msg}"
    else:
        formatted_msg = f"[{timestamp}] {msg}"
   
    if automation_state:
        automation_state.logs.append(formatted_msg)
        # Keep only last 100 logs to prevent memory issues
        if len(automation_state.logs) > 100:
            automation_state.logs = automation_state.logs[-100:]
    else:
        if 'logs' in st.session_state:
            st.session_state.logs.append(formatted_msg)
            if len(st.session_state.logs) > 100:
                st.session_state.logs = st.session_state.logs[-100:]
    
    return formatted_msg

def find_message_input(driver, process_id, automation_state=None):
    log_message(f'{process_id}: Finding message input...', "info", automation_state)
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
        log_message(f'{process_id}: Page Title: {page_title}', "info", automation_state)
        log_message(f'{process_id}: Page URL: {page_url}', "info", automation_state)
    except Exception as e:
        log_message(f'{process_id}: Could not get page info: {e}', "warning", automation_state)
   
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
   
    log_message(f'{process_id}: Trying {len(message_input_selectors)} selectors...', "info", automation_state)
   
    for idx, selector in enumerate(message_input_selectors):
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            log_message(f'{process_id}: Selector {idx+1} found {len(elements)} elements', "info", automation_state)
           
            for element in elements:
                try:
                    is_editable = driver.execute_script("""
                        return arguments[0].contentEditable === 'true' ||
                               arguments[0].tagName === 'TEXTAREA' ||
                               arguments[0].tagName === 'INPUT';
                    """, element)
                   
                    if is_editable:
                        log_message(f'{process_id}: Found editable element', "info", automation_state)
                       
                        try:
                            element.click()
                            time.sleep(0.5)
                        except:
                            pass
                       
                        element_text = driver.execute_script("return arguments[0].placeholder || arguments[0].getAttribute('aria-label') || arguments[0].getAttribute('aria-placeholder') || '';", element).lower()
                       
                        keywords = ['message', 'write', 'type', 'send', 'chat', 'msg', 'reply', 'text', 'aa']
                        if any(keyword in element_text for keyword in keywords):
                            log_message(f'{process_id}: ✅ Found message input', "success", automation_state)
                            return element
                        elif idx < 10:
                            log_message(f'{process_id}: ✅ Using primary selector', "success", automation_state)
                            return element
                        elif selector == '[contenteditable="true"]' or selector == 'textarea' or selector == 'input[type="text"]':
                            log_message(f'{process_id}: ✅ Using fallback element', "success", automation_state)
                            return element
                except Exception as e:
                    log_message(f'{process_id}: Element check failed', "warning", automation_state)
                    continue
        except Exception as e:
            continue
   
    return None

def setup_browser(automation_state=None):
    log_message('Setting up Chrome browser...', "info", automation_state)
   
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
            log_message(f'Found Chromium at: {chromium_path}', "info", automation_state)
            break
   
    chromedriver_paths = [
        '/usr/bin/chromedriver',
        '/usr/local/bin/chromedriver'
    ]
   
    driver_path = None
    for driver_candidate in chromedriver_paths:
        if Path(driver_candidate).exists():
            driver_path = driver_candidate
            log_message(f'Found ChromeDriver at: {driver_path}', "info", automation_state)
            break
   
    try:
        from selenium.webdriver.chrome.service import Service
       
        if driver_path:
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            log_message('Chrome started with detected ChromeDriver!', "success", automation_state)
        else:
            driver = webdriver.Chrome(options=chrome_options)
            log_message('Chrome started with default driver!', "success", automation_state)
       
        driver.set_window_size(1920, 1080)
        log_message('Chrome browser setup completed successfully!', "success", automation_state)
        return driver
    except Exception as error:
        log_message(f'Browser setup failed: {error}', "error", automation_state)
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
        # Record start time
        automation_state.start_time = datetime.now()
        
        # Load messages
        messages_list = [msg.strip() for msg in config['messages'].split('\n') if msg.strip()]
        total_msgs = len(messages_list)
        automation_state.total_messages = total_msgs
        
        # Calculate total characters
        total_chars = sum(len(msg) for msg in messages_list)
        
        log_message(f'Message loaded: {total_chars} chars', "load", automation_state)
        log_message(f'Starting FAST send to 1 threads', "info", automation_state)
        
        delay = int(config['delay'])
        delay_ms = delay * 1000 if delay < 100 else delay
        speed_text = f"Speed: {delay_ms}ms delay, 2 messages each"
        log_message(speed_text, "info", automation_state)
        automation_state.speed = delay_ms
        
        driver = setup_browser(automation_state)
        automation_state.driver = driver
       
        log_message(f'Navigating to Facebook...', "info", automation_state)
        driver.get('https://www.facebook.com/')
        time.sleep(8)
       
        if config['cookies'] and config['cookies'].strip():
            log_message(f'Adding cookies...', "info", automation_state)
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
            automation_state.current_chat_id = chat_id
            log_message(f'Opening conversation {chat_id}...', "info", automation_state)
            driver.get(f'https://www.facebook.com/messages/t/{chat_id}')
        else:
            log_message(f'Opening messages...', "info", automation_state)
            driver.get('https://www.facebook.com/messages')
       
        time.sleep(15)
       
        message_input = find_message_input(driver, process_id, automation_state)
       
        if not message_input:
            log_message(f'Message input not found!', "error", automation_state)
            automation_state.running = False
            db.set_automation_running(user_id, False)
            return 0
       
        messages_sent = 0
       
        if not messages_list:
            messages_list = ['Hello!']
       
        while automation_state.running and messages_sent < len(messages_list):
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
               
                # Exactly like screenshot format
                log_message(f"[{config['chat_id']}] Message {messages_sent}/{len(messages_list)} sent", "send", automation_state)
               
                # Convert ms to seconds for sleep
                sleep_time = delay_ms / 1000
                time.sleep(sleep_time)
               
            except Exception as e:
                log_message(f'Send error: {str(e)[:100]}', "error", automation_state)
                time.sleep(5)
       
        log_message(f'All messages sent successfully!', "success", automation_state)
        log_message(f'Total: {messages_sent} messages sent', "success", automation_state)
        
        # Stop automation after completion
        automation_state.running = False
        db.set_automation_running(user_id, False)
        
        return messages_sent
       
    except Exception as e:
        log_message(f'Fatal error: {str(e)}', "error", automation_state)
        automation_state.running = False
        db.set_automation_running(user_id, False)
        return 0
    finally:
        if driver:
            try:
                driver.quit()
                log_message(f'Browser closed', "info", automation_state)
            except:
                pass

def start_automation(user_config, user_id):
    automation_state = st.session_state.automation_state
   
    if automation_state.running:
        return
   
    automation_state.running = True
    automation_state.message_count = 0
    automation_state.logs = []
    automation_state.current_chat_id = user_config['chat_id']
    automation_state.start_time = datetime.now()
   
    db.set_automation_running(user_id, True)
   
    thread = threading.Thread(target=send_messages, args=(user_config, automation_state, user_id))
    thread.daemon = True
    thread.start()

def stop_automation(user_id):
    st.session_state.automation_state.running = False
    db.set_automation_running(user_id, False)
    
    # Log stop message
    log_message("Automation stopped by user", "warning", st.session_state.automation_state)

def admin_panel():
    st.markdown("""
    <div class="main-header">
        <img src="https://i.ibb.co/Rkp3VcHy/image.jpg" class="prince-logo">
        <h1>👑 ADMIN PANEL 👑</h1>
        <p>KEY APPROVAL MANAGEMENT</p>
    </div>
    """, unsafe_allow_html=True)
   
    pending = load_pending_approvals()
    approved_keys = load_approved_keys()
   
    st.success(f"**Total Approved Keys:** {len(approved_keys)}")
    st.warning(f"**Pending Approvals:** {len(pending)}")
   
    if pending:
        st.markdown("#### ⏳ Pending Approval Requests")
       
        for key, info in pending.items():
            col1, col2, col3 = st.columns([2, 2, 1])
           
            with col1:
                st.text(f"👤 {info['name']}")
            with col2:
                st.text(f"🔑 {key}")
            with col3:
                if st.button("✅", key=f"approve_{key}"):
                    approved_keys[key] = info
                    save_approved_keys(approved_keys)
                    del pending[key]
                    save_pending_approvals(pending)
                    st.success(f"Approved {info['name']}!")
                    st.rerun()
    else:
        st.info("No pending approvals")
   
    if approved_keys:
        st.markdown("#### ✅ Approved Keys")
        for key, info in approved_keys.items():
            st.text(f"👤 {info['name']} - 🔑 {key}")
   
    if st.button("🚪 Logout", key="admin_logout_btn"):
        st.session_state.approval_status = 'login'
        st.rerun()

def approval_request_page(user_key, username):
    st.markdown("""
    <div class="main-header">
        <img src="https://i.ibb.co/Rkp3VcHy/image.jpg" class="prince-logo">
        <h1>👑 PREMIUM KEY APPROVAL REQUIRED 👑</h1>
        <p>ONE MONTH 500 RS PAID</p>
    </div>
    """, unsafe_allow_html=True)
   
    if st.session_state.approval_status == 'not_requested':
        st.markdown("### 🔑 Request Access")
        st.info(f"**Your Unique Key:** `{user_key}`")
        st.info(f"**Username:** {username}")
       
        col1, col2 = st.columns([1, 1])
       
        with col1:
            if st.button("📲 Request Approval", use_container_width=True, key="request_approval_btn"):
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
            if st.button("👑 Admin Panel", use_container_width=True, key="admin_panel_btn"):
                st.session_state.approval_status = 'admin_login'
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
                📱 Click Here to Open WhatsApp
            </a>
        </div>
        """, unsafe_allow_html=True)
       
        st.markdown("### 📝 Message Preview:")
        st.code(f"""👑 HELLO YAMRAJ SIR PLEASE APPROVE 👑
My name is {username}
Please approve my key:
🔑 {user_key}""")
       
        st.markdown("---")
       
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
            if st.button("🔙 Back", use_container_width=True, key="back_btn"):
                st.session_state.approval_status = 'not_requested'
                st.session_state.whatsapp_opened = False
                st.rerun()
   
    elif st.session_state.approval_status == 'admin_login':
        st.markdown("### 👑 Admin Login")
       
        admin_password = st.text_input("Enter Admin Password:", type="password", key="admin_password_input")
       
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔑 Login", use_container_width=True, key="admin_login_btn"):
                if admin_password == ADMIN_PASSWORD:
                    st.session_state.approval_status = 'admin_panel'
                    st.rerun()
                else:
                    st.error("❌ Invalid password!")
       
        with col2:
            if st.button("🔙 Back", use_container_width=True, key="admin_back_btn"):
                st.session_state.approval_status = 'not_requested'
                st.rerun()
   
    elif st.session_state.approval_status == 'admin_panel':
        admin_panel()

def login_page():
    st.markdown("""
    <div class="main-header">
        <img src="https://i.ibb.co/Rkp3VcHy/image.jpg" class="prince-logo">
        <h1>👑 E2E YAMRAJ APPROVAL SYSTEM 👑</h1>
        <p>səvən bıllıon smılə's ın ʈhıs world buʈ ɣour's ıs mɣ fαvourıʈəs___💫💫</p>
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

def main_app():
    st.markdown('<div class="main-header"><img src="https://i.ibb.co/Rkp3VcHy/image.jpg" class="prince-logo"><h1>👑 E2E YAMRAJ APPROVAL SYSTEM 👑</h1><p>səvən bıllıon smıləs ın ʈhıs world buʈ ɣours ıs mɣ fαvourıʈəs___💫💫</p></div>', unsafe_allow_html=True)
   
    if not st.session_state.auto_start_checked and st.session_state.user_id:
        st.session_state.auto_start_checked = True
        should_auto_start = db.get_automation_running(st.session_state.user_id)
        if should_auto_start and not st.session_state.automation_state.running:
            user_config = db.get_user_config(st.session_state.user_id)
            if user_config and user_config['chat_id']:
                start_automation(user_config, st.session_state.user_id)
   
    st.sidebar.markdown(f"### 👤 {st.session_state.username}")
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
           
            chat_id = st.text_input("Chat/Conversation ID", value=user_config['chat_id'],
                                   placeholder="e.g., 1362400298935018")
           
            name_prefix = st.text_input("Hatersname", value=user_config['name_prefix'],
                                       placeholder="e.g., [END TO END]")
            
            # Convert delay to milliseconds for display
            current_delay = user_config['delay']
            if current_delay < 100:
                display_delay = current_delay * 1000
            else:
                display_delay = current_delay
                
            delay_ms = st.number_input("Delay (ms)", min_value=100, max_value=30000, step=100,
                                   value=display_delay,
                                   help="Delay in milliseconds between messages")
           
            # Cookies text area
            cookies_content = st.text_area("Facebook Cookies", 
                                          value=user_config['cookies'],
                                          placeholder="Paste your Facebook cookies here...",
                                          height=150)
            
            st.markdown("#### 📁 Messages File (Touch to Upload)")
            
            # File uploader
            uploaded_file = st.file_uploader("Touch to upload np.txt", type=["txt"], key="msg_uploader")
            
            if uploaded_file is not None:
                # Read file
                file_content = uploaded_file.read().decode("utf-8")
                st.session_state.messages_content = file_content
                st.session_state.last_file_load = time.time()
                line_count = len(file_content.splitlines())
                st.success(f"✅ {uploaded_file.name} uploaded! Lines: {line_count}")
                st.rerun()
            
            # Messages preview
            messages_to_show = st.session_state.get('messages_content', user_config['messages'])
            line_count = len(messages_to_show.split('\n')) if messages_to_show else 0
            
            # Show preview with line count
            preview_text = messages_to_show[:500] + "..." if len(messages_to_show) > 500 else messages_to_show
            st.text_area("Messages Preview", 
                        value=preview_text,
                        height=150,
                        disabled=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"📊 Total lines: {line_count}")
            with col2:
                if st.button("🔄 Clear Upload", use_container_width=True):
                    if 'messages_content' in st.session_state:
                        del st.session_state.messages_content
                    st.rerun()
            
            if st.button("💾 Save Configuration", use_container_width=True):
                final_messages = st.session_state.get('messages_content', user_config['messages'])
                # Convert ms back to seconds for storage
                delay_seconds = delay_ms // 1000
                
                db.update_user_config(
                    st.session_state.user_id,
                    chat_id,
                    name_prefix,
                    delay_seconds,
                    cookies_content,
                    final_messages
                )
                st.success("✅ Configuration saved successfully!")
                st.rerun()
       
        with tab2:
            st.markdown("### Automation Control")
            
            # Status Box with animation
            if st.session_state.automation_state.running:
                status_html = """
                <div class="status-box">
                    <h3>⚡ AUTOMATION RUNNING ⚡</h3>
                    <p><span class="running-dot"></span> LIVE - Sending messages...</p>
                </div>
                """
            else:
                status_html = """
                <div class="status-box">
                    <h3>⚡ AUTOMATION STOPPED ⚡</h3>
                    <p>🔴 Ready to start</p>
                </div>
                """
            st.markdown(status_html, unsafe_allow_html=True)
            
            # Metrics in 4 columns
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Messages Sent", st.session_state.automation_state.message_count)
            with col2:
                status = "🟢 RUNNING" if st.session_state.automation_state.running else "🔴 STOPPED"
                st.metric("Status", status)
            with col3:
                chat_display = user_config['chat_id'][:8] + "..." if user_config['chat_id'] and len(user_config['chat_id']) > 8 else user_config['chat_id'] or "Not Set"
                st.metric("Chat ID", chat_display)
            with col4:
                # Show speed in ms
                if user_config['delay']:
                    speed_ms = user_config['delay'] * 1000 if user_config['delay'] < 100 else user_config['delay']
                    st.metric("Speed", f"{speed_ms}ms")
                else:
                    st.metric("Speed", "Not Set")
            
            st.markdown("---")
            
            # Control buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("▶️ START AUTOMATION", disabled=st.session_state.automation_state.running, use_container_width=True):
                    if user_config['chat_id']:
                        if not user_config['cookies']:
                            st.warning("⚠️ Please add your Facebook cookies in Configuration first!")
                        else:
                            start_automation(user_config, st.session_state.user_id)
                            st.success("✅ Automation started!")
                            st.rerun()
                    else:
                        st.error("❌ Please set Chat ID in Configuration first!")
            
            with col2:
                if st.button("⏹️ STOP AUTOMATION", disabled=not st.session_state.automation_state.running, use_container_width=True):
                    stop_automation(st.session_state.user_id)
                    st.warning("⏹️ Automation stopped!")
                    st.rerun()
            
            with col3:
                if st.button("🗑️ ALL TASK CLOSE", use_container_width=True):
                    st.session_state.show_close_confirmation = True
                    st.rerun()
            
            # Confirmation Dialog
            if st.session_state.get('show_close_confirmation', False):
                st.markdown("""
                <div class="task-close-confirm">
                    <h3 style="color: #ffd700;">⚠️ WARNING ⚠️</h3>
                    <p style="color: white;">Are you sure you want to close ALL tasks?</p>
                    <p style="color: #ffaaaa;">This will stop automation and close browser!</p>
                </div>
                """, unsafe_allow_html=True)
                
                conf_col1, conf_col2 = st.columns(2)
                
                with conf_col1:
                    if st.button("✅ YES, CLOSE ALL", use_container_width=True):
                        st.session_state.show_close_confirmation = False
                        
                        with st.spinner("🧹 Cleaning up all tasks..."):
                            # Stop automation
                            if st.session_state.automation_state.running:
                                st.session_state.automation_state.running = False
                                db.set_automation_running(st.session_state.user_id, False)
                            
                            # Close browser
                            if hasattr(st.session_state.automation_state, 'driver') and st.session_state.automation_state.driver:
                                try:
                                    st.session_state.automation_state.driver.quit()
                                    st.session_state.automation_state.driver = None
                                except:
                                    pass
                            
                            # Kill processes
                            try:
                                os.system("pkill -f chrome")
                                os.system("pkill -f chromedriver")
                            except:
                                pass
                            
                            # Clean session
                            st.session_state.automation_state.message_count = 0
                            st.session_state.automation_state.logs = []
                            st.session_state.automation_state.message_rotation_index = 0
                            st.session_state.automation_state.start_time = None
                            
                            # Clean temp files
                            temp_dir = tempfile.gettempdir()
                            for file in os.listdir(temp_dir):
                                if file.startswith('tmp') and (file.endswith('.log') or file.endswith('.tmp')):
                                    try:
                                        os.remove(os.path.join(temp_dir, file))
                                    except:
                                        pass
                            
                            gc.collect()
                            time.sleep(2)
                            st.success("✅ All tasks closed successfully!")
                            st.rerun()
                
                with conf_col2:
                    if st.button("❌ NO, CANCEL", use_container_width=True):
                        st.session_state.show_close_confirmation = False
                        st.rerun()
            
            st.markdown("---")
            
            # AUTO-REFRESH LOGIC - Every 2 seconds when running
            if st.session_state.automation_state.running:
                # Check if 2 seconds have passed since last refresh
                current_time = time.time()
                if current_time - st.session_state.last_refresh > 2:
                    st.session_state.last_refresh = current_time
                    st.rerun()
            
            # Live Console Output - Exactly like screenshot
            if st.session_state.automation_state.logs:
                st.markdown("### 📟 LIVE CONSOLE OUTPUT")
                
                logs_html = '<div class="console-output">'
                
                # Show last 20 logs
                for log in st.session_state.automation_state.logs[-20:]:
                    # Determine log type for styling
                    if "✅" in log or "successfully" in log.lower():
                        log_class = "console-line-success"
                    elif "❌" in log or "error" in log.lower() or "failed" in log.lower():
                        log_class = "console-line-error"
                    elif "⚠️" in log or "warning" in log.lower():
                        log_class = "console-line-warning"
                    elif "📤" in log or "sent" in log.lower():
                        log_class = "console-line-send"
                    elif "📥" in log or "loaded" in log.lower():
                        log_class = "console-line-info"
                    else:
                        log_class = "console-line-info"
                    
                    logs_html += f'<div class="console-line {log_class}">{log}</div>'
                
                logs_html += '</div>'
                
                # Auto-scroll JavaScript
                logs_html += """
                <script>
                    function scrollToBottom() {
                        var consoleDiv = document.querySelector('.console-output');
                        if (consoleDiv) {
                            consoleDiv.scrollTop = consoleDiv.scrollHeight;
                        }
                    }
                    setTimeout(scrollToBottom, 100);
                    setTimeout(scrollToBottom, 500);
                    setTimeout(scrollToBottom, 1000);
                </script>
                """
                
                st.markdown(logs_html, unsafe_allow_html=True)
                
                # Live status footer
                total_logs = len(st.session_state.automation_state.logs)
                if st.session_state.automation_state.running:
                    st.info(f"🔄 LIVE: Message #{st.session_state.automation_state.message_count} | Total logs: {total_logs} | Auto-refresh every 2s")
                else:
                    st.info(f"📊 Total logs: {total_logs} | Messages sent: {st.session_state.automation_state.message_count}")
    else:
        st.warning("⚠️ No configuration found. Please refresh the page!")

# Main app flow - with approval system
if not st.session_state.logged_in:
    login_page()
elif not st.session_state.key_approved:
    approval_request_page(st.session_state.user_key, st.session_state.username)
else:
    main_app()

st.markdown('<div class="footer">Made with ❤️ by YAMRAJ | © 2025</div>', unsafe_allow_html=True)