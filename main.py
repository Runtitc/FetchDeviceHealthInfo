import paramiko
import os #to open the file with login and password

#Creating the paramiko object to connect to the convrete device
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
