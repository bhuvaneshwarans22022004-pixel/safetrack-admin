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

# Include Routers
app.include_router(auth_router)

# MongoDB Connection
MONGODB_URL = os.getenv("MONGODB_URL")
client = AsyncIOMotorClient(MONGODB_URL)
db = client.safetrack
reports_collection = db.reports

class SymptomReport(BaseModel):
    user_id: str
    heart_rate: int
    spo2: int
    blood_pressure: Optional[str] = "N/A"
    temperature: float
    symptoms: List[str]

@app.get("/")
async def root():
    return {"message": "SafeTrack API is running (MongoDB Edition)", "status": "connected" if client else "disconnected"}

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
