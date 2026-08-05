"""A classe Catalogo. Leia o README.md antes de começar.

Esta é a peça central do projeto: carrega o JSON uma vez, constrói os
índices no __init__ e expõe os 16 métodos que o main.py e o cli.py usam.
"""

import json

class Catalogo:
    def __init__(self, caminho_json: str):
        with open(caminho_json, "r", encoding="utf-8") as arquivo:
            self.dados = json.load(arquivo)

        self.id_conteudo = {}

        for conteudo in self.dados["conteudos"]:
            conteudo_id = conteudo["id"]
            self.id_conteudo[conteudo_id] = conteudo

        self.id_usuario = {}

        for usuario in self.dados["usuarios"]:
            usuario_id = usuario["id"]
            self.id_usuario[usuario_id] = usuario

        self.nome_usuario = {}

        for usuario in self.dados["usuarios"]:
            nome = usuario["nome"].lower()
            usuario_id = usuario["id"]
            self.nome_usuario[nome] = usuario_id

        self.fila_musica = []

    # --- usuários e playlists ---
    def listar_usuarios(self) -> list[str]:
        usuarios = []
        for usuario in self.dados["usuarios"]:
            usuarios.append(usuario["nome"])
        return sorted(usuarios)

    def buscar_usuario_por_nome(self, nome: str) -> str | None:
        nome = nome.lower()
        return self.nome_usuario.get(nome, None)
        
    def playlist_de(self, usuario_id: str) -> list[str] | None:

        if usuario_id not in self.id_usuario:
            return None

        return self.id_usuario[usuario_id].get("playlist", [])

    def conteudo_na_posicao(self, usuario_id: str, posicao: int) -> str | None:

        if usuario_id not in self.id_usuario:
            return None

        playlist = self.id_usuario[usuario_id].get("playlist", [])
        if posicao < 0 or posicao >= len(playlist):
            return None

        return playlist[posicao]
        
    def intersecao_playlists(self, usuario_ids: list[str]) -> list[str]:

        if not usuario_ids:
            return []

        playlists = []
        for usuario_id in usuario_ids:
            if usuario_id not in self.id_usuario:
                return []
            playlist = self.id_usuario[usuario_id].get("playlist", [])
            playlists.append(set(playlist))

        intersecao = set.intersection(*playlists)
        return sorted(intersecao)

    # --- dados de um conteúdo ---
    def rating_de(self, conteudo_id: str) -> float | None: ...
    def duracao_total_de(self, conteudo_id: str) -> int | None: ...
    def generos_de(self, conteudo_id: str) -> list[str] | None: ...
    def plataformas_de(self, conteudo_id: str) -> list[str] | None: ...
    def data_adicionado_de(self, conteudo_id: str) -> str | None: ...
    def execucoes_de(self, conteudo_id: str) -> int | None: ...
    def conteudos_do_genero(self, genero: str) -> list[str]: ...

    # --- fila de reprodução ---
    def enfileirar(self, conteudo_id: str) -> bool:

        if conteudo_id not in self.id_conteudo:
            return False

        self.fila_musica.append(conteudo_id)
        return True

    def proximo(self) -> str | None: 
        if self.fila_musica:
            return self.fila_musica.pop(0)
        else:
            return None

    def fila_atual(self) -> list[str]:
        return self.fila_musica[:]
