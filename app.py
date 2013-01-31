from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
	print 'yayyyyy'
	print request
	r = request.params
	#pull user

app.run(host='0.0.0.0', port=80)




