from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	print 'yayyyyy'
	print request
	r = request.params
	#pull user
	return '1'

app.run(host='0.0.0.0', port=80)




