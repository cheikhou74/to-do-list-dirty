import requests
import json
import sys

def send_discord_webhook(webhook_url, message, status="info"):
    """Send notification to Discord webhook"""
    
    colors = {
        "start": 0x3498db,     # Blue
        "success": 0x2ecc71,   # Green
        "failure": 0xe74c3c,   # Red
        "info": 0x9b59b6       # Purple
    }
    
    embed = {
        "title": "CI/CD Pipeline Notification",
        "description": message,
        "color": colors.get(status, 0x3498db),
        "timestamp": datetime.now().isoformat()
    }
    
    payload = {
        "embeds": [embed],
        "username": "CI Bot",
        "avatar_url": "https://cdn-icons-png.flaticon.com/512/2103/2103655.png"
    }
    
    response = requests.post(webhook_url, json=payload)
    return response.status_code == 204

if __name__ == "__main__":
    from datetime import datetime
    
    webhook_url = sys.argv[1] if len(sys.argv) > 1 else None
    status = sys.argv[2] if len(sys.argv) > 2 else "info"
    message = sys.argv[3] if len(sys.argv) > 3 else "CI Pipeline executed"
    
    if webhook_url:
        send_discord_webhook(webhook_url, message, status)