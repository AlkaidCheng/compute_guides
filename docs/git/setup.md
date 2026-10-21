# First-time setup

Configure Git once on a new machine: your identity, sensible defaults, and
access to GitHub.

## Set your name and email

=== "Syntax"

    ```text
    git config --global user.name "<name>"
    git config --global user.email "<email>"
    ```

=== "Example"

    ```bash
    git config --global user.name "Alice Smith"
    git config --global user.email "alice@example.com"
    ```

Every commit records this name and email as its author. `--global` writes them
to `~/.gitconfig`, so they apply to every repository you work in. GitHub links
a commit to your account by its email; to keep your address private, use the
`…@users.noreply.github.com` address shown under GitHub **Settings → Emails**.

## Use another email in one repository

=== "Syntax"

    ```text
    git config user.email "<email>"
    ```

=== "Example"

    ```bash
    cd ~/projects/analysis
    git config user.email "alice@work.example.org"
    ```

Without `--global`, the setting goes to `.git/config` of the repository you
are in and overrides the global one there only. The same works for
`user.name`.

## Use another email for a folder of repositories

=== "Syntax"

    ```text
    git config --global includeIf."gitdir:<folder>/".path <file>
    git config --file <file> user.email "<email>"
    ```

=== "Example"

    ```bash
    git config --global includeIf."gitdir:~/work/".path ~/.gitconfig-work
    git config --file ~/.gitconfig-work user.email "alice@work.example.org"
    ```

The first line tells Git to read an extra config file for every repository
under `<folder>`; the trailing `/` makes it match all repositories below that
folder. The second line writes the email into that file (`--file` edits a given
file instead of `~/.gitconfig`). Repositories elsewhere keep the global email.

## Set the default branch name

=== "Syntax"

    ```text
    git config --global init.defaultBranch <name>
    ```

=== "Example"

    ```bash
    git config --global init.defaultBranch main
    ```

Names the first branch of every new `git init` repository, matching GitHub's
default `main`. Needs Git 2.28 or later; older Git always uses `master`.

## Set your editor

=== "Syntax"

    ```text
    git config --global core.editor "<command>"
    ```

=== "Example"

    ```bash
    git config --global core.editor vim
    git config --global core.editor "code --wait"   # VS Code
    ```

The editor Git opens for commit messages and interactive rebases. A graphical
editor needs its wait flag (`--wait` for VS Code), so Git waits until you close
the file instead of committing an empty message.

## Choose what git pull does

=== "Syntax"

    ```text
    git config --global pull.rebase <true|false>
    git config --global pull.ff only
    ```

=== "Example"

    ```bash
    git config --global pull.rebase false   # merge
    ```

When your branch and the remote both have new commits, `git pull` stops with
"Need to specify how to reconcile divergent branches" until one of these is
set.

| Setting | On diverged branches |
|---|---|
| `pull.rebase false` | merges the remote commits into yours with a merge commit |
| `pull.rebase true` | replays your commits on top of the remote ones |
| `pull.ff only` | refuses, so you decide each time |

One pull can override the setting with `--no-rebase`, `--rebase` or
`--ff-only`.

## Ignore files in every repository

=== "Syntax"

    ```text
    git config --global core.excludesFile <file>
    ```

=== "Example"

    ```bash
    git config --global core.excludesFile ~/.gitignore_global
    echo ".DS_Store" >> ~/.gitignore_global
    ```

Patterns in this file, written as in `.gitignore`, apply to every repository.
Use it for files your own machine creates (`.DS_Store`, editor swap files),
and keep project files in the project's `.gitignore`. Without this setting,
Git still reads `~/.config/git/ignore` if it exists.

## Show your settings

=== "Syntax"

    ```text
    git config --list [--show-origin]
    git config <key>
    git config --global --edit
    ```

=== "Example"

    ```bash
    git config --list --show-origin   # every setting and the file it is in
    git config user.email             # the value in effect here
    git config --global --edit        # open ~/.gitconfig in your editor
    ```

