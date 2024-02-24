#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Flask
from flask_cors import CORS
from mongoengine import connect

from Shared.configs import (
    SECRET_KEY,APP_HOST,APP_PORT,
    DB_HOST,DB_NAME,DB_USERNAME,DB_PASSWORD
)
from Agents.routes import agnt_bp
from Users.routes import users_bp
from SysData.routes import sys_data_bp
from Session.routes import session_bp
from SystemInfo.routes import sys_info_bp
from SystemUsers.routes import sys_users_bp
from SystemInstalledApps.routes import sys_apps_bp
from SystemServices.routes import sys_srvc_bp
from SystemLastLogons.routes import sys_last_logons_bp
from InformationalData.routes import inf_data_bp
from PipPackages.routes import sys_pip_pkgs_bp

import socket
##############################################################################

# Configs
##############################################################################

# App Config
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# DB Config
db = connect(
    host     = DB_HOST,
    db       = DB_NAME,
    username = DB_USERNAME, 
    password = DB_PASSWORD
)

CORS(app)

##############################################################################


# Blueprints
##############################################################################
app.register_blueprint(agnt_bp, url_prefix='/agent')
app.register_blueprint(users_bp, url_prefix='/user')
app.register_blueprint(sys_data_bp, url_prefix='/data')
app.register_blueprint(session_bp, url_prefix='/session')

app.register_blueprint(sys_info_bp, url_prefix='/sysinfo')
app.register_blueprint(sys_users_bp, url_prefix='/sysusers')
app.register_blueprint(sys_last_logons_bp, url_prefix='/sysusers/lastlogons')
app.register_blueprint(sys_apps_bp, url_prefix='/sysapps')
app.register_blueprint(sys_srvc_bp, url_prefix='/sysservices')
app.register_blueprint(sys_srvc_bp, url_prefix='/pippkgs')

app.register_blueprint(inf_data_bp, url_prefix='/inf_data')
##############################################################################


# Functions
##############################################################################
def test_mongodb():
    try:
        db = connect(
            host     = DB_HOST,
            db       = DB_NAME,
            username = DB_USERNAME, 
            password = DB_PASSWORD
        )
        db.server_info() # This will raise an exception if the connection fail
        print('MongoDB connection successful!')
    except Exception as e:
        print(f'MongoDB connection failed: {e}')
##############################################################################


# Put Header Server Hostname
##############################################################################
@app.after_request
def add_server_header(response):
    response.headers['X-Server'] = socket.gethostname()
    return response
##############################################################################


# Main
##############################################################################
if __name__ == '__main__':
    test_mongodb()
    app.run(host=APP_HOST, port=APP_PORT, debug=True)
##############################################################################
