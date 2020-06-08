from flask import Flask
import logging.config, yaml
import os

logging.config.dictConfig(yaml.safe_load(open(os.path.dirname(__file__)+'/../logging.conf')))

app = Flask(__name__)

from app import routes
