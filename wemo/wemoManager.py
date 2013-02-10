#Based on UPNP wemo hacking work from issackelly -> see https://github.com/issackelly/wemo

from libs.miranda import upnp, msearch
import os
import json

class wemoUtils:

	def __init__(self):
		self.conn = upnp()
	
	# Returns list of wemo
	def getListOfWemoOnNetwork(self):
		msearch(0, 0, self.conn, 2)
		listOfWemo = {}	
		i=1
		for index in self.conn.ENUM_HOSTS:
			currentHost = self.conn.ENUM_HOSTS[index]
			currentName = str(currentHost.get('name'))
			if self._isHostAWemo(currentHost) and not self._find_key(listOfWemo,currentName):
				print ("new wemo found : " + currentName + "\n")
				#add "1","XXX.X.XX:XXX"
				listOfWemo.update({str(i):currentName})
				i = i+1
		return listOfWemo
		
	def _isHostAWemo(self,host):
		## works for me but could be test on ..
		return "setup.xml" in host.get('xmlFile') and host.get("name") is not None 
	
	def _find_key(self,dic, val):
		"""return the key of dictionary dic given the value"""
		return [k for k, v in dic.iteritems() if v == val]
	
	def _find_value(self,dic, key):
		"""return the value of dictionary dic given the key"""
		return dic[key]
		
	def _getHostFriendlyName(self, hostInfo, index):
		if hostInfo.get('dataComplete') == False:
			xmlHeaders, xmlData = conn.getXML(hostInfo.get('xmlFile'))
			conn.getHostInfo(xmlData,xmlHeaders,index)
			return str(hostInfo.get('deviceList').get('controllee').get('friendlyName'))
	
	def send(self, host, action, args=None):
		if not args:
			args = {}
		resp = self.conn.sendSOAP(
			host,
			'urn:Belkin:service:basicevent:1',
			"http://"+host+"/upnp/control/basicevent1",
			action,
			args
		)
		return resp
		
	def getState(self,response):
		return self.conn.extractSingleTag(response, 'BinaryState')
		
class wemoManager:
	
	def __init__(self, fileName):
		self.util = wemoUtils()
		self.fileName = fileName
		#load wemo
		self.LIST_OF_WEMO_HOST = self.getWemoFromJsonFile(fileName)
		#if file empty lookup for wemo
		if not self.LIST_OF_WEMO_HOST:
			self.allUpdate()
		else:
			print "Configuration contains "+  str(len(self.LIST_OF_WEMO_HOST)) + " wemo(s)"


	def setWemoToJsonFile(self,fileName,wemoList):
		wemoInJson = json.dumps(wemoList)
		print ("writing : "+ wemoInJson + " to " + fileName)
		with open(os.getcwd()+'/'+fileName, 'w') as f:	
			f.write(wemoInJson)
		return wemoInJson
				
	def getWemoFromJsonFile(self,fileName):
		print ("reading configuration file : "+ fileName)
		wemoDict = {}
		try: 
			with open(os.getcwd()+'/'+fileName, 'r') as f:	
				wemoDict = json.loads(f.read())
		except IOError: 
			print 'There is no configuration file named ' + fileName
			return wemoDict
		
		return wemoDict
	
	# Gets the value of the id wemo
	def status(self,id):
		print ("get status of : "+ id)
		controlURL = self.LIST_OF_WEMO_HOST.get(id)
		if  controlURL is not None:
			resp = self.util.send(controlURL, 'GetBinaryState')
			tagValue = self.util.getState(resp)
			return True if tagValue == '1' else False
		else:
			return False
	
	#    Turns on the switch that it finds.
	#     BinaryState is set to 'Error' in the case that it was already on.
	def on(self,id):
		print ("Put on : "+ id)
		controlURL = self.LIST_OF_WEMO_HOST.get(id)
		if  controlURL is not None:
			resp = self.util.send(controlURL,'SetBinaryState', {'BinaryState': (1, 'Boolean')})
			tagValue = self.util.getState(resp)
			return True if tagValue in ['1', 'Error'] else False
		else:
			return False
	
	#    Turns on the switch that it finds.
	#     BinaryState is set to 'Error' in the case that it was already off.
	def off(self,id):
		print ("Put off : "+ id)
		controlURL = self.LIST_OF_WEMO_HOST.get(id)
		if  controlURL is not None:
			resp = self.util.send(controlURL,'SetBinaryState', {'BinaryState': (0, 'Boolean')})
			tagValue = self.util.getState(resp)
			return True if tagValue in ['0', 'Error'] else False
		else:
			return False
		
		
	#    Turns on all the switch
	def allOn(self):
		for index in self.LIST_OF_WEMO_HOST:
			self.on(index)
			
	#    Turns on all the switch
	def allOff(self):
		for index in self.LIST_OF_WEMO_HOST:
			self.off(index)
			
	#    Get status of all the switch and return it in dict format
	def allStatus(self):
		statusDict = {}
		for index in self.LIST_OF_WEMO_HOST:
			curSatus = self.status(index)
			statusDict.update({str(index):str(curSatus)})
		return statusDict
			
	#    Update list of Wemo and return it in dict format
	def allUpdate(self):
		print ("Update wemo configuration")
		listOfWemo = self.util.getListOfWemoOnNetwork()
		print "allUpdate :: Find "+  str(len(listOfWemo)) + " wemo"
		self.setWemoToJsonFile(self.fileName,listOfWemo)
		self.LIST_OF_WEMO_HOST = listOfWemo
		return listOfWemo
	