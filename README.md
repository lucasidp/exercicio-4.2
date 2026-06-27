# MCP server da TODO list - exercício 4.2

MCP server (stdio) que expõe as tools `criar_tarefa` e `listar_tarefas`,
implementadas chamando a API REST do exercício 4.1 (`http://localhost:8000`).
`cliente_teste.py` exercita as tools e imprime o envelope JSON validado.

## Pré-requisito
A API do 4.1 precisa estar no ar em `localhost:8000` (reinicie para store limpo).

## Rodar
```
pip install -r requirements.txt
py cliente_teste.py
```

## validar
```
autograde validar 4.2
```
