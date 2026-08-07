"""Compara respostas.json com gabarito_publico.json."""

import json


def respostas_iguais(resposta_correta, resposta_obtida):
    if isinstance(resposta_correta, float):
        if not isinstance(resposta_obtida, (int, float)):
            return False

        diferenca = abs(resposta_correta - resposta_obtida)
        return diferenca < 1e-6

    return resposta_correta == resposta_obtida


with open("gabarito_publico.json", "r", encoding="utf-8") as arquivo:
    gabarito = json.load(arquivo)

with open("respostas.json", "r", encoding="utf-8") as arquivo:
    respostas = json.load(arquivo)
