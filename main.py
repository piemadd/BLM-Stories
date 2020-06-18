#!/usr/bin/python
# coding: utf-8
from flask import Flask, render_template, request, redirect
from mapping import *
from flask_restful import Api, Resource, reqparse
import json
import os
import requests
import numpy as np
import folium
from folium import plugins
from random import randint
import logging

print("libraries done")

logging.basicConfig(filename='logs1.log', level=logging.INFO)

print("logs?")

url = os.getenv("DB_URL")
key = os.getenv("KEY")

app = Flask(__name__)
api = Api(app)

@app.route('/')
def mainPage():
	print("yeet")
	return render_template('index.html')

@app.route('/stories/rand')
def randStory():
	data = requests.get(str(url) + '?auth=' + str(key))
	content = data.content
	content = json.loads(content)
	max = len(content)
	return redirect('https://blm.piemadd.com/stories/' + str(randint(0, max)))

@app.route('/stories/choose')
def chooseStoryPage():
	return render_template('choose.html')

@app.route('/stories/choose/num')
def chooseStory():
	args = request.args
	id = args['id']
	data = requests.get(str(url) + '?auth=' + str(key))
	content = data.content
	content = json.loads(content)
	max = len(content)
	if int(id) > max:
		return "That story does not exist. Please go back and try again."
	return redirect('https://blm.piemadd.com/stories/' + str(id))

@app.route('/mapElement')
def getMap():
	data = requests.get(str(url) + '?auth=' + str(key))
	content = data.content
	content = json.loads(content)
	stuff = []
	x = 0
	while x < len(content):
		temp = content[x]
		stuff.append([temp['lat'], temp['lon']])
		x = x + 1
	x = np.array(stuff)
	m = folium.Map([44.9343385, -93.262231], zoom_start=9, title="BLM Stories Map")
	m.add_children(plugins.HeatMap(x, radius=15))
	html_string = m.get_root().render()
	return html_string

@app.route('/viewMap')
def viewMap():
	html_string = '''<html><head><style>body{margin: 0;}iframe{display: block; background: #000; border: none; height: 100vh; width: 100vw;}</style><title>BLM Stories Map</title></head><body><iframe src="https://blm.piemadd.com/mapElement" title="BLM Stories Map"></iframe></body></html>'''
	return html_string


@app.route('/submit')
def newSub():
    return render_template('submit.html')

@app.route('/viewSubs')
def viewSubs():
    return render_template('submitted.html')
	
@app.route('/stories/<string:id>')
def viewStory(id):
	data = requests.get(str(url) + '?auth=' + str(key))
	content = data.content
	content = json.loads(content)
	x = int(id) - 1
	story = content[x]
	lat = story['lat']
	lon = story['lon']
	g = geocoder.osm([lat, lon], method='reverse')
	try:
		location = g.city + ', ' + g.state + ', ' + g.country
	except:
		location = 'Unknown Location. Manually overrided to ' + str(lat) + ', ' + str(lon)
	rContent = '''<html><head><title>BLM Story #''' + str(id) + '''</title><link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/kognise/water.css@latest/dist/dark.min.css"></head><body><h1>BLM Stories</h1><h2>Name:</h2><p>''' + story['name'] + '''</p><h2>Story</h2><p>''' + story['message'] + '''</p><h2>Story Number</h2><p>''' + str(id) + '''</p><h2>General Location</h2><p>''' + location + '''</p><form action="https://blm.piemadd.com/"><input type="submit" value="Return to Home"/></form></body></html>'''
	return rContent

@app.route('/stories/list')
def listSubs():
	f = open("unfinished/storiesList/1.uhtml", "r")
	a = f.read()
	f = open("unfinished/storiesList/2.uhtml", "r")
	b = f.read()
	buttons = ""
	data = requests.get(str(url) + '?auth=' + str(key))
	content = data.content
	content = json.loads(content)
	x = 0
	while x < len(content):
		buttons = buttons + '''<div class="grid-item"><center><form action="https://blm.piemadd.com/stories/''' + str(x + 1) + '''"><input type="submit" value="&nbsp;''' + str(x + 1) + '''&nbsp;"/></form></center></div>'''
		x = x + 1
	return a + buttons + b
	
	return render_template('submitted.html')

@app.route('/addloc')
def newLoc():
	data = requests.get(str(url) + '?auth=' + str(key))
	args = request.args
	content = data.content
	content = json.loads(content)
	addy = args['addy']
	try:
		lat, lon = getLoc(addy)
	except:
		return "Invalid Location, Please Try again with something more general"
	upload = {}
	upload['lat'] = lat
	upload['lon'] = lon
	upload['message'] = args['message']
	upload['name'] = args['name']
	content.append(upload)
	content = json.dumps(content, separators=(',', ':'))
	requests.put('https://mds-database-524ce.firebaseio.com/.json?auth=' + key, data=content)
	return render_template('thankyou.html')


app.run(host='0.0.0.0',port=8080)