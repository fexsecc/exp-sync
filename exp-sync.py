#!/usr/bin/env python
import os
import paramiko
import hashlib
import sys
import argparse

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


def main():
    parser = argparse.ArgumentParser(
                        prog="exp-sync.py",
                        description="Sync a file and watch for (local only) changes over scp"
    )
    parser.add_argument('-f', "--file", type=str, help="Path to file to sync")
    parser.add_argument('-r', "--rpath", type=str, help="Remote path of where to sync file to on server")
    parser.add_argument('-h', '--host', type=str, default="dojo.pwn.college", help="Hostname of remote ssh server")
    parser.add_argument('-p', '--port', type=int, default=22, help="Port of ssh server")
    parser.add_argument('-u', '--user', type=str, default="hacker", help="User to use on remote ssh server")
    parser.add_argument('-k', '--key', type=str, default=os.path.expanduser("~/.ssh/id_ed25519"), help="Private key used to authenticate")

    args = parser.parse_args()

    key = paramiko.Ed25519Key.from_private_key_file(args.key)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=args.host, port=args.port, username=args.user, pkey=key, timeout=10)
        sftp = client.open_sftp()
        sftp.put(args.path, args.rpath)
        sftp.flush()
    except Exception as e:
        print(f"An error occurred while syncing: {e}")
    finally:
        client.close()


if __name__ == '__main__':
    main()
