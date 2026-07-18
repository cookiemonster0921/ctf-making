#!/bin/bash
set -e

# Write the flag from the environment into a root-only file at container
# start. The real flag never lives in an image layer.
echo "${FLAG:-CSEC{missing_flag_env}}" > /root/flag.txt
chown root:root /root/flag.txt
chmod 600 /root/flag.txt

# Expose an unauthenticated, unprivileged shell on TCP 9001. Anyone who
# connects lands as the low-priv "player" user -- same as a "you have SSH
# access to a normal user account" pwn box.
exec socat TCP-LISTEN:9001,reuseaddr,fork EXEC:"su - player",pty,stderr,setsid,sigint,sane
