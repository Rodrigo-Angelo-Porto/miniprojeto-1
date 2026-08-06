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
    def rating_de(self, conteudo_id: str) -> float | None:

        if conteudo_id not in self.id_conteudo:
            return None
        rating = self.id_conteudo[conteudo_id].get("rating", None)
        if rating is None:
            return None
        return float(rating)

    def duracao_total_de(self, conteudo_id: str) -> int | None:
        total = 0
        if conteudo_id not in self.id_conteudo:
            return None
        elif self.id_conteudo[conteudo_id].get("tipo") == "album":
            for faixa in self.id_conteudo[conteudo_id].get("faixas", []):
                duracao = faixa.get("duracao_seg", None)
                if duracao is not None:
                    total += duracao
            return total
        elif self.id_conteudo[conteudo_id].get("tipo") == "musica":
            duracao = self.id_conteudo[conteudo_id].get("duracao_seg", None)
            if duracao is None:
                return None
            return int(duracao)

    def generos_de(self, conteudo_id: str) -> list[str] | None:
        if conteudo_id not in self.id_conteudo:
            return None

        generos = self.id_conteudo[conteudo_id].get("generos", None)
        if generos is None:
            return None
    
        pendentes = [generos]
        generos_achatados = []

        while pendentes:
            genero = pendentes.pop()

            if isinstance(genero, str):
                generos_achatados.append(genero)
            elif isinstance(genero, list):
                for elemento in genero:
                    pendentes.append(elemento)

        return sorted(generos_achatados)

    def plataformas_de(self, conteudo_id: str) -> list[str] | None:
        if conteudo_id not in self.id_conteudo:
            return None
        todas_as_plataformas = self.id_conteudo[conteudo_id].get("plataformas", [])
        return sorted(todas_as_plataformas)

    def data_adicionado_de(self, conteudo_id: str) -> str | None:
        if conteudo_id not in self.id_conteudo:
            return None
        formato_do_ano = self.id_conteudo[conteudo_id].get("data_adicionado", None)

        if formato_do_ano is None:
            return None

        if "/" in formato_do_ano:
            dia, mes, ano = formato_do_ano.split("/")
            return f"{ano}-{mes}-{dia}"

        return formato_do_ano

    def execucoes_de(self, conteudo_id: str) -> int | None:
        if conteudo_id not in self.id_conteudo:
            return None
        numero_de_execucoes = self.id_conteudo[conteudo_id].get("engajamento", {}).get("execucoes")
        if numero_de_execucoes is None:
            return None
        if isinstance(numero_de_execucoes, str):
            numero_de_execucoes = numero_de_execucoes.replace(",", "")
        return int(numero_de_execucoes)

    def conteudos_do_genero(self, genero: str) -> list[str]:
        conteudos = []

        for conteudo in self.id_conteudo:
            genero_da_musica = self.generos_de(conteudo)

            if genero_da_musica is not None and genero in genero_da_musica:
                conteudos.append(conteudo)

        return sorted(conteudos)

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
