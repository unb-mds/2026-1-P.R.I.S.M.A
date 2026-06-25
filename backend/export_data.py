import os
import json
import requests
from datetime import datetime
from urllib.parse import quote

TOKEN = os.getenv('PRISMA_GITHUB_TOKEN')
REPO = "unb-mds/2026-1-P.R.I.S.M.A"
BASE_URL = f"https://api.github.com/repos/{REPO}"
HEADERS = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json"}

# MÓDULO DE EXCLUSÃO DE USUÁRIOS

EXCLUDED_USERS = [
    "github-actions[bot]",
    "dependabot[bot]",
    "github-actions",
    "login",
]

def fetch_all_pages(endpoint):
    all_data = []
    page = 1
    while True:
        separator = '&' if '?' in endpoint else '?'
        url = f"{BASE_URL}/{endpoint}{separator}per_page=100&page={page}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            break
        data = response.json()
        if not data:
            break
        all_data.extend(data)
        if len(data) < 100 or page > 50:
            break
        page += 1
    return all_data

def main():
    print("Iniciando extração purificada de dados do PRISMA...")
    
    # 1. Busca as branches
    branches = fetch_all_pages("branches")
    
    # 2. Busca e filtra commits
    all_commits_raw = []
    for branch in branches:
        branch_name = quote(branch['name'])
        commits = fetch_all_pages(f"commits?sha={branch_name}")
        all_commits_raw.extend(commits)
        
    unique_commits = {}
    for c in all_commits_raw:
        if 'sha' in c:
            # Aplica o filtro do Módulo de Exclusão
            author_login = c.get('author', {}).get('login') if c.get('author') else None
            if author_login in EXCLUDED_USERS:
                continue
            unique_commits[c['sha']] = c

    all_commits = sorted(list(unique_commits.values()), key=lambda x: x['commit']['author']['date'], reverse=True)
    
    # 3. Busca e filtra Issues
    all_issues_raw = fetch_all_pages("issues?state=all")
    issues = []
    for i in all_issues_raw:
        # Ignorar Pull Requests (o GitHub trata PRs como Issues na API de issues)
        if 'pull_request' in i:
            continue
        user_login = i.get('user', {}).get('login')
        if user_login in EXCLUDED_USERS:
            continue
        issues.append(i)
    
    # 4. Monta o pacote final com metadados reais
    data_package = {
        "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "raw_commits": all_commits,
        "raw_issues": issues
    }
    
    output_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dados.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data_package, f, ensure_ascii=False)
        
    print(f"Sucesso! {len(all_commits)} commits limpos e {len(issues)} issues salvas.")

if __name__ == "__main__":
    main()