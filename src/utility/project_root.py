

def get_project_root():
    """
        Returns root of the project
    """
    from pathlib import Path

    current_directory = Path.cwd()

    for parent in current_directory.parents:
        if (parent / "uv.lock").exists():
            return parent
    return current_directory







