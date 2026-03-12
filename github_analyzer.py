import asyncio
import httpx

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
    

res = asyncio.run(github_user_summary("octocat"))
print(res)
