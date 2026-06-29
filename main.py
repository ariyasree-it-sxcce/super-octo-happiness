from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from database import SessionLocal, User
 
app = FastAPI()
 
 
# ── Helper ────────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        pass  # kept simple — db closed after each request below
 
 
# ── Pages (GET) ───────────────────────────
 
@app.get("/", response_class=HTMLResponse)
def signup_page():
    return """
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
        }

        fieldset {
            padding: 30px;
            background: white;
            border-radius: 8px;
            border: 2px solid #ccc;
            width: 300px;
        }

        legend {
            font-size: 20px;
            font-weight: bold;
            padding: 10px 10px;
        }

        input {
            width: 100%;
            padding: 8px;
            margin: 8px 0 16px 0;
            box-sizing: border-box;
        }

        button {
            width: 100%;
            padding: 10px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
    </style>

    <fieldset>
        <legend>Sign Up</legend>
        <form action="/signup" method="post">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <button type="submit">Sign Up</button>
        </form>
        <p class="form-text"><a href="/login">Already have an account? Login</a></p>
    </fieldset>
    """
@app.get("/login", response_class=HTMLResponse)
def login_page():
    return """
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            background: #f0f0f0;
        }

        fieldset {
            padding: 30px;
            background: white;
            border-radius: 8px;
            border: 2px solid #ccc;
            width: 300px;
        }

        legend {
            font-size: 20px;
            font-weight: bold;
            padding: 0 10px;
        }

        input {
            width: 100%;
            padding: 8px;
            margin: 8px 0 16px 0;
            box-sizing: border-box;
        }

        button {
            width: 100%;
            padding: 10px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
    </style>

    <fieldset>
        <legend>Login</legend>
        <form action="/login" method="post">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <button type="submit">Login</button>
        </form>
        <p><a href="/">Don't have an account? Sign Up</a></p>
    </fieldset>
    """
 
@app.get("/home", response_class=HTMLResponse)
def home(username: str):
    return f"""
    <style>
        body {{
            display: flex;
            justify-content: center;
            align-items: center;
            background: #f0f0f0;
        }}

    </style>

    <div class="box">
        <h2>Welcome, {username}! 🎉</h2>
        <a href='/login'>Logout</a>
    </div>
    """
 
 
# ── Actions (POST) ────────────────────────
 
@app.post("/signup", response_class=HTMLResponse)
def signup(username: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
 
    # Check if username already exists
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        db.close()
        return "<p>Username already taken. <a href='/'>Try again</a></p>"
 
    # Save new user
    new_user = User(username=username, password=password)
    db.add(new_user)
    db.commit()
    db.close()
 
    return "<p>Account created! <a href='/login'>Login now</a></p>"
 
 
@app.post("/login", response_class=HTMLResponse)
def login(username: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
 
    user = db.query(User).filter(
        User.username == username,
        User.password == password
    ).first()
    db.close()
 
    if not user:
        return "<p>Wrong username or password. <a href='/login'>Try again</a></p>"
 
    return f"<p>Login successful! <a href='/home?username={username}'>Go to Home</a></p>"
 