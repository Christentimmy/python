import asyncio
import httpx
from datetime import datetime

base_url = "https://api.github.com/users"


async def get_github_user(name: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/{name}")
        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch user data: {response.status_code}")
        decoded = response.json()
        created_at = datetime.fromisoformat(decoded["created_at"].rstrip("Z"))
        formatted = datetime.strftime(created_at,"%d %b %Y")
        return {
            "name": decoded["name"],
            "public_repos": decoded["public_repos"],
            "followers": decoded["followers"],
            "following": decoded["following"],
            "created_at": formatted
        }


res = asyncio.run(get_github_user("Christentimmy"))
print(res)
