#!/user/bin/env python
# -*- coding: utf-8 -*-
from bottle import route, HTTPResponse
from api import account, block, structure

import json

def responce(data):
	body = json.dumps(data)
	r = HTTPResponse(status=200, body=body)
	r.set_header('Content-Type', 'application/json')
	r.set_header('Access-Control-Allow-Origin', '*')
	r.set_header('Access-Control-Allow-Headers', 'Content-Type')
	return r
