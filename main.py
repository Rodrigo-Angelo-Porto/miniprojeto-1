"""Modo batch: lê consultas.json, responde em ordem, grava respostas.json.

Uso: python main.py consultas.json respostas.json
"""
import json
import sys

from catalogo import Catalogo

caminho_consultas = sys.argv[1]
caminho_respostas = sys.argv[2]

with open(caminho_consultas, "r", encoding="utf-8") as arquivo:
    dados_consultas = json.load(arquivo)

catalogo = Catalogo("catalogo_final.json")
respostas = {}

for consulta in dados_consultas["consultas"]:
    id_consulta = str(consulta["id"])
    tipo = consulta["tipo"]
    parametros = consulta["parametros"]

    funcao = getattr(catalogo, tipo)
    resultado = funcao(**parametros)

    respostas[id_consulta] = resultado

with open(caminho_respostas, "w", encoding="utf-8") as arquivo:
    json.dump(respostas, arquivo, ensure_ascii=False, indent=4)
