#!/usr/bin/python

import paramiko
import sys
import os #to open the file with login and password
from modules import sherlock
from modules import config
import os


while True:
	check=0
	try:	
		try:
			os.system("clear")
			check = int(raw_input(	
				"\n========Main========\n Enter - Configuration file\n" \
				" 1 - Run program\n" \
				" 2 - Exit program (Ctr-c)" \
				"\nSet Action: "
			))

		except (ValueError):
			pass
			
		#Configuration file object
		config_object = config.Config()

		os.system("clear")
		if check==0:
			try:
				check = int(raw_input(	
					"\n========Config File Menu========\n"\
					" Enter - Read file\n" \
					" 1 - Override file\n" \
					" 2 - exit\n" \
					"\nConfiguration file - Set Action: "
					#" 3 - ---\n:  \
				))
			except (ValueError):
				pass

			if check==0:
				#fetching all the necessary information from the configuration file
				print config_object.readFileToString()
				raw_input("\nPress Enter to continue...")


			elif check==1:
				config_object.updateConfigFile()
				raw_input("\nPress Enter to continue...")
			elif check==2:
				pass

		elif check==1:
			while True:	
				#running menu to choose the right action
				check2 = 0
				directories = config_object.buildTemplatesMenu()

				if config_object.getTemplate():
					current_command = config_object.getTemplate()
				else:
					current_command = "template not specified"
				 
				try:
					os.system("clear")
					check2 = int(raw_input(
						"\n========Fetch Device Info========\n\n" \
						"Enter - Fetch information ("+current_command+") \n" \
						" 1 - Modify templates\n" \
						" 2 - Choose template\n" \
						" 3 - exit\n" \
						"\n Set Action: "
						)) 

				except ValueError:
					pass
				config_object.readFileToString()

				if check2==0: 
					sherlock_object = sherlock.Sherlock(str(config_object.getHost()))
					

					lines = [line.rstrip('\n') for line in open('../commands/'+config_object.getTemplate())]
					for i in lines:
						print i
						sherlock_object.makeCommand(i)
					
					raw_input("\nPress Enter to continue...")

				elif check2==1:
					os.system("clear")
					counter = 1
					counterlist = {}
					if len(directories):
						print "Available Templates:\n"
						for command in directories:
							print str(counter)+": "+command 
							counterlist[counter] = command
							counter += 1
						print counterlist
						check = raw_input("Which one modify? : ")
						#print os.system("pwd")
						if check in directories:
							os.system(
								"nano "+ os.path.dirname(os.path.realpath(__file__))+"/../commands/"+ str(check))
						elif counterlist[int(check)] in directories:
							os.system(
								"nano "+ os.path.dirname(os.path.realpath(__file__))+"/../commands/"+ counterlist[int(check)])
						else:
							print "Template name does not match"
					else:
						raw_input("Templates not found")
				elif check2==2:
					otpt = os.system("ls ../commands")
					check = raw_input("Which one choose? : ")
					
					#checking if template exist
					if check in directories:
						config_object.replacePartConfig("Template", check)
					else:
						print "Bad format"

				elif check2==3:
					break

		elif check==2:
			print "Goodbye"
			sys.exit() 

	except KeyboardInterrupt:
		print "\nSystem: Goodbye"
		sys.exit()



	#Creating the paramiko object to connect to the convrete device
	'''
	ssh = paramiko.SSHClient()


	#donwload the neccessary login/password from an appropriate file
	if os.path.isfile('../passToTheRemoteMachine'):
					file = open("../passToTheRemoteMachine", "r")
					login = file.readline()
					login = login.strip()

					passw = file.readline()
					passw = passw.strip()


	#against rejection of the host keys in the known hosts:
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	#connection:
	ssh.connect('localhost', port=22, username=login, password=passw)

	print ssh.get_transport().is_active()

	stdin, stdout, stderr = ssh.exec_command('expert')
	checking = stdout.readlines()
	checking_error = stderr.readlines()
	for l in checking:
		print l

	print len(checking) # +"\n" + str(stdout) +"\n" + str(stderr)
	print "".join(checking)
	print "".join(checking_error)
	'''
