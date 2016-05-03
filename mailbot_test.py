import imaplib, email, getpass
import time
import email.message
import email
import imaplib_connect
import pytz
import dateutil
import smtplib
from datetime import timedelta
from email.utils import getaddresses
from mailbot import MailBot, register, Callback

from datetime import datetime, timedelta
import csv
import numpy
import pandas as pd
import math

# Email settings
imap_server = 'imap.gmail.com'
imap_user = 'nediyana_daskalova@brown.edu'
imap_password = ''

mailbot = MailBot(imap_server, imap_user, imap_password,port=993, ssl=True)

def make_prediction(incoming_email, test_features):
	new_emailer = 0
	incoming = []
	outgoing = []
	
	list_feature = {}
	cc_feature = {}
	reply_time_feature = {}
	weekday_feature = {}
	for line in csv.reader(open("/home/nediyana/course/a4/all_mail.csv")):
		if len(line)>5:
			if 'from' in line[5] and 'nediyana_daskalova' in line[5]:
				if 'to' in line[6]:
					receiver = line[6].split()
					if len(receiver)>1:
						if receiver[1] == incoming_email:
							outgoing.append(line[4])

		if len(line)>5:
			if 'from' in line[5]:
				sender = line[5].split()
				if len(sender)>1:
					if sender[1] == incoming_email:
						incoming.append(line[0])

	replied_to = []
	for item in incoming:
		if item in outgoing:
			# replied_to is a list of all the emails I have replied to.
			replied_to.append(item)

	# If replied_to is empty, it means I have never replied to this person
	# If they have emailed me many times and I have not replied, I probably won't reply, so 'predicted time' will be set to 'never'. 

	if len(replied_to) < 1 and len(incoming) > 0:
		new_emailer = 0
		return 'never'
	elif len(replied_to) < 1 and len(incoming) == 0:
		new_emailer = 1
		for line in csv.reader(open("/home/nediyana/course/a4/all_mail.csv")):
			if len(line)>5:
				if 'from' in line[5] and 'nediyana_daskalova' in line[5]:
					if 'to' in line[6]:
						receiver = line[6].split()
						if len(receiver)>1:
							if '2016' in line[2]:
								email_date = dateutil.parser.parse(line[2])
								difference = (datetime.now(pytz.timezone('US/Eastern'))- email_date).total_seconds()
								if difference < 604800:	
									new_emailer = 1						
									outgoing.append(line[4])

			if len(line)>5:
				if 'from' in line[5]:
					sender = line[5].split()
					if len(sender)>1:
						incoming.append(line[0])

		replied_to = []
		for item in incoming:
			if item in outgoing:
				# replied_to is a list of all the emails I have replied to.
				replied_to.append(item)
		

		

	else:
		new_emailer = 0
		print 'hi'
		
		# If they have never email me before, then I will calculate how long it has taken me to answer emails in the last few days and ive that as a prediction. 

	# Otherwise, just calculate reply rate based on the sender. 
	if 1 ==1:
		reply_times = []
		for item in replied_to:
			for line in csv.reader(open("/home/nediyana/course/a4/all_mail.csv")):
				if line[0] == item:
					date_incoming = line[2]
					date_in = date_incoming.split()[:3]
					# find out day of the week
					if date_in[1] == 'Jun':
						date_in[1] = 6
					elif date_in[1] == 'Feb':
						date_in[1] = 2
					elif date_in[1] == 'Mar':
						date_in[1] = 3
					elif date_in[1] == 'Apr':
						date_in[1]=4
					elif date_in[1] == 'Aug':
						date_in[1]=8
					elif date_in[1] == 'Sep':
						date_in[1]=9
					elif date_in[1] == 'Oct':
						date_in[1]=10
					elif date_in[1] == 'Nov':
						date_in[1]=11
					elif date_in[1] == 'Dec':
						date_in[1]=12
					elif date_in[1] == 'Jan':
						date_in[1]=1
					elif date_in[1] == 'May':
						date_in[1]=5
					elif date_in[1] == 'Jul':
						date_in[1]=7
					weekday_feature[line[0]] = datetime(int(date_in[2]), int(date_in[1]), int(date_in[0])).weekday()

					time_in = date_incoming.split()[3]
					timezone_in = date_incoming.split()[4]
					cc_ed = line[6].split()
					cc_feature[line[0]] = len(cc_ed)-1

					if 'lists' in line[6] or 'lists' in line[5]:
						list_feature[line[0]] = 1
					else:
						list_feature[line[0]] = 0

				if len(line)>4:
					if line[4] == item and 'nediyana' in line[5]:
						date_outgoing = line[2]
						date_out = date_outgoing.split()[:3]
						if date_out[1] == 'Jun':
							date_out[1] = 6
						elif date_out[1] == 'Feb':
							date_out[1] = 2
						elif date_out[1] == 'Mar':
							date_out[1] = 3
						elif date_out[1] == 'Apr':
							date_out[1]=4
						elif date_out[1] == 'Aug':
							date_out[1]=8
						elif date_out[1] == 'Sep':
							date_out[1]=9
						elif date_out[1] == 'Oct':
							date_out[1]=10
						elif date_out[1] == 'Nov':
							date_out[1]=11
						elif date_out[1] == 'Dec':
							date_out[1]=12
						elif date_out[1] == 'Jan':
							date_out[1]=1
						elif date_out[1] == 'May':
							date_out[1]=5
						elif date_out[1] == 'Jul':
							date_out[1]=7

						time_out = date_outgoing.split()[3]
						timezone_out = date_outgoing.split()[4]


			if date_in == date_out or not(date_in==date_out):
				# http://stackoverflow.com/questions/3096953/difference-between-two-time-intervals-in-python
				FMT = '%H:%M:%S'
				tdelta = datetime.strptime(time_out, FMT) - datetime.strptime(time_in, FMT)

				# http://stackoverflow.com/questions/2119472/convert-a-timedelta-to-days-hours-and-minutes
				tdelta_seconds = float(tdelta.seconds)
				reply_times.append(tdelta_seconds)

				reply_time_feature[item] = tdelta_seconds
				#print 'Reply TIME feature', reply_time_feature[item]

		# # # # # LINEAR REGRESSION # # # # # #

		with open('/home/nediyana/course/a4/features.csv', 'wb') as csvfile:
			spamwriter = csv.writer(csvfile)
			spamwriter.writerow(['cc_feature', 'weekday_feature','reply_time', 'list_feature'])
			for item in reply_time_feature:
				spamwriter.writerow([str(cc_feature[item]), str(weekday_feature[item]), str(reply_time_feature[item]), str(list_feature[item])])

		data = pd.read_csv('/home/nediyana/course/a4/features.csv')
		data.head()

		# create X and y
		feature_cols = ['cc_feature', 'weekday_feature', 'list_feature']
		X = data[feature_cols]
		y = data.reply_time

		# follow the usual sklearn pattern: import, instantiate, fit
		from sklearn.linear_model import LinearRegression
		lm = LinearRegression()
		lm.fit(X, y)

		# print intercept and coefficients
		# print lm.intercept_
		print lm.coef_

		# pair the feature names with the coefficients
		print 'pair features with coeffs', zip(feature_cols, lm.coef_)

		# predict for a new observation
		predicted_reply_time =  lm.predict([test_features[0], test_features[1], test_features[2]])
	
		# calculate the R-squared
		# print 'SCORE', lm.score(X, y)

		# calculate average reply time and reply rate for this sender
		average_reply_time = numpy.mean(reply_times)
		reply_rate = float(len(outgoing))/float(len(incoming))
		return  [str(float(predicted_reply_time)/float(3600)), float(average_reply_time)/float(3600),reply_rate, new_emailer]

	# http://stackoverflow.com/questions/4048651/python-function-to-convert-seconds-into-minutes-hours-and-days

	def GetTime(input_seconds):
	    sec = timedelta(seconds=int(input_seconds))
	    d = datetime(1,1,1) + sec

	    return ("%d:%d:%d:%d" % (d.day-1, d.hour, d.minute, d.second))



	
	# possible features: whether I am the only one this message was sent to, what percentage of the time I have replied to this person, average reply time for this person so far, how many email I have received 
	# how busy I am based on my recent email replies - so based on the number of emails i got in the last 24 hours, how many of them have I replied to? those that i have replied to, how long did it take me to reply to them?
	# whether it's the weekend, time of day, length of email


	# for item in reply_time_feature:
	# 	print 'time', reply_time_feature[item] # EXCEPT THIS IS NOT A FEATURE! this is the result, so i need another feature
	# 	print 'cc', cc_feature[item]
	# 	print 'weekeday', weekday_feature[item]
		# if cc_feature is equal to 1, then I am the only person who got this email


	
