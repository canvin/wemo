#!/usr/bin/python
from wemo.libs.bottle import route, run, template, static_file
from wemo.wemoManager import *
import time
import json

wemoManager = wemoManager('wemo.json')

@route('/wemo/<id>/on')
def routeOn(id=1):
	status = wemoManager.on(id)
	return _getStatusInJson(id,status)
    
@route('/wemo/<id>/off')
def routeOff(id=1):
	status = wemoManager.off(id)
	return _getStatusInJson(id,status)
    
@route('/wemo/<id>/status')
def routeStatus(id=1):
	status = wemoManager.status(id)
	return _getStatusInJson(id,status)
    
@route('/wemo/all/on')
def routeAllOn():
	wemoClass.allOn()
	return routeStatusAll()

@route('/wemo/all/off')
def routeAllOff():
	wemoManager.allOff()
	return routeStatusAll()
    
@route('/wemo/all/status')
def routeStatusAll():
	returnStatus = wemoManager.allStatus()
	return json.dumps(returnStatus)
	
@route('/wemo/update')
def routeUpdateAll():
	wemoManager.allUpdate()
	return routeStatusAll()
	
def _getStatusInJson(id,status):
	printStatus = ('OFF' if status else 'ON')
	return json.dumps({id: printStatus})
    
@route('/favicon.ico', method='GET')
def get_favicon():
	return static_file('favicon.ico', root='./static/')
    
def launchServer(portToListen):
	run(host='', port=portToListen)
	
def stopServer():
	close()
	