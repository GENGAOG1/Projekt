from flask import Flask, request, render_template_string

app = Flask(__name__)

PASSWORD = "MeinPasswort123"

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Terminal</title>
<style>
body{
    background:#000;
    color:#ff0000;
    font-family:Consolas, monospace;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
}
.box{
    width:700px;
    border:2px solid red;
    padding:20px;
}
input{
    width:100%;
    background:#000;
    color:red;
    border:1px solid red;
    padding:10px;
    font-family:inherit;
}
button{
    margin-top:10px;
    background:red;
    color:black;
    border:none;
    padding:10px 20px;
    cursor:pointer;
}
</style>
</head>
<body>
<div class="box">
<pre>
[INFO] Connecting...
[INFO] Data got logged
[INFO] Waiting for authentication...
</pre>

<form method="POST">
<input type="password" name="password" placeholder="Password">
<button>Login</button>
</form>

<p>{{ message }}</p>
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        if request.form.get("password") == PASSWORD:
            message = "Access granted."
        else:
            app.logger.warning(
                "Failed login attempt from %s",
                request.remote_addr
            )
            message = "Access denied."

    return render_template_string(HTML, message=message)

if __name__ == "__main__":
    app.run(debug=True)
