#!/bin/sh
#
# Synology DSM init script for Wemo REST server
# Requires: sabnzbd
#           python
#           wget
#
# Configured Variables:
#
WEMO_EXEC="/volume1/homes/canvin/wemo/run.py"  
WEMO_PID="/tmp/wemo.pid"                       
                                               
# Begin script                               
#                                            
case "$1" in                                 
start)                                       
  PATH=$PATH:/opt/bin                        
  printf "%-30s" "Starting wemo rest server" 
  ${PYTHON_EXEC} ${WEMO_EXEC} &              
  echo $! > $WEMO_PID                        
  printf "[%4s]\n" "done"                   
  ;;                                        
stop)                                       
  printf "%-30s" "Stopping wemo server"     
  PID=$(cat $WEMO_PID)                      
  kill $PID                                 
  printf "[%4s]\n" "done"                   
  ;;                                        
status)                                
PID=$(cat $WEMO_PID)                   
if [ -e /proc/${PID} -a /proc/${PID}/exe ]; then
echo "Still running" 
else                                            
echo "not running"                              
fi                                              
;;                                              
*)                                              
  echo "Usage: $0 {start|stop|status}"          
  exit 1                                        
esac                                            
 
exit 0
