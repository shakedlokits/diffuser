"""Render markdown with Rich-markup-tagged CriticMarkup to the terminal."""

from rich.console import Console
from rich.markdown import Markdown, TextElement
from rich.text import Text


class _MarkupAwareTextElement(TextElement):
    """TextElement that interprets Rich markup tags in text content."""

    def on_text(self, context, text):
        if isinstance(text, str):
            styled = Text.from_markup(text)
            # Apply the current markdown style (bold, italic, etc.) as base
            current = context.current_style
            if current:
                styled.stylize(current)
            self.text.append_text(styled)
        else:
            super().on_text(context, text)


# Patch all text-bearing element types to use our markup-aware version.
# This is the documented extension point: Markdown.elements is a ClassVar dict.
_TEXT_ELEMENT_TYPES = [
    "paragraph_open",
    "heading_open",
    "list_item_open",
    "td_open",
    "th_open",
]

_original_elements = Markdown.elements.copy()


class CriticMarkdown(Markdown):
    """Markdown renderer that supports Rich markup tags in text content."""

    elements = {
        **_original_elements,
        **{
            key: type(
                f"_MarkupAware{_original_elements[key].__name__}",
                (_MarkupAwareTextElement, _original_elements[key]),
                {},
            )
            for key in _TEXT_ELEMENT_TYPES
            if key in _original_elements
        },
    }


def render(text: str, console: Console | None = None) -> None:
    """Render markdown with CriticMarkup Rich-markup annotations to the terminal."""
    if console is None:
        console = Console()
    console.print(CriticMarkdown(text))
