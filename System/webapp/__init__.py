from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from datetime import datetime

webapp = Flask(__name__)
Bootstrap(webapp)

#@webapp.route('/')
#def index():
#  return render_template('index.html')


