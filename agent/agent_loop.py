
import json
from agent.llm_client import call_llm
from agent.github_tools import run_tool


async def run_agent(user_input, tools):
    messages = [
        {
            "role": "system",
            "content": "You are an AI agent that can use tools when needed."
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    for _ in range(5):
        response = await call_llm(messages, tools)
        message = response["choices"][0]["message"]

        if "tool_calls" not in message:
            return message["content"]

        messages.append(message)

        for tool_call in message["tool_calls"]:
            tool_name = tool_call["function"]["name"]
            args = json.loads(tool_call["function"]["arguments"])

            result = await run_tool(tool_name, args)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "content": str(result)
            })

    return "Agent reached maximum steps"

