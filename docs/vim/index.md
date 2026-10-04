---
icon: simple/vim
---

# Vim

The modal text editor found on almost every Unix machine: switching modes,
saving and quitting, moving the cursor, editing lines, and search and replace.
Unless a task says otherwise, everything here works in both Vim and Neovim.

<div class="page-list" markdown>

- [Basics](basics.md)
  Switch modes, save and quit, undo and repeat.
- [Moving around](moving.md)
  Jump by line, word, paragraph and screen, or to a line number.

</div>

## Reading the keys

Keys are typed in Normal mode unless a task says otherwise. Commands that
start with `:` are typed in full and run with ++enter++.

- `<Esc>`, `<CR>` (Enter), `<Space>` and `<C-r>` (++ctrl+r++) name single
  keys, as in Vim's own help. A lowercase `<name>` is a placeholder.
- `[<count>]` is an optional number typed first: `3dd` deletes three lines.

A few patterns cover most of the keys:

- **A capital letter is the same command, reversed or bigger.** `o` opens a
  line below, `O` above; `p` pastes after, `P` before; `i` inserts at the
  cursor, `I` at the start of the line.
- **`^` and `$` are the regex anchors** for the start and end of a line, in
  motions and in search patterns alike.
- **`{` and `}` are the braces around a block:** a paragraph's start and end.
- **`[` points back and `]` points forward:** `[<Space>` and `]<Space>` add a
  blank line above and below.
- **Operators take a motion.** `d` (delete), `c` (change), `y` (copy) and `>`
  (indent) act on wherever a motion goes: `d$` deletes to the end of the line,
  `y}` copies to the end of the paragraph. Doubled, they act on the whole
  line: `dd`, `cc`, `yy`, `>>`.
