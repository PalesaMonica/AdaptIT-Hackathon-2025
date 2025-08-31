def process_ussd_input(session, user_input):
    """Process user input and update session state"""
    current_screen = st.session_state.current_screen
    
    session.log_interaction(user_input, f"Screen: {current_screen}")
    
    if current_screen == 'main_menu':
        service_map = {
            '1': 'service_grant_application',
            '2': 'service_identity_verification', 
            '3': 'service_biometric_capture',
            '4': 'service_status_appeal',
            '5': 'service_document_collection',
            '6': 'check_appointments',
            '7': 'find_office'
        }
        if user_input in service_map:
            if user_input in ['1', '2', '3', '4', '5']:
                session.user_data['service_type'] = user_input
                st.session_state.current_screen = service_map[user_input]
            else:
                st.session_state.current_screen = service_map[user_input]
        elif user_input == '0':
            st.session_state.current_screen = 'start'
    
    elif current_screen == 'service_grant_application':
        if user_input in ['1', '2', '3', '4', '5', '6']:
            session.user_data['grant_type'] = user_input
            st.session_state.current_screen = 'appointment_type'
        elif user_input == '0':
            st.session_state.current_screen = 'main_menu'
    
    elif current_screen in ['service_identity_verification', 'service_biometric_capture', 
                           'service_status_appeal', 'service_document_collection']:
        if user_input == '1':
            st.session_state.current_screen = 'appointment_type'
        elif user_input == '0':
            st.session_state.current_screen = 'main_menu'
    
    elif current_screen == 'appointment_type':
        if user_input in ['1', '2', '3']:
            session.user_data['duration_type'] = user_input
            st.session_state.current_screen = 'province_menu'
        elif user_input == '0':
            st.session_state.current_screen = 'main_menu'
    
    elif current_screen == 'province_menu':
        provinces = {'1': 'GP', '2': 'WC', '3': 'KZN'}
        if user_input in provinces:
            session.user_data['province_code'] = provinces[user_input]
            st.session_state.current_screen = 'office_menu'
        elif user_input == '0':
            st.session_state.current_screen = 'appointment_type'
    
    elif current_screen == 'office_menu':
        province_code = session.user_data.get('province_code', 'GP')
        offices = session.locations[province_code]['offices']
        if user_input in offices:
            session.user_data['office_name'] = offices[user_input]
            st.session_state.current_screen = 'date_menu'
        elif user_input == '0':
            st.session_state.current_screen = 'province_menu'
    
    elif current_screen == 'date_menu':
        if user_input in [str(i) for i in range(1, 11)]:
            # Calculate the selected date
            current = datetime.now() + timedelta(days=1)
            count = 1
            selected_date = None
            
            while count <= int(user_input):
                if current.weekday() < 5:  # Working days only
                    if count == int(user_input):
                        selected_date = current
                        break
                    count += 1
                current += timedelta(days=1)
            
            if selected_date:
                session.user_data['date_str'] = selected_date.strftime("%Y-%m-%d")
                session.user_data['date_display'] = selected_date.strftime("%a %d %b")
                st.session_state.current_screen = 'time_menu'
        elif user_input == '0':
            st.session_state.current_screen = 'office_menu'
    
    elif current_screen == 'time_menu':
        # Process time selection based on duration type
        duration_type = session.user_data.get('duration_type', '1')
        duration_map = {"1": "standard", "2": "complex", "3": "group"}
        duration_key = duration_map.get(duration_type, 'standard')
        
        # Define time mappings for each duration type
        time_mappings = {
            "standard": {
                "1": "08:00 - 08:30", "2": "08:30 - 09:00", "3": "09:00 - 09:30", "4": "09:30 - 10:00",
                "5": "10:00 - 10:30", "6": "10:30 - 11:00", "7": "11:00 - 11:30", "8": "11:30 - 12:00",
                "9": "13:00 - 13:30", "10": "13:30 - 14:00", "11": "14:00 - 14:30", "12": "14:30 - 15:00",
                "13": "15:00 - 15:30", "14": "15:30 - 16:00", "15": "16:00 - 16:30", "16": "16:30 - 17:00"
            },
            "complex": {
                "1": "08:00 - 09:00", "2": "09:00 - 10:00", "3": "10:00 - 11:00", "4": "11:00 - 12:00",
                "5": "13:00 - 14:00", "6": "14:00 - 15:00", "7": "15:00 - 16:00", "8": "16:00 - 17:00"
            },
            "group": {
                "1": "08:00 - 09:30", "2": "10:00 - 11:30", "3": "13:00 - 14:30", "4": "15:00 - 16:30"
            }
        }
        
        current_mappings = time_mappings.get(duration_key, time_mappings["standard"])
        max_slots = len(current_mappings)
        
        if user_input in [str(i) for i in range(1, max_slots + 1)]:
            session.user_data['time_slot'] = user_input
            session.user_data['time_display'] = current_mappings.get(user_input, 'Unknown Time')
            st.session_state.current_screen = 'reference_input'
        elif user_input == '0':
            st.session_state.current_screen = 'date_menu'
    
    elif current_screen == 'reference_input':
        session.user_data['reference_number'] = user_input.strip() if user_input.strip() else 'SKIP'
        st.session_state.current_screen = 'name_input'
    
    elif current_screen == 'name_input':
        if user_input.strip():
            session.user_data['name'] = user_input.strip().upper()
            st.session_state.current_screen = 'id_input'
    
    elif current_screen == 'id_input':
        if len(user_input.strip()) == 13 and user_input.strip().isdigit():
            session.user_data['id_number'] = user_input.strip()
            st.session_state.current_screen = 'confirmation'
        else:
            st.error("Invalid ID number. Must be 13 digits.")
    
    elif current_screen == 'confirmation':
        if user_input == '1':
            # Confirm booking
            appointment_id = save_appointment(session)
            session.user_data['appointment_id'] = appointment_id
            st.session_state.current_screen = 'success'
        elif user_input == '2':
            st.session_state.current_screen = 'name_input'
        elif user_input == '0':
            st.session_state.current_screen = 'main_menu'# pages/ussd_service.py
