============
WeMo as REST 
============

Launch run.py

Then you can access your Wemo with http://localhost:8083/wemo/<id>/status

Replace <id> with 1,2,3,.. depending of how many wemo you have

This saved your wemo configuration in a file called wemo.json

Current command support:

wemo/<id>/on
wemo/<id>/off
wemo/<id>/status

wemo/all/on
wemo/all/off
wemo/all/status

wemo/update
