from fpdf import FPDF
import os

class SafeTrackPDF(FPDF):
    def header(self):
        self.set_fill_color(29, 78, 216)
        self.rect(0, 0, 210, 18, 'F')
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(255, 255, 255)
        self.cell(0, 18, 'SafeTrack - AI-Powered Remote Patient Monitoring', align='C', new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(0, 0, 0)
        self.ln(4)

    def footer(self):
        self.set_y(-12)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'SafeTrack Technical Stack Document | Page {self.page_no()}', align='C')

    def section_title(self, text):
        self.set_fill_color(29, 78, 216)
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 9, text, fill=True, new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def sub_title(self, text):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(30, 64, 175)
        self.cell(0, 7, text, new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(0, 0, 0)
        self.ln(1)

    def body_text(self, text, indent=0):
        self.set_font('Helvetica', '', 9)
        self.set_x(self.l_margin + indent)
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def bullet(self, text, indent=5):
        self.set_font('Helvetica', '', 9)
        self.set_x(self.l_margin + indent)
        self.multi_cell(0, 5.5, f' - {text}')

    def table_row(self, cols, widths, bold=False, fill=False):
        self.set_font('Helvetica', 'B' if bold else '', 8.5)
        if fill:
            self.set_fill_color(219, 234, 254)
        else:
            self.set_fill_color(255, 255, 255)
        for text, w in zip(cols, widths):
            self.cell(w, 7, str(text), border=1, fill=fill)
        self.ln()

    def code_block(self, text):
        self.set_fill_color(240, 240, 240)
        self.set_font('Courier', '', 8)
        self.multi_cell(0, 5, text, fill=True, border=1)
        self.ln(2)


pdf = SafeTrackPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Cover Info
pdf.set_font('Helvetica', 'B', 20)
pdf.set_text_color(29, 78, 216)
pdf.ln(4)
pdf.cell(0, 12, 'SafeTrack', align='C', new_x='LMARGIN', new_y='NEXT')
pdf.set_font('Helvetica', '', 12)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 7, 'Complete Technical Stack Document', align='C', new_x='LMARGIN', new_y='NEXT')
pdf.set_font('Helvetica', 'I', 9)
pdf.cell(0, 6, 'AI-Powered Remote Patient Monitoring System | Version 2.0 | March 2026', align='C', new_x='LMARGIN', new_y='NEXT')
pdf.set_text_color(0, 0, 0)
pdf.ln(8)

# 1. Executive Overview
pdf.section_title('1. Executive Overview')
pdf.body_text(
    'SafeTrack is a full-stack, AI-powered remote patient monitoring (RPM) platform that tracks patient '
    'health in real time, predicts clinical deterioration using an Early Warning Score (EWS) engine, '
    'and automatically escalates critical alerts to healthcare providers via push notifications.'
)
pdf.body_text('The system spans three integrated layers:')
pdf.bullet('Mobile App (Flutter)  -  Patients log vitals and symptoms in real time')
pdf.bullet('Backend API (FastAPI + Python)  -  AI analysis, MongoDB storage, escalation logic')
pdf.bullet('Admin Dashboard (React)  -  Medical directors monitor patients and download triage reports')
pdf.ln(3)

# 2. Technology Stack
pdf.section_title('2. Technology Stack')

pdf.sub_title('2.1  Mobile Application - Flutter (Dart)')
pdf.table_row(['Component', 'Technology', 'Purpose'], [50, 60, 80], bold=True, fill=True)
rows = [
    ('Framework', 'Flutter 3.x (Dart)', 'Cross-platform Android/iOS app'),
    ('State Management', 'ChangeNotifier', 'Theme & auth state'),
    ('HTTP Client', 'http package', 'REST API calls to backend'),
    ('Session Storage', 'shared_preferences', 'Persistent login sessions'),
    ('Environment Config', 'flutter_dotenv', 'API URL management'),
    ('Animations', 'animate_do', 'Smooth screen transitions'),
    ('Icons', 'lucide_icons', 'Consistent icon library'),
    ('Typography', 'google_fonts (Outfit)', 'Premium look and feel'),
    ('Charts', 'fl_chart', 'Health trend visualization'),
]
for r in rows:
    pdf.table_row(r, [50, 60, 80])
pdf.ln(4)

