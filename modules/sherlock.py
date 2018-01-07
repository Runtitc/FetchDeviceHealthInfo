import os #basic system commands like whether some directory exist
import paramiko
import getpass
import time

class Sherlock:
	'This class defines functions to operate in the SHELL'
	output = 0

	def __init__(self, ip):
		
		self.ssh = paramiko.SSHClient()
		self.fileoutput = open('../Infos/info.'+str(time.time()), 'w+') #output for docum.
		self.login(ip)

	def login(self, ip):
		login = ""
		passw = ""
		print "login processing.."

		#fetch necessary files
		if os.path.isfile('../../passToTheRemoteMachine'):
			file = open("../../passToTheRemoteMachine", "r")
			login = file.readline()
			login = login.strip()

			passw = file.readline()
			passw = passw.strip()
		
		#if not, then ask user for input:
		else:
			print "You can create the file \"pass\" in the upper folder and put the login and password seperated by new line character"
			login = getpass.getpass("Enter login:\n")
			passw = getpass.getpass("Enter password:\n")

		#against rejection of the host keys in the known hosts:
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		
		#connection:
		try:
			conn = self.ssh.connect(ip, port=22, username=login, password=passw)
		except paramiko.AuthenticationException:
			print "Wrong!"
			return False
		print "Correct credentials!"
		return True

	def makeCommand(self, jebcommand):
		stdin, stdout, stderr = self.ssh.exec_command(jebcommand)
		output = stdout.readlines()
		output2 = stderr.readlines()
		print "".join(output)
		print "".join(output2)
		

		# Tutaj sprawdzam, co sie dieje z bledami

		#najpierw czy w ogole bledy sa jakies
		#print output2
		if not output2:
			print "stderr jest empty"
		else:
			print "stderr nie jest empty"
			#najpierw lacze wszystkie elementry listy w calosc
			stringoslacozny = "".join(output2)
			
			#tworz znowu liste dzielac po spacjach
			items = []
			items = stringoslacozny.split(" ")
			#for i in items:
			#	print i
			if "command not found" in stringoslacozny:
				print "Nie znaleziono takiej komendy"
			else:
				print "Znaleziono taka komende, spokojnie"

		#Obrabiam tekscik, ttaj bedziemy wykrywac konkretne stringi i odpowiednio reagowac, np
		self.detectSomething(output)




	def detectSomething(self, sequenceString):
		#print sequenceString
		for line in sequenceString:
			if "0% packet loss" in line:
				print "Pingnelo sie fajnie"
				self.addInfo("pingnelo sie fajnie..."+"".join(sequenceString))

	def addInfo(self, sequenceStringInfo):
		self.fileoutput.write(sequenceStringInfo)


	def showInfo(self):
		pass