`--list` prints every setting in effect, `--show-origin` adds the file each
one comes from, and `git config <key>` prints one value. `--edit` opens the
config file itself. When a key is set in several files, the more specific one
wins:

| Scope | File | Applies to |
|---|---|---|
| `--system` | `/etc/gitconfig` | every user on the machine |
| `--global` | `~/.gitconfig` | all your repositories |
| `--local` (the default) | `.git/config` | the current repository |

## Sign in to GitHub

=== "Syntax"

    ```text
    gh auth login [--git-protocol <ssh|https>]
    gh auth status
    ```

=== "Example"

    ```bash
    gh auth login --git-protocol https
    gh auth status   # which account is signed in
    ```

Create the account at <https://github.com> first. `gh auth login` (the GitHub
CLI) signs you in through the browser and stores a token. With `https` it also
sets itself up as Git's credential helper, so `git push` and `git pull` work
without a password prompt; with `ssh` it uploads an SSH key instead (see
[Use an SSH key with GitHub](#use-an-ssh-key-with-github)). GitHub no longer
accepts your account password for Git over HTTPS: use `gh`, an SSH key, or a
personal access token.

## Use an SSH key with GitHub

```bash title="Check"
ssh -T git@github.com
```

Git over SSH (the `git@github.com:` addresses) signs in with a key pair
instead of a token. Set it up once, following the SSH page:

1. [Generate a key pair](../unix/ssh.md#generate-a-key-pair).
2. [Add the public key to GitHub](../unix/ssh.md#add-your-public-key-to-github).
3. [Add the key to the agent](../unix/ssh.md#add-the-key-to-the-agent), so
   you type its passphrase once per session.

The check then greets you by your GitHub username ("You've successfully
authenticated"); GitHub offers no shell, so it exits right after.

## Save HTTPS credentials without gh

=== "Linux"

    === "Syntax"

        ```text
        git config --global credential.helper "cache [--timeout=<seconds>]"
        git config --global credential.helper store
        ```

    === "Example"

        ```bash
        git config --global credential.helper "cache --timeout=3600"   # one hour
        ```

=== "macOS"

    === "Syntax"

        ```text
        git config --global credential.helper osxkeychain
        ```

    === "Example"

        ```bash
        git config --global credential.helper osxkeychain
        ```

On the next push Git asks for your username and, as the password, a personal
access token made under GitHub **Settings → Developer settings → Personal
access tokens**. The helper then remembers them:

| Helper | Keeps the token |
|---|---|
| `cache` | in memory, for `--timeout` seconds (default 900) |
| `store` | in `~/.git-credentials`, as plain text |
| `osxkeychain` | in the macOS Keychain; Apple's Git sets this already |

## Clone over SSH or HTTPS

=== "Syntax"

    ```text
    git clone git@github.com:<owner>/<repo>.git [<folder>]
    git clone https://github.com/<owner>/<repo>.git [<folder>]
    ```

=== "Example"

    ```bash
    git clone git@github.com:alice/analysis.git                      # SSH
    git clone https://github.com/alice/analysis.git ~/projects/analysis
    ```

The `git@github.com:` form authenticates with your
[SSH key](#use-an-ssh-key-with-github), the `https://` form with
[gh](#sign-in-to-github) or a
[credential helper](#save-https-credentials-without-gh). Both copy the repository into a new folder,
named after the repository unless you give `<folder>`, with the remote
`origin` pointing back at GitHub.

## Switch a repository between HTTPS and SSH

=== "Syntax"

    ```text
    git remote set-url origin <url>
    git remote -v
    ```

=== "Example"

    ```bash
    git remote set-url origin git@github.com:alice/analysis.git
    git remote -v   # check the new URL
    ```

Points `origin` at a new address without cloning again. `git remote -v`
shows the URLs the repository fetches from and pushes to.
