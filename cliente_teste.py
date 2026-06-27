import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def _parse(result):
    sc = getattr(result, "structuredContent", None)
    if sc is not None:
        if isinstance(sc, dict) and list(sc.keys()) == ["result"]:
            return sc["result"]
        return sc

    for item in result.content:
        text = getattr(item, "text", None)
        if text:
            try:
                payload = json.loads(text)
                return payload   # this already returns a real list/dict
            except json.JSONDecodeError:
                return text

    return None

def _as_list(parsed):
    """Garante lista de dicts: string -> json.loads; dict -> [dict]; lista -> parseia cada item."""
    if isinstance(parsed, str):
        parsed = json.loads(parsed)
    if isinstance(parsed, dict):
        return [parsed]
    return [json.loads(x) if isinstance(x, str) else x for x in parsed]

async def main():
    params = StdioServerParameters(command="python", args=["servidor_mcp.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools_resp = await session.list_tools()
            tools = [t.name for t in tools_resp.tools]

            criar = await session.call_tool(
                "criar_tarefa", {"titulo": "estudar MCP", "concluida": False}
            )
            listar = await session.call_tool("listar_tarefas", {})

            envelope = {
                "tools": tools,
                "criar_resultado": _parse(criar),
                "listar_resultado": _as_list(_parse(listar)),
            }
            print(json.dumps(envelope, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
