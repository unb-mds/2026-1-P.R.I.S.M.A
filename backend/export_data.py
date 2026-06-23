import os
import json
import requests
from urllib.parse import quote

# Puxa o token injetado pelo GitHub Actions com segurança
TOKEN = os.getenv('PRISMA_GITHUB_TOKEN')
REPO = "unb-mds/2026-1-P.R.I.S.M.A"
BASE_URL = f"https://api.github.com/repos/{REPO}"
HEADERS = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json"}

def fetch_all_pages(endpoint):
    all_data = []
    page = 1
    while True:
        separator = '&' if '?' in endpoint else '?'
        url = f"{BASE_URL}/{endpoint}{separator}per_page=100&page={page}"
        
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Erro ao acessar {url}: {response.status_code}")
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
    print("Iniciando extração de dados do Prisma...")
    
    # 1. Puxa branches
    branches = fetch_all_pages("branches")
    
    # 2. Puxa commits de cada branch
    all_commits_raw = []
    for branch in branches:
        branch_name = quote(branch['name'])
        print(f"Buscando commits da branch: {branch['name']}")
        commits = fetch_all_pages(f"commits?sha={branch_name}")
        all_commits_raw.extend(commits)
        
    # 3. Remove duplicatas
    unique_commits = {c['sha']: c for c in all_commits_raw if 'sha' in c}
    all_commits = sorted(list(unique_commits.values()), key=lambda x: x['commit']['author']['date'], reverse=True)
    
    # 4. Puxa Issues
    print("Buscando issues...")
    issues = fetch_all_pages("issues?state=all")
    
    # 5. Monta o pacote final
    data_package = {
        "raw_commits": all_commits,
        "raw_issues": issues
    }
    
    # 6. Salva o JSON direto na pasta do frontend
    output_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dados.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data_package, f, ensure_ascii=False)
        
    print(f"Sucesso! {len(all_commits)} commits e {len(issues)} issues salvos em dados.json")

if __name__ == "__main__":
    main()