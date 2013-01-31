from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
	print 'yayyyyy'
	print request
	r = request.params
	#pull user

app.run(port=80)




