# backend/services/github_service.py
import requests
from fastapi import HTTPException
from config import settings


class GitHubService:
    BASE_URL = "https://api.github.com/repos"

    @staticmethod
    def get_headers():
        if not settings.GITHUB_TOKEN:
            raise HTTPException(
                status_code=500, detail="GITHUB_TOKEN não configurado no backend."
            )
        return {
            "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
        }

    @staticmethod
    def fetch_commits():
        url = f"{GitHubService.BASE_URL}/{settings.PROJECT_OWNER}/{settings.PROJECT_REPO}/commits"

        response = requests.get(
            f"{url}?per_page=100", headers=GitHubService.get_headers()
        )

        if response.status_code == 401:
            raise HTTPException(
                status_code=401, detail="Token do GitHub inválido no .env."
            )
        elif response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Erro ao buscar commits no repositório.",
            )

        return response.json()

    @staticmethod
    def fetch_issues():
        url = f"{GitHubService.BASE_URL}/{settings.PROJECT_OWNER}/{settings.PROJECT_REPO}/issues"

        response = requests.get(
            f"{url}?state=all&per_page=100", headers=GitHubService.get_headers()
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail="Erro ao buscar issues."
            )

        return response.json()
