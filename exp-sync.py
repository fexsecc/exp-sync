#!/usr/bin/env python
import os
import paramiko
import argparse
import time

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

parser = argparse.ArgumentParser(
                        prog="exp-sync.py",
                        description="Sync a file and watch for (local only) changes over scp"
)

parser.add_argument('-f', "--path", type=str, default="exploit.py", help="Path to file to sync")
parser.add_argument('-r', "--rpath", type=str, default="/home/hacker/exploit.py", help="Remote path of where to sync file to on server")
parser.add_argument('-H', '--host', type=str, default="dojo.pwn.college", help="Hostname of remote ssh server")
parser.add_argument('-p', '--port', type=int, default=22, help="Port of ssh server")
parser.add_argument('-u', '--user', type=str, default="hacker", help="User to use on remote ssh server")
parser.add_argument('-k', '--key', type=str, default=os.path.expanduser("~/.ssh/id_ed25519"), help="Private key used to authenticate")

args = parser.parse_args()

def sync(sftp):
    try:
        print(f"[!] Syncing {args.path} to remote {args.rpath}...")
        sftp.put(args.path, args.rpath)
        print("[+] Sync done")
    except Exception as e:
        print(f"An error occurred while syncing: {e}")


def main():
    # NOTE: You might need to swap this if you're using older key algorithms
    key = paramiko.Ed25519Key.from_private_key_file(args.key)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Keep connection open for low latency
    print(f"[!] Connecting to {args.host} on port {args.port} as {args.user}...")
    client.connect(hostname=args.host, port=args.port, username=args.user, pkey=key, timeout=10)
    sftp = client.open_sftp()
    print(f"[+] Connected to {args.host} on port {args.port} as {args.user}")

    # Sync once for starters
    sync(sftp)
    # Busy loop to check if file changed 
    # https://stackoverflow.com/questions/28057308/check-if-a-file-is-modified-in-python#74497600
    get_time = lambda f: os.stat(f).st_ctime
    prev_time = get_time(args.path)

    while True:
        time.sleep(0.6)
        t = get_time(args.path)
        if t != prev_time:
            sync(sftp)
            prev_time = t


if __name__ == '__main__':
    main()

