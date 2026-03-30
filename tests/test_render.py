"""Tests for diffuser.render -- CriticMarkup-aware markdown rendering."""

from rich.console import Console

from diffuser.parse import prepare
from diffuser.render import CriticMarkdown


def _render_to_text(markdown_source: str, width: int = 80) -> str:
    """Render markdown through the full pipeline and capture plain text output."""
    prepared = prepare(markdown_source)
    console = Console(file=None, force_terminal=True, width=width)
    with console.capture() as capture:
        console.print(CriticMarkdown(prepared))
    return capture.get()


def _render_to_ansi(markdown_source: str, width: int = 80) -> str:
    """Render and capture raw ANSI output to verify styling."""
    prepared = prepare(markdown_source)
    console = Console(
        file=None, force_terminal=True, width=width, color_system="truecolor"
    )
    with console.capture() as capture:
        console.print(CriticMarkdown(prepared))
    return capture.get()


class TestCriticAnnotationsRender:
    def test_insertion_appears_in_output(self):
        result = _render_to_text("text {++added++} here")
        assert "added" in result

    def test_deletion_appears_in_output(self):
        result = _render_to_text("text {--removed--} here")
        assert "removed" in result

    def test_substitution_shows_both(self):
        result = _render_to_text("{~~old~>new~~}")
        assert "old" in result
        assert "new" in result

    def test_highlight_appears(self):
        result = _render_to_text("{==noted==}")
        assert "noted" in result

    def test_comment_appears(self):
        result = _render_to_text("{>>a note<<}")
        assert "a note" in result


class TestCriticAnnotationStyles:
    def test_insertion_has_green(self):
        ansi = _render_to_ansi("{++added++}")
        assert "\x1b[32m" in ansi or "\x1b[38;2;0;128;0m" in ansi or "32" in ansi

    def test_deletion_has_strikethrough(self):
        ansi = _render_to_ansi("{--removed--}")
        assert "\x1b[9" in ansi  # strikethrough ANSI code


class TestMarkdownRenderingPreserved:
    def test_heading_renders(self):
        result = _render_to_text("# Title\n\nBody text")
        assert "Title" in result
        assert "Body text" in result

    def test_bold_renders(self):
        result = _render_to_text("**bold text**")
        assert "bold text" in result

    def test_italic_renders(self):
        result = _render_to_text("*italic text*")
        assert "italic text" in result

    def test_list_renders(self):
        result = _render_to_text("- item one\n- item two")
        assert "item one" in result
        assert "item two" in result


class TestCriticWithinMarkdown:
    def test_insertion_in_paragraph(self):
        result = _render_to_text("A paragraph with {++new words++} in it.")
        assert "new words" in result
        assert "A paragraph with" in result

    def test_critic_in_heading(self):
        result = _render_to_text("# A {++great++} title")
        assert "great" in result

    def test_no_style_bleed(self):
        """Annotations should not bleed style into subsequent text."""
        ansi = _render_to_ansi("{++added++} normal text after")
        # Find where "normal" starts - it should not have green styling
        normal_idx = ansi.find("normal")
        green_before_normal = ansi.rfind("\x1b[32m", 0, normal_idx)
        reset_before_normal = ansi.rfind("\x1b[0m", 0, normal_idx)
        # If green was applied, a reset must come before "normal"
        if green_before_normal >= 0:
            assert reset_before_normal > green_before_normal
