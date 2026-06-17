# app.py — VERSÃO SEGURA (sem falso positivo no Semgrep)
import sqlite3
import os
import html
import time

DB_PASSWORD = os.environ.get('DB_PASSWORD')
API_KEY     = os.environ.get('API_KEY')

def buscar_usuario(username):
    with sqlite3.connect('database.db') as conn:
        # ✅ Sem variável intermediária — Semgrep reconhece como seguro
        return conn.execute(
            "SELECT * FROM users WHERE name = ?",
            (username,)
        ).fetchall()

def exibir_nome(nome):
    nome_seguro = html.escape(nome)
    return f"<p>Ola, {nome_seguro}!</p>"

_tentativas = {}
MAX_TENTATIVAS = 5
JANELA_SEGUNDOS = 60

def login(usuario, senha):
    agora = time.time()

    _tentativas[usuario] = [
        t for t in _tentativas.get(usuario, [])
        if agora - t < JANELA_SEGUNDOS
    ]

    if len(_tentativas[usuario]) >= MAX_TENTATIVAS:
        raise PermissionError("Muitas tentativas. Tente novamente em 1 minuto.")

    _tentativas[usuario].append(agora)

    with sqlite3.connect('database.db') as conn:
        # ✅ Inline também — sem variável query
        return conn.execute(
            "SELECT * FROM users WHERE user = ? AND pass = ?",
            (usuario, senha)
        ).fetchone()