pdf.sub_title('2.2  Backend API - FastAPI (Python)')
pdf.table_row(['Component', 'Technology', 'Purpose'], [50, 60, 80], bold=True, fill=True)
rows = [
    ('Framework', 'FastAPI', 'High-performance async REST API'),
    ('ASGI Server', 'Uvicorn', 'Production-grade server'),
    ('Database Driver', 'Motor (async)', 'Async MongoDB operations'),
    ('Data Validation', 'Pydantic', 'Request/response model validation'),
    ('Auth Security', 'hashlib + secrets', 'Salted SHA-256 password hashing'),
    ('PDF Generation', 'fpdf2', 'Weekly triage report generation'),
    ('Push Notifications', 'Firebase Admin SDK', 'Doctor escalation alerts'),
    ('CORS', 'FastAPI CORSMiddleware', 'Cross-origin support for all clients'),
    ('Environment', 'python-dotenv', 'Secret & config management'),
]
for r in rows:
    pdf.table_row(r, [50, 60, 80])
pdf.ln(4)

pdf.sub_title('2.3  Admin Dashboard - React (Vite)')
pdf.table_row(['Component', 'Technology', 'Purpose'], [50, 60, 80], bold=True, fill=True)
rows = [
    ('Framework', 'React 18 (JSX)', 'Component-based UI'),
    ('Build Tool', 'Vite', 'Fast dev server & bundling'),
    ('Styling', 'Vanilla CSS', 'Custom dark-themed design'),
    ('Data Fetching', 'Fetch API', 'REST calls with 5s polling'),
    ('State', 'useState / useEffect', 'Local component state'),
]
for r in rows:
    pdf.table_row(r, [50, 60, 80])
pdf.ln(4)

pdf.sub_title('2.4  Database - MongoDB Atlas')
pdf.table_row(['Collection', 'Key Fields', 'Purpose'], [35, 95, 60], bold=True, fill=True)
rows = [
    ('reports', 'user_id, heart_rate, spo2, temp, symptoms, timestamp, medical_analysis', 'Patient vitals & AI analysis'),
    ('users', 'full_name, email, password (hashed), role, created_at', 'User accounts'),
]
for r in rows:
    pdf.table_row(r, [35, 95, 60])
pdf.ln(4)

# 3. AI Medical Analysis Engine
pdf.section_title('3. AI Medical Analysis Engine (analyzer.py)')
pdf.body_text('The MedicalAnalyzer class is the clinical intelligence core of SafeTrack.')

pdf.sub_title('Early Warning Score (EWS) - Predictive Scoring')
pdf.table_row(['Vital Sign', 'Threshold Range', 'EWS Points'], [55, 85, 50], bold=True, fill=True)
ews_rows = [
    ('SpO2', '< 91%', '+3'),
    ('SpO2', '91-93%', '+2'),
    ('SpO2', '94-95%', '+1'),
    ('Heart Rate', '> 130 bpm or < 40 bpm', '+3'),
    ('Heart Rate', '> 110 bpm or < 50 bpm', '+2'),
    ('Heart Rate', '> 100 bpm or < 60 bpm', '+1'),
    ('Temperature', '> 39.1 C or < 35.0 C', '+3'),
    ('Temperature', '> 38.0 C or < 36.0 C', '+1'),
]
for r in ews_rows:
    pdf.table_row(r, [55, 85, 50])
pdf.ln(3)

pdf.sub_title('Clinical Forecast Logic')
pdf.table_row(['EWS Score', 'Forecast', 'Action Taken'], [35, 45, 110], bold=True, fill=True)
for r in [
    ('>= 5', 'GRAVE', 'Immediate doctor escalation + Firebase push notification'),
    ('>= 3', 'DECLINING', 'Close monitoring, warning issued to system'),
    ('< 3, score < 70', 'UNSTABLE', 'Continue monitoring, no alert'),
    ('All normal', 'STABLE', 'No alerts required'),
]:
    pdf.table_row(r, [35, 45, 110])
pdf.ln(4)

# 4. API Endpoints
pdf.section_title('4. API Endpoints')
pdf.sub_title('Authentication (auth.py - APIRouter)')
pdf.table_row(['Method', 'Endpoint', 'Description'], [25, 40, 125], bold=True, fill=True)
for r in [
    ('POST', '/register', 'Create new user account {full_name, email, password, role}'),
    ('POST', '/login', 'Authenticate user and return profile data'),
    ('GET', '/users', 'List all registered users (passwords excluded)'),
]:
    pdf.table_row(r, [25, 40, 125])
pdf.ln(3)

pdf.sub_title('Health Reports (main.py)')
pdf.table_row(['Method', 'Endpoint', 'Description'], [25, 55, 110], bold=True, fill=True)
for r in [
    ('POST', '/report', 'Submit vitals, trigger AI analysis, save to DB'),
    ('GET', '/reports', 'Fetch all patient reports sorted by latest'),
    ('GET', '/core/insights', 'Population-level health trend analysis'),
    ('GET', '/core/report/weekly', 'Generate and download PDF triage report'),
    ('GET', '/', 'API health check'),
]:
    pdf.table_row(r, [25, 55, 110])
