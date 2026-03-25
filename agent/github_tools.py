
import asyncio
import httpx
import inspect

base_url = "https://api.github.com/users"


async def get_github_profile(name: str) -> dict:
    async with httpx.AsyncClient() as client:
        try:
            for _ in range(3):
                response = await client.get(f"{base_url}/{name}", timeout=5.0)

                if response.status_code == 429:
                    await asyncio.sleep(2)
                    continue

                if response.status_code != 200:
                    await asyncio.sleep(1)
                    continue

                decoded = response.json()

                if not decoded:
                    raise Exception("No data found")

                return {
                    "name": decoded["login"],
                    "public_repos": decoded["public_repos"],
                    "followers": decoded["followers"],
                    "following": decoded["following"],
                    "created_at": decoded["created_at"]
                }

        except httpx.RequestError as exc:
            print(f"Connection error: {exc}. Retrying...")
            await asyncio.sleep(1)


async def get_github_repo_stat(name: str) -> dict:
    async with httpx.AsyncClient() as client:
        try:
            for _ in range(3):
                response = await client.get(f"{base_url}/{name}/repos", timeout=5.0)

                if response.status_code == 429:
                    await asyncio.sleep(2)
                    continue

                if response.status_code != 200:
                    await asyncio.sleep(1)
                    continue

                decoded = response.json()

                if not decoded:
                    raise Exception("No data found")

                total_repos = len(decoded)
                most_starred_repo = max(
                    decoded, key=lambda x: x["stargazers_count"])
                return {
                    "total_repos": total_repos,
                    "most_starred_repo": most_starred_repo["name"]
                }
        except httpx.RequestError as exc:
            print(f"Connection error: {exc}. Retrying...")
            await asyncio.sleep(1)


async def github_user_summary(name: str) -> dict:
    try:
        profile, repo_stat = await asyncio.gather(
            get_github_profile(name),
            get_github_repo_stat(name)
        )
        return {**profile, **repo_stat}
    except Exception as exc:
        print(f"Error fetching data for user {name}: {exc}")
        return {}


async def run_tool(tool_name: str, arg: dict):
    from agent.tool_registry import TOOLS
    try:
        tool = next((t for t in TOOLS if t["name"] == tool_name), None)

        if tool is None:
            raise ValueError(f"Tool {tool_name} not found")

        tool_func = tool["func"]
        # print(f"Func ${tool_func}")

        sig = inspect.signature(tool_func)
        expected_params = list(sig.parameters.keys())
        if set(arg.keys()) != set(expected_params):
            raise ValueError(
                f"Invalid parameters. Expected {expected_params}, got {list(arg.keys())}"
            )

    except Exception as e:
        print(e)
        return {
            "error": str(e),
            "tool": tool_name
        }

    return await tool_func(**arg)
