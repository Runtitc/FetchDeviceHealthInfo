import os
import sys
import logging
import time
import re #to parse the config file
class Config:
	'This class describes the infomration for configuration file'
	

	def __init__(self):
		logging.basicConfig(filename='logs/'+str(time.time())+'.log',level=logging.DEBUG)
		logging.info('Configuration file.')
		
		#attributes in the file
		self.Attributes={
		'Time':"",
		'Host':"",
		'Path':"",
		'Template':""
		}
		self.regexes = {
			'Time' : r'(?<=Time: ).*(?=)',
			'Host' : r'(?<=Host \(IP\): ).*(?=)',
			'Path' : r'(?<=Path: ).*(?=)',
			'Template' : r'(?<=Template: ).*(?=)'}

		self.commandsfiles = self.buildTemplatesMenu()

		self.readFileToString()

	def updateConfigFile(self):		
		logging.info('Updating the file.')

		checkU=0
		os.system("clear")
		try:
			checkU = int(raw_input(\
				"\n========Edit file mode========\n ENTER - Default mode\n" \
				" 1 - nano\n" \
				" 2 - gedit\n" \
				"\nConfiguration mode - Set Action: "
			))
		except ValueError:
			pass

		if checkU==0:
			self.subUpdateConfigFile()			
		elif checkU==1 or checkU==2:
			loc=""
			try:
				loc = raw_input("Path to the config file: ")
			except ValueError:
				pass

			if loc=="":
				os.system("nano config") if checkU==1 else os.system("gedit config")
			else:
				print "Exec: nano " + loc + "/config"
				os.system("nano " + loc + "/config") if checkU==1 else os.system("gedit " + loc + "/config")
		
	def subUpdateConfigFile(self):
		self.configFile = open('../config', 'w')

		TimeUpdate = raw_input("Time to update: ")
		TimeUpdate += raw_input("Unit [ms/s]: ")
		self.Attributes["Time"] = TimeUpdate
		self.configFile.write("Time: " + TimeUpdate + "\n")
		
		HostUpdate = raw_input("Host IP address: ")
		self.Attributes["Host"] = HostUpdate
		self.configFile.write("Host (IP): " + self.getHost() + "\n")

		PathUpdate = raw_input("Path \n [Enter] - if current folder")
		if (PathUpdate == ""):
			PathUpdate = os.path.dirname(os.path.realpath(__file__)) #path to the current script location
			#it was printing the folder where was the config.py placed, so I need to delete this folder form the path
			PathUpdate =  PathUpdate.replace("/modules", "")
			self.Attributes["Path"] = PathUpdate
			#print self.Attributes["Path"]
			self.configFile.write("Path: " + PathUpdate + "\n")

		print "\n"
		otpt = os.system("ls ../commands")
		if otpt=="":
			print "Create Templates with commands in the Commands folder"
		else:	
			try:
				while True:
					TemplateUpdate = raw_input(
						"Choose one of the above templates: "
						)
					if TemplateUpdate in self.commandsfiles:
						self.Attributes["Template"] = TemplateUpdate
						self.configFile.write("Template: " + self.getTemplate() + "\n")
						break
					else:
						print "Not found\n"
			except KeyboardInterrupt:
				self.Attributes["Template"] = "Not specified"
				self.configFile.write("Template: " + self.getTemplate() + "\n")
		logging.info('File updated.')

		self.configFile.close()
		logging.info('File closed.')
		


		#tutaj dopisac jeszcze manual/automaty

	def readFileToString(self):
		#here we are reading particular attributes: Time, Path, Host.
		logging.info('Reading the file.')
		self.configFile = open("../config", "r+")
		self.configFileotpt = self.configFile.read()

		
		#print " A tutaj mamy config file otp:\n"
		#print self.configFileotpt
		#loop through the dictionary of regexes and match to the particular attributes
		
		for key,value in self.regexes.iteritems():
			#print key
			try:
				checking_regex = re.search(value, self.configFileotpt)
			except AttributeError:
				checking_regex="N/A"

			if checking_regex:
				#print checking_regex.group(0)
				self.Attributes[key]=checking_regex.group(0)
			else:
				self.Attributes[key]="N/A"

			#print self.Attributes[key]
				
		#print self.configFileotpt
		return self.configFileotpt

	def buildTemplatesMenu(self):
		os.chdir(os.path.dirname(os.path.realpath(__file__))+"/../commands")
		commands = os.listdir(os.path.dirname(os.path.realpath(__file__))+"/../commands")
		os.chdir(os.path.dirname(os.path.realpath(__file__))+"/../modules")

		return commands

	def replacePartConfig(self, regex, forWhat):
		self.configFile = open("../config", "r")
		self.configFileotpt = self.configFile.read()
		#key substitution 
		self.configFileotpt = re.sub(self.regexes[regex], forWhat, self.configFileotpt)
		self.configFile.close()
		#adding modified text 
		self.configFile = open("../config", "w")
		self.configFile.write(self.configFileotpt)
		self.readFileToString()

	def getTime(self):
		return self.Attributes["Time"]

	def getHost(self):
		return self.Attributes["Host"]

	def getPath(self):
		return self.Attributes["Path"]

	def getTemplate(self):
		return self.Attributes["Template"]

def promptQuestion(reason):
	print reason
	text=""
	while 1==1:
		additionalInformation = raw_input()
		if additionalInformation!="":
			text += additionalInformation + "\n\n"
		else:
			break
	return text