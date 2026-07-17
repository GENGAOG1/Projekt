from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

PASSWORD = "Fuck Society"

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

    if request.form.get("password") == PASSWORD:
    return redirect("https://www.tiktok.com")
        else:
            app.logger.warning(
                "Failed login attempt from %s",
                request.remote_addr
            )
            message = "Wrong password!"

    return render_template_string(LOGIN_PAGE, message=message)

@app.route("/success")
def success():
    return SUCCESS_PAGE

if __name__ == "__main__":
    app.run(debug=True)
