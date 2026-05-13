import { GitHubCommit, GitHubIssue, GitHubDiff } from './types';

const REPO_OWNER = 'unb-mds';
const REPO_NAME = '2026-1-P.R.I.S.M.A';
const BASE_URL = 'https://api.github.com';

function getHeaders(): HeadersInit {
  const token = localStorage.getItem('gh_token');
  const headers: HeadersInit = {
    'Accept': 'application/vnd.github.v3+json',
  };
  if (token) {
    headers['Authorization'] = `token ${token}`;
  }
  return headers;
}

/**
 * Tenta carregar dados de um arquivo estático (para suporte a GitHub Actions)
 * ou fallbacks para a API do GitHub.
 */
async function fetchWithFallback<T>(apiPath: string, staticPath: string): Promise<T> {
  try {
    const staticRes = await fetch(staticPath);
    if (staticRes.ok) return await staticRes.json();
  } catch (e) {
    // Silently continue to API
  }

  const res = await fetch(`${BASE_URL}${apiPath}`, { headers: getHeaders() });
  if (!res.ok) {
    if (res.status === 403) {
      const rateLimit = res.headers.get('X-RateLimit-Remaining');
      if (rateLimit === '0') {
        throw new Error('Limite de taxa do GitHub atingido (60/req por hora). Insira um GitHub Token nas configurações para continuar.');
      }
    }
    throw new Error(`Erro GitHub (${res.status}): ${res.statusText}`);
  }
  return res.json();
}

export async function fetchCommits(): Promise<GitHubCommit[]> {
  return fetchWithFallback<GitHubCommit[]>(
    `/repos/${REPO_OWNER}/${REPO_NAME}/commits?per_page=100`,
    '/commits_data.json'
  );
}

export async function fetchIssues(): Promise<GitHubIssue[]> {
  return fetchWithFallback<GitHubIssue[]>(
    `/repos/${REPO_OWNER}/${REPO_NAME}/issues?state=all&per_page=100`,
    '/issues_data.json'
  );
}

export async function compareCommits(base: string, head: string): Promise<GitHubDiff> {
  const res = await fetch(`${BASE_URL}/repos/${REPO_OWNER}/${REPO_NAME}/compare/${base}...${head}`, {
    headers: getHeaders()
  });
  
  if (!res.ok) {
    if (res.status === 404) throw new Error('Um dos commits não foi encontrado ou a URL de comparação está inválida.');
    if (res.status === 403) throw new Error('Limite de taxa atingido. Use um Token nas configurações.');
    throw new Error(`Erro na comparação: ${res.statusText}`);
  }
  
  return res.json();
}

export async function fetchCommitDetail(sha: string): Promise<GitHubCommit & { files: any[] }> {
  const response = await fetch(`${BASE_URL}/repos/${REPO_OWNER}/${REPO_NAME}/commits/${sha}`);
  if (!response.ok) throw new Error('Failed to fetch commit detail');
  return response.json();
}
