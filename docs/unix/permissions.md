# Permissions and groups

Control who can read, change and run a file: `chmod` sets the permissions,
`chgrp` the group, `umask` the defaults for new files.

## Read the permission string

=== "Syntax"

    ```text
    ls -l <file>
    ls -ld <dir>
    ```

=== "Example"

    ```console
    $ ls -l run.sh
    -rwxr-x---  1 alice  research  2048 Sep 25 12:00 run.sh
    ```

The first ten characters are the file type followed by three sets of
permissions, always in the order read, write, execute:

```text
 -   rwx   r-x   ---
 |    |     |     |
 |    |     |     +-- others (o): everyone else
 |    |     +-------- group  (g): the file's group
 |    +-------------- owner  (u): the file's owner
 +------------------- type: - file, d dir, l link
```

A `-` in a permission slot means that permission is off. Here, alice can read,
write and run `run.sh`, members of research can read and run it, and everyone
else has no access. `ls -ld` shows a directory's own permissions rather than
its contents.

## What r, w and x mean

| Letter | Value | On a file | On a directory |
|---|---|---|---|
| `r` | 4 | read the contents | list the names inside |
| `w` | 2 | change the contents | create, delete and rename entries (needs `x` too) |
| `x` | 1 | run it as a program | enter it (`cd`) and reach the entries inside |

Deleting a file depends on the `w` of the directory that holds it, not on the
file's own permissions.

## Change permissions with numbers

=== "Syntax"

    ```text
    chmod <mode> <path>...
    ```

=== "Example"

    ```bash
    chmod 644 notes.txt
    chmod 755 run.sh
    chmod 600 ~/.ssh/id_ed25519
    ```

Each set of three permissions is a 3-bit mask, written as one octal digit: add
4 for `r`, 2 for `w` and 1 for `x`. The three digits are owner, group and
others:

```text
          owner   group   others
letters    rwx     r-x     ---
bits       111     101     000
digit       7       5       0      ->  chmod 750 run.sh
```

| Digit | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
|---|---|---|---|---|---|---|---|---|
| Letters | `rwx` | `rw-` | `r-x` | `r--` | `-wx` | `-w-` | `--x` | `---` |

| Mode | Letters | Typical use |
|---|---|---|
| `644` | `rw-r--r--` | files you edit and others read |
| `755` | `rwxr-xr-x` | directories and programs others may use |
| `600` | `rw-------` | private files: keys, credentials |
| `700` | `rwx------` | private directories, such as `~/.ssh` |
| `640` | `rw-r-----` | files readable by your group only |
| `750` | `rwxr-x---` | directories shared with your group only |
| `664` | `rw-rw-r--` | files your group can edit |
| `775` | `rwxrwxr-x` | directories your group can add to |

A number sets all nine permissions at once, replacing whatever was there.

!!! warning "Avoid `chmod -R` with numbers"

    `chmod -R 755` makes every file executable, and `chmod -R 644` locks
    everyone out of the directories, since none of them keeps its `x`. Use
    letters with `X` instead; see
    [Share a directory with your group](#share-a-directory-with-your-group).

## Change permissions with letters

=== "Syntax"

    ```text
    chmod <who><op><perms>[,...] <path>...
    ```

=== "Example"

    ```bash
    chmod u+x run.sh              # owner: add execute
    chmod go-w notes.txt          # group and others: remove write
    chmod o-rwx secrets.txt       # others: remove everything
    chmod u=rw,g=r,o= notes.txt   # set exactly (same as 640)
    ```

| Part | Values |
|---|---|
| `<who>` | `u` owner, `g` group, `o` others, `a` all three |
| `<op>` | `+` add, `-` remove, `=` set exactly |
| `<perms>` | `r`, `w`, `x`, or `X` (see below) |

Unlike a number, letters change only the permissions you name.

## Share a directory with your group

=== "Syntax"

    ```text
    chmod -R g+rX <dir>
    ```

=== "Example"

    ```bash
    chmod -R g+rX ~/projects/analysis
    ```

Capital `X` adds execute only to directories (and to files that are already
executable), so the group can open every directory and read every file without
turning data files into programs. Use `g+rwX` to let the group edit as well.
The group also needs `x` on each parent directory on the way there.

## Change the group of a file

=== "Syntax"

    ```text
    chgrp [-R] <group> <path>...
    ```

=== "Example"

    ```bash
    chgrp research results.csv
    chgrp -R research ~/projects/analysis   # the directory and everything inside
    chown :research results.csv             # same as chgrp
    ```

You must own the file, and you can only choose a group you belong to; anything
else fails with "Operation not permitted". Changing the owner itself
(`chown <user>:<group> <path>`) needs root.

## Make new files inherit the directory's group

=== "Linux"

    === "Syntax"

        ```text
        chgrp <group> <dir>
        chmod g+s <dir>
        ```

    === "Example"

        ```bash
        chgrp research /data/shared
        chmod g+s /data/shared
        ```

=== "macOS"

    === "Syntax"

        ```text
        chgrp <group> <dir>
        ```

    === "Example"

        ```bash
        chgrp research /data/shared
        ```

On Linux a new file normally gets its creator's primary group. The setgid bit
(`g+s`, shown as `s` in the group slot: `drwxrwsr-x`) makes new files and
subdirectories take the directory's group instead, and new subdirectories
inherit the bit. As a number, setgid is a leading `2`: `chmod 2775`. On macOS,
new files always take the directory's group, so the group change is enough.

## List the groups you belong to

=== "Syntax"

    ```text
    id -Gn [<user>]
    ```

=== "Example"

    ```bash
    id -Gn          # all your groups
    id -gn          # your primary group
    id -Gn alice    # another user's groups
    ```

`groups` prints the same list as `id -Gn`. After you are added to a group, the
change applies from your next login.

## Check permissions as numbers

=== "Linux"

    === "Syntax"

        ```text
        stat -c '%A %a %U:%G %n' <path>...
        ```

    === "Example"

        ```bash
        stat -c '%A %a %U:%G %n' results.csv
        ```

=== "macOS"

    === "Syntax"

        ```text
        stat -f '%Sp %Lp %Su:%Sg %N' <path>...
        ```

    === "Example"

        ```bash
        stat -f '%Sp %Lp %Su:%Sg %N' results.csv
        ```

Both print a line such as `-rw-r--r-- 644 alice:research results.csv`.

## Set default permissions for new files

=== "Syntax"

    ```text
    umask [<mask>]
    ```

=== "Example"

    ```bash
    umask          # show the current mask, e.g. 0022
    umask -S       # show what it allows, e.g. u=rwx,g=rx,o=rx
    umask 002      # change it for this shell
    ```

The umask lists the permissions to leave *off* new files. New files start from
`666` (`rw-rw-rw-`) and new directories from `777` (`rwxrwxrwx`); every bit
set in the mask is switched off:

| umask | New files | New directories | Use |
|---|---|---|---|
| `022` | `644` | `755` | common default: only you can write |
| `002` | `664` | `775` | working in a shared group |
| `077` | `600` | `700` | private |

To keep a umask, add the `umask` line to your shell's startup file
(`~/.bashrc` or `~/.zshrc`).
