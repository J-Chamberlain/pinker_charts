from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests

from .config import GitHubConfig


@dataclass
class GitHubClient:
    config: GitHubConfig

    def _headers(self) -> dict[str, str]:
        if not self.config.token:
            raise RuntimeError(f"Missing GitHub token in {self.config.token_env}")
        return {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.config.token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def create_issue(self, title: str, body: str, labels: tuple[str, ...] = (), assignees: tuple[str, ...] = ()) -> dict[str, Any]:
        url = f"{self.config.api_url}/repos/{self.config.owner}/{self.config.repo}/issues"
        payload: dict[str, Any] = {"title": title, "body": body}
        if labels:
            payload["labels"] = list(labels)
        if assignees:
            payload["assignees"] = list(assignees)
        response = requests.post(url, headers=self._headers(), json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
