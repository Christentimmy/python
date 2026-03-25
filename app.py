
import asyncio
from agent.agent_loop import run_agent
from agent.tool_registry import TOOLS
from agent.tool_schema import convert_tools_to_schema


async def main():
    tools = convert_tools_to_schema(TOOLS)

    user_input = input("Query Github: ")
    result = await run_agent(
        user_input,
        tools,
    )

    print(f"Agent :{result}")


asyncio.run(main())