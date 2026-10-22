# Compute Guides

Quick-reference guides for everyday computing: the commands, flags and idioms
that are easy to forget between projects, organized by tool for fast lookup.

**Read the guides at <https://alkaidcheng.github.io/compute_guides/>.**

## Topics

- **Unix command line**: files, text processing, processes, archives and remote machines.
- **Bash**: expansions, quoting, redirection, control flow and scripting idioms.
- **Git**: everyday workflow, branching, history rewriting and recovery.
- **Vim**: modes, moving around, editing lines, and search and replace.

## Building locally

The site is generated from Markdown by `build.py`, which needs Python 3.10 or
later and the packages in `requirements.txt`.

```bash
pip install -r requirements.txt
python3 build.py
python3 -m http.server --directory site 8000
```

Then open <http://127.0.0.1:8000/>. The build fails on a broken link or
anchor, a page missing from `site.yaml`, and an absolute or unrecognized link.

## Adding a page

1. Write the page as Markdown in its topic's directory under `docs/`, starting
   with a YAML front matter block that gives its `title` and a one-line
   `summary` for the contents lists. The first paragraph is shown as the
   page's introduction.
2. Add the file name to the topic's `pages` list in `site.yaml`.

A new topic is a new directory with an `index.md` (front matter `title` and
`icon`, one of the names in `theme/icons/`) and an entry in `site.yaml`.

Every pull request is built by CI, and each push to `main` is deployed to
GitHub Pages.

## License

[MIT](LICENSE). Topic icons are from [Material Design
Icons](https://pictogrammers.com/library/mdi/) (Apache 2.0) and [Simple
Icons](https://simpleicons.org/) (CC0).

Developed with the assistance of Claude Code.
