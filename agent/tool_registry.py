

from agent.github_tools import get_github_profile, get_github_repo_stat, github_user_summary

TOOLS = [
    {
        "name": "get_github_profile",
        "func": get_github_profile,
        "description": "Fetches GitHub user profile information",
        "parameters": {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"]
        }
    },
    {
        "name": "get_github_repo_stat",
        "func": get_github_repo_stat,
        "description": "Fetches GitHub user repository statistics",
        "parameters": {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"]
        }
    },
    {
        "name": "github_user_summary",
        "func": github_user_summary,
        "description": "Fetches a summary of GitHub user profile and repository stats",
        "parameters": {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"]
        }
    }
]
