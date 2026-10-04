# Moving around

Move the cursor in Normal mode: within a line, by word and paragraph, across
the file and back to where you were.

## Jump to the start or end of a line

=== "Syntax"

    ```text
    0  ^  $  g_
    ```

=== "Example"

    ```text
        total = total + 1;---
    ^   ^                ^  ^
    0   ^                g_ $
    ```

In the Example view, `-` marks a trailing space, as `:set list` shows it in
Neovim.

| Key | Moves to |
|---|---|
| `0` | column 0, before any indentation |
| `^` | the first non-blank character |
| `$` | the last character |
| `g_` | the last non-blank character, before trailing spaces |

`I` and `A` jump to the start and end of the line and enter Insert mode.

## Move by word

=== "Syntax"

    ```text
    [<count>]w  b  e
    [<count>]W  B  E
    ```

=== "Example"

    ```text
    out = os.path.join(root, name)
    ^   ^ ^ ^^   ^^   ^^   ^ ^   ^   w
    ^   ^ ^                  ^       W
    ```

`w` and `b` move to the start of the next and previous word, `e` to the end of
the word. A word is a run of letters, digits and `_`, or a run of
punctuation. The capital forms move by whitespace-separated runs instead,
which skips over dots and brackets in one step.

## Jump to a character on the line

=== "Syntax"

    ```text
    f<char>  F<char>
    t<char>  T<char>
    ;  ,
    ```

=== "Example"

    ```vim
    f(               " to the next ( on the line
    dt,              " delete up to, not including, the next comma
    ```

`f` lands on the character and `t` just before it; the capitals search
backwards. `;` repeats the last `f`/`t` search and `,` repeats it in the other
direction.

## Jump to the start or end of a paragraph

=== "Syntax"

    ```text
    [<count>]{
    [<count>]}
    ```

=== "Example"

    ```vim
    }                " to the blank line after this paragraph
    3{               " back three paragraphs
    ```

A paragraph is a block of lines between blank lines. `{` and `}` stop on the
blank line before and after it, or on the first or last line of the file.
`dap` deletes the whole paragraph and the blank line after it.

## Go to a line or the end of the file

=== "Syntax"

    ```text
    gg
    G
    <line>G
    :<line>
    ```

=== "Example"

    ```vim
    gg               " first line
    G                " last line
    42G              " line 42
    :42              " line 42
    ```

`gg` goes to the first line and `G` to the last. With a line number, both
`<line>G` and `:<line>` go to that line. ++ctrl+g++ shows the current line
number and the file's length, and `:set number` shows line numbers in the
margin.

## Scroll the screen

=== "Syntax"

    ```text
    <C-d>  <C-u>
    <C-f>  <C-b>
    zz  zt  zb
    H  M  L
    ```

=== "Example"

    ```vim
    <C-d>            " half a screen down
    zz               " center the cursor's line on the screen
    ```

| Key | Does |
|---|---|
| ++ctrl+d++ / ++ctrl+u++ | scroll down / up half a screen |
| ++ctrl+f++ / ++ctrl+b++ | scroll down / up a full screen |
| `zz` | put the cursor's line in the middle of the screen |
| `zt` / `zb` | put it at the top / bottom |
| `H` / `M` / `L` | move the cursor to the top / middle / bottom of the screen |

## Jump to the matching bracket

=== "Syntax"

    ```text
    %
    ```

=== "Example"

    ```vim
    %                " from ( to its ), or back
    d%               " delete from here to the matching bracket
    ```

Works on `()`, `[]` and `{}`. If the cursor is not on a bracket, `%` jumps
from the next one on the line.

## Jump back to where you were

=== "Syntax"

    ```text
    [<count>]<C-o>
    [<count>]<C-i>
    ```

=== "Example"

    ```vim
    G                " jump to the end of the file
    <C-o>            " and back again
    ```

Vim records each jump: `gg`, `G`, searches, `%`, `{`, `}` and line numbers,
but not single-line moves. ++ctrl+o++ steps back through them and ++ctrl+i++
(or ++tab++) forward. `` `. `` goes to the position of the last change.
