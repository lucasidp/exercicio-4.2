import json
import httpx
from mcp.server.fastmcp import FastMCP

API_BASE = "http://localhost:8000"

mcp = FastMCP("todo-mcp")


@mcp.tool()
def criar_tarefa(titulo: str, concluida: bool = False) -> dict:
    """Cria uma tarefa na API REST 4.1 e retorna a tarefa criada."""
    resp = httpx.post(
        f"{API_BASE}/tarefas",
        json={"titulo": titulo, "concluida": concluida},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


@mcp.tool()
def listar_tarefas() -> str:
    """Lista todas as tarefas da API REST 4.1 (JSON array como texto)."""
    resp = httpx.get(f"{API_BASE}/tarefas", timeout=10)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    mcp.run()