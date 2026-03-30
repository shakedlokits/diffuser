"""Read the SKILL.md file for CriticMarkup agent instructions."""

from importlib.resources import files
from pathlib import Path


def get_skill_content() -> str:
    """Read and return the SKILL.md content from the package.

    In an installed wheel, SKILL.md is force-included into the package
    by hatchling. In editable/dev mode, it lives at the repo root under
    skills/diffuser/SKILL.md.
    """
    # Installed wheel: SKILL.md is inside the package
    pkg_path = files("diffuser").joinpath("SKILL.md")
    try:
        return pkg_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        pass

    # Editable/dev mode: resolve from the repo root
    repo_path = (
        Path(__file__).resolve().parent.parent.parent
        / "skills"
        / "diffuser"
        / "SKILL.md"
    )
    return repo_path.read_text(encoding="utf-8")
