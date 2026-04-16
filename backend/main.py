import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import uvicorn
from analyzer import MedicalAnalyzer
from notifier import notifier
from reporter import reporter
from auth import router as auth_router
from contextlib import asynccontextmanager

# Load environment variables
load_dotenv()

app = FastAPI(title="SafeTrack API")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Hospital(BaseModel):
    name: str
    phone: str
    category: Optional[str] = "General"
    address: Optional[str] = "Coimbatore"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Seed Hospitals if empty
    hospitals_count = await db.hospitals.count_documents({})
    if hospitals_count == 0:
        print("Seeding hospitals database...")
        coimbatore_hospitals = [
            {'name': 'Sri Ramakrishna Hospital', 'phone': '0422-3500000', 'category': 'Multi-Speciality & Major Hospitals'},
            {'name': 'PSG Hospitals', 'phone': '0422-4345353', 'category': 'Multi-Speciality & Major Hospitals'},
            {'name': 'KG Hospital', 'phone': '0422-4042121', 'category': 'Multi-Speciality & Major Hospitals'},
            {'name': 'Kongunad Hospital', 'phone': '0422-4316000', 'category': 'Multi-Speciality & Major Hospitals'},
            {'name': 'Royal Care Super Speciality Hospital', 'phone': '0422-2227000', 'category': 'Multi-Speciality & Major Hospitals'},
            {'name': 'GEM Hospital', 'phone': '0422-4695100', 'category': 'Multi-Speciality & Major Hospitals'},
            {'name': 'KMCH (Kovai Medical Center and Hospital)', 'phone': '0422-4323800', 'category': 'Multi-Speciality & Major Hospitals'},
            {'name': 'Ganga Hospital', 'phone': '0422-2485000', 'category': 'Multi-Speciality & Major Hospitals'},
            {'name': 'Lotus Eye Hospital and Institute', 'phone': '0422-4229900', 'category': 'Multi-Speciality & Major Hospitals'},
            {'name': 'Aravind Eye Hospital', 'phone': '0422-4360400', 'category': 'Multi-Speciality & Major Hospitals'},
            {'name': 'Coimbatore Medical College Hospital', 'phone': '0422-2301393', 'category': 'Government & Public Hospitals'},
            {'name': 'ESI Hospital Singanallur', 'phone': '0422-2574391', 'category': 'Government & Public Hospitals'},
            {'name': 'Government District Headquarters Hospital', 'phone': '0422-2300521', 'category': 'Government & Public Hospitals'},
            {'name': 'Urban Primary Health Centre RS Puram', 'phone': '0422-2471188', 'category': 'Government & Public Hospitals'},
            {'name': 'Primary Health Centre Peelamedu', 'phone': '0422-2562555', 'category': 'Government & Public Hospitals'},
            {'name': 'GKNM Hospital', 'phone': '0422-4255555', 'category': 'Heart / Critical / Specialty Care'},
            {'name': 'Sri Ramakrishna Heart Centre', 'phone': '0422-3500000', 'category': 'Heart / Critical / Specialty Care'},
            {'name': 'Kovai Heart Centre', 'phone': '0422-2230111', 'category': 'Heart / Critical / Specialty Care'},
            {'name': 'Sree Abirami Hospital', 'phone': '0422-2466666', 'category': 'Heart / Critical / Specialty Care'},
            {'name': 'Ashwin Hospital', 'phone': '0422-4224444', 'category': 'Heart / Critical / Specialty Care'},
            {'name': 'Sundaram Medical Foundation Hospital', 'phone': '0422-2232323', 'category': 'Orthopaedic / Trauma / General'},
            {'name': 'VGM Hospital', 'phone': '0422-2512345', 'category': 'Orthopaedic / Trauma / General'},
            {'name': 'Ortho One Orthopaedic Hospital', 'phone': '0422-2227777', 'category': 'Orthopaedic / Trauma / General'},
            {'name': 'Medwin Hospital', 'phone': '0422-2599999', 'category': 'Orthopaedic / Trauma / General'},
            {'name': 'Nirmala Hospital', 'phone': '0422-2223456', 'category': 'Orthopaedic / Trauma / General'},
            {'name': 'Dr. Muthus Hospital', 'phone': '07094614000', 'category': 'Private Multi-Speciality (Affordable Range)'},
            {'name': 'Sumith Multi Speciality Hospital', 'phone': '0422-4572222', 'category': 'Private Multi-Speciality (Affordable Range)'},
            {'name': 'Sri Bala Medical Centre', 'phone': '0422-2644444', 'category': 'Private Multi-Speciality (Affordable Range)'},
            {'name': 'Sheela Hospital', 'phone': '0422-2498383', 'category': 'Private Multi-Speciality (Affordable Range)'},
            {'name': 'NG Hospital', 'phone': '0422-2595963', 'category': 'Private Multi-Speciality (Affordable Range)'},
            {'name': 'Cloudnine Hospital', 'phone': '18602662667', 'category': 'Women & Child Care'},
            {'name': 'Kovai Medical Center Women Care', 'phone': '0422-4323800', 'category': 'Women & Child Care'},
            {'name': 'Sri Krishna Hospital', 'phone': '0422-2678000', 'category': 'Women & Child Care'},
            {'name': 'Motherhood Hospital', 'phone': '08067238900', 'category': 'Women & Child Care'},
            {'name': 'Anurag Hospital', 'phone': '0422-2432333', 'category': 'Women & Child Care'},
            {'name': 'Sankara Eye Hospital', 'phone': '0422-2678000', 'category': 'Eye / ENT / Dental / Other Specialty'},
            {'name': 'Vasan Eye Care', 'phone': '0422-3989000', 'category': 'Eye / ENT / Dental / Other Specialty'},
            {'name': 'PSG Dental Hospital', 'phone': '0422-4345800', 'category': 'Eye / ENT / Dental / Other Specialty'},
            {'name': 'Kovai ENT Hospital', 'phone': '0422-2559999', 'category': 'Eye / ENT / Dental / Other Specialty'},
            {'name': 'Dental Care Centre Coimbatore', 'phone': '0422-2445678', 'category': 'Eye / ENT / Dental / Other Specialty'},
            {'name': 'Sree Andal Hospital', 'phone': '0422-2591000', 'category': 'Additional Hospitals'},
            {'name': 'Rao Hospital', 'phone': '0422-2433333', 'category': 'Additional Hospitals'},
            {'name': 'Shanmuga Hospital', 'phone': '0422-2222222', 'category': 'Additional Hospitals'},
            {'name': 'VG Hospital', 'phone': '0422-2511111', 'category': 'Additional Hospitals'},
            {'name': 'Sree Renga Hospital', 'phone': '0422-2488888', 'category': 'Additional Hospitals'},
            {'name': 'Narayana Multispeciality Hospital', 'phone': '0422-2460000', 'category': 'Additional Hospitals'},
            {'name': 'Sree Saraswathi Hospital', 'phone': '0422-2666666', 'category': 'Additional Hospitals'},
            {'name': 'Kovai Diabetes Speciality Centre', 'phone': '0422-2232666', 'category': 'Additional Hospitals'},
            {'name': 'Bethesda Hospital', 'phone': '0422-2305555', 'category': 'Additional Hospitals'},
            {'name': 'Sri Lakshmi Medical Centre', 'phone': '0422-2456789', 'category': 'Additional Hospitals'},
        ]
        await db.hospitals.insert_many(coimbatore_hospitals)
    yield

