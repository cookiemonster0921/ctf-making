#!/bin/bash
set -e

# Write the flag (sourced from the FLAG environment variable at container
# start) to a location outside the web-servable docroot.
FLAG_VALUE="${FLAG:-CSEC_missing_flag_env}"
echo "${FLAG_VALUE}" > /usr/local/apache2/flag.txt
chmod 644 /usr/local/apache2/flag.txt

exec "$@"
