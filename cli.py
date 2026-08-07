"""Menu interativo no terminal.

Uso: python cli.py catalogo_final.json
"""

import sys
from catalogo import Catalogo


caminho_catalogo = sys.argv[1]
catalogo = Catalogo(caminho_catalogo)


def formatar_conteudo(conteudo_id):
    conteudo = catalogo.id_conteudo[conteudo_id]
    titulo = conteudo["titulo"]
    artista = conteudo["artista"]

    return f"{titulo} — {artista}"


def terminal():
    while True:
        print()
        print("Trilha sonora")
        print("=============")
        print("1. Listar todos os usuários")
        print("2. Ver playlist completa de um usuário")
        print("3. Conteúdo na posição N da playlist")
        print("4. Interseção de playlists (N usuários)")
        print("5. Dados de um conteúdo")
        print("6. Conteúdos de um gênero")
        print("7. Enfileirar conteúdo na fila de reprodução")
        print("8. Tocar próximo da fila")
        print("9. Ver fila atual")
        print("0. Sair")

        try:
            comando = int(input("> "))
        except ValueError:
            print("Comando inválido. Digite um número de 0 a 9.")
            continue

        if comando == 0:
            break

        elif comando == 1:
            usuarios = catalogo.listar_usuarios()
            print("Usuários:")

            for nome in usuarios:
                print(nome)

        elif comando == 2:
            nome = input("Digite o nome do usuário: ").strip()
            usuario_id = catalogo.buscar_usuario_por_nome(nome)

            if usuario_id is None:
                print(f"Usuário {nome} não encontrado.")
            else:
                playlist = catalogo.playlist_de(usuario_id)

                if len(playlist) == 0:
                    print("A playlist deste usuário está vazia.")
                else:
                    print(f"Playlist de {nome}:")

                    for conteudo_id in playlist:
                        print(formatar_conteudo(conteudo_id))

        elif comando == 3:
            nome = input("Digite o nome do usuário: ").strip()
            usuario_id = catalogo.buscar_usuario_por_nome(nome)

            if usuario_id is None:
                print(f"Usuário {nome} não encontrado.")
            else:
                playlist = catalogo.playlist_de(usuario_id)

                if len(playlist) == 0:
                    print("A playlist deste usuário está vazia.")
                else:
                    print(f"A playlist possui {len(playlist)} conteúdos.")

                    try:
                        posicao = int(input(f"Digite a posição (1 a {len(playlist)}): ")) - 1
                    except ValueError:
                        print("Posição inválida. Digite um número inteiro.")
                        continue

                    conteudo_id = catalogo.conteudo_na_posicao(usuario_id, posicao)

                    if conteudo_id is None:
                        print(f"Posição {posicao + 1} inválida para o usuário {nome}.")
                    else:
                        print(formatar_conteudo(conteudo_id))

        elif comando == 4:
            nomes = input("Digite os nomes dos usuários separados por vírgula: ").split(",")
            usuario_ids = []
            usuario_invalido = False

            for nome in nomes:
                nome = nome.strip()

                if nome == "":
                    continue

                usuario_id = catalogo.buscar_usuario_por_nome(nome)

                if usuario_id is None:
                    print(f"Usuário {nome} não encontrado.")
                    usuario_invalido = True
                else:
                    usuario_ids.append(usuario_id)

            if len(usuario_ids) < 2:
                print("Digite ao menos dois usuários válidos.")
                continue

            if usuario_invalido:
                print("Não foi possível calcular a interseção.")
                continue

            intersecao = catalogo.intersecao_playlists(usuario_ids)

            if len(intersecao) == 0:
                print("Os usuários não possuem conteúdos em comum.")
            else:
                print("Conteúdos em comum:")

                for conteudo_id in intersecao:
                    print(formatar_conteudo(conteudo_id))

        elif comando == 5:
            conteudo_id = input("Digite o ID do conteúdo: ").strip()

            if conteudo_id not in catalogo.id_conteudo:
                print(f"Conteúdo {conteudo_id} não encontrado.")
                continue

            conteudo = catalogo.id_conteudo[conteudo_id]
            rating = catalogo.rating_de(conteudo_id)
            duracao = catalogo.duracao_total_de(conteudo_id)
            generos = catalogo.generos_de(conteudo_id)
            plataformas = catalogo.plataformas_de(conteudo_id)
            data_adicionado = catalogo.data_adicionado_de(conteudo_id)

            print(formatar_conteudo(conteudo_id))
            print(f"Tipo: {conteudo['tipo']}")
            print(f"Rating: {rating}")
            print(f"Duração: {duracao} segundos")
            print(f"Gêneros: {generos}")
            print(f"Plataformas: {plataformas}")
            print(f"Data adicionada: {data_adicionado}")

            if conteudo["tipo"] == "musica":
                execucoes = catalogo.execucoes_de(conteudo_id)
                print(f"Execuções: {execucoes}")

        elif comando == 6:
            genero = input("Digite o gênero: ").strip()
            conteudos = catalogo.conteudos_do_genero(genero)

            if len(conteudos) == 0:
                print(f"Nenhum conteúdo encontrado para o gênero {genero}.")
            else:
                print(f"Conteúdos do gênero {genero}:")

                for conteudo_id in conteudos:
                    print(formatar_conteudo(conteudo_id))

        elif comando == 7:
            conteudo_id = input("Digite o ID do conteúdo: ").strip()

            if catalogo.enfileirar(conteudo_id):
                print("Conteúdo enfileirado:")
                print(formatar_conteudo(conteudo_id))
            else:
                print(f"Conteúdo {conteudo_id} não encontrado.")

        elif comando == 8:
            proximo_conteudo = catalogo.proximo()

            if proximo_conteudo is None:
                print("Fila de reprodução vazia.")
            else:
                print("Tocando próximo conteúdo:")
                print(formatar_conteudo(proximo_conteudo))

        elif comando == 9:
            fila_atual = catalogo.fila_atual()

            if len(fila_atual) == 0:
                print("Fila de reprodução vazia.")
            else:
                print("Fila atual:")

                for conteudo_id in fila_atual:
                    print(formatar_conteudo(conteudo_id))

        else:
            print("Comando inválido. Digite um número de 0 a 9.")


terminal()
