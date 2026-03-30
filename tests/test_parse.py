"""Tests for diffuser.parse -- CriticMarkup to Rich markup conversion."""

from diffuser.parse import prepare


class TestInsertion:
    def test_simple(self):
        assert "[green]added[/green]" in prepare("text {++added++} here")

    def test_preserves_surrounding(self):
        result = prepare("before {++added++} after")
        assert result.startswith("before ")
        assert result.endswith(" after")

    def test_multiline(self):
        result = prepare("start {++line one\nline two++} end")
        assert "[green]line one\nline two[/green]" in result


class TestDeletion:
    def test_simple(self):
        assert "[red strike]removed[/red strike]" in prepare("text {--removed--} here")

    def test_preserves_surrounding(self):
        result = prepare("before {--removed--} after")
        assert result.startswith("before ")
        assert result.endswith(" after")

    def test_multiline(self):
        result = prepare("start {--line one\nline two--} end")
        assert "[red strike]line one\nline two[/red strike]" in result


class TestSubstitution:
    def test_simple(self):
        result = prepare("text {~~old~>new~~} here")
        assert "[red strike]old[/red strike]" in result
        assert "[green]new[/green]" in result

    def test_order(self):
        result = prepare("{~~old~>new~~}")
        del_pos = result.index("[red strike]")
        ins_pos = result.index("[green]")
        assert del_pos < ins_pos

    def test_multiline(self):
        result = prepare("{~~old text\nmore~>new text\nmore~~}")
        assert "[red strike]old text\nmore[/red strike]" in result
        assert "[green]new text\nmore[/green]" in result


class TestHighlight:
    def test_simple(self):
        assert "[on yellow black]noted[/on yellow black]" in prepare("{==noted==}")

    def test_with_surrounding(self):
        result = prepare("see {==this part==} closely")
        assert result.startswith("see ")
        assert "[on yellow black]this part[/on yellow black]" in result


class TestComment:
    def test_simple(self):
        result = prepare("{>>a note<<}")
        assert "[dim italic blue]" in result
        assert "a note" in result
        assert "[/dim italic blue]" in result

    def test_bracket_wrapping(self):
        result = prepare("{>>a note<<}")
        assert "\u2e28a note\u2e29" in result


class TestEscaping:
    def test_existing_rich_markup_escaped(self):
        result = prepare("text with [bold]brackets[/bold] here")
        assert "\\[bold]" in result
        assert "\\[/bold]" in result

    def test_critic_markup_not_escaped(self):
        """CriticMarkup should produce working Rich markup even after escaping."""
        result = prepare("{++added++}")
        assert "[green]added[/green]" in result


class TestMixed:
    def test_insertion_and_deletion_together(self):
        result = prepare("{--old--}{++new++}")
        assert "[red strike]old[/red strike]" in result
        assert "[green]new[/green]" in result

    def test_with_markdown(self):
        result = prepare("# Heading\n\n{++added++} and **bold**")
        assert "# Heading" in result
        assert "[green]added[/green]" in result
        assert "**bold**" in result

    def test_empty_insertion(self):
        result = prepare("{++++}")
        assert "[green][/green]" in result

    def test_empty_deletion(self):
        result = prepare("{----}")
        assert "[red strike][/red strike]" in result
