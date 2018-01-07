import sherlock

class Info:
	'This class defines template for the Engineering ticketing system'
	

	def __init__(self, managedIP):
		self.BusinessImpact = "********************\nBusiness Impact:\n"
		self.ProblemDescription = "********************\nProblem Description:\n"
		self.CurrentStatus = "********************\nCurrent Status:\n"
		self.ActionPlan = "********************\nAction Plan:\n"
		self.Documentation = "********************\nDocumentation:\n"
		self.sherlockObj = sherlock.Sherlock("216.141.34.83") # this is jumphost IP
		self.managedIP = managedIP
	#number is the priority enter-unknown ; 1-low ; 2-medium ; 3-high
	def addBussinessImpact(self, number):
		print "\n**Adding Bussiness Impact**\n\n"

		if number==1:
			self.BusinessImpact += "Low\n\n"
		elif number==2:
			self.BusinessImpact += "Medium\n\n"
		elif number==3:
			self.BusinessImpact += "High\n\n"
		else:
			self.BusinessImpact += "Unknown\n\n"

	def addProblemDescription(self, text):
		print "**Adding Problem Description**\n\n"

		self.ProblemDescription += text + "\n"
		self.ProblemDescription += promptQuestion("Any other information regarding the problem? ([E] to skip; 2x[E] to finish typing)")

	def addActionPlan(self, number):
		print "\n**Adding Action Plan**\n\n"

		self.ActionPlan += promptQuestion("Do you wan to add some notes?")
		
		if number==1:
			self.ActionPlan += "Escalating to tier 2 for further investigation\n\n"
		elif number==2:
			self.ActionPlan += "Closure\n\n"
		elif number==3:
			self.ActionPlan = raw_input("Type, what is the current status: ")
		else:
			self.ActionPlan += "Monitoring\n\n"


	def addCurrentStatus(self):
		print "\n**Adding Current Status**\n\n"
		
		self.CurrentStatus += promptQuestion("What is the current status of a ticket? ([E] to skip; 2x[E] to finish typing)")
		
	def basicChecks(self):
		print "\n**Adding Documentation**\n\n"

		self.Documentation += "Availability of a device checked: \n" 
		self.Documentation += self.sherlockObj.pingD(self.managedIP)
		self.Documentation += "\nSSH/HTTPS connectivity information: \n"
		self.Documentation += self.sherlockObj.checkTelnet(self.managedIP, 22)
		self.Documentation += self.sherlockObj.checkTelnet(self.managedIP, 443)

	def addDocumentation(self, sentence):
	## here will be everything that goes from the shell, I mean the output..

		print "\n**Adding Documentation**\n\n"
		self.Documentation += sentence




	def showTemplate(self):
		print self.BusinessImpact+self.ProblemDescription+self.CurrentStatus+self.ActionPlan+self.Documentation



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