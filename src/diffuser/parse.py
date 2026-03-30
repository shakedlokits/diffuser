"""Convert CriticMarkup syntax to Rich markup tags in markdown text."""

import re

from rich.markup import escape


# CriticMarkup patterns → Rich markup replacements.
# Order matters: substitution must come before insertion/deletion
# since it contains both delimiter types.
_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    # Substitution: {~~old~>new~~}
    (
        re.compile(r"\{~~(.*?)~>(.*?)~~\}", re.DOTALL),
        r"[red strike]\1[/red strike][green]\2[/green]",
    ),
    # Insertion: {++text++}
    (
        re.compile(r"\{\+\+(.*?)\+\+\}", re.DOTALL),
        r"[green]\1[/green]",
    ),
    # Deletion: {--text--}
    (
        re.compile(r"\{--(.*?)--\}", re.DOTALL),
        r"[red strike]\1[/red strike]",
    ),
    # Highlight: {==text==}
    (
        re.compile(r"\{==(.*?)==\}", re.DOTALL),
        r"[on yellow black]\1[/on yellow black]",
    ),
    # Comment: {>>text<<}
    # Use unicode brackets ⸨⸩ to avoid Rich markup and markdown-it conflicts
    (
        re.compile(r"\{>>(.*?)<<\}", re.DOTALL),
        "[dim italic blue] \u2e28\\1\u2e29[/dim italic blue]",
    ),
]


def prepare(text: str) -> str:
    """Convert CriticMarkup annotations to Rich markup within markdown text.

    Escapes any existing Rich markup in the source first, then applies
    CriticMarkup-to-Rich-markup transformations. The result is markdown
    that can be rendered by a Rich-markup-aware Markdown renderer.
    """
    text = escape(text)
    for pattern, replacement in _PATTERNS:
        text = pattern.sub(replacement, text)
    return text
