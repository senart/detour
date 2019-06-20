# Detour v.0.0.1

This script create an `SSH tunnel` with local port forwarding for the specified domain entries. It also updates the `/etc/hosts` file and adds an alias with `ifconfig`, so that connections to the specified domains are possible.

Tested only on `macos`.

## Example Usage

To get help for `detour.py` simply run `python3 detour.py --help`.

In order to get it going, you need 3 things:

1. SSH access to the machine
2. An input file, containing the host name and port for each domain.
3. Sudo access to edit the `/etc/hosts` file and use `ifconfig` commands.

### 1. Prepare Input File

The input file is a newline separted file containing the destination hosts and their ports, for example a `file.txt`.
If no file is given as input, by default the script uses the `file.txt` in the local directory.

```
private.server.com:8443
xyz.server.com:8443
ssh.cool.net:9999
```

### 2. Using Detour

Issue `start` to open an SSH tunnel like this:

```shell
$ sudo python3 detour.py start ./file.txt -s username@myserver.com
```
The `./file.txt` is the Input File with the specified domain entries.

In order to stop the SSH tunnel and clear up the `/etc/hosts`, use `stop`:

```shell
$ sudo python3 detour.py stop ./file.txt -s username@myserver.com
```

## Known issues
1. You need your public key for the SSH connection at `~/.ssh/id_rsa` in order to connect
2. If you run `start` twice, you'll have to either reboot or kill the first session:
    ```shell
    # Note the PID of the stale SSH session
    $ ps aux | grep ssh
    $ sudo kill <PID of ssh session>
    ```

## TODO:
* Add `--k` flag for optionaly specifying public ssh key.
* Figure out a way to use `sudo` only for the commands that require it - editing `/etc/hosts/` and calling `ifconfig`. Might need to refactor code in multiple files.
* Handle errors more appropriately - e.g. running `start` twice shouldn't crash the app.
* Store the ssh socket file `ssh-control-socket` somewhere in `/tmp`.
* Test on Ubuntu.
* Port to Windows (add checks for `/etc/hosts` and `ifconfig` commands)
* Make the `stop` command not required - e.g. run in interactive mode and kill with CTRL+C.
* Add a `status` command that shows more info for the current SSH session - ssh sockets supports this.
* Maybe refactor to use [Paramiko](https://github.com/paramiko/paramiko)?
* Use `venv` and `setuptools` to package the app like the [Click guys suggest](https://click.palletsprojects.com/en/7.x/quickstart/#switching-to-setuptools), possibly distribute to pip3.
