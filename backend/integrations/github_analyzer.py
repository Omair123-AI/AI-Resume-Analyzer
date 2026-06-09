"""
github_analyzer.py - Analyze a GitHub profile via GitHub REST API
"""
import os
import re
import requests
from utils.helpers import normalize_score


GITHUB_API = "https://api.github.com"


def analyze_github(profile_url: str) -> dict:
    username = _extract_username(profile_url)
    if not username:
        return {"error": "Invalid GitHub URL. Expected: https://github.com/username"}

    headers = _get_headers()

    user    = _fetch_user(username, headers)
    if "error" in user:
        return user

    repos   = _fetch_repos(username, headers)
    langs   = _aggregate_languages(repos)
    stats   = _compute_stats(repos)
    score   = _calculate_score(user, repos, stats)

    return {
        "username":         username,
        "name":             user.get("name", username),
        "bio":              user.get("bio", ""),
        "public_repos":     user.get("public_repos", 0),
        "followers":        user.get("followers", 0),
        "following":        user.get("following", 0),
        "profile_url":      profile_url,
        "avatar_url":       user.get("avatar_url", ""),
        "top_languages":    langs,
        "stats":            stats,
        "score":            score["total"],
        "score_breakdown":  score["breakdown"],
        "score_label":      score["label"],
        "top_repos":        _format_top_repos(repos),
        "suggestions":      _generate_suggestions(user, repos, stats),
    }


def _extract_username(url: str) -> str | None:
    m = re.search(r"github\.com/([a-zA-Z0-9\-]+)/?$", url)
    return m.group(1) if m else None


def _get_headers() -> dict:
    token = os.getenv("GITHUB_TOKEN", "")
    h = {"Accept": "application/vnd.github.v3+json"}
    if token and token != "your-github-personal-access-token":
        h["Authorization"] = f"token {token}"
    return h


def _fetch_user(username: str, headers: dict) -> dict:
    try:
        resp = requests.get(f"{GITHUB_API}/users/{username}", headers=headers, timeout=10)
        if resp.status_code == 404:
            return {"error": f"GitHub user '{username}' not found."}
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


def _fetch_repos(username: str, headers: dict, per_page: int = 50) -> list:
    try:
        resp = requests.get(
            f"{GITHUB_API}/users/{username}/repos",
            headers=headers,
            params={"per_page": per_page, "sort": "updated"},
            timeout=10
        )
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return []


def _aggregate_languages(repos: list) -> list[dict]:
    lang_stars = {}
    for repo in repos:
        lang = repo.get("language")
        if lang:
            lang_stars[lang] = lang_stars.get(lang, 0) + repo.get("stargazers_count", 0) + 1
    sorted_langs = sorted(lang_stars.items(), key=lambda x: x[1], reverse=True)
    return [{"language": l, "weight": w} for l, w in sorted_langs[:8]]


def _compute_stats(repos: list) -> dict:
    total_stars   = sum(r.get("stargazers_count", 0) for r in repos)
    total_forks   = sum(r.get("forks_count", 0) for r in repos)
    total_commits = 0  # Requires per-repo API calls; skip for rate limit
    has_readme    = sum(1 for r in repos if not r.get("fork") and r.get("description"))
    forked        = sum(1 for r in repos if r.get("fork"))
    original      = len(repos) - forked

    return {
        "total_repos":    len(repos),
        "original_repos": original,
        "forked_repos":   forked,
        "total_stars":    total_stars,
        "total_forks":    total_forks,
        "repos_with_desc": has_readme,
    }


def _calculate_score(user: dict, repos: list, stats: dict) -> dict:
    breakdown = {}

    # Repos (25pts)
    breakdown["repositories"] = min(stats["original_repos"] / 10 * 25, 25)

    # Stars (20pts)
    breakdown["stars"] = min(stats["total_stars"] / 20 * 20, 20)

    # Followers (15pts)
    breakdown["followers"] = min(user.get("followers", 0) / 50 * 15, 15)

    # Language diversity (20pts)
    # Get from top_languages count
    lang_count = len(_aggregate_languages(repos))
    breakdown["language_diversity"] = min(lang_count / 5 * 20, 20)

    # Profile completeness (20pts)
    completeness = 0
    if user.get("name"):       completeness += 5
    if user.get("bio"):        completeness += 5
    if user.get("location"):   completeness += 5
    if user.get("email"):      completeness += 5
    breakdown["profile_completeness"] = completeness

    total = sum(breakdown.values())
    total = normalize_score(total)

    label = ("Excellent" if total >= 80 else
             "Good"      if total >= 60 else
             "Average"   if total >= 40 else "Needs Work")

    return {
        "total":     round(total, 1),
        "breakdown": {k: round(v, 1) for k, v in breakdown.items()},
        "label":     label,
    }


def _format_top_repos(repos: list, top_n: int = 5) -> list[dict]:
    original = [r for r in repos if not r.get("fork")]
    sorted_r = sorted(original, key=lambda r: r.get("stargazers_count", 0), reverse=True)
    return [
        {
            "name":        r.get("name", ""),
            "description": r.get("description", ""),
            "language":    r.get("language", ""),
            "stars":       r.get("stargazers_count", 0),
            "forks":       r.get("forks_count", 0),
            "url":         r.get("html_url", ""),
            "updated_at":  r.get("updated_at", "")[:10],
        }
        for r in sorted_r[:top_n]
    ]


def _generate_suggestions(user: dict, repos: list, stats: dict) -> list[str]:
    suggestions = []
    if not user.get("bio"):
        suggestions.append("Add a bio to your GitHub profile.")
    if not user.get("location"):
        suggestions.append("Add your location to increase visibility.")
    if stats["repos_with_desc"] < stats["original_repos"] // 2:
        suggestions.append("Add descriptions to your repositories.")
    if stats["original_repos"] < 5:
        suggestions.append("Create more original repositories to showcase your skills.")
    if stats["total_stars"] == 0:
        suggestions.append("Promote your projects to earn stars and increase credibility.")
    if not user.get("email"):
        suggestions.append("Add a public email for networking opportunities.")
    return suggestions or ["Your GitHub profile is well maintained. Keep contributing!"]