app = FastAPI(title="SafeTrack API", lifespan=lifespan)

# Include Routers
app.include_router(auth_router)

# MongoDB Connection
MONGODB_URL = os.getenv("MONGODB_URL")
client = AsyncIOMotorClient(MONGODB_URL)
db = client.safetrack
reports_collection = db.reports
hospitals_collection = db.hospitals

class SymptomReport(BaseModel):
    user_id: str
    heart_rate: int
    spo2: int
    blood_pressure: Optional[str] = "N/A"
    temperature: float
    symptoms: List[str]

support_collection = db.support_requests

class SupportRequest(BaseModel):
    user_id: str
    action: str  # e.g., "sos", "consult_video", "chat_doctor"
    details: Optional[str] = ""

@app.post("/support/request")
async def request_support(req: SupportRequest):
    req_dict = req.dict()
    req_dict["timestamp"] = datetime.now()
    req_dict["status"] = "pending"
    
    # Trigger emergency notification for SOS
    if req.action == "sos":
        try:
            notifier.send_alert(
                title=f"🚨 SOS EMERGENCY: {req.user_id}",
                body=f"Patient requires immediate assistance!",
                topic="emergency_alerts"
            )
        except Exception as e:
            print(f"Failed to send SOS notification: {e}")
            
    try:
        new_req = await support_collection.insert_one(req_dict)
        return {"status": "success", "ticket_id": str(new_req.inserted_id), "message": "Support request submitted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "SafeTrack API is running (MongoDB Edition)", "status": "connected" if client else "disconnected"}

@app.get("/hospitals")
async def get_hospitals():
    hospitals = []
    cursor = hospitals_collection.find()
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        hospitals.append(doc)
    return hospitals

@app.post("/hospitals")
async def add_hospital(hospital: Hospital):
    try:
        new_hosp = await hospitals_collection.insert_one(hospital.dict())
        return {"id": str(new_hosp.inserted_id), "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/report")
async def create_report(report: SymptomReport):
    # 1. Analyze Core Vitals
    current_analysis = MedicalAnalyzer.analyze_vitals(report.heart_rate, report.spo2, report.temperature)
    
    # 2. Automated Doctor Escalation Logic (Predictive)
    try:
        # Fetch the previous report for this user to calculate trends
        last_report = await reports_collection.find_one(
            {"user_id": report.user_id},
            sort=[("timestamp", -1)]
        )
        
        escalation_required = False
        escalation_reason = ""
        
        current_ews = current_analysis.get("ews_score", 0)
        
        if last_report:
            prev_analysis = last_report.get("medical_analysis", {})
            prev_ews = prev_analysis.get("ews_score", 0)
            
            # Predictive Tier 1: Rapid EWS rise (+3 points)
            if current_ews >= prev_ews + 3:
                escalation_required = True
                escalation_reason = "Rapid EWS Rise (+3 pts)"
            
        # Predictive Tier 2: Grave Forecast
        if current_analysis.get("clinical_forecast") == "Grave" or current_ews >= 5:
            escalation_required = True
            escalation_reason = "Critical/Grave Forecast"

        # Trigger Push Notification for Escalation
        if escalation_required:
            notifier.send_alert(
                title=f"🚨 DOCTOR ESCALATION: {report.user_id}",
                body=f"Reason: {escalation_reason} | Forecast: {current_analysis.get('clinical_forecast')} | Score: {current_analysis.get('recovery_score')}%",
                topic="doctor_alerts"
            )
        elif current_analysis.get("risk_level") == "Red":
            # Fallback for critical absolute values
            notifier.send_alert(
                title=f"⚠️ Vitals Alert: {report.user_id}",
                body=f"Risk: {current_analysis.get('status_summary')} | Recovery: {current_analysis.get('recovery_score')}%",
                topic="doctor_alerts"
            )

    except Exception as n_err:
        print(f"Notification Error: {n_err}")

    # 3. Save to Database
    report_dict = report.dict()
    report_dict["timestamp"] = datetime.now()
    report_dict["medical_analysis"] = current_analysis
    
    try:
        new_report = await reports_collection.insert_one(report_dict)
        return {"status": "success", "id": str(new_report.inserted_id), "analysis": current_analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reports")
async def get_all_reports():
    reports = []
    try:
        cursor = reports_collection.find().sort("timestamp", -1)
        async for document in cursor:
            document["_id"] = str(document["_id"])
            # Format datetime for JSON response
            if isinstance(document["timestamp"], datetime):
              document["timestamp"] = document["timestamp"].isoformat()
            reports.append(document)
        return reports
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/core/insights")
async def get_core_insights():
    try:
        reports = []
        cursor = reports_collection.find()
        async for document in cursor:
            document["_id"] = str(document["_id"])
            reports.append(document)
            
        insights = MedicalAnalyzer.analyze_trends(reports)
        return insights
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/core/report/weekly")
async def generate_weekly_report():
    try:
        reports = []
        cursor = reports_collection.find()
        async for document in cursor:
            document["_id"] = str(document["_id"])
            reports.append(document)
            
        insights = MedicalAnalyzer.analyze_trends(reports)
        anomalies = insights.get("anomalies", [])
        
        pdf_path = reporter.generate_weekly_triage(insights, anomalies)
        
        if os.path.exists(pdf_path):
            return FileResponse(
                path=pdf_path,
                filename=os.path.basename(pdf_path),
                media_type='application/pdf'
            )
        else:
            raise HTTPException(status_code=500, detail="PDF generation failed")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
