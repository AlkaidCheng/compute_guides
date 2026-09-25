# Links

Give a file or directory a second name: a symbolic link points to a path, a
hard link is another name for the same file.

## Create a symbolic link

=== "Syntax"

    ```text
    ln -s <target> <link>
    ```

=== "Example"

    ```bash
    ln -s /data/shared/results.csv results.csv
    ln -s /data/shared/results.csv ~/analysis/   # creates ~/analysis/results.csv
    ```

The target comes first, the new link second. If `<link>` is an existing
directory, the link is created inside it under the target's name. A link can
point to a file or a directory, and to a path that does not exist yet.

## Make a relative link

=== "Linux"

    === "Syntax"

        ```text
        ln -sr <target> <link>
        ```

    === "Example"

        ```bash
        ln -sr data/results.csv links/results.csv   # stores ../data/results.csv
        ```

=== "macOS"

    === "Syntax"

        ```text
        ln -s <target-relative-to-link> <link>
        ```

    === "Example"

        ```bash
        ln -s ../data/results.csv links/results.csv
        ```

A relative target is resolved from the directory the link lives in, not from
where you ran `ln`. GNU `ln -r` works the path out for you; on macOS, write it
relative to the link's directory. Relative links keep working when the whole
tree is moved.

## Repoint an existing link

=== "Syntax"

    ```text
    ln -sfn <new-target> <link>
    ```

=== "Example"

    ```bash
    ln -sfn ~/tools/python-3.12 ~/tools/current
    ```

`-f` replaces the existing link. `-n` treats a link to a directory as the link
itself; without it, `ln` follows the old link and creates the new one *inside*
the directory it pointed to.

## See where a link points

=== "Syntax"

    ```text
    readlink [-f] <link>
    ```

=== "Example"

    ```bash
    ls -l ~/tools/current           # current -> /home/alice/tools/python-3.12
    readlink ~/tools/current        # the target, exactly as stored
    readlink -f ~/tools/current     # the full path, following every link
    ```

`realpath <link>` prints the same as `readlink -f`.

## Remove a link

=== "Syntax"

    ```text
    rm <link>
    ```

=== "Example"

    ```bash
    rm ~/tools/current
    ```

Removing a link never touches its target.

!!! warning "No trailing slash"

    For a link to a directory, `rm -r ~/tools/current/` (with the slash) acts
    on the target directory: it deletes the target's contents (on macOS, the
    target directory too) and leaves the link in place.

## Find broken links

=== "Linux"

    === "Syntax"

        ```text
        find <dir> -xtype l
        ```

    === "Example"

        ```bash
        find ~/projects -xtype l
        ```

=== "macOS"

    === "Syntax"

        ```text
        find -L <dir> -type l
        ```

    === "Example"

        ```bash
        find -L ~/projects -type l
        ```

Lists symlinks whose target no longer exists. The macOS form also works on
Linux.

## Create a hard link

=== "Syntax"

    ```text
    ln <file> <new-name>
    ```

=== "Example"

    ```bash
    ln ~/data/input.h5 ~/analysis/input.h5
    ```

Both names refer to the same data, so a large file appears in two places
without being copied. It is only freed when the last name is removed; `ls -l`
shows the number of names in its second column. Hard links work only for
files, not directories, and only within one filesystem.