import streamlit as st
import csv
import os
from datetime import datetime, timedelta
import uuid
import json

# ---------------- Config ----------------
USSD_DATA_FILE = "data/ussd_sessions.csv"
APPOINTMENTS_FILE = "data/appointments.csv"
LOCATIONS_FILE = "data/sassa_locations.json"
os.makedirs("data", exist_ok=True)

# ---------------- SASSA Colors ----------------
def apply_sassa_styling():
    st.markdown("""
    <style>
    .main .block-container {
        padding: 2rem;
        background: linear-gradient(135deg, #2E8B57 0%, #1F5F3F 100%);
        border-radius: 10px;
    }
    
    .ussd-screen {
        background: #000000;
        color: #00FF00;
        font-family: 'Courier New', monospace;
        padding: 20px;
        border-radius: 10px;
        border: 3px solid #333333;
        margin: 20px 0;
        min-height: 400px;
        font-size: 14px;
        line-height: 1.5;
    }
    
    .ussd-title {
        color: #FFD700;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    
    .menu-item {
        color: #00FF00;
        margin: 5px 0;
    }
    
    .input-prompt {
        color: #FFFF00;
        font-weight: bold;
    }
    
    .success-msg {
        color: #00FF00;
        font-weight: bold;
    }
    
    .error-msg {
        color: #FF4444;
        font-weight: bold;
    }
    
    .info-msg {
        color: #FFFFFF;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- Data Initialization ----------------
def initialize_data():
    # Initialize CSV files
    if not os.path.exists(USSD_DATA_FILE):
        with open(USSD_DATA_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["session_id", "phone_number", "timestamp", "menu_path", "user_input", "response"])
    
    if not os.path.exists(APPOINTMENTS_FILE):
        with open(APPOINTMENTS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["appointment_id", "phone_number", "full_name", "id_number", "service_type",
                           "grant_type", "reference_number", "location", "date", "time", "duration", "status", "timestamp"])
    
    # Initialize SASSA locations
    if not os.path.exists(LOCATIONS_FILE):
        locations = {
            "GP": {
                "name": "Gauteng",
                "offices": {
                    "1": "Johannesburg Central - 127 Fox St, Johannesburg",
                    "2": "Pretoria Central - 263 Pretorius St, Pretoria",
                    "3": "Soweto - 1 Klipspruit Valley Rd, Soweto",
                    "4": "Alexandra - 1st Ave, Alexandra",
                    "5": "Sandton - 222 Rivonia Rd, Sandton"
                }
            },
            "WC": {
                "name": "Western Cape",
                "offices": {
                    "1": "Cape Town Central - 47 Strand St, Cape Town",
                    "2": "Mitchell's Plain - Town Centre, Mitchell's Plain",
                    "3": "Khayelitsha - Graceland Shopping Centre",
                    "4": "Bellville - 19 Voortrekker Rd, Bellville"
                }
            },
            "KZN": {
                "name": "KwaZulu-Natal",
                "offices": {
                    "1": "Durban Central - 420 Anton Lembede St, Durban",
                    "2": "Pietermaritzburg - 237 Pietermaritz St",
                    "3": "Pinetown - 1 Josiah Gumede Rd, Pinetown",
                    "4": "Umlazi - Mega City Shopping Centre"
                }
            }
        }
        with open(LOCATIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(locations, f, indent=2)

def load_locations():
    with open(LOCATIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------------- USSD Session Management ----------------
class USSDSession:
    def __init__(self, session_id, phone_number):
        self.session_id = session_id
        self.phone_number = phone_number
        self.menu_path = []
        self.user_data = {}
        self.locations = load_locations()
        
    def log_interaction(self, user_input, response):
        with open(USSD_DATA_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                self.session_id, 
                self.phone_number, 
                datetime.now().isoformat(),
                "->".join(self.menu_path),
                user_input,
                response[:100] + "..." if len(response) > 100 else response
            ])
    
    def main_menu(self):
        return """
*120*32390#

SASSA USSD SERVICE
==================

Sawubona! Welcome to SASSA!

1. Book Grant Application Appointment
2. Book Identity Verification
3. Book Biometric Capture
4. Book Status Appeal Meeting
5. Book Document Collection
6. Check My Appointments
7. Find SASSA Office
0. Exit

Please select option (1-7):
"""

    def service_type_menu(self, service_type):
        menus = {
            "grant_application": """
SELECT GRANT TYPE
=================

1. Old Age Pension (60+ years)
2. Disability Grant
3. Child Support Grant  
4. Foster Child Grant
5. Care Dependency Grant
6. Social Relief Grant (R370)
0. Back to Main Menu

Select grant type (1-6):
""",
            "identity_verification": """
IDENTITY VERIFICATION
====================

Required for:
- First-time applicants
- ID document updates
- Address changes
- Bank detail updates

What to bring:
- Original ID document
- Proof of residence
- Bank statement

1. Book Appointment
0. Back to Main Menu

Press 1 to continue:
""",
            "biometric_capture": """
BIOMETRIC CAPTURE
=================

Required for:
- Fingerprint scanning
- Photo capture
- Voice verification
- Signature capture

Usually needed when:
- Identity verification fails
- System flags for manual check
- Appeal process

1. Book Appointment  
0. Back to Main Menu

Press 1 to continue:
""",
            "status_appeal": """
STATUS APPEAL MEETING
====================

Book if your application was:
- Rejected
- Suspended
- Payment stopped
- Identity verification failed

Required documents:
- ID document
- Appeal form
- Supporting documents
- Previous correspondence

1. Book Appeal Meeting
0. Back to Main Menu

Press 1 to continue:
""",
            "document_collection": """
DOCUMENT COLLECTION
==================

Collect:
- Grant approval letter
- Payment card
- Appeal outcome letter
- Updated documents

You will receive SMS when
documents are ready.

1. Book Collection Slot
0. Back to Main Menu

Press 1 to continue:
"""
        }
        return menus.get(service_type, self.main_menu())
    
    def appointment_type_menu(self):
        service_names = {
            "1": "Grant Application",
            "2": "Identity Verification", 
            "3": "Biometric Capture",
            "4": "Status Appeal Meeting",
            "5": "Document Collection"
        }
        
        service_type = self.user_data.get('service_type')
        return f"""
{service_names.get(service_type, 'Service').upper()} APPOINTMENT
{'=' * 25}

Select appointment duration:

1. Standard (30 minutes)
2. Complex Case (60 minutes)
3. Family Group (90 minutes)

Note: Complex cases include:
- Multiple grants
- Appeal hearings
- Disability assessments

0. Back

Select duration (1-3):
"""

    def province_menu(self):
        menu = """
SELECT PROVINCE
===============

"""
        provinces = {
            "1": ("GP", "Gauteng"),
            "2": ("WC", "Western Cape"), 
            "3": ("KZN", "KwaZulu-Natal")
        }
        
        for key, (code, name) in provinces.items():
            menu += f"{key}. {name}\n"
        
        menu += "0. Back\n\nSelect province (1-3):"
        return menu

    def office_menu(self, province_code):
        province = self.locations[province_code]
        menu = f"""
{province['name'].upper()} OFFICES
{'=' * 20}

"""
        for key, office in province['offices'].items():
            menu += f"{key}. {office}\n"
        
        menu += "0. Back\n\nSelect office (1-" + str(len(province['offices'])) + "):"
        return menu

    def date_menu(self):
        # Generate next 14 working days
        dates = []
        current = datetime.now() + timedelta(days=1)
        count = 1
        
        while len(dates) < 10:  # Show 10 available dates
            if current.weekday() < 5:  # Monday to Friday
                dates.append((count, current.strftime("%Y-%m-%d"), current.strftime("%a %d %b")))
                count += 1
            current += timedelta(days=1)
        
        menu = """
SELECT DATE
===========

"""
        for num, date_str, display_date in dates:
            menu += f"{num}. {display_date}\n"
        
        menu += "0. Back\n\nSelect date (1-10):"
        return menu

    def time_menu(self, duration_type="standard"):
        duration_slots = {
            "standard": {  # 30-minute slots
                "morning": [
                    ("1", "08:00 - 08:30"), ("2", "08:30 - 09:00"), 
                    ("3", "09:00 - 09:30"), ("4", "09:30 - 10:00"),
                    ("5", "10:00 - 10:30"), ("6", "10:30 - 11:00"),
                    ("7", "11:00 - 11:30"), ("8", "11:30 - 12:00")
                ],
                "afternoon": [
                    ("9", "13:00 - 13:30"), ("10", "13:30 - 14:00"),
                    ("11", "14:00 - 14:30"), ("12", "14:30 - 15:00"),
                    ("13", "15:00 - 15:30"), ("14", "15:30 - 16:00"),
                    ("15", "16:00 - 16:30"), ("16", "16:30 - 17:00")
                ]
            },
            "complex": {  # 60-minute slots
                "morning": [
                    ("1", "08:00 - 09:00"), ("2", "09:00 - 10:00"), 
                    ("3", "10:00 - 11:00"), ("4", "11:00 - 12:00")
                ],
                "afternoon": [
                    ("5", "13:00 - 14:00"), ("6", "14:00 - 15:00"),
                    ("7", "15:00 - 16:00"), ("8", "16:00 - 17:00")
                ]
            },
            "group": {  # 90-minute slots
                "morning": [
                    ("1", "08:00 - 09:30"), ("2", "10:00 - 11:30")
                ],
                "afternoon": [
                    ("3", "13:00 - 14:30"), ("4", "15:00 - 16:30")
                ]
            }
        }
        
        slots = duration_slots.get(duration_type, duration_slots["standard"])
        
        menu = f"""
SELECT TIME SLOT
================

Morning Slots:
"""
        for slot_id, time_range in slots["morning"]:
            menu += f"{slot_id}. {time_range}\n"
        
        menu += "\nAfternoon Slots:\n"
        for slot_id, time_range in slots["afternoon"]:
            menu += f"{slot_id}. {time_range}\n"
        
        menu += "\n0. Back\n\nSelect time slot:"
        return menu

    def collect_reference_info(self, step):
        if step == "reference_number":
            return """
REFERENCE NUMBER
================

For existing applications, 
please enter your:
- Application reference number
- Appeal reference number
- Payment reference number

Leave blank if first application.

(Reply with reference or SKIP)
"""
        elif step == "name":
            return """
PERSONAL INFORMATION
===================

Please enter your FULL NAME 
as it appears on your ID:

(Reply with your full name)
"""
        elif step == "id":
            return """
ID NUMBER REQUIRED  
==================

Please enter your 13-digit 
South African ID number:

Format: YYMMDDGGGGSAV

(Reply with ID number)
"""

    def confirmation_screen(self):
        service_names = {
            "1": "Grant Application",
            "2": "Identity Verification", 
            "3": "Biometric Capture",
            "4": "Status Appeal Meeting",
            "5": "Document Collection"
        }
        
        grant_types = {
            "1": "Old Age Pension",
            "2": "Disability Grant", 
            "3": "Child Support Grant",
            "4": "Foster Child Grant",
            "5": "Care Dependency Grant",
            "6": "Social Relief Grant"
        }
        
        duration_names = {
            "1": "Standard (30min)",
            "2": "Complex (60min)",
            "3": "Group (90min)"
        }
        
        service_type = self.user_data.get('service_type', '')
        service_name = service_names.get(service_type, 'Unknown Service')
        
        confirmation = f"""
CONFIRM APPOINTMENT
==================

Service: {service_name}
"""
        
        if service_type == "1" and self.user_data.get('grant_type'):
            grant_name = grant_types.get(self.user_data.get('grant_type', ''), '')
            confirmation += f"Grant: {grant_name}\n"
        
        if self.user_data.get('reference_number') and self.user_data.get('reference_number') != 'SKIP':
            confirmation += f"Ref: {self.user_data.get('reference_number', '')}\n"
        
        confirmation += f"""Name: {self.user_data.get('name', '')}
ID: {self.user_data.get('id_number', '')}
Office: {self.user_data.get('office_name', '')}
Date: {self.user_data.get('date_display', '')}
Time: {self.user_data.get('time_display', '')}
Duration: {duration_names.get(self.user_data.get('duration_type', '1'), 'Standard')}

REQUIRED DOCUMENTS:
{self.get_required_documents()}

1. CONFIRM BOOKING
2. EDIT DETAILS  
0. CANCEL

Please select (1, 2, or 0):
"""
        return confirmation
    
    def get_required_documents(self):
        service_type = self.user_data.get('service_type', '')
        docs = {
            "1": "- Original ID\n- Bank statement\n- Proof of income\n- Medical certificates (if applicable)",
            "2": "- Original ID document\n- Proof of residence\n- Bank statement\n- Previous correspondence",
            "3": "- Original ID document\n- SASSA reference letter\n- Previous biometric results",
            "4": "- Original ID document\n- Appeal form\n- Supporting evidence\n- Previous SASSA letters",
            "5": "- Original ID document\n- SMS collection notice\n- Previous correspondence"
        }
        return docs.get(service_type, "- Original ID document\n- Supporting documents")

    def success_screen(self, appointment_id):
        service_names = {
            "1": "Grant Application",
            "2": "Identity Verification", 
            "3": "Biometric Capture",
            "4": "Status Appeal Meeting",
            "5": "Document Collection"
        }
        
        service_type = self.user_data.get('service_type', '')
        service_name = service_names.get(service_type, 'SASSA Service')
        
        return f"""
BOOKING CONFIRMED!
==================

Appointment ID: {appointment_id}
Service: {service_name}

Your appointment has been booked successfully.

IMPORTANT REMINDERS:
{self.get_appointment_reminders()}

Arrive 15 minutes early.
Bring all required documents.
SMS confirmation sent to {self.phone_number}

Dial * 120*32390# then option 6
to check your appointments.

Thank you for using SASSA USSD!

Session will end in 10 seconds...
"""
    
    def get_appointment_reminders(self):
        service_type = self.user_data.get('service_type', '')
        reminders = {
            "1": "- Complete application forms\n- Bring supporting documents\n- Allow 2 hours for process",
            "2": "- Bring original documents\n- No photocopies accepted\n- Update address if changed",
            "3": "- Clean hands for fingerprints\n- Remove hats/sunglasses\n- Speak clearly for voice capture",
            "4": "- Bring all correspondence\n- Prepare your case summary\n- Allow up to 2 hours",
            "5": "- Bring SMS collection notice\n- Bring original ID only\n- Quick 15-minute service"
        }
        return reminders.get(service_type, "- Bring required documents\n- Arrive on time")

def save_appointment(session):
    appointment_id = str(uuid.uuid4())[:8].upper()
    
    service_names = {
        "1": "Grant Application",
        "2": "Identity Verification", 
        "3": "Biometric Capture",
        "4": "Status Appeal Meeting",
        "5": "Document Collection"
    }
    
    with open(APPOINTMENTS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            appointment_id,
            session.phone_number,
            session.user_data.get('name', ''),
            session.user_data.get('id_number', ''),
            service_names.get(session.user_data.get('service_type', ''), 'Unknown'),
            session.user_data.get('grant_type', ''),  # Only for grant applications
            session.user_data.get('reference_number', ''),
            session.user_data.get('office_name', ''),
            session.user_data.get('date_str', ''),
            session.user_data.get('time_display', ''),
            session.user_data.get('duration_type', '1'),
            "Confirmed",
            datetime.now().isoformat()
        ])
    
    return appointment_id

# ---------------- Streamlit App ----------------
def run():
    st.set_page_config(
        page_title="SASSA USSD Service Simulator",
        layout="wide"
    )
    
    apply_sassa_styling()
    initialize_data()

    st.title("🇿🇦 SASSA USSD Service Simulator")
    st.markdown("**Dial * 120*32390# to access SASSA services**")

    # Initialize session state
    if 'ussd_session' not in st.session_state:
        st.session_state.ussd_session = None
    if 'current_screen' not in st.session_state:
        st.session_state.current_screen = 'start'
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ''

    col1, col2 = st.columns([3, 1])
    
    with col1:
        # USSD Screen Simulation
        st.markdown("### 📱 USSD Interface")
        
        # Phone number input for new session
        if st.session_state.current_screen == 'start':
            phone = st.text_input("Enter phone number to start USSD session:", value="27831234567")
            if st.button("Dial * 120*32390#"):
                if phone:
                    session_id = str(uuid.uuid4())[:8]
                    st.session_state.ussd_session = USSDSession(session_id, phone)
                    st.session_state.current_screen = 'main_menu'
                    st.rerun()
        
        # USSD Screen Display
        if st.session_state.ussd_session:
            session = st.session_state.ussd_session
            
            # Display current screen
            screen_content = ""
            
            if st.session_state.current_screen == 'main_menu':
                screen_content = session.main_menu()
            elif st.session_state.current_screen.startswith('service_'):
                service_type = st.session_state.current_screen.split('_')[1]
                screen_content = session.service_type_menu(service_type)
            elif st.session_state.current_screen == 'appointment_type':
                screen_content = session.appointment_type_menu()
            elif st.session_state.current_screen == 'province_menu':
                screen_content = session.province_menu()
            elif st.session_state.current_screen == 'office_menu':
                province_code = session.user_data.get('province_code', 'GP')
                screen_content = session.office_menu(province_code)
            elif st.session_state.current_screen == 'date_menu':
                screen_content = session.date_menu()
            elif st.session_state.current_screen == 'time_menu':
                duration_type = session.user_data.get('duration_type', 'standard')
                duration_map = {"1": "standard", "2": "complex", "3": "group"}
                screen_content = session.time_menu(duration_map.get(duration_type, 'standard'))
            elif st.session_state.current_screen == 'reference_input':
                screen_content = session.collect_reference_info('reference_number')
            elif st.session_state.current_screen == 'name_input':
                screen_content = session.collect_reference_info('name')
            elif st.session_state.current_screen == 'id_input':
                screen_content = session.collect_reference_info('id')
            elif st.session_state.current_screen == 'confirmation':
                screen_content = session.confirmation_screen()
            elif st.session_state.current_screen == 'success':
                appointment_id = session.user_data.get('appointment_id', 'UNKNOWN')
                screen_content = session.success_screen(appointment_id)
            
            # Display screen
            st.markdown(f'<div class="ussd-screen">{screen_content.replace(chr(10), "<br>")}</div>', 
                       unsafe_allow_html=True)
            
            # User Input
            if st.session_state.current_screen not in ['success', 'start']:
                user_input = st.text_input("Your response:", key=f"input_{st.session_state.current_screen}")
                
                if st.button("Send", key=f"send_{st.session_state.current_screen}"):
                    # Process user input
                    process_ussd_input(session, user_input)
                    st.rerun()
                
                if st.button("End Session"):
                    st.session_state.ussd_session = None
                    st.session_state.current_screen = 'start'
                    st.rerun()

    with col2:
        # Instructions panel
        st.markdown("### 📋 How to Use")
        st.info("""
        **USSD Service Guide:**
        
        1️⃣ Enter your phone number
        
        2️⃣ Dial * 120*32390#
        
        3️⃣ Select service type
        
        4️⃣ Choose appointment details
        
        5️⃣ Confirm booking
        
        📱 **Works on any phone**
        🌐 **No internet needed**
        🆓 **Free USSD service**
        """)
        
        st.markdown("### 🏢 Service Types")
        st.markdown("""
        - **Grant Applications**
        - **Identity Verification** 
        - **Biometric Capture**
        - **Status Appeals**
        - **Document Collection**
        """)
        
        st.markdown("### ⏰ Operating Hours")
        st.markdown("""
        **Monday - Friday**  
        08:00 - 17:00
        
        **Appointment Slots:**
        - Standard: 30 minutes
        - Complex: 60 minutes  
        - Group: 90 minutes
        """)

def process_ussd_input(session, user_input):
    """Process user input and update session state"""
    current_screen = st.session_state.current_screen
    
    session.log_interaction(user_input, f"Screen: {current_screen}")
    
    if current_screen == 'main_menu':
        if user_input == '1':
            st.session_state.current_screen = 'grant_menu'
        elif user_input == '2':
            st.session_state.current_screen = 'status_check'
        elif user_input == '3':
            st.session_state.current_screen = 'find_office'
        elif user_input == '0':
            st.session_state.current_screen = 'start'
    
    elif current_screen == 'grant_menu':
        if user_input in ['1', '2', '3', '4', '5', '6']:
            session.user_data['grant_type'] = user_input
            st.session_state.current_screen = 'province_menu'
        elif user_input == '0':
            st.session_state.current_screen = 'main_menu'
    
    elif current_screen == 'province_menu':
        provinces = {'1': 'GP', '2': 'WC', '3': 'KZN'}
        if user_input in provinces:
            session.user_data['province_code'] = provinces[user_input]
            st.session_state.current_screen = 'office_menu'
        elif user_input == '0':
            st.session_state.current_screen = 'grant_menu'
    
    elif current_screen == 'office_menu':
        province_code = session.user_data.get('province_code', 'GP')
        offices = session.locations[province_code]['offices']
        if user_input in offices:
            session.user_data['office_name'] = offices[user_input]
            st.session_state.current_screen = 'date_menu'
        elif user_input == '0':
            st.session_state.current_screen = 'province_menu'
    
    elif current_screen == 'date_menu':
        if user_input in [str(i) for i in range(1, 11)]:
            # Calculate the selected date
            current = datetime.now() + timedelta(days=1)
            count = 1
            selected_date = None
            
            while count <= int(user_input):
                if current.weekday() < 5:  # Working days only
                    if count == int(user_input):
                        selected_date = current
                        break
                    count += 1
                current += timedelta(days=1)
            
            if selected_date:
                session.user_data['date_str'] = selected_date.strftime("%Y-%m-%d")
                session.user_data['date_display'] = selected_date.strftime("%a %d %b")
                st.session_state.current_screen = 'time_menu'
        elif user_input == '0':
            st.session_state.current_screen = 'office_menu'
    
    elif current_screen == 'time_menu':
        if user_input in [str(i) for i in range(1, 9)]:
            session.user_data['time_slot'] = user_input
            st.session_state.current_screen = 'name_input'
        elif user_input == '0':
            st.session_state.current_screen = 'date_menu'
    
    elif current_screen == 'name_input':
        if user_input.strip():
            session.user_data['name'] = user_input.strip().upper()
            st.session_state.current_screen = 'id_input'
    
    elif current_screen == 'id_input':
        if len(user_input.strip()) == 13 and user_input.strip().isdigit():
            session.user_data['id_number'] = user_input.strip()
            st.session_state.current_screen = 'confirmation'
        else:
            st.error("Invalid ID number. Must be 13 digits.")
    
    elif current_screen == 'confirmation':
        if user_input == '1':
            # Confirm booking
            appointment_id = save_appointment(session)
            session.user_data['appointment_id'] = appointment_id
            st.session_state.current_screen = 'success'
        elif user_input == '2':
            st.session_state.current_screen = 'name_input'
        elif user_input == '0':
            st.session_state.current_screen = 'main_menu'

if __name__ == "__main__":
    run()