from fpdf import FPDF
from datetime import datetime, timedelta
import os

class MedicalReportGenerator:
    def __init__(self):
        self.report_dir = "reports"
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)

    def generate_weekly_triage(self, insights: dict, anomalies: list) -> str:
        pdf = FPDF()
        pdf.add_page()
        
        # Header
        pdf.set_fill_color(29, 78, 216) # SafeTrack Blue
        pdf.rect(0, 0, 210, 40, 'F')
        
        pdf.set_font("Arial", 'B', 24)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 20, "SafeTrack | Auto-Triage Report", ln=True, align='C')
        
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
        pdf.ln(20)

        # Executive Summary
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "1. Executive Health Summary", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.ln(5)
        
        # Metrics Table
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(95, 10, "Metric", 1, 0, 'L', True)
        pdf.cell(95, 10, "Value", 1, 1, 'L', True)
        
        stats = [
            ("System Health Index", f"{insights.get('system_health_index', 0)}%"),
            ("Total Active Monitors", f"{insights.get('total_active_monitors', 0)}"),
            ("Predicted Recovery Rate", f"{insights.get('predicted_recovery_rate', '0%')}"),
            ("Impending Failures Forecast", f"{insights.get('impending_failure_forecast', 0)} patients")
        ]
        
        for label, val in stats:
            pdf.cell(95, 10, label, 1)
            pdf.cell(95, 10, val, 1, 1)
        
        pdf.ln(10)

        # Risk Distribution
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "2. Population Risk Distribution", ln=True)
        pdf.set_font("Arial", '', 12)
        dist = insights.get('risk_distribution', {})
        pdf.cell(0, 10, f"- Red (Critical): {dist.get('Red', 0)}", ln=True)
        pdf.cell(0, 10, f"- Yellow (Warning): {dist.get('Yellow', 0)}", ln=True)
        pdf.cell(0, 10, f"- Green (Stable): {dist.get('Green', 0)}", ln=True)
        
        pdf.ln(10)

        # Anomalies & Deteriorating Patients
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(220, 38, 38) # Red
        pdf.cell(0, 10, "3. Critical Anomalies & Deteriorating Patients", ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", '', 10)
        pdf.ln(5)

        if not anomalies:
            pdf.cell(0, 10, "No critical anomalies detected in this period.", ln=True)
        else:
            # Header for anomalies table
            pdf.set_fill_color(254, 226, 226)
            pdf.cell(40, 10, "Patient ID", 1, 0, 'C', True)
            pdf.cell(40, 10, "Score Drop", 1, 0, 'C', True)
            pdf.cell(40, 10, "Forecast", 1, 0, 'C', True)
            pdf.cell(70, 10, "Clinical Status", 1, 1, 'C', True)
            
            for a in anomalies:
                pdf.cell(40, 10, str(a.get('user_id')), 1)
                pdf.cell(40, 10, f"-{a.get('score_drop')} pts", 1)
                pdf.cell(40, 10, str(a.get('forecast')), 1)
                pdf.cell(70, 10, str(a.get('status')), 1, 1)

        pdf.ln(20)
        pdf.set_font("Arial", 'I', 8)
        pdf.set_text_color(150, 150, 150)
        pdf.multi_cell(0, 5, "CONFIDENTIAL: This document contains sensitive medical data. Intended only for clinical review by the Medical Director of SafeTrack Health Systems.", align='C')

        filename = f"Weekly_Triage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.report_dir, filename)
        pdf.output(filepath)
        return filepath

reporter = MedicalReportGenerator()
