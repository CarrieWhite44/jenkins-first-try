from flask import Flask, request, redirect, url_for, session, render_template_string
import psycopg2
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"


# ----------- DB CONNECTION ONLY -----------
def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("DB_NAME", "mydb"),
        user=os.environ.get("DB_USER", "user"),
        password=os.environ.get("DB_PASSWORD", "pass")
    )


# ----------- LOGIN / SIGNUP -----------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        cur = conn.cursor()

        # check if user exists
        cur.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cur.fetchone()

        if user:
            if user[2] == password:
                session["user"] = username
                return redirect(url_for("dashboard"))
            else:
                return "Wrong password 😢"
        else:
            # create user
            cur.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, password)
            )
            conn.commit()

            session["user"] = username
            return redirect(url_for("dashboard"))

        cur.close()
        conn.close()

    return render_template_string("""
        <h1>Hello, this is your website</h1>
        <form method="POST">
            <input name="username" placeholder="Username"><br><br>
            <input name="password" type="password" placeholder="Password"><br><br>
            <button type="submit">Enter</button>
        </form>
    """)


@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return f"<h1>Hello {session['user']} 🎉</h1><a href='/logout'>Logout</a>"
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return "<h1>Logged out 👋</h1><a href='/'>Back</a>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)