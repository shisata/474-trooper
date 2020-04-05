
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__, static_url_path='/static', static_folder='/static')

from blueprints import login
from blueprints import maps
from blueprints import group
from blueprints import success
from blueprints import routes



