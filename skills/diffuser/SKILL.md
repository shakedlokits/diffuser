---
name: diffuser
description: >-
  Add editorial suggestions to markdown files using CriticMarkup syntax.
  Use when reviewing, editing, or suggesting changes to prose and writing.
  Annotates files in-place without destroying original content.
---

# CriticMarkup Editorial Annotations

When reviewing or suggesting changes to markdown writing, use CriticMarkup
syntax to annotate the file directly. CriticMarkup is non-destructive -- the
original text is always recoverable from the annotated file.

The author previews annotations by running `diffuser <file>` in their terminal.

## Syntax Reference

Full specification: http://criticmarkup.com/spec.php

There are five markup types:

### Insertion

Suggest adding new text:

```
The quick brown fox {++jumped over the lazy dog and++} ran away.
```

### Deletion

Suggest removing text:

```
The quick {--brown--} fox ran away.
```

### Substitution

Suggest replacing text:

```
The quick brown fox {~~jumped~>leaped~~} over the lazy dog.
```

### Highlight

Call attention to a passage:

```
{==The quick brown fox==} ran away.
```

### Comment

Leave an editorial note (often paired with a highlight):

```
{==The quick brown fox==}{>>This opening feels abrupt. Consider adding
context about where the fox came from.<<}
```

## Rules

1. **Never delete or replace original text directly.** Always use CriticMarkup
   to wrap your suggestions so the author can review each change.

2. **Annotate the file in-place.** CriticMarkup preserves the original content
   within its syntax, so the source file serves as both the original and the
   annotated version.

3. **Do not modify text outside of CriticMarkup delimiters.** Whitespace,
   punctuation, and formatting outside your annotations must stay untouched.

## Example

Before your edit, the file contains:

```markdown
The system processed the data and returned results to the user.
```

After your edit:

```markdown
The system processed the data and {~~returned results to~>delivered results
back to~~} the user.
```

The author runs `diffuser <file>` to see your suggestions color-coded in their
terminal, then decides which to accept.
