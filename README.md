# Miniprojeto

## Decisões de modelagem

O projeto foi dividido em arquivos com funções diferentes. O catalogo.py tem Catalogo e as operações principais. O cli.py possui o menu interativo, o main.py processa as consultas do arquivo JSON e o conferir.py compara as respostas com o gabarito.

Foram criados dicionários para localizar usuários e conteúdos, evitando percorrer todas as listas a cada busca.

Na busca por nome, os nomes são convertidos para letras minúsculas, para evitar que por diferença de letras mmaiúsculas e minúsculas dê erro para o usuário.

As playlists são representadas por listas, para preservar a ordem dos conteúdos. Para encontrar conteúdos presentes em várias playlists, elas são convertidas temporariamente em sets, porque nos sets nâo tem itens duplicados, para calcular a interseção.

A fila de reprodução também utiliza uma lista. Os conteúdos são adicionados ao final com append() e retirados do início com pop(0), funcionando como FIFO, já que a primeira música adicionada será a primeira reproduzida.

Quando um usuário, conteúdo ou posição não existe, os métodos retornam None, False ou uma lista vazia, evitando que o programa seja interrompido.
