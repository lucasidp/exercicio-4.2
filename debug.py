import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    params = StdioServerParameters(command="python", args=["servidor_mcp.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            listar = await session.call_tool("listar_tarefas", {})
            print("structuredContent:", repr(getattr(listar, "structuredContent", None)))
            print("content:", repr(listar.content))

if __name__ == "__main__":
    asyncio.run(main())