# Search and replace

Find text in the file, replace it in a line, a range or the whole file, and
act on every line that matches a pattern.

## Search for text

=== "Syntax"

    ```text
    /<pattern>
    ?<pattern>
    n  N
    *  #
    ```

=== "Example"

    ```vim
    /total           " search forward for total
    ?def             " search backward for def
    n                " next match
    N                " previous match
    ```

`/` searches forward and `?` backward; `n` repeats the search in the same
direction and `N` in the opposite one. `*` and `#` search forward and backward
for the whole word under the cursor. ++ctrl+o++ returns to where the search
started.

| Command | Does |
|---|---|
| `:set ignorecase smartcase` | ignore case, unless the pattern has a capital |
| `/total\c` | ignore case in this search only |
| `:set hlsearch` | highlight every match (on by default in Neovim) |
| `:noh` | clear the highlight until the next search |

## Replace in the whole file

=== "Syntax"

    ```text
    :%s/<pattern>/<replacement>/[<flags>]
    ```

=== "Example"

    ```vim
    :%s/colour/color/g     " every match in the file
    :%s/colour/color/gc    " every match, asking at each one
    ```

`%` is the whole file. Without `g`, only the first match on each line is
replaced. With `c`, Vim stops at each match: `y` replaces it, `n` skips it,
`a` replaces it and all the rest, and `q` stops.

| Flag | Does |
|---|---|
| `g` | replace every match on a line, not just the first |
| `c` | confirm each replacement |
| `i` | ignore case |
| `e` | no error when nothing matches |
| `n` | count the matches instead of replacing them |

## Replace in some lines

=== "Syntax"

    ```text
    :s/<pattern>/<replacement>/[<flags>]
    :<from>,<to>s/<pattern>/<replacement>/[<flags>]
    ```

=== "Example"

    ```vim
    :s/colour/color/g        " the current line only
    :10,20s/colour/color/g   " lines 10 to 20
    :.,$s/colour/color/g     " from here to the end of the file
    ```

To replace in a selection, select the lines with `V` and press `:`. Vim
fills in the range as `:'<,'>`; type `s/colour/color/g` after it.

## Match a whole word

=== "Syntax"

    ```text
    :%s/\<<word>\>/<replacement>/g
    ```

=== "Example"

    ```vim
    :%s/\<cat\>/dog/g      " cat becomes dog, but concat is left alone
    ```

`\<` and `\>` match the start and end of a word. `*` searches with them
already added.

## Replace text that contains a slash

=== "Syntax"

    ```text
    :%s#<pattern>#<replacement>#[<flags>]
    ```

=== "Example"

    ```vim
    :%s#/usr/local#/opt#g    " no need to escape each / as \/
    ```

Any punctuation character can stand in for `/` as the separator; `#` and `|`
are common choices.

## Reuse the matched text

=== "Syntax"

    ```text
    &
    \(<group>\)   \1  \2  ...
    ```

=== "Example"

    ```vim
    :%s/v[0-9]/(&)/g                 " v1 becomes (v1)
    :%s/\(\w\+\) \(\w\+\)/\2 \1/     " hello world becomes world hello
    ```

In the replacement, `&` is the whole match and `\1`, `\2` are the groups
captured with `\(` and `\)`. `\r` inserts a line break: `:%s/,/\r/g` puts each
comma-separated item on its own line.

In Vim patterns, `+`, `?`, `|`, `(`, `)` and `{` match themselves; a
backslash gives them their regex meaning (`\+`, `\(`). Starting the pattern
with `\v` (*very magic*) lets them be written as in other regex tools:
`:%s/\v(\w+) (\w+)/\2 \1/`.

## Remove trailing whitespace

```vim
:%s/\s\+$//e
```

`\s\+$` matches one or more spaces or tabs at the end of a line, and the
empty replacement removes them. `e` keeps Vim quiet when there are none.

## Act on matching lines

=== "Syntax"

    ```text
    :g/<pattern>/<command>
    :v/<pattern>/<command>
    ```

=== "Example"

    ```vim
    :g/DEBUG/d             " delete every line containing DEBUG
    :v/ERROR/d             " delete every line not containing ERROR
    :g/^\s*$/d             " delete blank lines
    :g/TODO/normal A !     " run Normal-mode keys on each match
    ```

`:g` runs a command on every line that matches and `:v` (or `:g!`) on every
line that does not. The command defaults to printing the lines, so
`:g/<pattern>` lists them.