pdf.ln(4)

# 5. Security Model
pdf.section_title('5. Security Model')
pdf.table_row(['Layer', 'Method', 'Details'], [45, 55, 90], bold=True, fill=True)
for r in [
    ('Password Storage', 'Salted SHA-256 (hashlib)', '16-byte random salt, plaintext never stored'),
    ('Environment Secrets', '.env file', 'MongoDB URL, Firebase keys, Secret Key'),
    ('API Exposure', 'Password stripping', '/users endpoint removes password field'),
    ('CORS', 'allow_origins=["*"]', 'Open for dev; restrict to domain in production'),
    ('Session', 'shared_preferences', 'User ID + name stored locally on device'),
]:
    pdf.table_row(r, [45, 55, 90])
pdf.ln(4)

# 6. Deployment
pdf.section_title('6. Deployment Guide')

pdf.sub_title('Local - Windows')
pdf.code_block(
    '# Install dependencies\n'
    'venv\\Scripts\\python -m pip install -r requirements.txt\n\n'
    '# Start server\n'
    'venv\\Scripts\\python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload'
)

pdf.sub_title('Render.com (Cloud Deployment - Linux)')
pdf.table_row(['Setting', 'Value'], [55, 135], bold=True, fill=True)
for r in [
    ('Build Command', 'pip install -r requirements.txt'),
    ('Start Command', 'uvicorn main:app --host 0.0.0.0 --port $PORT'),
    ('Env: MONGODB_URL', 'mongodb+srv://user:pass@cluster.mongodb.net/safetrack'),
    ('Env: SECRET_KEY', 'your-secret-key'),
]:
    pdf.table_row(r, [55, 135])
pdf.ln(3)

pdf.sub_title('Flutter App - Update .env for Production')
pdf.code_block('API_BASE_URL=https://your-safetrack-api.onrender.com')

# 7. Key Features
pdf.section_title('7. Key Features Summary')
pdf.table_row(['Feature', 'Status'], [155, 35], bold=True, fill=True)
features = [
    ('User Registration & Secure Login', 'DONE'),
    ('Persistent Login Session (SharedPreferences)', 'DONE'),
    ('Real-time Vitals Submission via App', 'DONE'),
    ('AI Medical Analysis (EWS Score + Risk Level)', 'DONE'),
    ('Predictive Clinical Forecast', 'DONE'),
    ('Automated Doctor Escalation Push Alerts', 'DONE'),
    ('Admin Registered User Directory', 'DONE'),
    ('Admin Real-time Vitals Dashboard (5s polling)', 'DONE'),
    ('Weekly PDF Triage Report Generation', 'DONE'),
    ('Dark / Light Theme Toggle', 'DONE'),
    ('Auth router separated into auth.py', 'DONE'),
    ('Render.com deployment ready (render.yaml)', 'DONE'),
]
for r in features:
    pdf.table_row(r, [155, 35])
pdf.ln(4)

# 8. File Structure
pdf.section_title('8. Project Folder Structure')
pdf.code_block(
    'safetrack_projects/\n'
    '  safetrack-app/                  # Flutter Mobile App\n'
    '    lib/\n'
    '      main.dart                   # App entry point\n'
    '      auth_controller.dart        # Auth state management\n'
    '      theme_controller.dart       # Dark/Light theme\n'
    '      screens/\n'
    '        login_screen.dart\n'
    '        register_screen.dart\n'
    '        dashboard_screen.dart\n'
    '        vitals_screen.dart\n'
    '        symptom_log_screen.dart\n'
    '        alerts_screen.dart\n'
    '        profile_screen.dart\n'
    '  safetrack-admin/\n'
    '    backend/                      # FastAPI Python Backend\n'
    '      main.py\n'
    '      auth.py                     # Auth router (register/login/users)\n'
    '      analyzer.py                 # Medical AI engine\n'
    '      notifier.py                 # Firebase push notifications\n'
    '      reporter.py                 # PDF report generator\n'
    '      requirements.txt\n'
    '      render.yaml                 # Render.com deployment config\n'
    '    frontend/                     # React Admin Dashboard\n'
    '      src/App.jsx\n'
    '      src/index.css'
)

# Confidential Footer
pdf.set_font('Helvetica', 'I', 8)
pdf.set_text_color(100, 100, 100)
pdf.multi_cell(0, 5, 'CONFIDENTIAL - SafeTrack Technical Documentation | Built with Flutter, FastAPI, MongoDB, React', align='C')

# Save
output_path = r'C:\Users\HAI\.gemini\antigravity\brain\e8da948d-5730-4c69-977b-c7b64c9a023f\SafeTrack_Stack_Document.pdf'
pdf.output(output_path)
print(f'PDF generated successfully: {output_path}')
