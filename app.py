# app.py — VULNERABILIDADES INTENCIONAIS (so para demo!)
import sqlite3, os

# VULN 1: Credenciais hardcoded (GitLeaks vai detectar)
DB_PASSWORD = os.environ.get('DB_PASSWORD')
API_KEY     = os.environ.get('API_KEY')

def buscar_usuario(username):
    conn = sqlite3.connect('database.db')
    # VULN 2: SQL Injection (Semgrep vai detectar)
    query = f"SELECT * FROM users WHERE name = '{username}'"
    return conn.execute(query).fetchall()

def exibir_nome(nome):
    # VULN 3: XSS — saida sem sanitizacao (Semgrep vai detectar)
    return f"<p>Ola, {nome}!</p>"

def login(usuario, senha):
    conn = sqlite3.connect('database.db')
    # VULN 4: Sem limite de tentativas — Brute Force possivel
    query = f"SELECT * FROM users WHERE user='{usuario}' AND pass='{senha}'"
    return conn.execute(query).fetchone()