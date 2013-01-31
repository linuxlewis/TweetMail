from flask import Flask, request
import re
from twitter import *
from tweetslice.app import _sendHtmlEmail
#def _sendHtmlEmail(fromAddress, toAddress, title, textMessage, htmlMessage, fromName=None, toName=None, attachments=None, ignoreOverride=False, sender=None):

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

users = {'SerenaKeith':'keith.serena@gmail.com', 'linuxlewis':'sbolgert@gmail.com'}

@app.route('/', methods=['GET', 'POST'])
def index():
	#try:
	to = request.form['to']
	tweet_match = re.search('([\w]*)\+([\d]*)@maintenance.livelovely.com', to)
	reply_user = tweet_match.group(1)
	print reply_user
	in_reply_to = tweet_match.group(2)
	print in_reply_to

	#forward email
	from_ad = request.form['envelope'][1]

	text = request.form['html']

	user_email = users[reply_user]

	_sendHtmlEmail(from_ad, user_email, 'RE:Lovely Maintenance Request', None, text, request.form['from'])
	print 'email'

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
	#except Exception as ex:
	#	raise ex
	#finally:
	return '1'

@app.route('/sms', methods=['GET', 'POST'])
def sms():
	print request.form
	return '1'

app.run(host='0.0.0.0', port=80)




