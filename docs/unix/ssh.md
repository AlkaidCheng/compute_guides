# SSH

Log in to remote machines and services such as GitHub with a key pair instead
of a password.

## Generate a key pair

=== "Syntax"

    ```text
    ssh-keygen -t ed25519 -C "<comment>" [-f <file>]
    ```

=== "Example"

    ```bash
    ssh-keygen -t ed25519 -C "your_email@example.com"
    ssh-keygen -t ed25519 -C "your_email@example.com" -f ~/.ssh/id_ed25519_github
    ```

`-t ed25519` picks the Ed25519 key type: short, fast and secure. `-C` adds a
comment to the public key, usually your email, so you can tell keys apart; it
has no effect on security. `ssh-keygen` then asks for a file name (Enter keeps
`~/.ssh/id_ed25519`; `-f` skips the question) and a passphrase, which encrypts
the private key on disk and is recommended.

| File | What it is | Share it? |
|---|---|---|
| `~/.ssh/id_ed25519` | private key | never |
| `~/.ssh/id_ed25519.pub` | public key | yes: servers and GitHub get this one |

For a server too old for Ed25519, use `-t rsa -b 4096` instead.

## Install your public key on a server

=== "Syntax"

    ```text
    ssh-copy-id -i <public-key> <user>@<host>
    ```

=== "Example"

    ```bash
    ssh-copy-id -i ~/.ssh/id_ed25519.pub alice@login.example.org
    ```

Adds the key to `~/.ssh/authorized_keys` on the server, asking for your
password one last time. From then on `ssh alice@login.example.org` logs in with
the key. Without `ssh-copy-id`, append it by hand:

```bash title="Without ssh-copy-id"
cat ~/.ssh/id_ed25519.pub | ssh alice@login.example.org 'mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys'
```

## Add your public key to GitHub

=== "Linux"

    === "Syntax"

        ```text
        cat <public-key>
        ```

    === "Example"

        ```bash
        cat ~/.ssh/id_ed25519.pub   # then copy the printed line
        ```

=== "macOS"

    === "Syntax"

        ```text
        pbcopy < <public-key>
        ```

    === "Example"

        ```bash
        pbcopy < ~/.ssh/id_ed25519.pub   # copies it to the clipboard
        ```

Paste the key under GitHub **Settings → SSH and GPG keys → New SSH key**, then
check the connection:

```bash title="Check"
ssh -T git@github.com
```

## Add the key to the agent

=== "Linux"

    === "Syntax"

        ```text
        ssh-add <private-key>
        ```

    === "Example"

        ```bash
        eval "$(ssh-agent -s)"      # start an agent, if none is running
        ssh-add ~/.ssh/id_ed25519
        ```

=== "macOS"

    === "Syntax"

        ```text
        ssh-add --apple-use-keychain <private-key>
        ```

    === "Example"

        ```bash
        ssh-add --apple-use-keychain ~/.ssh/id_ed25519
        ```

The agent holds your unlocked key in memory, so you type the passphrase once
instead of on every connection. `ssh-add -l` lists the keys it holds. On macOS
the passphrase is also saved in the Keychain; to load the key automatically in
every session, add this to `~/.ssh/config` (macOS only: Linux ssh rejects
`UseKeychain`):

```text title="~/.ssh/config"
Host *
  UseKeychain yes
  AddKeysToAgent yes
  IdentityFile ~/.ssh/id_ed25519
```

## Fix key file permissions

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519 ~/.ssh/authorized_keys ~/.ssh/config
chmod 644 ~/.ssh/id_ed25519.pub
```

SSH refuses a private key that other users can read ("UNPROTECTED PRIVATE KEY
FILE"). These are the usual permissions; see
[Permissions and groups](permissions.md) for what the numbers mean.

## Show a key's fingerprint

=== "Syntax"

    ```text
    ssh-keygen -lf <key>
    ```

=== "Example"

    ```bash
    ssh-keygen -lf ~/.ssh/id_ed25519.pub
    ```

Prints a line such as `256 SHA256:… your_email@example.com (ED25519)`, to
compare with the fingerprint GitHub or a server shows.

## Change or remove the passphrase

=== "Syntax"

    ```text
    ssh-keygen -p -f <private-key>
    ```

=== "Example"

    ```bash
    ssh-keygen -p -f ~/.ssh/id_ed25519
    ```

Asks for the old and the new passphrase; leave the new one empty to remove it.
The key itself does not change, so servers need no update.
