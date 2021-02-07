from flask import Flask, request, make_response, jsonify
from tinydb import TinyDB, Query

import subprocess
from datetime import datetime as dt 

db = TinyDB('db.json')

app = Flask(__name__)

@app.route ('/', methods=['GET'])
def index():
	return ("RESTful Script server is running")

@app.route('/api/cec', methods=['POST'])
def send_cec():
	tvIP = request.form["tv"]
	commands = request.form.getlist('commands')
		
	for command in commands:
		subprocess.call(['./cec.sh', tvIP, command])
		
		if command == 'E0 04':
			db.upsert({'device': tvIP, 'status': 'on'},Query()['device'] == tvIP)
		elif command == 'E0 36': 
			db.upsert({'device': tvIP, 'status': 'off'},Query()['device'] == tvIP)
		elif command == 'EF 82 20 00':
			db.upsert({'device': tvIP, 'input': 'HMDI2'},Query()['device'] == tvIP)	
		elif command == 'EF 82 10 00':
			db.upsert({'device': tvIP, 'input': 'HDMI1'},Query()['device'] == tvIP)

		result = db.get(Query()['device'] == tvIP)

		if result != None:
			return  jsonify ({'status': result['status']})
		else:
			return  jsonify({'status': 'off'})

@app.route('/api/cec', methods=['GET'])
def cec_status():
	tvIP = request.args.get("tv")
	result = db.get(Query()['device'] == tvIP)

	if result != None:
		print(result)
		return jsonify ({'status': result['status']})
	else: 
		return jsonify({'status' :'off'})

@app.route('/api/jap', methods=['POST'])
def change_input():
	
	state = None
	
	state = request.form["turn"]
	room = request.form["room"]
	source = request.form["source"]
	offsource = "11"

	if  state == 'on':
		subprocess.call (['./changejap.sh',room,source,"switchon"])
		db.upsert({'room': room,'source' : source, 'status': state},Query()['room'] == room)
		return jsonify ({'status': "on"})

	elif state == 'off':
		subprocess.call(['./changejap.sh',room,offsource,"switchoff"])
		db.upsert({'room': room, 'source': source, 'status': state}, Query()['room'] == room)
		return jsonify ({'status': "off"})
	else:
		result = db.get(Query()['room'] == room)
		return jsonify ({'status': result['status']})

@app.route('/api/jap', methods=['GET'])
def status():
	room = request.args.get("room")
	source = request.args.get("source")	
	result = db.get((Query()['room'] == room) & (Query()['source'] == source))	
	
	if result == None:
		return jsonify ({'status' : "off"})
	else:
		print (result)
		return jsonify ({'status' : result['status']})


if __name__== '__main__':
 app.run(host="0.0.0.0", port=1906)
