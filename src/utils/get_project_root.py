import os
from pathlib import Path

def get_project_root():
    current = Path.cwd()
    
    for parent in [current]+list(current.parents):
        if (parent/".git").exists() or (parent/"requirements.txt").exists() or (parent/"pyproject.toml").exists():
            return parent
    return current