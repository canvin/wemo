#!/bin/sh
#
# Synology DSM init script for Wemo REST server
# Requires: sabnzbd
#           python
#           wget
#
# Configured Variables:
#
PYTHON_EXEC="/usr/bin/python"
WEMO_EXEC="/opt/share/restWemo/server.py"
 
# Begin script
#
case "$1" in
start)
  PATH=$PATH:/opt/bin
  printf "%-30s" "Starting wemo rest server"
  ${PYTHON_EXEC} ${WEMO_EXEC} &
  printf "[%4s]\n" "done"
  ;;
stop)
  printf "%-30s" "Stopping SABnzbd"
  /opt/bin/wget -q --delete-after "http://127.0.0.1:${SABNZBD_PORT}/shutdown?session=${SAB_API_KEY}"
  printf "[%4s]\n" "done"
  ;;
*)
  echo "Usage: $0 {start|stop}"
  exit 1
esac
 
exit 0