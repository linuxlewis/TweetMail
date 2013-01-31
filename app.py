from flask import Flask, request
import re
from twitter import *
from tweetslice.app import _sendHtmlEmail
from jinja2 import Environment, PackageLoader
from twilio.rest import TwilioRestClient
#def _sendHtmlEmail(fromAddress, toAddress, title, textMessage, htmlMessage, fromName=None, toName=None, attachments=None, ignoreOverride=False, sender=None):

twilio_sid = 'AC6a38eca8cd604f1ab3ea96f8c5838dd6'
twilio_token = 'd7c2e03b4f1f8af4af9f7ad8c3a649b6'
consumer_key = 'Wx2lGU5aLowSXDxFNmMBzg'
consumer_secret = 'pF9BYbosXaRZQaIORc4KNviY29LbtOBdEyfJmaAXnwA'

oauth_token = '1135522998-RMEw1Z7MSmv3yWkFM3TszQX0MzWdkGOpmykVw1e'
oauth_secret = 'ZxZ1ey5qyoUmpV5etMXfm3CktukaM2mVdCAkxIGgo'

app = Flask(__name__)

import logging
from logging.handlers import SMTPHandler
mail_handler = SMTPHandler('smtp.sendgrid.net',
	'noreply@livelovely.com',
	'sam@livelovely.com', 'TweetMail Ate Shit in', credentials=('doug@homeboodle.com', '88gg88'))
mail_handler.setLevel(logging.ERROR)
app.logger.addHandler(mail_handler)

users = {'SerenaKeith':'keith.serena@gmail.com', 'linuxlewis':'sbolgert@gmail.com', '+19178550483':'keith.serena@gmail.com'}

@app.route('/', methods=['GET', 'POST'])
def index():
	#try:
	to = request.form['to']

	#match tweet
	tweet_match = re.search('([\w]*)\+([\d]*)@maintenance.livelovely.com', to)
	reply_user = tweet_match.group(1)
	print reply_user
	in_reply_to = tweet_match.group(2)
	print in_reply_to

	sms_match = re.search('([\d]*)@maintenance.livelovely.com', to)
	from_sms = sms_match.group(1)
	print from_sms

	twitter = False
	sms = False
	if reply_user is not None and in_reply_to is not None:
		user_email = users[reply_user]
		twitter = True
	else:
		sms = True
		user_email = users[from_sms]

	#forward email
	from_ad = request.form['envelope'][1]
	text = request.form['html']
	_sendHtmlEmail(from_ad, user_email, 'RE:Lovely Maintenance Request', None, text, request.form['from'])
	print 'email'

	if twitter is True:
		#create twitter
		t = Twitter(
			auth=OAuth(oauth_token, oauth_secret,
				consumer_key, consumer_secret)
		)
		try:
			tweet = '%s Check your email for your landlord\'s response! Rate their repair by replying 1-5 (5=best) to this tweet.' % ('@'+reply_user)
			t.statuses.update(status=tweet, in_reply_to_status_id=in_reply_to)
			print 'tweet'
		except Exception as ex:
			pass

	if sms is True:
		client = TwilioRestClient(twilio_sid, twilio_token)
		message = client.sms.messages.create(to=from_sms, from_="+14842402676",
		body="Check your email for your landlord\'s response! Rate their repair by replying 1-5 (5=best) to this text.'")
	#except Exception as ex:
	#	raise ex
	#finally:
	return '1'

types = ['washer', 'dryer', 'toilet', 'sink', 'dishwasher', 'broken']
tenet_user = {'+19178550483':{'name':'Serena Keith'}, '+12622275823':{'name':'Sam Bolgert'} }
user = {'email':'sam@livelovely.com', 'name':'Sam Bolgert', 'phone':'+12622275823'}
@app.route('/sms', methods=['GET', 'POST'])
def sms():
	print request.form
	#look for types
	email = False
	for type in types:
		match = re.search(type, request.form['Body'])
		if match is not None:
			print 'Type Email Sent'
			send_email_to_user(user, type, request.form['From'], request.form['Body'])
			email = True
			break
	if email is False:
		send_email_to_user(user, '', request.form['From'], request.form['Body'])
	return '1'

def send_email_to_user(user, type, from_number, text):
	print 'Sending Email'
	c = dict()
	c['type'] = type
	c['name'] = tenet_user[from_number]['name']
	c['text'] = text
	c['first'] = False

	env = Environment(loader=PackageLoader('tweetslice', 'templates'))
	tmp = env.get_template('general.html')
	html = tmp.render({'c':c})
	#html = render('/messages/alert.html')
	from_ad = '%s@maintenance.livelovely.com' % (str(from_number[1:]))

	subject = "Request to fix %s's maintenance issue" % (tenet_user[from_number]['name'])

	_sendHtmlEmail(from_ad, user['email'], subject ,None, html, 'Lovely FixIt', user['name'])

app.run(host='0.0.0.0', port=80)




