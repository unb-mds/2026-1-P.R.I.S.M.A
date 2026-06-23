# backend/controllers/github_controller.py
from fastapi import APIRouter
from services.github_service import GitHubService

router = APIRouter()

@router.get("/metrics")
def get_dashboard_metrics():
    # As chamadas agora não precisam de parâmetros, o service já sabe o que fazer
    commits_data = GitHubService.fetch_commits()
    issues_data = GitHubService.fetch_issues()
    
    # Processamento e agregação básica
    open_issues = len([i for i in issues_data if i.get("state") == "open"])
    
    # Extrai e-mails únicos dos autores dos commits
    collaborators = set()
    for c in commits_data:
        if c.get("commit") and c["commit"].get("author"):
            collaborators.add(c["commit"]["author"]["email"])
    
    return {
        "status": "success",
        "data": {
            "total_commits": len(commits_data),
            "open_issues": open_issues,
            "total_issues": len(issues_data),
            "active_collaborators": len(collaborators),
            "latest_commits": commits_data[:5]
        }
    }