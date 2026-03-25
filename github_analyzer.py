# import asyncio
# import httpx
# import inspect

# base_url = "https://api.github.com/users"

# async def get_github_profile(name: str) -> dict:
#     async with httpx.AsyncClient() as client:
#         try:
#             for _ in range(3):
#                 response = await client.get(f"{base_url}/{name}", timeout=5.0)

#                 if response.status_code == 429:
#                     await asyncio.sleep(2)
#                     continue

#                 if response.status_code != 200:
#                     await asyncio.sleep(1)
#                     continue

#                 decoded = response.json()

#                 if not decoded:
#                     raise Exception("No data found")

#                 return {
#                     "name": decoded["login"],
#                     "public_repos": decoded["public_repos"],
#                     "followers": decoded["followers"],
#                     "following": decoded["following"],
#                     "created_at": decoded["created_at"]
#                 }

#         except httpx.RequestError as exc:
#             print(f"Connection error: {exc}. Retrying...")
#             await asyncio.sleep(1)

# async def get_github_repo_stat(name: str) -> dict:
#     async with httpx.AsyncClient() as client:
#         try:
#             for _ in range(3):
#                 response = await client.get(f"{base_url}/{name}/repos", timeout=5.0)

#                 if response.status_code == 429:
#                     await asyncio.sleep(2)
#                     continue

#                 if response.status_code != 200:
#                     await asyncio.sleep(1)
#                     continue

#                 decoded = response.json()

#                 if not decoded:
#                     raise Exception("No data found")

#                 total_repos = len(decoded)
#                 most_starred_repo = max(
#                     decoded, key=lambda x: x["stargazers_count"])
#                 return {
#                     "total_repos": total_repos,
#                     "most_starred_repo": most_starred_repo["name"]
#                 }
#         except httpx.RequestError as exc:
#             print(f"Connection error: {exc}. Retrying...")
#             await asyncio.sleep(1)

# async def github_user_summary(name: str) -> dict:
#     try:
#         profile, repo_stat = await asyncio.gather(
#             get_github_profile(name),
#             get_github_repo_stat(name)
#         )
#         return {**profile, **repo_stat}
#     except Exception as exc:
#         print(f"Error fetching data for user {name}: {exc}")
#         return {}

# TOOLS = [
#     {
#         "name": "get_github_profile",
#         "func": get_github_profile,
#         "description": "Fetches GitHub user profile information",
#         "parameters": {
#             "type": "object",
#             "properties": {"name": {"type": "string"}},
#             "required": ["name"]
#         }
#     },
#     {
#         "name": "get_github_repo_stat",
#         "func": get_github_repo_stat,
#         "description": "Fetches GitHub user repository statistics",
#         "parameters": {
#             "type": "object",
#             "properties": {"name": {"type": "string"}},
#             "required": ["name"]
#         }
#     },
#     {
#         "name": "github_user_summary",
#         "func": github_user_summary,
#         "description": "Fetches a summary of GitHub user profile and repository stats",
#         "parameters": {
#             "type": "object",
#             "properties": {"name": {"type": "string"}},
#             "required": ["name"]
#         }
#     }
# ]

# async def run_tool(tool_name: str, arg: dict):
#     try:
#         tool = next((t for t in TOOLS if t["name"] == tool_name), None)

#         if tool is None:
#             raise ValueError(f"Tool {tool_name} not found")

#         tool_func = tool["func"]

#         sig = inspect.signature(tool_func)
#         expected_params = list(sig.parameters.keys())
#         if set(arg.keys()) != set(expected_params):
#             raise ValueError(
#                 f"Invalid parameters. Expected {expected_params}, got {list(arg.keys())}"
#             )
        
#     except Exception as e:
#         return {
#             "error": str(e),
#             "tool": tool_name
#         }
#     return await tool_func(**arg)

# async def ask_llm(user_input: str) -> dict:
#     if "summary" in user_input:
#         name = user_input.split("summary")[1].strip()
#         return {
#             "tool": "github_user_summary",
#             "arg": {"name": name}
#         }
#     if "profile" in user_input:
#         name = user_input.split("profile")[1].strip()
#         return {
#             "tool": "get_github_profile",
#             "arg": {"name": name}
#         }
#     if "repo stats" in user_input:
#         name = user_input.split("repo stats")[1].strip()
#         return {
#             "tool": "get_github_repo_stat",
#             "arg": {"name": name}
#         }
#     return {
#         "tool": "",
#         "arg": {}
#     }

# async def main():
#     try:
#         user_input = input("Enter your query: ")
#         if user_input == "exit":
#             print("Exiting...")
#             return

#         decision = await ask_llm(user_input)

#         if "tool" in decision and "arg" in decision:
#             tool_name = decision["tool"]
#             arg = decision["arg"]

#         if tool_name and arg:
#             result = await run_tool(tool_name, arg)
#             print(result)

#     except Exception as e:
#         print(f"Error: {e}")


# asyncio.run(main())
