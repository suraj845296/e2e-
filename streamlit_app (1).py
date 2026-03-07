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
import psutil
from datetime import datetime

st.set_page_config(
    page_title="E2E RISHU SERVER",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
custom_css = """
<style>
    /* Clean font for everyone */
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Background */
    .stApp {
        background: linear-gradient(135deg, #000428, #004e92);
    }

    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        border: 2px solid #00ffff;
    }

    /* Header with RISHU name */
    .main-header {
        background: linear-gradient(135deg, #000428, #004e92);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        text-align: center;
        border: 3px solid #00ffff;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.3);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 3rem;
        color: #00ffff;
        text-shadow: 0 0 20px #00ffff;
    }
    
    .main-header p {
        color: white;
        font-size: 1.2rem;
        margin: 5px 0 0 0;
    }

    /* E2E Server Badge */
    .server-badge {
        display: inline-block;
        background: #00ffff;
        color: black;
        padding: 5px 20px;
        border-radius: 30px;
        font-weight: bold;
        margin-top: 10px;
        animation: glow 2s infinite;
    }
    
    @keyframes glow {
        0% { box-shadow: 0 0 5px #00ffff; }
        50% { box-shadow: 0 0 20px #00ffff; }
        100% { box-shadow: 0 0 5px #00ffff; }
    }

    /* Uptime Engine - Live Display */
    .uptime-engine {
        background: linear-gradient(135deg, #000428, #001f3f);
        border: 3px solid #00ffff;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 25px;
        color: white;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.3);
    }
    
    .uptime-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 15px;
        border-bottom: 1px solid #00ffff;
        padding-bottom: 10px;
    }
    
    .uptime-header h2 {
        color: #00ffff;
        margin: 0;
        font-size: 1.8rem;
        text-shadow: 0 0 10px #00ffff;
    }
    
    .live-badge {
        background: #00ffff;
        color: black;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        animation: pulse 1s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    /* Live Display Grid */
    .uptime-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
        margin-bottom: 15px;
    }
    
    .uptime-card {
        background: rgba(0, 255, 255, 0.1);
        border: 1px solid #00ffff;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        transition: all 0.3s;
    }
    
    .uptime-card:hover {
        background: rgba(0, 255, 255, 0.2);
        transform: scale(1.02);
    }
    
    .uptime-card .label {
        color: #00ffff;
        font-size: 0.9rem;
        text-transform: uppercase;
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    .uptime-card .value {
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
    }

    /* GitHub Button */
    .github-btn {
        background: linear-gradient(135deg, #6e5494, #bd93f9);
        border: none;
        border-radius: 50px;
        padding: 15px;
        text-align: center;
        margin: 20px 0;
        cursor: pointer;
        transition: all 0.3s;
        border: 2px solid white;
        box-shadow: 0 0 20px rgba(110, 84, 148, 0.5);
    }
    
    .github-btn:hover {
        transform: scale(1.02);
        box-shadow: 0 0 40px rgba(110, 84, 148, 0.8);
    }

    /* Cookies Upload Button */
    .cookies-upload {
        background: linear-gradient(135deg, #ff9900, #ff5500);
        border: none;
        border-radius: 50px;
        padding: 15px;
        text-align: center;
        margin: 20px 0;
        cursor: pointer;
        transition: all 0.3s;
        border: 2px solid white;
        box-shadow: 0 0 20px rgba(255, 153, 0, 0.5);
    }
    
    .cookies-upload:hover {
        transform: scale(1.02);
        box-shadow: 0 0 40px rgba(255, 153, 0, 0.8);
    }

    /* Buttons */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        padding: 10px 20px;
        transition: all 0.3s;
        border: none;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
    }

    /* START Button */
    div[data-testid="column"]:nth-of-type(1) .stButton>button {
        background: linear-gradient(135deg, #00b09b, #96c93d);
        color: white;
    }
    
    /* STOP Button */
    div[data-testid="column"]:nth-of-type(2) .stButton>button {
        background: linear-gradient(135deg, #eb3349, #f45c43);
        color: white;
    }
    
    /* CLOSE ALL Button */
    div[data-testid="column"]:nth-of-type(3) .stButton>button {
        background: linear-gradient(135deg, #f12711, #f5af19);
        color: white;
        animation: pulse 2s infinite;
    }

    /* Input Fields */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stNumberInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #00ffff;
        padding: 12px;
        font-size: 1rem;
        color: black !important;
        background: white;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus,
    .stNumberInput>div>div>input:focus {
        border-color: #000428;
        box-shadow: 0 0 0 3px rgba(0, 255, 255, 0.3);
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #00ffff;
        font-size: 2rem;
        font-weight: 700;
        text-shadow: 0 0 10px #00ffff;
    }
    
    [data-testid="stMetricLabel"] {
        color: #000428;
        font-weight: 600;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: white;
        padding: 20px;
        font-size: 1rem;
        border-top: 2px solid #00ffff;
        margin-top: 30px;
    }
    
    .rishu-signature {
        color: #00ffff;
        font-weight: bold;
        font-size: 1.2rem;
        text-shadow: 0 0 10px #00ffff;
    }
    
    /* Console Output */
    .console-output {
        background: #1e1e2f;
        border-radius: 10px;
        padding: 15px;
        color: #00ff00;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        max-height: 400px;
        overflow-y: auto;
        margin-top: 20px;
        border: 2px solid #00ffff;
    }

    .console-line {
        border-bottom: 1px solid #333;
        padding: 5px 10px;
        margin: 3px 0;
        font-family: 'Courier New', monospace;
        color: #00ff00;
    }
    
    .console-line.success { color: #00ff00; }
    .console-line.error { color: #ff4444; }
    .console-line.warning { color: #ffff00; }
    .console-line.send { color: #00ffff; }
    .console-line.info { color: #aaaaaa; }
    .console-line.github { color: #bd93f9; }
    
    /* Direct Access */
    .direct-access {
        background: linear-gradient(135deg, #00b09b, #96c93d);
        border: none;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin: 10px 0;
        color: white;
        font-weight: bold;
    }
    
    /* Status Indicators */
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 5px;
    }
    
    .status-green { background-color: #00ff00; box-shadow: 0 0 10px #00ff00; }
    .status-yellow { background-color: #ffff00; box-shadow: 0 0 10px #ffff00; }
    .status-red { background-color: #ff0000; box-shadow: 0 0 10px #ff0000; }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# ==================== CONSTANTS ====================
UPTIME_START = datetime.now()
GITHUB_RAW_URL = "https://raw.githubusercontent.com/YAMRAJ275/e2e-/main/np.txt"

# ==================== SESSION STATE ====================
if 'user_id' not in st.session_state:
    # Create default user automatically - NO LOGIN REQUIRED
    db.init_database()
    success, _ = db.create_user("rishu", "rishu123")
    if success:
        st.session_state.user_id = db.verify_user("rishu", "rishu123")
    else:
        st.session_state.user_id = 1  # Fallback
    
if 'username' not in st.session_state:
    st.session_state.username = "RISHU"
if 'automation_running' not in st.session_state:
    st.session_state.automation_running = False
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0
if 'show_close_confirmation' not in st.session_state:
    st.session_state.show_close_confirmation = False
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()
if 'messages_content' not in st.session_state:
    st.session_state.messages_content = ""
if 'cookies_content' not in st.session_state:
    st.session_state.cookies_content = ""
if 'cpu_usage' not in st.session_state:
    st.session_state.cpu_usage = 0
if 'memory_usage' not in st.session_state:
    st.session_state.memory_usage = 0
if 'server_status' not in st.session_state:
    st.session_state.server_status = "🟢 Healthy"

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
        self.last_activity = None

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

# ==================== UPTIME ENGINE FUNCTIONS ====================
def get_uptime():
    """Get system uptime"""
    delta = datetime.now() - UPTIME_START
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    seconds = delta.seconds % 60
    return f"{days}d {hours:02d}h {minutes:02d}m {seconds:02d}s"

def get_system_stats():
    """Get system stats"""
    try:
        st.session_state.cpu_usage = psutil.cpu_percent(interval=0.5)
        memory = psutil.virtual_memory()
        st.session_state.memory_usage = memory.percent
        
        # Update server status
        if st.session_state.cpu_usage > 80:
            st.session_state.server_status = "🔴 High Load"
        elif st.session_state.cpu_usage > 50:
            st.session_state.server_status = "🟡 Moderate"
        else:
            st.session_state.server_status = "🟢 Healthy"
        
        return True
    except Exception as e:
        print(f"Error getting stats: {e}")
        return False

def get_status_color():
    """Get status color class"""
    if "🔴" in st.session_state.server_status:
        return "status-red"
    elif "🟡" in st.session_state.server_status:
        return "status-yellow"
    else:
        return "status-green"

# ==================== LOGGING FUNCTION ====================
def log_message(msg, msg_type="info", automation_state=None):
    now = datetime.now()
    timestamp = now.strftime("%H:%M:%S")
    
    emoji_map = {
        "success": "✅",
        "error": "❌",
        "warning": "⚠️",
        "send": "📤",
        "load": "📥",
        "github": "🐙",
        "system": "🖥️",
        "browser": "🌐",
        "cookie": "🍪",
        "config": "⚙️",
        "start": "▶️",
        "stop": "⏹️",
        "close": "🗑️",
        "info": "ℹ️"
    }
    emoji = emoji_map.get(msg_type, "ℹ️")
    
    formatted_msg = f"[{timestamp}] {emoji} {msg}"
   
    if automation_state:
        automation_state.logs.append(formatted_msg)
        automation_state.last_activity = now
        if len(automation_state.logs) > 100:
            automation_state.logs = automation_state.logs[-100:]
    else:
        st.session_state.logs.append(formatted_msg)
        if len(st.session_state.logs) > 100:
            st.session_state.logs = st.session_state.logs[-100:]
    
    return formatted_msg

# ==================== GITHUB LOAD FUNCTION ====================
def load_messages_from_github():
    """Load messages directly from GitHub raw URL"""
    try:
        with st.spinner("🐙 Loading messages from GitHub..."):
            response = requests.get(GITHUB_RAW_URL, timeout=30)
            
            if response.status_code == 200:
                messages = response.text
                st.session_state.messages_content = messages
                line_count = len(messages.splitlines())
                log_message(f"🐙 GitHub loaded: {line_count} messages", "github")
                return True, f"✅ Loaded {line_count} messages from GitHub!"
            else:
                log_message(f"❌ GitHub error: {response.status_code}", "error")
                return False, f"❌ GitHub returned status {response.status_code}"
    except Exception as e:
        log_message(f"❌ GitHub error: {str(e)}", "error")
        return False, f"❌ Error: {str(e)}"

# ==================== AUTOMATION FUNCTIONS ====================
def setup_browser(automation_state=None):
    """Setup Chrome browser"""
    log_message('🌐 Setting up Chrome browser...', "browser", automation_state)
    
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    chrome_paths = [
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
        '/usr/bin/google-chrome',
        '/usr/bin/chrome'
    ]
    
    for path in chrome_paths:
        if Path(path).exists():
            chrome_options.binary_location = path
            log_message(f'🌐 Found browser at: {path}', "browser", automation_state)
            break
    
    try:
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            log_message('🌐 Browser started!', "success", automation_state)
        except:
            driver = webdriver.Chrome(options=chrome_options)
            log_message('🌐 Browser started with default driver!', "success", automation_state)
        
        return driver
    except Exception as error:
        log_message(f'❌ Browser setup failed: {error}', "error", automation_state)
        raise error

def find_message_input(driver, process_id, automation_state=None):
    """Find message input"""
    log_message(f'🔍 Finding message input...', "info", automation_state)
    time.sleep(5)
    
    selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[aria-label*="message" i][contenteditable="true"]',
        '[role="textbox"][contenteditable="true"]',
        'textarea'
    ]
    
    for selector in selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                if element.is_displayed():
                    log_message(f'✅ Found message input', "success", automation_state)
                    return element
        except:
            continue
    
    log_message(f'❌ Message input not found!', "error", automation_state)
    return None

def send_messages(config, automation_state, user_id, process_id='RISHU'):
    """Send messages"""
    driver = None
    try:
        automation_state.start_time = datetime.now()
        
        messages_list = [msg.strip() for msg in config['messages'].split('\n') if msg.strip()]
        total_msgs = len(messages_list)
        automation_state.total_messages = total_msgs
        
        log_message(f'📥 Loaded: {total_msgs} messages', "load", automation_state)
        log_message(f'▶️ Starting RISHU automation...', "start", automation_state)
        
        delay = int(config['delay'])
        log_message(f'⏱️ Delay: {delay}s', "info", automation_state)
        
        driver = setup_browser(automation_state)
        automation_state.driver = driver
        
        log_message(f'🌐 Opening Facebook...', "browser", automation_state)
        driver.get('https://www.facebook.com/')
        time.sleep(5)
        
        if config['cookies']:
            try:
                cookie_pairs = config['cookies'].split(';')
                for cookie in cookie_pairs:
                    if '=' in cookie:
                        name, value = cookie.split('=', 1)
                        driver.add_cookie({
                            'name': name.strip(),
                            'value': value.strip(),
                            'domain': '.facebook.com'
                        })
                log_message(f'🍪 Cookies added', "cookie", automation_state)
            except:
                pass
        
        if config['chat_id']:
            chat_id = config['chat_id'].strip()
            automation_state.current_chat_id = chat_id
            log_message(f'💬 Opening chat {chat_id}...', "info", automation_state)
            driver.get(f'https://www.facebook.com/messages/t/{chat_id}')
            time.sleep(8)
        
        message_input = find_message_input(driver, process_id, automation_state)
        if not message_input:
            log_message(f'❌ No message input!', "error", automation_state)
            return 0
        
        messages_sent = 0
        for i, message in enumerate(messages_list):
            if not automation_state.running:
                break
            
            try:
                if config['name_prefix']:
                    full_message = f"{config['name_prefix']} {message}"
                else:
                    full_message = message
                
                message_input.clear()
                message_input.send_keys(full_message)
                time.sleep(1)
                message_input.send_keys(Keys.RETURN)
                
                messages_sent += 1
                automation_state.message_count = messages_sent
                
                log_message(f"📤 [{chat_id}] {messages_sent}/{total_msgs}", "send", automation_state)
                time.sleep(delay)
                
            except Exception as e:
                log_message(f'❌ Send error', "error", automation_state)
                time.sleep(5)
        
        log_message(f'✅ Completed: {messages_sent} messages', "success", automation_state)
        automation_state.running = False
        return messages_sent
        
    except Exception as e:
        log_message(f'❌ Fatal: {str(e)}', "error", automation_state)
        automation_state.running = False
        return 0
    finally:
        if driver:
            driver.quit()
            log_message('🌐 Browser closed', "browser", automation_state)

def start_automation(user_config, user_id):
    if st.session_state.automation_state.running:
        return
    st.session_state.automation_state.running = True
    st.session_state.automation_state.message_count = 0
    st.session_state.automation_state.logs = []
    st.session_state.automation_state.last_activity = datetime.now()
    thread = threading.Thread(target=send_messages, args=(user_config, st.session_state.automation_state, user_id))
    thread.daemon = True
    thread.start()

def stop_automation(user_id):
    st.session_state.automation_state.running = False
    log_message("⏹️ Stopped by user", "stop", st.session_state.automation_state)

def close_all_tasks():
    with st.spinner("🧹 Cleaning up..."):
        if st.session_state.automation_state.running:
            st.session_state.automation_state.running = False
        if hasattr(st.session_state.automation_state, 'driver') and st.session_state.automation_state.driver:
            try:
                st.session_state.automation_state.driver.quit()
            except:
                pass
        try:
            os.system("pkill -f chrome")
            os.system("pkill -f chromedriver")
        except:
            pass
        st.session_state.automation_state.message_count = 0
        st.session_state.automation_state.logs = []
        gc.collect()
        log_message("🗑️ All tasks closed", "close")
        time.sleep(2)
        st.success("✅ All tasks closed!")

# ==================== LIVE DISPLAY FUNCTION ====================
def display_live_status():
    """Display live server status at top"""
    get_system_stats()
    status_color = get_status_color()
    
    status_html = f'''
    <div class="uptime-engine">
        <div class="uptime-header">
            <div>
                <h2>⚡ E2E RISHU SERVER LIVE STATUS ⚡</h2>
                <div style="display: flex; gap: 15px; margin-top: 5px;">
                    <span><span class="status-indicator {status_color}"></span> {st.session_state.server_status}</span>
                    <span>🔄 Auto-refresh: 2s</span>
                    <span>🕒 {datetime.now().strftime("%H:%M:%S")}</span>
                </div>
            </div>
            <span class="live-badge">🔴 LIVE</span>
        </div>
        
        <div class="uptime-grid">
            <div class="uptime-card">
                <div class="label">Server Uptime</div>
                <div class="value">{get_uptime()}</div>
            </div>
            <div class="uptime-card">
                <div class="label">CPU Usage</div>
                <div class="value">{st.session_state.cpu_usage}%</div>
            </div>
            <div class="uptime-card">
                <div class="label">Memory</div>
                <div class="value">{st.session_state.memory_usage}%</div>
            </div>
            <div class="uptime-card">
                <div class="label">Messages Sent</div>
                <div class="value">{st.session_state.automation_state.message_count}</div>
            </div>
        </div>
        
        <div style="margin-top: 10px; text-align: center; color: #00ffff; font-size: 0.9rem;">
            {'🟢 Automation Running' if st.session_state.automation_state.running else '🔴 Automation Stopped'}
            {' | Chat: ' + st.session_state.automation_state.current_chat_id if st.session_state.automation_state.current_chat_id else ''}
        </div>
    </div>
    '''
    
    st.markdown(status_html, unsafe_allow_html=True)

# ==================== MAIN APP - DIRECT ACCESS ====================
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 E2E RISHU SERVER</h1>
        <p>Direct Access - No Login Required</p>
        <span class="server-badge">🔓 OPEN FOR ALL</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Display LIVE STATUS at TOP
    display_live_status()
    
    # Get user config
    user_config = db.get_user_config(st.session_state.user_id)
    
    if user_config:
        tab1, tab2 = st.tabs(["⚙️ Configuration", "🤖 Automation"])
        
        with tab1:
            st.markdown("### ⚙️ Configuration")
            
            chat_id = st.text_input("Chat ID", value=user_config['chat_id'], placeholder="e.g., 1362400298935018")
            name_prefix = st.text_input("Prefix", value=user_config['name_prefix'], placeholder="e.g., [RISHU]")
            delay = st.number_input("Delay (seconds)", 1, 300, user_config['delay'])
            
            # ==================== GITHUB BUTTON ====================
            st.markdown("### 🐙 Load Messages from GitHub")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("🐙 LOAD FROM GITHUB", use_container_width=True):
                    success, message = load_messages_from_github()
                    if success:
                        st.success(message)
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(message)
            
            with col2:
                st.markdown(f"[View on GitHub](https://github.com/YAMRAJ275/e2e-/blob/main/np.txt)")
            
            # ==================== COOKIES UPLOAD BUTTON ====================
            st.markdown("### 🍪 Facebook Cookies Upload")
            
            cookies_file = st.file_uploader("", type=['txt'], key="cookies_upload", label_visibility="collapsed")
            
            if cookies_file:
                cookies_content = cookies_file.read().decode('utf-8')
                st.session_state.cookies_content = cookies_content
                line_count = len(cookies_content.split(';'))
                st.success(f"✅ Cookies loaded from {cookies_file.name}")
                log_message(f"🍪 Cookies uploaded: {cookies_file.name}", "cookie")
                time.sleep(1)
                st.rerun()
            
            st.markdown("""
            <div class="cookies-upload" onclick="document.querySelector('input[type=file][key=cookies_upload]').click()">
                <h3>🍪 TOUCH HERE TO UPLOAD COOKIES</h3>
                <p>Upload your Facebook cookies.txt file - No copy-paste needed</p>
            </div>
            """, unsafe_allow_html=True)
            
            cookies_to_show = st.session_state.get('cookies_content', user_config['cookies'])
            if cookies_to_show:
                preview = cookies_to_show[:200] + "..." if len(cookies_to_show) > 200 else cookies_to_show
                st.text_area("Cookies Preview", value=preview, height=100, disabled=True)
                st.info(f"📊 Cookies loaded: {len(cookies_to_show.split(';'))} pairs")
            else:
                st.info("📊 No cookies loaded yet. Upload a cookies.txt file")
            
            st.markdown("---")
            
            # Messages preview
            st.markdown("### 📁 Current Messages")
            messages_to_show = st.session_state.get('messages_content', user_config['messages'])
            line_count = len(messages_to_show.split('\n')) if messages_to_show else 0
            
            preview = messages_to_show[:500] + "..." if len(messages_to_show) > 500 else messages_to_show
            st.text_area("Messages Preview", value=preview, height=150, disabled=True)
            st.info(f"📊 Total messages: {line_count} lines")
            
            st.markdown("---")
            
            # Save button
            if st.button("💾 Save Configuration", use_container_width=True):
                final_messages = st.session_state.get('messages_content', user_config['messages'])
                final_cookies = st.session_state.get('cookies_content', user_config['cookies'])
                if db.update_user_config(st.session_state.user_id, chat_id, name_prefix, delay, final_cookies, final_messages):
                    st.success("✅ Configuration saved successfully!")
                    log_message("⚙️ Configuration saved", "config")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Failed to save configuration")
        
        with tab2:
            st.markdown("### 🤖 Automation Control")
            
            # Status metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Messages Sent", st.session_state.automation_state.message_count)
            with col2:
                status = "🟢 RUNNING" if st.session_state.automation_state.running else "🔴 STOPPED"
                st.metric("Status", status)
            with col3:
                chat_display = user_config['chat_id'][:10] + "..." if user_config['chat_id'] and len(user_config['chat_id']) > 10 else user_config['chat_id'] or "Not Set"
                st.metric("Chat ID", chat_display)
            
            st.markdown("---")
            
            # Control buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                start_disabled = st.session_state.automation_state.running or not user_config['chat_id'] or not user_config['cookies']
                if st.button("▶️ START AUTOMATION", disabled=start_disabled, use_container_width=True):
                    if user_config['chat_id'] and user_config['cookies']:
                        start_automation(user_config, st.session_state.user_id)
                        st.success("✅ Automation started!")
                        log_message("▶️ Automation started", "start")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Please set Chat ID and Cookies first!")
            
            with col2:
                if st.button("⏹️ STOP AUTOMATION", disabled=not st.session_state.automation_state.running, use_container_width=True):
                    stop_automation(st.session_state.user_id)
                    st.warning("⏹️ Automation stopped!")
                    time.sleep(1)
                    st.rerun()
            
            with col3:
                if st.button("🗑️ CLOSE ALL TASKS", use_container_width=True):
                    st.session_state.show_close_confirmation = True
            
            # Confirmation dialog for CLOSE ALL
            if st.session_state.show_close_confirmation:
                st.warning("⚠️ Are you sure you want to close ALL tasks? This will stop automation and close browser!")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ YES, CLOSE ALL", use_container_width=True):
                        st.session_state.show_close_confirmation = False
                        close_all_tasks()
                        st.rerun()
                with col2:
                    if st.button("❌ NO, CANCEL", use_container_width=True):
                        st.session_state.show_close_confirmation = False
                        st.rerun()
            
            # Auto-refresh when running
            if st.session_state.automation_state.running:
                time.sleep(2)
                st.rerun()
            
            # Full logs at bottom
            if st.session_state.automation_state.logs:
                st.markdown("### 📟 Complete Log History")
                logs_html = '<div class="console-output">'
                for log in st.session_state.automation_state.logs[-50:]:
                    log_class = ""
                    if "✅" in log:
                        log_class = 'success'
                    elif "❌" in log:
                        log_class = 'error'
                    elif "📤" in log:
                        log_class = 'send'
                    elif "🐙" in log:
                        log_class = 'github'
                    elif "🌐" in log or "🍪" in log or "⚙️" in log:
                        log_class = 'info'
                    logs_html += f'<div class="console-line {log_class}">{log}</div>'
                logs_html += '</div>'
                st.markdown(logs_html, unsafe_allow_html=True)
    else:
        st.error("❌ Configuration not found. Please check database.")

# ==================== RUN ====================
if __name__ == "__main__":
    main()
    st.markdown('<div class="footer">⚡ <span class="rishu-signature">E2E RISHU SERVER</span> ⚡ | Direct Access | No Login Required</div>', unsafe_allow_html=True)