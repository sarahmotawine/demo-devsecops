# app.py — VERSÃO SEGURA
import sqlite3
import os
import html
from functools import wraps
import time

# ✅ FIX 1: Credenciais via variáveis de ambiente (sem hardcode)
DB_PASSWORD = os.environ.get('DB_PASSWORD')
API_KEY     = os.environ.get('API_KEY')

def buscar_usuario(username):
    conn = sqlite3.connect('database.db')
    # ✅ FIX 2: Parameterized query — elimina SQL Injection
    query = "SELECT * FROM users WHERE name = ?"
    return conn.execute(query, (username,)).fetchall()

def exibir_nome(nome):
    # ✅ FIX 3: Escape do HTML — elimina XSS
    nome_seguro = html.escape(nome)
    return f"<p>Ola, {nome_seguro}!</p>"

# ✅ FIX 4: Rate limiting simples contra Brute Force
_tentativas = {}
MAX_TENTATIVAS = 5
JANELA_SEGUNDOS = 60

def login(usuario, senha):
    agora = time.time()

    # Limpa tentativas antigas
    _tentativas[usuario] = [
        t for t in _tentativas.get(usuario, [])
        if agora - t < JANELA_SEGUNDOS
    ]

    if len(_tentativas[usuario]) >= MAX_TENTATIVAS:
        raise PermissionError("Muitas tentativas. Tente novamente em 1 minuto.")

    _tentativas[usuario].append(agora)

    conn = sqlite3.connect('database.db')
    # ✅ Também usa parameterized query aqui
    query = "SELECT * FROM users WHERE user = ? AND pass = ?"
    return conn.execute(query, (usuario, senha)).fetchone()