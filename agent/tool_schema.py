

def convert_tools_to_schema(tools):
    openai_tools = []

    for tool in tools:
        openai_tool = {
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"]
            }
        }
        openai_tools.append(openai_tool)

    return openai_tools     
