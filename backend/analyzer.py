from typing import Dict, Any, List

class MedicalAnalyzer:
    @staticmethod
    def calculate_ews(heart_rate: int, spo2: int, temperature: float) -> int:
        """
        Calculates an Early Warning Score (EWS) 0-10.
        Higher scores indicate higher risk of clinical collapse.
        """
        ews = 0
        # SpO2 EWS
        if spo2 < 91: ews += 3
        elif spo2 < 94: ews += 2
        elif spo2 < 96: ews += 1
        
        # HR EWS
        if heart_rate > 130 or heart_rate < 40: ews += 3
        elif heart_rate > 110 or heart_rate < 50: ews += 2
        elif heart_rate > 100 or heart_rate < 60: ews += 1
        
        # Temperature EWS
        if temperature > 39.1 or temperature < 35.0: ews += 3
        elif temperature > 38.0 or temperature < 36.0: ews += 1
        
        return min(10, ews)

    @staticmethod
    def analyze_vitals(heart_rate: int, spo2: int, temperature: float) -> Dict[str, Any]:
        """
        Analyzes patient vitals and returns status, risk level, EWS, and clinical forecast.
        """
        score = 100
        risk_level = "Green"
        status_message = "All vitals within normal range."
        alerts = []

        # Calculate Early Warning Score (EWS) - Predictive Baseline
        ews = MedicalAnalyzer.calculate_ews(heart_rate, spo2, temperature)

        # 1. SpO2 Analysis
        if spo2 < 92:
            score -= 50
            risk_level = "Red"
            status_message = "Critical: Low Oxygen Levels (Hypoxia)"
            alerts.append("Low SpO2 detected. Immediate medical consultation recommended.")
        elif spo2 < 95:
            score -= 15
            risk_level = "Yellow"
            status_message = "Warning: Oxygen levels slightly low."
            alerts.append("Monitor oxygen levels every 2 hours.")

        # 2. Heart Rate Analysis
        if heart_rate > 110 or heart_rate < 50:
            score -= 25
            risk_level = "Red"
            status_message = "Critical Heart Rate Anomaly"
            alerts.append("Tachycardia/Bradycardia detected. Monitor cardiovascular stability.")
        elif heart_rate > 90:
            score -= 10
            if risk_level == "Green": risk_level = "Yellow"

        # 3. Temperature Analysis
        if temperature > 39.0 or temperature < 35.0:
            score -= 30
            risk_level = "Red"
            status_message = "Critical Thermal Dysregulation"
            alerts.append("High fever or hypothermia detected.")
        elif temperature > 37.8:
            score -= 10
            if risk_level == "Green": risk_level = "Yellow"

        # Predictive Forecast Logic
        forecast = "Stable"
        if ews >= 5: forecast = "Grave"
        elif ews >= 3 or risk_level == "Yellow": forecast = "Declining"
        elif score < 70: forecast = "Unstable"

        return {
            "recovery_score": max(0, score),
            "risk_level": risk_level,
            "ews_score": ews,
            "clinical_forecast": forecast,
            "status_summary": status_message,
            "medical_alerts": alerts
        }

    @staticmethod
    def analyze_trends(reports: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Processes multiple reports to find population-level insights and predictive trends.
        """
        if not reports:
            return {"message": "No data available for analysis"}

        total_reports = len(reports)
        avg_score = sum(r.get("medical_analysis", {}).get("recovery_score", 0) for r in reports) / total_reports
        
        # Risk Distribution
        risks = [r.get("medical_analysis", {}).get("risk_level", "Green") for r in reports]
        risk_dist = {"Red": risks.count("Red"), "Yellow": risks.count("Yellow"), "Green": risks.count("Green")}

        # Predictive Trend Analysis: Group by user and identify Impending Failure
        user_history = {}
        for r in reports:
            uid = r.get("user_id")
            if uid not in user_history: user_history[uid] = []
            user_history[uid].append(r)
        
        anomalies = []
        impending_failures = 0
        for uid, logs in user_history.items():
            sorted_logs = sorted(logs, key=lambda x: x.get("timestamp", ""))
            if len(sorted_logs) >= 2:
                curr = sorted_logs[-1].get("medical_analysis", {})
                prev = sorted_logs[-2].get("medical_analysis", {})
                
                # Predictive Alert: Rapid EWS rise
                if curr.get("ews_score", 0) > prev.get("ews_score", 0) + 2:
                    impending_failures += 1
                
                drop = prev.get("recovery_score", 0) - curr.get("recovery_score", 0)
                if drop >= 20:
                    anomalies.append({
                        "user_id": uid,
                        "score_drop": drop,
                        "forecast": curr.get("clinical_forecast"),
                        "status": curr.get("status_summary")
                    })

        return {
            "system_health_index": round(avg_score, 2),
            "total_active_monitors": total_reports,
            "risk_distribution": risk_dist,
            "impending_failure_forecast": impending_failures,
            "anomalies": anomalies,
            "predicted_recovery_rate": f"{round(risk_dist['Green'] / total_reports * 100, 1)}%" if total_reports > 0 else "0%"
        }
