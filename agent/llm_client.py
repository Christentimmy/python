import httpx
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")

OPENAI_URL = "https://api.openai.com/v1/chat/completions"

async def call_llm(messages, tools):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                OPENAI_URL,
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": messages,
                    "tools": tools,
                    "max_tokens": 500,
                    "tool_choice": "auto",
                    "temperature": 0
                },
            )

            response.raise_for_status()
            return response.json()
        except httpx.RequestError as exc:
            print(f"An error occurred while requesting: {exc}")
            raise exc
        except httpx.HTTPStatusError as exc:
            print(
                f"HTTP error occurred: {exc.response.status_code} - {exc.response.text}")
            raise exc



