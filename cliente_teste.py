import asyncio
import json
import logging
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

logging.disable(logging.CRITICAL)


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
                return json.loads(text)
            except json.JSONDecodeError:
                return text
    return None


async def run():
    params = StdioServerParameters(command="python", args=["servidor_mcp.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = [t.name for t in (await session.list_tools()).tools]
            criar = await session.call_tool(
                "criar_tarefa", {"titulo": "tarefa via mcp", "concluida": False}
            )
            listar = await session.call_tool("listar_tarefas", {})
            return {
                "tools": tools,
                "criar_resultado": _parse(criar),
                "listar_resultado": _parse(listar),
            }


def main():
    envelope = asyncio.run(run())
    sys.stdout.write(json.dumps(envelope, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()