class MyCallback(Callback):

    def trigger(self):
        features = []
	date = self.message['Date'].strip()
	if "<" in self.message['From'].strip():
        	incoming_email = self.message['From'].strip().split("<")[1].strip(">")
	else:
		incoming_email = self.message['From'].strip()
	if "<" in self.message['To'].strip():
       		receiver = self.message['To'].strip().split("<")[1].strip(">")	

	else:
		receiver = self.message['To'].strip()

	receiver = 'nediyana_daskalova@brown.edu'
	subject = self.message['Subject']
	# print "In reference to " + subject

	if self.message['Cc']:
		cc_ed = self.message['Cc'].strip().split(',')

	else:
		cc_ed = []
	features.append(len(cc_ed))
	date_in = date.split(',')[1].split()[:3]

	if date_in[1] == 'Jun':
		date_in[1] = 6
	elif date_in[1] == 'Feb':
		date_in[1] = 2
	elif date_in[1] == 'Mar':
		date_in[1] = 3
	elif date_in[1] == 'Apr':
		date_in[1]=4
	elif date_in[1] == 'Aug':
		date_in[1]=8
	elif date_in[1] == 'Sep':
		date_in[1]=9
	elif date_in[1] == 'Oct':
		date_in[1]=10
	elif date_in[1] == 'Nov':
		date_in[1]=11
	elif date_in[1] == 'Dec':
		date_in[1]=12
	elif date_in[1] == 'Jan':
		date_in[1]=1
	elif date_in[1] == 'May':
		date_in[1]=5
	elif date_in[1] == 'Jul':
		date_in[1]=7
	weekday_feature = datetime(int(date_in[2]), int(date_in[1]), int(date_in[0])).weekday()	
	features.append(weekday_feature)

	if 'lists' in self.message['To'].strip():
		list_feature = 1
	else:
		list_feature = 0
	features.append(list_feature)

	response = "Hi!\nThank you for the email. This is an auto-generated message for a class assignment  in reference to your email with subject '" + subject + "'. Based on Nediyana's recent email reply rate and the email history between the two of you, she will respond to you in about RESPONSE_TIME. She has replied to PERCENTAGE% of your emails, and on average it has taken her AVERAGE_REPLY_TIME to reply to you.\nBest, Nediyana\'s Auto Responder."

	predicted_time = make_prediction(incoming_email, features)

	# if this is a new emailer, he/she gets a special response
	if predicted_time[3] == 1:
		response= "Hi!\nThank you for the email. This is an auto-generated message for a class assignment in reference to your email with subject ' " + subject + "'. Based on Nediyana's recent email reply rate, she will respond to you in about RESPONSE_TIME. She has replied to PERCENTAGE% of her incoming emails in the last week, and on average it has taken her AVERAGE_REPLY_TIME to reply to them.\nBest, Nediyana\'s Auto Responder."

	# if predicted is 'never', that means that I have never replied to this person and I never will
	if predicted_time == 'never':
		response = "Hi!\nThank you for the email. This is an auto-generated message for a class assignment in reference to your email with subject '" + subject + "'. Based on Nediyana's recent email reply rate and the email history between the two of you, she will never respond to you. \nBest, Nediyana\'s Auto Responder."
	else:
		
		predicted_hours = int(predicted_time[0].split('.')[0])
		predicted_minutes = math.ceil(float("0."+predicted_time[0].split('.')[1])*60)
		average_hours = int(str(predicted_time[1]).split('.')[0])
		average_minutes =math.ceil(float("0."+str(predicted_time[1]).split('.')[1])*60)
		response = response.replace('AVERAGE_REPLY_TIME', (str(average_hours) +" hours and {:.0f} minutes".format(float(average_minutes))))
		response = response.replace('PERCENTAGE', '{:.0f}'.format(float(predicted_time[2]*100)))

		if predicted_hours > 1:
			response = response.replace('RESPONSE_TIME',(str(predicted_hours) +" hours and {:.0f} minutes".format(float(predicted_minutes))))
		else:
			if predicted_minutes < 5:
				response = response.replace('RESPONSE_TIME', "5 minutes" )

			else:
				response = response.replace('RESPONSE_TIME', str(int(predicted_minutes)) + " minutes" )

	c = imaplib.IMAP4_SSL(imap_server)
	c.login(imap_user, imap_password)
	try:
		# add a draft to my gmail
		# http://bioportal.weizmann.ac.il/course/python/PyMOTW/PyMOTW/docs/imaplib/index.html#
		if predicted_time == 'never':
	    		c.append("[Gmail]/Drafts", '', imaplib.Time2Internaldate(time.time()), str(email.message_from_string(response)))

		# send an auto response!
		else:
		#if ('jeff' in incoming_email) or 
		#if 'nediyana' in incoming_email:		
			msg = response
			# Send the message via our own SMTP server
			# calculate average reply time for this sender
			s = smtplib.SMTP('smtp.gmail.com', 587)
			s.starttls()
			s.login(imap_user, imap_password)
			s.sendmail(imap_user, [incoming_email], msg)
			s.quit()
		
	finally:
	    try:
		c.close()
	    except:
		pass
	    c.logout()

# register your callback
register(MyCallback)

# check the unprocessed messages and trigger the callback
mailbot.process_messages()
print 'processing'

