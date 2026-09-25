# Compute Guides

Quick-reference guides for everyday computing: the commands, flags and idioms
that are easy to forget between projects, organized by tool for fast lookup.

**Read the guides at <https://alkaidcheng.github.io/compute_guides/>.**

## Topics

- **Unix command line**: files, text processing, processes, archives and remote machines.
- **Bash**: expansions, quoting, redirection, control flow and scripting idioms.
- **Git**: everyday workflow, branching, history rewriting and recovery.

## Building locally

The site is built with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

```bash
pip install -r requirements.txt
mkdocs serve
```

Then open <http://127.0.0.1:8000/compute_guides/>; the page reloads as you edit.
`mkdocs build --strict` runs the same check as CI and fails on broken links or
pages missing from the navigation.

## Adding a page

1. Write the page as Markdown in its topic's directory under `docs/`. A new
   topic is a new directory with an `index.md` landing page.
2. Add the page to `nav` in `mkdocs.yml`.
3. Link it from the topic's `index.md`.

Every pull request is built with `--strict`, and each push to `main` is
deployed to GitHub Pages.

## License

[MIT](LICENSE)

Developed with the assistance of Claude Code.
