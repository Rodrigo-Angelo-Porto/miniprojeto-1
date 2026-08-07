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


quantidade_acertos = 0
respostas_erradas = []
respostas_ausentes = []


for consulta_id, resposta_correta in gabarito.items():
    if consulta_id not in respostas:
        respostas_ausentes.append(consulta_id)
        continue

    resposta_obtida = respostas[consulta_id]

    if respostas_iguais(resposta_correta, resposta_obtida):
        quantidade_acertos += 1
    else:
        respostas_erradas.append((consulta_id, resposta_correta, resposta_obtida))


print(f"Acertos: {quantidade_acertos}/{len(gabarito)}")
print(f"Respostas erradas: {len(respostas_erradas)}")
print(f"Respostas ausentes: {len(respostas_ausentes)}")


if len(respostas_erradas) > 0:
    print()
    print("Respostas erradas:")

    for consulta_id, resposta_correta, resposta_obtida in respostas_erradas:
        print(f"Consulta {consulta_id}")
        print(f"Esperado: {resposta_correta}")
        print(f"Obtido: {resposta_obtida}")
        print()


if len(respostas_ausentes) > 0:
    print()
    print("Respostas ausentes:")

    for consulta_id in respostas_ausentes:
        print(f"Consulta {consulta_id}")
