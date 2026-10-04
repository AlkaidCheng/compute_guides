# Editing lines

Add, delete, copy, move, join and indent whole lines, without leaving Normal
mode for longer than you need to.

## Add a line below or above

=== "Syntax"

    ```text
    o
    O
    ```

=== "Example"

    ```vim
    oprint(total)<Esc>   " add a line below and type into it
    ```

`o` opens a new line below the cursor and `O` one above, and both enter Insert
mode.

## Add a blank line

=== "Syntax"

    ```text
    [<count>]o<Esc>
    [<count>]O<Esc>
    [<count>]]<Space>
    [<count>][<Space>
    ```

=== "Example"

    ```vim
    o<Esc>           " one blank line below
    3O<Esc>          " three blank lines above
    ]<Space>         " a blank line below, cursor stays put (Neovim)
    ```

`o<Esc>` and `O<Esc>` add the line and return to Normal mode, with the cursor
on the new line. Neovim 0.11 and later also map `]<Space>` and `[<Space>`,
which add blank lines below and above and leave the cursor where it was.

??? tip "`]<Space>` and `[<Space>` in Vim"

    Vim has no such keys by default. These lines in `~/.vimrc` add them, with
    the same behaviour and counts as in Neovim:

    ```vim title="~/.vimrc"
    nnoremap <silent> ]<Space> :<C-u>put =repeat(nr2char(10), v:count1)<CR>'[k
    nnoremap <silent> [<Space> :<C-u>put! =repeat(nr2char(10), v:count1)<CR>']j
    ```

## Delete lines

=== "Syntax"

    ```text
    [<count>]dd
    D
    :<from>,<to>d
    ```

=== "Example"

    ```vim
    dd               " delete this line
    5dd              " delete this line and the four below
    D                " delete from the cursor to the end of the line
    :10,20d          " delete lines 10 to 20
    ```

`dd` deletes the current line, and a count deletes that many lines starting
with it. `D` deletes from the cursor to the end of the line, and
`:<from>,<to>d` deletes a range of lines by number. `dG` deletes to the end of
the file and `dgg` to the start; `cc` empties the line and enters Insert mode
to retype it.

Deleted text is kept, so `p` pastes it back elsewhere: deleting is cutting.

## Copy and paste lines

=== "Syntax"

    ```text
    [<count>]yy
    [<count>]p
    [<count>]P
    ```

=== "Example"

    ```vim
    yy               " copy this line
    3yy              " copy this line and the two below
    p                " paste below the cursor's line
    P                " paste above it
    ```

`yy` copies the current line, and a count copies that many lines starting
with it; `y` is *yank*, Vim's word for copy. `p` and `P` paste whatever was
last yanked or deleted: whole lines go below or above the cursor's line, a
part of a line after or before the cursor. A count pastes that many copies. In Visual mode, `y` copies the selection
and `d` cuts it.

## Copy to the system clipboard

=== "Syntax"

    ```text
    "+y<motion>
    "+p
    ```

=== "Example"

    ```vim
    "+yy             " copy this line to the clipboard
    gg"+yG           " copy the whole file
    "+p              " paste from the clipboard
    ```

Vim keeps copied text in its own registers; `"+` names the system clipboard
instead. In Visual mode, select and press `"+y`. Check that it is available
with `:echo has('clipboard')`, which prints `1`:

- **macOS:** the system Vim includes it.
- **Linux:** install a Vim built with it, such as the `vim-gtk3` package on
  Debian and Ubuntu.
- **Neovim:** uses a clipboard tool, which macOS includes; on Linux, install
  `wl-clipboard` or `xclip`.

`set clipboard=unnamedplus` in your config makes every `y`, `d` and `p` use
the clipboard.

## Duplicate a line

=== "Syntax"

    ```text
    yyp
    :t.
    ```

=== "Example"

    ```vim
    yyp              " copy the line and paste it below
    :t.              " the same, without touching the copied text
    ```

`yyp` copies the line and pastes the copy below it. `:t.` does the same as
one command: `:t` copies lines to below a target line, and `.` is the current
line. Unlike `yyp`, it leaves the last copied text unchanged, so a later `p`
still pastes it.

## Move a line up or down

=== "Syntax"

    ```text
    :m <target>
    ```

=== "Example"

    ```vim
    :m +1            " down one line
    :m -2            " up one line
    :m 0             " to the top of the file
    :m $             " to the bottom
    ddp              " down one line, the quick way
    ```

`:m` moves the line to just *below* the target: a line number, or an offset
from the current line. That is why moving up one line targets two lines up
(`-2`), and the top of the file is `0`. To move several lines, select them with
`V` and run `:m '>+1` (down) or `:m '<-2` (up); Vim fills in the selection
range.

`ddp` cuts the line and pastes it below the next one. Its counterpart for
moving up, `ddkP`, moves the last line of the file up two lines, so use `:m`
there.

??? tip "Move lines with `]e` and `[e`"

    These lines in `~/.vimrc` (or `init.vim`) move the line, or the selected
    lines, down with `]e` and up with `[e`. They re-indent the moved lines; in
    Normal mode they take a count, and in Visual mode they keep the selection,
    so the key can be pressed again:

    ```vim title="~/.vimrc"
    nnoremap <silent> ]e :<C-u>execute 'move +' . v:count1<CR>==
    nnoremap <silent> [e :<C-u>execute 'move -' . (v:count1 + 1)<CR>==
    xnoremap <silent> ]e :move '>+1<CR>gv=gv
    xnoremap <silent> [e :move '<-2<CR>gv=gv
    ```

## Join lines

=== "Syntax"

    ```text
    [<count>]J
    [<count>]gJ
    ```

=== "Example"

    ```vim
    J                " join the next line onto this one
    4J               " join four lines into one
    ```

`J` replaces the line break and the next line's indentation with one space.
`gJ` joins without adding or removing any spaces.

## Indent lines

=== "Syntax"

    ```text
    [<count>]>>
    [<count>]<<
    [<count>]==
    ```

=== "Example"

    ```vim
    >>               " indent this line one level
    3<<              " unindent this line and the two below
    gg=G             " re-indent the whole file
    ```

`>>` shifts the current line one level right and `<<` one level left; a
count shifts that many lines. `==` re-indents the line using the indent rules
of the file's type, and `gg=G` re-indents the whole file. In Visual mode, `>`,
`<` and `=` act on the selected lines. One level is set by `shiftwidth`, for
example `:set shiftwidth=4`.

## Change case

=== "Syntax"

    ```text
    ~
    gU<motion>  gu<motion>  g~<motion>
    ```

=== "Example"

    ```vim
    gUiw             " make the word upper case
    guu              " make the line lower case
    ```

| Keys | Does |
|---|---|
| `~` | swap the case of the character under the cursor and move on |
| `gUiw` / `guiw` | make the word upper / lower case |
| `gUU` / `guu` | make the line upper / lower case |
| `g~~` | swap the case of every character on the line |

`gU` and `gu` take a motion like any operator: `gU$` uppercases to the end of
the line. In Visual mode, `U` and `u` change the selection.
