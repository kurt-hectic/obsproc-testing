#!/bin/sh

# Abort on any error (including if wait-for-it fails).
set -e

# Wait for the backend to be up, if we know where it is.
if [ -n "$BROKER_HOST" ]; then
  /app/wait-for-it.sh "$BROKER_HOST:${BROKER_PORT:-6000}"
fi

# Run the main container command.
exec "$@"