```
██████╗ ██╗███████╗███████╗██╗   ██╗███████╗███████╗██████╗ 
██╔══██╗██║██╔════╝██╔════╝██║   ██║██╔════╝██╔════╝██╔══██╗
██║  ██║██║█████╗  █████╗  ██║   ██║███████╗█████╗  ██████╔╝
██║  ██║██║██╔══╝  ██╔══╝  ██║   ██║╚════██║██╔══╝  ██╔══██╗
██████╔╝██║██║     ██║     ╚██████╔╝███████║███████╗██║  ██║
╚═════╝ ╚═╝╚═╝     ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝ 
```

CriticMarkup viewer for the terminal.

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
back to~~} the user.
```

Render it in the terminal with color-coded annotations:

```bash
diffuser view my-document.md
```

## Background & Rationale

Writing blog posts in markdown is straightforward until you start editing.
You change a sentence, rewrite a paragraph, cut a section. The next morning,
you're not sure what you changed or why. Git solves this for code, but
version control for prose is a different problem. You don't want branches
and merge conflicts for a blog post. You want to see what changed, right
there in the text.

Fletcher Penney saw this clearly. Penney is the creator of
[MultiMarkdown](https://fletcherpenney.net/multimarkdown/). He has spent
years building tools for writers who think in plain text. Together with Gabe
Weatherhead, he created [CriticMarkup](http://criticmarkup.com): five
simple inline annotations that track changes without leaving the document.
`{++add this++}`, `{--remove this--}`, `{~~old~>new~~}`. No external
tooling. No version control. Just the text.

The idea was brilliant. I just needed it in the terminal. That's diffuser.

## How It Works

diffuser preprocesses CriticMarkup syntax into Rich markup, then delegates
all markdown rendering to the `rich` library. No custom HTML parser, no
browser. Just your terminal.

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

### Releasing

```bash
git tag v0.1.0
git push origin v0.1.0
```

## Credits

CriticMarkup was created by [Fletcher Penney](https://fletcherpenney.net/)
and [Gabe Weatherhead](http://macdrifter.com). Full specification at
[criticmarkup.com](http://criticmarkup.com/spec.php).
