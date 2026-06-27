import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

def _unwrap(result):
    """Extrai o conteúdo estruturado do CallToolResult."""
    if getattr(result, "structuredContent", None) is not None:
        sc = result.structuredContent
        return sc.get("result", sc) if isinstance(sc, dict) else sc
    blocks = []
    for item in result.content:
        text = getattr(item, "text", None)
        if text is not None:
            try:
                blocks.append(json.loads(text))
            except json.JSONDecodeError:
                blocks.append(text)
    return blocks[0] if len(blocks) == 1 else blocks

async def main():
    params = StdioServerParameters(command="python", args = ["servidor_mcp.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools_resp = await session.list_tools()
            tools = [t.name for t in tools_resp.tools]

            criar = await session.call_tool(
                "criar_tarefa", {"titulo": "estudar MCP", "concluida", False}
            )

            listar = await session.call_tool("listar_tarefas", {})

            envelope = {
                "tools": tools,
                "criar_resultado": _unwrap(criar),
                "listar_resultado": _unwrap(listar),
            }
            print(json.dumps(envelope, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
