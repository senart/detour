# Detour v.0.0.1

This script create an `SSH tunnel` with local port forwarding for the specified domain entries. It also updates the `/etc/hosts` file and adds an alias with `ifconfig`, so that connections to the specified domains are possible.

## Example Usage

To get help for `detour.py` simply run `python3 detour.py --help`.

In order to get it going, you need 3 things:

1. SSH access to the machine
2. An input file, containing the host name and port for each domain.
3. Sudo access to edit the `/etc/hosts` file and use `ifconfig` commands.

### 1. Prepare Input File

The input file is a newline separted file containing the destination hosts and their ports, for example a `file.txt`:

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