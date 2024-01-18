#!/usr/bin/env python3

# Libraries
##############################################################################
from configparser import ConfigParser
##############################################################################

# Config
##############################################################################
CONFIG_FILE = 'config.ini'
config = ConfigParser()
config.read(CONFIG_FILE)

# App
SECRET_KEY  = config.get('Flask','SECRET_KEY')
APP_HOST    = config.get('Flask','HOST')
APP_PORT    = int(config.get('Flask','PORT'))

# JWT Algorithm
JWT_ALG = config.get('JWT','JWT_ALG') 

# DB
DB_HOST      = config.get('Database','HOST')
DB_PORT      = config.get('Database','PORT')
DB_NAME      = config.get('Database','DB')
DB_USERNAME  = config.get('Database','USERNAME')
DB_PASSWORD  = config.get('Database','PASSWORD')
#############################################################################