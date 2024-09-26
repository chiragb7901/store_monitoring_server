from flask import Flask, jsonify, request, send_file
from datetime import timedelta
from models import StoreStatus, BusinessHours, StoreTimezone
from database import session
from utils import convert_utc_to_local
from calculations import calculate_uptime_downtime
import uuid
import os
import csv
import threading

app = Flask(__name__)

reports = {}

@app.route('/trigger_report', methods=['POST'])
def trigger_report():
    report_id = str(uuid.uuid4())
    
    reports[report_id] = {
        'status': 'Running',
        'file_path': None
    }
    
    thread = threading.Thread(target=generate_report, args=(report_id,))
    thread.start()
    
    return jsonify({"report_id": report_id})

def generate_report(report_id):
    try:
        store_status_data = session.query(StoreStatus).all()
        business_hours_data = session.query(BusinessHours).all()
        timezone_data = session.query(StoreTimezone).all()
        
        report_data = []

        for store in timezone_data:
            store_id = store.id
            store_polls = [s for s in store_status_data if s.store_id == store_id]
            store_hours = [h for h in business_hours_data if h.store_id == store_id]
            store_timezone = next((t for t in timezone_data if t.id == store_id), None)
            
            tz_str = store_timezone.timezone.strip() if store_timezone else 'America/Denver'
            
            for poll in store_polls:
                poll.timestamp_utc = convert_utc_to_local(poll.timestamp_utc, tz_str)
            
            uptime_last_hour, downtime_last_hour = calculate_uptime_downtime(store_polls, store_hours, timedelta(hours=1))
            uptime_last_day, downtime_last_day = calculate_uptime_downtime(store_polls, store_hours, timedelta(days=1))
            uptime_last_week, downtime_last_week = calculate_uptime_downtime(store_polls, store_hours, timedelta(weeks=1))

            report_data.append({
                "store_id": store_id,
                "uptime_last_hour": uptime_last_hour.total_seconds() / 60,
                "downtime_last_hour": downtime_last_hour.total_seconds() / 60,
                "uptime_last_day": uptime_last_day.total_seconds() / 3600,
                "downtime_last_day": downtime_last_day.total_seconds() / 3600,
                "uptime_last_week": uptime_last_week.total_seconds() / 3600,
                "downtime_last_week": downtime_last_week.total_seconds() / 3600
            })

        file_path = save_report_to_csv(report_id, report_data)
        reports[report_id]['status'] = 'Complete'
        reports[report_id]['file_path'] = file_path

    except Exception as e:
        print(f"Error generating report: {e}")
        file_path = save_report_to_csv(report_id, report_data)
        reports[report_id]['status'] = 'Failed'

@app.route('/get_report', methods=['GET'])
def get_report():
    report_id = request.args.get('report_id')

    if report_id not in reports:
        return jsonify({"error": "Invalid report_id"}), 404

    report_info = reports[report_id]

    if report_info['status'] == 'Running':
        return jsonify({"status": "Running"})
    
    if report_info['status'] == 'Complete':
        return send_file(report_info['file_path'], as_attachment=True)

    return jsonify({"status": "Failed"}), 500

def save_report_to_csv(report_id, report_data):
    if not os.path.exists('reports'):
        os.makedirs('reports')

    file_path = f'reports/report_{report_id}.csv'
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["store_id", "uptime_last_hour", "downtime_last_hour", "uptime_last_day", "downtime_last_day", "uptime_last_week", "downtime_last_week"])
        writer.writeheader()
        writer.writerows(report_data)

    return file_path

@app.route('/health', methods=['GET'])
def health_check():
    return "Server is working"

if __name__ == '__main__':
    app.run(debug=True)
