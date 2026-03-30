```

     ██████  ██ ████████ ████████ ██    ██ ▄█████ ████████ ██████
     ██   ██ ██ ██       ██       ██    ██ ▀▀▀▄▄▄ ██       ██   ██
     ██   ██ ██ ██████   ██████   ██    ██ █████▀ ██████   ██████
     ██   ██ ██ ██       ██       ██    ██       █ ██       ██  ██
     ██████  ██ ██       ██        ██████  ██████▀ ████████ ██   ██

```

CriticMarkup-aware markdown viewer for the terminal.

## Getting Started

### Installation

```bash
pip install diffuser-cli
```

Or with uv:

```bash
uv tool install diffuser-cli
```

### Quick Example

Given a markdown file with CriticMarkup annotations:

```markdown
The system processed the data and {~~returned results to~>delivered results
back to~~} the user.{>>"Delivered back" is more active and specific.<<}
```

Render it in the terminal with color-coded annotations:

```bash
diffuser view my-document.md
```

## Background & Rationale

When AI agents suggest changes to writing, they typically rewrite the whole
file. The original is gone. If you disagree with one sentence, tough luck --
you're diffing walls of prose in a terminal.

CriticMarkup solves this. It's a plain-text syntax for editorial annotations
that sits inside the document without destroying what was already there.
`{++add this++}`, `{--remove this--}`, `{~~old~>new~~}` -- five simple
marks that let an agent suggest changes while preserving every word of the
original.

What was missing was a way to view these annotations clearly from the
command line. Rich terminal rendering, color-coded by change type, without
leaving the shell. That's what diffuser does.

## How It Works

diffuser preprocesses CriticMarkup syntax into Rich markup, then delegates
all markdown rendering to the `rich` library. No custom HTML parser, no
browser -- just your terminal.

### CriticMarkup Syntax

| Syntax | Meaning |
|---|---|
| `{++text++}` | Insertion |
| `{--text--}` | Deletion |
| `{~~old~>new~~}` | Substitution |
| `{==text==}` | Highlight |
| `{>>text<<}` | Comment |

Full specification: http://criticmarkup.com/spec.php

## Agent Skill

diffuser ships with a skill that teaches AI agents how to use CriticMarkup
when editing your writing. Install it with the [skills CLI](https://skills.sh):

```bash
npx skills add shakedlokits/diffuser
```

Or view the skill content directly:

```bash
diffuser skill
```

The skill instructs the agent to annotate files in-place using CriticMarkup
syntax, never deleting or replacing original text directly.

## Development

### Setup

```bash
git clone https://github.com/shakedlokits/diffuser.git
cd diffuser
uv sync
```

### Running

```bash
uv run diffuser view my-document.md
```

### Running Tests

```bash
uv run pytest
```
