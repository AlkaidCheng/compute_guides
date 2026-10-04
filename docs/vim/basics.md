# Basics

Open a file, switch between modes, save and quit, and undo or repeat a change.

## Open a file

=== "Syntax"

    ```text
    vim <file>...
    vim +<line> <file>
    vim +/<pattern> <file>
    ```

=== "Example"

    ```bash
    vim notes.txt
    vim +42 analysis.py          # open at line 42
    vim +/TODO analysis.py       # open at the first TODO
    ```

A file that does not exist yet is created when you first save. Inside Vim,
`:e <file>` opens another file.

## Switch modes

=== "Syntax"

    ```text
    i  a  I  A  o  O
    v  V  <C-v>
    :
    <Esc>
    ```

=== "Example"

    ```vim
    A;<Esc>          " append a semicolon to the end of the line
    Vjj              " select this line and the two below
    ```

Vim starts in **Normal** mode, where keys are commands. Each key below enters
another mode; ++esc++ always returns to Normal mode, so press it whenever you
are unsure where you are.

| Key | Enters | Where |
|---|---|---|
| `i` / `a` | Insert | before / after the cursor |
| `I` / `A` | Insert | at the start / end of the line |
| `o` / `O` | Insert | on a new line below / above |
| `v` | Visual | select characters |
| `V` | Visual | select whole lines |
| `<C-v>` | Visual | select a rectangular block |
| `:` | Command-line | type a command such as `:w` |

## Save and quit

=== "Syntax"

    ```text
    :w [<file>]
    :q
    :wq
    :q!
    ```

=== "Example"

    ```vim
    :w               " save
    :w backup.txt    " save a copy under another name
    :wq              " save and quit
    :q!              " quit and discard unsaved changes
    ```

`:q` refuses to quit while there are unsaved changes; `:q!` discards them.

| Command | Does |
|---|---|
| `:x` or `ZZ` | save if changed, then quit |
| `ZQ` | quit without saving, like `:q!` |
| `:wa` / `:qa` | save / quit every open file |

## Undo and redo

=== "Syntax"

    ```text
    [<count>]u
    [<count>]<C-r>
    ```

=== "Example"

    ```vim
    u                " undo the last change
    3u               " undo the last three changes
    <C-r>            " redo
    ```

Undo steps back one change at a time, where a change is one Normal-mode
command or everything typed in a single visit to Insert mode.

## Repeat the last change

=== "Syntax"

    ```text
    [<count>].
    ```

=== "Example"

    ```vim
    dd               " delete a line
    .                " delete the next one too
    3.               " and the three after it
    ```

`.` repeats the last change at the cursor: a deletion, an insertion, an
indent. Combined with `n` (next search match), it applies one edit at each
match in turn.
