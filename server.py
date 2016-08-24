
from flask import Flask
from flask import request
from flask import json
from flask import jsonify
import json
import os
import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection
from random import randint
import cairosvg
app = Flask(__name__)

@app.route('/')
def index():
	return "Hello World!"

@app.route('/svg-to-png', methods=['POST'])
def convert():
	if request.method =='POST':
		try:
			conn = S3Connection(os.getenv('AWS_KEY_ID'), os.getenv('AWS_SECRET_KEY'))
			bucket = conn.get_bucket(os.getenv('BUCKET_NAME'))
			bucket.list()
			k = Key(bucket)
			k.key = 'tickets/' + str(randint(0,999999999999999)) + ".png"
			k.set_contents_from_string(cairosvg.svg2png(bytestring=request.json['svg']))
			return jsonify({'url': k.key})
		except Exception as e:
			return "ERROR" + str(e) 


if __name__ == "__main__":
    app.run(host='0.0.0.0')
