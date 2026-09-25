# Archives

Pack directories and files into one compressed file with `tar` or `zip`, and
unpack them again. Use `tar` between Linux and macOS machines, since it keeps
permissions and symlinks; use `zip` for Windows users.

## Create a tar archive

=== "Syntax"

    ```text
    tar -czf <archive.tar.gz> <path>...
    ```

=== "Example"

    ```bash
    tar -czf project.tar.gz src docs README.md
    ```

| Flag | Meaning |
|---|---|
| `-c` | create an archive |
| `-z` | compress with gzip |
| `-f <archive>` | the archive file; keep `f` last in the group, as the name follows it |
| `-v` | print each file as it is added (optional) |

Paths are stored as you type them: archiving `projects/src` stores
`projects/src/…`. To store just `src/…`, see the next section.

## Archive directories from different places

=== "Syntax"

    ```text
    tar -czf <archive.tar.gz> -C <parent> <dir> [-C <parent> <dir>]...
    ```

=== "Example"

    ```bash
    tar -czf bundle.tar.gz \
      -C /data/runs run-042 \
      -C ~/analysis plots \
      -C ~/notes 2026-09
    ```

`-C` changes directory before adding the paths that follow it, so the archive
holds only `run-042/`, `plots/` and `2026-09/` at its top level. The archive
itself is written relative to where you ran the command.

!!! tip "Use absolute paths after `-C`"

    Each relative `-C` is resolved from the previous one: `-C a dir1 -C b dir2`
    looks for `a/b/dir2`.

## Exclude files

=== "Syntax"

    ```text
    tar -czf <archive.tar.gz> --exclude=<pattern>... <path>...
    ```

=== "Example"

    ```bash
    tar -czf project.tar.gz --exclude='*.pyc' --exclude='.git' project
    ```

Excludes matching files and directories at any depth. Put `--exclude` before
the paths: GNU tar ignores it after them, and macOS tar mistakes it for a file
name. Quote the pattern so the shell does not expand it.

## Choose the compression

=== "Syntax"

    ```text
    tar -c<compression>f <archive> <path>...
    ```

=== "Example"

    ```bash
    tar -cJf project.tar.xz project
    ```

| Flag | Compression | Extension |
|---|---|---|
| `z` | gzip: fast, universal | `.tar.gz`, `.tgz` |
| `j` | bzip2: smaller than gzip, slower | `.tar.bz2` |
| `J` | xz: smallest, slowest | `.tar.xz` |
| `--zstd` | zstd: fast and small | `.tar.zst` |
| (none) | uncompressed | `.tar` |

zstd is a long option: `tar --zstd -cf project.tar.zst project`. It needs a
recent tar (GNU tar 1.31 or later) and, on Linux, the `zstd` program.

## Leave out macOS metadata

=== "Syntax"

    ```text
    tar --no-mac-metadata --no-xattrs -czf <archive.tar.gz> <path>...
    ```

=== "Example"

    ```bash
    tar --no-mac-metadata --no-xattrs -czf project.tar.gz project
    ```

On macOS, files with extended attributes (anything downloaded with a browser,
for example) are archived with extra `._name` files and attribute headers.
Unpacked on Linux, these show up as stray `._*` files and "Ignoring unknown
extended header keyword" warnings. These flags leave them out; Linux tar needs
nothing extra.

## List the contents of a tar archive

=== "Syntax"

    ```text
    tar -tzf <archive.tar.gz>
    ```

=== "Example"

    ```bash
    tar -tzf project.tar.gz
    ```

Add `-v` to also show permissions, sizes and dates.

## Extract a tar archive

=== "Syntax"

    ```text
    tar -xzf <archive.tar.gz> [-C <dest>] [<path>...]
    ```

=== "Example"

    ```bash
    tar -xzf project.tar.gz                             # into the current directory
    tar -xzf project.tar.gz -C ~/restore                # into another directory
    tar -xzf project.tar.gz project/README.md           # only the listed paths
    tar -xzf project-1.0.tar.gz --strip-components=1    # without the top-level directory
    ```

The directory given to `-C` must already exist. Both GNU and macOS tar detect
the compression when extracting, so `tar -xf` works for every format above.

!!! warning "Existing files are overwritten"

    Extracting replaces files of the same name without asking. Add `-k` to
    keep existing files instead.

## Create a zip archive

=== "Syntax"

    ```text
    zip -r <archive.zip> <path>...
    ```

=== "Example"

    ```bash
    zip -r project.zip src docs README.md
    ```

| Option | Meaning |
|---|---|
| `-r` | include the contents of directories |
| `-q` | quiet |
| `-x <pattern>...` | exclude matching files; goes after the paths |
| `-y` | store symlinks as links (by default zip stores a copy of the target) |
| `-9` | best compression, slower |

## Zip directories from different places

=== "Syntax"

    ```text
    (cd <parent> && zip -r <absolute-archive-path> <dir>)
    ```

=== "Example"

    ```bash
    out="$PWD/bundle.zip"
    (cd /data/runs && zip -r "$out" run-042)
    (cd ~/analysis && zip -r "$out" plots)
    (cd ~/notes && zip -r "$out" 2026-09)
    ```

zip stores paths as you type them and has no `-C`, so run it from each parent
directory. The subshell `( … )` changes directory without moving your own
shell, and zip adds to an archive that already exists. Save the archive path
first, since a relative path changes meaning after the `cd`.

## List and extract a zip archive

=== "Syntax"

    ```text
    unzip [-l | -o] <archive.zip> [<pattern>...] [-d <dest>]
    ```

=== "Example"

    ```bash
    unzip -l project.zip                  # list the contents
    unzip project.zip                     # extract into the current directory
    unzip project.zip -d ~/restore        # extract into another directory
    unzip project.zip 'project/docs/*'    # extract only matching paths
    unzip -o project.zip                  # overwrite existing files without asking
    ```

`-d` creates the destination directory if needed, but not its parents; run
`mkdir -p` first for a nested path. Without `-o`, `unzip` asks before replacing
each existing file.
