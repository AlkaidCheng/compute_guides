# Finding files

Search a directory tree with `find` and count what it matches.

## Count files in a directory

=== "Syntax"

    ```text
    find <dir> -mindepth 1 | wc -l
    ```

=== "Example"

    ```bash
    find ~/projects/analysis -mindepth 1 | wc -l
    ```

Counts everything inside the directory, at any depth: files, directories and
symlinks. `-mindepth 1` leaves out the directory itself.

Symlinks are counted as links, not followed. A file with several
[hard links](links.md#create-a-hard-link) is counted once per name; see
[Count each file once](#count-each-file-once).

## Count by type

=== "Syntax"

    ```text
    find <dir> -mindepth 1 -type <type> | wc -l
    ```

=== "Example"

    ```bash
    find ~/projects/analysis -mindepth 1 -type f | wc -l   # regular files
    find ~/projects/analysis -mindepth 1 -type d | wc -l   # directories
    ```

| Type | Matches |
|---|---|
| `f` | regular files |
| `d` | directories |
| `l` | symlinks |

## Count only the top level

=== "Syntax"

    ```text
    find <dir> -mindepth 1 -maxdepth 1 | wc -l
    ```

=== "Example"

    ```bash
    find ~/Downloads -mindepth 1 -maxdepth 1 | wc -l
    ```

Counts the entries directly inside the directory, hidden ones included,
without descending into subdirectories.

## Count each file once

=== "Linux"

    === "Syntax"

        ```text
        find <dir> -mindepth 1 -printf '%D:%i\n' | sort -u | wc -l
        ```

    === "Example"

        ```bash
        find ~/projects/analysis -mindepth 1 -printf '%D:%i\n' | sort -u | wc -l
        ```

=== "macOS"

    === "Syntax"

        ```text
        find <dir> -mindepth 1 -exec stat -f '%d:%i' {} + | sort -u | wc -l
        ```

    === "Example"

        ```bash
        find ~/projects/analysis -mindepth 1 -exec stat -f '%d:%i' {} + | sort -u | wc -l
        ```

A file with several hard links has several names but one inode. Counting
distinct device and inode numbers counts it once.
