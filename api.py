#!/usr/bin/python
# coding: utf-8
from flask import Flask, render_template, request
from mapping import *

app = Flask(__name__)

@app.route('/')
def mainPage():
    return render_template('index.html')

@app.route('/addloc')
def newLoc():
	name = request.headers['name']
	addy = request.headers['location']
	story = request.headers['story']
	lat, lon = getLoc(addy)


if __name__ == '__main__':
    app.run(debug=True)